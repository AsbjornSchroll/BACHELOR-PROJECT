

import tkinter as tk
from ui import UI_tab1_tab2
from serial_connection import ESP32Hardware
from callbacks import user_input_to_esp, user_input_to_update_tab2, user_input_to_update_tab1
from real_time_data_handle import RealTimeData


#Initialization of the individual modules
esp = ESP32Hardware()

root = tk.Tk()

ui = UI_tab1_tab2(root)

ui_items_tab1 = ui.get_ui_items_tab1()
ui_items_tab2 = ui.get_ui_items_tab2()


realtime_data = RealTimeData(ui_items_tab1["plot_frame"], ui_items_tab1["chosen_mounting"], ui_items_tab1["choose_plot"])

callback_handles_tab1_esp = user_input_to_esp(esp, ui_items_tab1["chosen_mounting"])


callback_handles_tab1_ui = user_input_to_update_tab1(realtime_data)



callback_handles_tab2 = user_input_to_update_tab2(ui_items_tab2)



# Callback functions to send serial commands to the ESP32 based on user interaction (tab1)
ui_items_tab1["btn_inner"].config(command = lambda: callback_handles_tab1_esp.go_to_inner_position())


ui_items_tab1["btn_outer"].config(command = lambda: callback_handles_tab1_esp.go_to_outer_position())


ui_items_tab1["btn_manual_height"].config(command = lambda: callback_handles_tab1_esp.enable_manual_height_adjustment())


ui_items_tab1["btn_engage_grip"].config(command = lambda: callback_handles_tab1_esp.engage_grip())


ui_items_tab1["btn_start_extraction"].config(command=lambda: (realtime_data.start_new_process(ui_items_tab1["chosen_mounting"].get()),callback_handles_tab1_esp.start_extraction()))


# Callbacks that updates the real time plot based on user interaction (tab1)
ui_items_tab1["choose_plot"].trace_add("write", lambda *_: callback_handles_tab1_ui.on_plot_mode_change())



# Callback functions used for tab2 'process history' 
# (tab2) Calls the callback function that allows the user to choose/plot a single process file
ui_items_tab2["file_button"].config(command=lambda: callback_handles_tab2.choose_file_button())

# (tab2) Calls the callback function that allows the user to choose/plot an average of all disassembly cases a specific bearing type (average on all files in specific folder)
ui_items_tab2["folder_button"].config(command=lambda: callback_handles_tab2.choose_folder_button())

# Calls the callback function for plotting the "perfect" disassembly
ui_items_tab2["checkbox"].config(command=lambda: callback_handles_tab2.handle_comparison_cb(ui_items_tab2["comp"]))






# Function that reads and processes ESP messages
def poll_serial():
    msg = esp.read_from_serial()
    if msg and (msg.startswith("DATA,")):
        try:
            payload = msg.replace("DATA,", "")

            time_str, disp_str, force_str = payload.split(",")
            realtime_data.update_real_time_plot(float(time_str), float(disp_str), float(force_str))
            print("ESP says:", msg)

        except ValueError:
            pass
            


    if msg and msg == "PROCESS_DONE":
        realtime_data.on_process_done()
    

    root.after(50, poll_serial)


poll_serial()


root.mainloop()

