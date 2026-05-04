import csv
import os
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class RealTimeData:
    def __init__(self, frame, current_mounting, plot_mode):
        self.frame = frame
        self.current_mounting = current_mounting.get()
        self.plot_mode = plot_mode

        self.process_finished = False


        # Plot setup
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'b-')
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        self.time_ms_data = []
        self.disp_data = []
        self.force_data = []




    def update_real_time_plot(self, time_ms, disp, force):

        plotting_mode = self.plot_mode.get() # Tjekker, om der skal plottes Force vs. Displacement, Force vs. time, Displacement vs. time 

        force_new = (force/1000)*9.81
        if self.process_finished == True:
            self.process_finished = False
        # Plot-opdatering
        self.time_ms_data.append(time_ms)
        self.disp_data.append(disp)
        self.force_data.append(force_new)


        self.redraw_plot(plotting_mode)

        if plotting_mode == "Force vs Displacement":
            self.line.set_xdata(self.disp_data)
            self.line.set_ydata(self.force_data)

        elif plotting_mode == "Force vs Time":
            self.line.set_xdata(self.time_ms_data)
            self.line.set_ydata(self.force_data)


        elif plotting_mode == "Displacement vs Time":
            self.line.set_xdata(self.time_ms_data)
            self.line.set_ydata(self.disp_data)


        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()


    def redraw_plot(self, plotting_mode):

        if plotting_mode == "Force vs Displacement":
            self.line.set_xdata(self.disp_data)
            self.line.set_ydata(self.force_data)

            self.ax.set_xlabel("Displacement [mm]")
            self.ax.set_ylabel("Force [N]")

        elif plotting_mode == "Force vs Time":
            self.line.set_xdata(self.time_ms_data)
            self.line.set_ydata(self.force_data)

            self.ax.set_xlabel("Time [ms]")
            self.ax.set_ylabel("Force [N]")

        elif plotting_mode == "Displacement vs Time":
            self.line.set_xdata(self.time_ms_data)
            self.line.set_ydata(self.disp_data)

            self.ax.set_xlabel("Time [ms]")
            self.ax.set_ylabel("Displacement [mm]")

        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw_idle()


    def update_plot(self):
        plotting_mode = self.plot_mode.get()
        self.redraw_plot(plotting_mode) 


    def start_new_process(self, current_mounting):
        self.current_mounting = current_mounting
        self.process_finished = False
        self.reset()




    def on_process_done(self):
        if self.process_finished:
            return

        self.process_finished = True
        self.save_live_data_to_csv()


    def reset(self):
        self.disp_data.clear()
        self.force_data.clear()

        self.line.set_xdata([])
        self.line.set_ydata([])

        self.ax.relim()
        self.ax.autoscale_view()

        self.canvas.draw()





    def save_live_data_to_csv(self):

        mount = str(self.current_mounting)

        if mount not in ("internal", "external"):
            print("No valid mounting defined – CSV not saved")
            return

        base_path = r"C:\Users\asgra\OneDrive\Dokumenter\DTU\bachelor\proof_of_concept\data"
        folder = os.path.join(base_path, mount)
        os.makedirs(folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{mount}_{timestamp}.csv"
        full_path = os.path.join(folder, filename)

        with open(full_path, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp_ms", "displacement_mm", "force_N"])

            for t_val, d_val, f_val in zip(
                self.time_ms_data,
                self.disp_data,
                self.force_data
            ):
                writer.writerow([t_val, d_val, f_val])

        print("Saved CSV:", full_path)

