import serial
import time





class ESP32Hardware:

    def __init__(self, port="COM9", baud=115200):
        try:
            self.ser = serial.Serial(port=port, baudrate=baud, timeout=0)
            time.sleep(2)
            print("Serial connection established")
        
        except serial.SerialException as e:
            print("Could not open serial port: ", e)
            self.ser = None

    def write_to_serial(self, cmd):
        if not self.ser:
            print("Serial port not open")
            return
        
        command = f"{cmd}\r\n"
        print(f"sending: {command.strip()}")
        self.ser.write(command.encode("utf-8"))
        self.ser.flush()



    def read_from_serial(self):

        if not self.ser:
            return None
        
        if self.ser.in_waiting:
            try:
                line = self.ser.readline().decode("utf-8").strip()
                return line
            except UnicodeDecodeError:
                return None
            
        return None

    def close_serial(self):
        if self.ser:
            self.ser.close()

