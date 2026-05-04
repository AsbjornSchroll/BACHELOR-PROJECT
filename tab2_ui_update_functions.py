import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk



def read_process_csv(filepath):

    time_ms = []
    displacement = []
    force = []

    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)

        required_fields = {"timestamp_ms", "displacement_mm", "force_N"}
        if not required_fields.issubset(reader.fieldnames):
            raise ValueError(
                f"CSV file {filepath} does not contain required columns: "
                f"{required_fields}"
            )

        for row in reader:
            try:
                time_ms.append(float(row["timestamp_ms"]))
                displacement.append(float(row["displacement_mm"]))
                force.append(float(row["force_N"]))
            except (ValueError, TypeError):
                
                continue

    return time_ms, displacement, force



def perfect_case_filepath(mounting: str):
    base = os.path.join("data", "perfect_disassemble_cases")

    if mounting == "internal":
        return os.path.join(base, "internal.csv")
    elif mounting == "external":
        return os.path.join(base, "external.csv")
    else:
        return None











def get_all_measurements(folder_path):
    
    #Reads all process CSV files in a folder.

    all_time_ms = []
    all_displacement = []
    all_force = []

    for file in os.listdir(folder_path):
        if not file.lower().endswith(".csv"):
            continue

        filepath = os.path.join(folder_path, file)

        time_ms, displacement, force = read_process_csv(filepath)

        all_time_ms.append(time_ms)
        all_displacement.append(displacement)
        all_force.append(force)

    return all_time_ms, all_displacement, all_force



def calculate_average_measurements(all_force, all_displacement):

    if not all_force or not all_displacement:
        return [], []

    num_cases = len(all_force)

    min_points = min(
        min(len(f) for f in all_force),
        min(len(d) for d in all_displacement)
    )

    avg_force = []
    avg_displacement = []

    for j in range(min_points):
        avg_force.append(
            sum(all_force[i][j] for i in range(num_cases)) / num_cases
        )
        avg_displacement.append(
            sum(all_displacement[i][j] for i in range(num_cases)) / num_cases
        )

    return avg_force, avg_displacement







def plot_process_history(placeholder_f_d, placeholder_f_t, placeholder_d_t,
                         time_ms, displacement, force):

    def clear_frame(frame):
        if frame is None:
            return
        for widget in frame.winfo_children():
            widget.destroy()

    def embed_canvas(frame, canvas):
        if frame is None:
            return
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    clear_frame(placeholder_f_d)
    clear_frame(placeholder_f_t)
    clear_frame(placeholder_d_t)

    # ---------- Force vs Displacement ----------
    if placeholder_f_d is not None:
        fig_fx, ax_fx = plt.subplots(
            figsize=(5, 2.5),
            constrained_layout=True
        )
        ax_fx.plot(displacement, force, linewidth=2)
        ax_fx.set_xlabel("Displacement [mm]")
        ax_fx.set_ylabel("Force [N]")
        ax_fx.set_title("Force vs Displacement")
        ax_fx.grid(True)

        canvas_fx = FigureCanvasTkAgg(fig_fx, master=placeholder_f_d)
        canvas_fx.draw()
        embed_canvas(placeholder_f_d, canvas_fx)
        plt.close(fig_fx)

    # ---------- Force vs Time ----------
    if placeholder_f_t is not None:
        fig_ft, ax_ft = plt.subplots(
            figsize=(5, 2.5),
            constrained_layout=True
        )
        ax_ft.plot(time_ms, force, linewidth=2)
        ax_ft.set_xlabel("Time [ms]")
        ax_ft.set_ylabel("Force [N]")
        ax_ft.set_title("Force vs Time")
        ax_ft.grid(True)

        canvas_ft = FigureCanvasTkAgg(fig_ft, master=placeholder_f_t)
        canvas_ft.draw()
        embed_canvas(placeholder_f_t, canvas_ft)
        plt.close(fig_ft)

    # ---------- Displacement vs Time ----------
    if placeholder_d_t is not None:
        fig_xt, ax_xt = plt.subplots(
            figsize=(5, 2.5),
            constrained_layout=True
        )
        ax_xt.plot(time_ms, displacement, linewidth=2)
        ax_xt.set_xlabel("Time [ms]")
        ax_xt.set_ylabel("Displacement [mm]")
        ax_xt.set_title("Displacement vs Time")
        ax_xt.grid(True)

        canvas_xt = FigureCanvasTkAgg(fig_xt, master=placeholder_d_t)
        canvas_xt.draw()
        embed_canvas(placeholder_d_t, canvas_xt)
        plt.close(fig_xt)




def plot_comparison_cb(frame, force, displacement, p_force, p_displacement):

    # Clear frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Create figure
    fig, ax = plt.subplots(
        figsize=(5, 3),
        constrained_layout=True
    )

    ax.plot(
        displacement, force,
        linewidth=2,
        color="tab:blue",
        label="Measured case"
    )
    ax.plot(
        p_displacement, p_force,
        linewidth=2,
        linestyle="--",
        color="tab:orange",
        label="Perfect case"
    )

    ax.set_xlabel("Displacement [mm]")
    ax.set_ylabel("Force [N]")
    ax.set_title("Force vs Displacement")
    ax.grid(True)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    plt.close(fig)










