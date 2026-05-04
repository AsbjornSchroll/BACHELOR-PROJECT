

#include <Arduino.h>
#include <SCServo.h>
#include <HX711.h>




#define SERVO1 1
#define SERVO2 2

#define SERVO1_VELOCITY_MOVE_OUT -200
#define SERVO1_VELOCITY_MOVE_IN 200
#define SERVO1_LOAD_THRESHOLD 120

#define SERVO2_VELOCITY_EXTRACTION 200
#define SERVO2_DETECT_LOAD_THRESHOLD 200
#define SERVO2_RELEASE_LOAD_THRESHOLD 100


#define ACC 20


// Pins for loadcell
#define LOAD_CELL_DATA_PIN 32
#define LOAD_CELL_CLOCK_PIN 33


// Pins for joystick controller
#define JOY_X     27
#define JOY_BTN   14


// Initialise motor
SMS_STS st;


// Initialise HX711 for load cell measuring
HX711 load_cell;
int k_value = 30403;




// State machine
enum State {
    IDLE = 0,
    MOVE_TO_INNER = 1,
    MOVE_TO_OUTER = 2, 
    MANUAL_HEIGHT_ADJUSTMENT = 3, 
    ENGAGE_GRIP = 4,
    START_EXTRACTION = 5,
    EXTRACTING_BEARING = 6,
    PROCESS_DONE = 7
};  

// Initialise state machine
State current_state = IDLE;

// Global variabels, for measuring linear displacement
static long accumulated_ticks = 0;
static int last_encoder_pos = 0;
float displacement_mm = 0.0;
#define PULSE_PER_MM (4095.0/((20.0 + 1.5) * 3.1415)) // From formula described in displacement reading chapter

// Global variabels on load feedback from servo motors to be updated in loop 
int servo1_load_fb  = 0;
int servo2_load_fb = 0;


// Global variable containing load cell reading
int load_cell_val = 0;




// Joystick parameters
#define DEADZONE   150
#define MAX_SPEED  800
#define ACC_WHEEL  20
int  joystick_center = 0;
bool lastButtonState = HIGH;



// TRACKING THE DIRECTION OF THE VELOCITY
int previous_velocity_servo1 = 0;
int current_velocity_servo1 = 0;
int current_velocity_servo2 = 0;



// PRINT VARIABLE. WHEN THIS VARIABLE IS TRUE, DATA IS BEING PRINTED TO THE SERIAL PORT.
bool print_live_data = false;




unsigned long state_entry_time = 0;


// Transition to the next state used in the state machine
void transition_to(State next) {
    current_state = next;
    state_entry_time = millis();
}



bool every100ms() {
    static unsigned long lastTime = 0;
    unsigned long now = millis();
    if (now - lastTime >= 100) {
        lastTime += 100;
        return true;
    }
    return false;
}








// Function that returns the relative displacement
float read_displacement_mm() {
    int current_pos = st.ReadPos(SERVO2);
    int delta = current_pos - last_encoder_pos;

    if (delta > 2048) delta -= 4096;
    else if (delta < -2048) delta += 4096;

    accumulated_ticks += delta;
    last_encoder_pos = current_pos;

    return fabs(accumulated_ticks * (PULSE_PER_MM / 4096.0f));
}




void reset_displacement() {
    accumulated_ticks = 0;
    last_encoder_pos = st.ReadPos(SERVO2);
}



String listen_for_serial() {

    if (!Serial.available()) return "";

    String msg = Serial.readStringUntil('\n');
    msg.trim();

    if (msg.startsWith("DATA:")) {
      return "";
    }

    return msg;
}




// Joystick handling
void handleJoystick() {
  int raw = analogRead(JOY_X);
  int centered = raw - joystick_center;

  int speed = 0;
  if (abs(centered) > DEADZONE) {
    speed = map(centered, -2048, 2048, -MAX_SPEED, MAX_SPEED);
  }
  Serial.print("centered value: ");
  Serial.print(centered);
  Serial.print("   ");
  Serial.print("speed: ");
  Serial.println(speed);

  current_velocity_servo2 = speed;
}


// Button handling
bool handleButton() {
    bool buttonState = digitalRead(JOY_BTN);
    bool pressed = (buttonState == LOW && lastButtonState == HIGH);
    lastButtonState = buttonState;
    if (pressed) {
        current_velocity_servo2 = 0;
        return true;
    }
    else {
        return false;
    }
}








void handleStateMachine(String cmd, bool button) {

    switch (current_state) {


        case IDLE:


            if (cmd == "MOVE_INNER") {
                current_velocity_servo1 = SERVO1_VELOCITY_MOVE_IN;
                st.EnableTorque(1, 1);
                transition_to(MOVE_TO_INNER);

            }
            else if (cmd == "MOVE_OUTER") {
                current_velocity_servo1 = SERVO1_VELOCITY_MOVE_OUT;
                st.EnableTorque(1, 1);
                transition_to(MOVE_TO_OUTER);
            }

            else if (cmd == "MANUAL_HEIGHT_ADJUSTMENT") {
                st.EnableTorque(2, 1); 
                transition_to(MANUAL_HEIGHT_ADJUSTMENT);
            }

            else if (cmd == "ENGAGE_GRIP") {
                current_velocity_servo1 = -1*previous_velocity_servo1;
                st.EnableTorque(1, 1);
                transition_to(ENGAGE_GRIP);
            }
            
            else if (cmd == "START_EXTRACTION") {
                current_velocity_servo2 = SERVO2_VELOCITY_EXTRACTION;
                st.EnableTorque(2, 1);
                transition_to(START_EXTRACTION);
            }


        break;

        

        case MOVE_TO_INNER:
            // Small buffer to ensure, that load threshold is not reached in the beginning caused by acceleration
            if (millis() - state_entry_time <= 100) {
              break;
            }
            
            if (servo1_load_fb >= SERVO1_LOAD_THRESHOLD) {

                st.EnableTorque(1, 0);

                st.EnableTorque(2, 0);

                previous_velocity_servo1 = current_velocity_servo1;

                current_velocity_servo1 = 0;

                Serial.println("DONE_INNER");

                transition_to(IDLE);
            }

            break;


        case MOVE_TO_OUTER:
            if (millis() - state_entry_time <= 100) {
                break;
            }

            if (servo1_load_fb >= SERVO1_LOAD_THRESHOLD) {

                st.EnableTorque(1, 0);

                previous_velocity_servo1 = current_velocity_servo1;

                current_velocity_servo1 = 0;

                Serial.println("DONE_OUTER");

                transition_to(IDLE);
            }

            break;
        

        case MANUAL_HEIGHT_ADJUSTMENT:
            if (button == true) {
                st.EnableTorque(2, 0);
                transition_to(IDLE);
            }
            else {
                handleJoystick();
            }
            break;
        

        case ENGAGE_GRIP:
            if (servo1_load_fb >= SERVO1_LOAD_THRESHOLD) {
                previous_velocity_servo1 = current_velocity_servo1;
                current_velocity_servo1 = 0;
                Serial.println("DONE_SELF_ALLIGN");
                transition_to(IDLE);
            }
            break;
        

        case START_EXTRACTION:
            print_live_data = true;
            if (servo2_load_fb >= SERVO2_DETECT_LOAD_THRESHOLD) {
                transition_to(EXTRACTING_BEARING);
            }
            break;


        case EXTRACTING_BEARING:
            if (servo2_load_fb <= SERVO2_RELEASE_LOAD_THRESHOLD) {
                transition_to(PROCESS_DONE);
            }
            break;


        case PROCESS_DONE:
            print_live_data = false;

            if (millis() - state_entry_time <= 50) {

                current_velocity_servo1 = previous_velocity_servo1;

                break;
            }

            Serial.println("PROCESS_DONE");
            current_velocity_servo1 = 0;
            transition_to(IDLE);
            
            break;
    
    }
}


void setup() {
    Serial.begin(115200);
    Serial1.begin(1000000, SERIAL_8N1, 16, 17);
    st.pSerial = &Serial1;

    pinMode(JOY_BTN, INPUT_PULLUP);
    pinMode(JOY_X, INPUT);

    


    // Using the HX711 library
    //load_cell.begin(load_cell_pin, load_cell_clock_pin);
    //load_cell.set_scale(k_value);
    //load_cell.tare();
    //load_cell.set_raw_mode(); 
    delay(500);

    load_c
    st.WheelMode(SERVO1);
    st.WheelMode(SERVO2);
    st.EnableTorque(SERVO1, 1);
    st.EnableTorque(SERVO2, 1);
    joystick_center = analogRead(JOY_X);
    Serial.print(joystick_center);
    Serial.println("ESP READY");
}


void loop() {

    String cmd = listen_for_serial();
    bool button = handleButton();

    if (every100ms()) {
        displacement_mm = read_displacement_mm();
        servo1_load_fb = abs(st.ReadLoad(SERVO1));
        servo2_load_fb = abs(st.ReadLoad(SERVO2));
        if (print_live_data) {
            Serial.printf("DATA,%.3f,%d\n", displacement_mm, servo2_load_fb);
            Serial.flush();
        } 
    }
 
    handleStateMachine(cmd, button);
    // State machine sets the correct current velocity speeds for the two servo motors
    st.WriteSpe(SERVO1, current_velocity_servo1, ACC);
    st.WriteSpe(SERVO2, current_velocity_servo2, ACC);

}










