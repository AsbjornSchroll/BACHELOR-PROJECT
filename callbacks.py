import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import csv
import os

from tab2_ui_update_functions import (
    read_process_csv,
    get_all_measurements,
    calculate_average_measurements,
    plot_process_history,
    perfect_case_filepath,
    plot_comparison_cb

)



class user_input_to_esp:

    def __init__(self, esp, current_mounting):
        self.current_mounting = current_mounting
        self.esp = esp



    def go_to_inner_position(self):
        self.current_mounting.set("internal")
        cmd = "MOVE_INNER"
        self.esp.write_to_serial(cmd)


    def go_to_outer_position(self):
        self.current_mounting.set("external")
        cmd = "MOVE_OUTER"
        self.esp.write_to_serial(cmd)


    def enable_manual_height_adjustment(self):
        cmd = "MANUAL_HEIGHT_ADJUSTMENT"
        self.esp.write_to_serial(cmd)


    def engage_grip(self):
        cmd = "ENGAGE_GRIP"
        self.esp.write_to_serial(cmd)


    def start_extraction(self):
        cmd = "START_EXTRACTION"
        self.esp.write_to_serial(cmd)
        



class user_input_to_update_tab1:

    def __init__(self, realtime_data):
        self.realtime_data = realtime_data


    def on_plot_mode_change(self, event=None):
        self.realtime_data.update_plot() 


class user_input_to_update_tab2:

    def __init__(self, tab2_items):
        """
        Handles user interaction for Tab 2 (Process history)
        """

        # 0 = nothing selected, 1 = file, 2 = folder
        self.chosen_item = 0

        self.selected_mounting_type = None

        self.time_ref = None
        self.displacement = None
        self.force = None



        # UI elements
        self.label = tab2_items["label"]

        self.ph_fx = tab2_items["placeholder_force_displacement"]
        self.ph_ft = tab2_items["placeholder_force_time"]
        self.ph_xt = tab2_items["placeholder_displacement_time"]

    # -------------------------------------------------
    # Choose single CSV file
    # -------------------------------------------------
    def choose_file_button(self):

        filepath = filedialog.askopenfilename(
            title="Select process file",
            initialdir="data",
            filetypes=[("CSV files", "*.csv")]
        )

        if not filepath:
            return

        filename = os.path.basename(filepath)

        if "internal" in filename:
            self.selected_mounting_type = "internal"
        elif "external" in filename:
            self.selected_mounting_type = "external"
        else:
            self.selected_mounting_type = None

        self.label.config(text=filename, foreground="black")

        # Read data
        time_ms, displacement, force = read_process_csv(filepath)

        self.time_ref = time_ms
        self.displacement = displacement
        self.force = force

        self.chosen_item = 1

        # Plot all three representations
        plot_process_history(
            self.ph_fx,
            self.ph_ft,
            self.ph_xt,
            time_ms,
            displacement,
            force
        )

    # -------------------------------------------------
    # Choose folder → average of all cases
    # -------------------------------------------------
    def choose_folder_button(self):

        folder = filedialog.askdirectory(
            title="Select folder",
            initialdir="data"
        )

        if not folder:
            return

        if "internal" in folder:
            self.selected_mounting_type = "internal"
        elif "external" in folder:
            self.selected_mounting_type = "external"
        else:
            self.selected_mounting_type = None


        self.label.config(text=os.path.basename(folder), foreground="black")







        # Load all measurements
        all_time, all_disp, all_force = get_all_measurements(folder)





        # Calculate averages
        avg_force, avg_disp = calculate_average_measurements(
            all_force,
            all_disp
        )



                # Find fælles længde
        min_len = min(
            len(avg_force),
            len(avg_disp),
            len(all_time[0])
        )




        # Use first time axis as reference
        time_ref = all_time[0][:min_len]
        avg_force = avg_force[:min_len]
        avg_disp = avg_disp[:min_len]

        self.time_ref = time_ref
        self.displacement = avg_disp
        self.force = avg_force

        self.chosen_item = 2

        # Plot averaged data
        plot_process_history(
            self.ph_fx,
            self.ph_ft,
            self.ph_xt,
            self.time_ref,
            self.displacement,
            self.force
        )



    def handle_comparison_cb(self, compare_var: tk.BooleanVar):

        if self.time_ref is None:
            return

        # ---------- comparison FRA ----------
        if not compare_var.get():
            plot_process_history(
                self.ph_fx,
                self.ph_ft,
                self.ph_xt,
                self.time_ref,
                self.displacement,
                self.force
            )
            return

        # ---------- comparison TIL ----------
        mount = self.selected_mounting_type
        if mount not in ("internal", "external"):
            print("No valid mounting type for selected data")
            return

        perfect_fp = perfect_case_filepath(mount)
        if not perfect_fp or not os.path.exists(perfect_fp):
            print("Perfect case not found")
            return

        # perfect reference
        _, p_disp, p_force = read_process_csv(perfect_fp)

        # Force vs Displacement → comparison
        plot_comparison_cb(
            frame=self.ph_fx,
            force=self.force,
            displacement=self.displacement,
            p_force=p_force,
            p_displacement=p_disp
        )

        # Force vs Time → measured only
        plot_process_history(
            placeholder_f_d=None,
            placeholder_f_t=self.ph_ft,
            placeholder_d_t=None,
            time_ms=self.time_ref,
            displacement=self.displacement,
            force=self.force
        )

        # Displacement vs Time → measured only
        plot_process_history(
            placeholder_f_d=None,
            placeholder_f_t=None,
            placeholder_d_t=self.ph_xt,
            time_ms=self.time_ref,
            displacement=self.displacement,
            force=self.force
        )

















