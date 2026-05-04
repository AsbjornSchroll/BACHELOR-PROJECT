import tkinter as tk
from tkinter import ttk


# This is the code for the User interface. It is partened into two tabs: tab1 = 'current process' and tab2 = 'process history'

# The functions 



class UI_tab1_tab2:

    def __init__(self, root):
        self.root = root
        self.root.title("Bearing Disassembly Control")
        self.root.geometry("1100x700")


        # State variable (kommandoer)
        self.chosen_mounting = tk.StringVar(value="")

 

        # To be used in tab2 to compare the chosen mounting disassembly case to that of the 'perfect' disassembly case
        self.compare = tk.BooleanVar()



        # Dividing the app into two tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky="nsew")



        # TAB 1
        self.tab1 = ttk.Frame(self.notebook)
        self.tab1.columnconfigure(0, weight=1)
        self.tab1.columnconfigure(1, weight=4)
        self.tab1.rowconfigure(0, weight=1)

        # TAB 2
        self.tab2 = ttk.Frame(self.notebook)
        self.tab2.columnconfigure(0, weight=1)
        self.tab2.columnconfigure(1, weight=4)
        self.tab2.rowconfigure(0, weight=0)
        self.tab2.rowconfigure(1, weight=1)

        self.notebook.add(self.tab1, text="Current process")
        self.notebook.add(self.tab2, text="Process history")


        self.ui_setup_tab1()
        self.ui_setup_tab2()
        self.get_ui_items_tab1()
        self.get_ui_items_tab2()


    def ui_setup_tab1(self):
        # ------ Current process layout --------
        main_frame = ttk.Frame(self.tab1, padding=10)
        main_frame.pack(fill="both", expand=True)

        main_frame.columnconfigure(0, weight=1)   # controls
        main_frame.columnconfigure(1, weight=3)   # plot
        main_frame.rowconfigure(0, weight=1)

        # -------- LEFT: Controls --------
        controls = ttk.Frame(main_frame, padding=10)
        controls.grid(row=0, column=0, sticky="nsew")

        controls.columnconfigure(0, weight=1)

        self.btn_inner = ttk.Button(
            controls,
            text="Move to inner position"
        )

        self.btn_inner.grid(row=0, column=0, sticky="ew", pady=5)

        self.btn_outer = ttk.Button(
            controls,
            text="Move to outer position"
        )
        self.btn_outer.grid(row=1, column=0, sticky="ew", pady=5)

        self.btn_manual_height = ttk.Button(
            controls,
            text="Manual height adjustment"
        )
        self.btn_manual_height.grid(row=2, column=0, sticky="ew", pady=5)

        self.btn_engage_grip = ttk.Button(
            controls,
            text="Engage grip"
        )
        self.btn_engage_grip.grid(row=3, column=0, sticky="ew", pady=5)

        self.btn_start_extraction = ttk.Button(
            controls,
            text="Start extraction"
        )
        self.btn_start_extraction.grid(row=4, column=0, sticky="ew", pady=5)





        # -------- RIGHT: Plot frame --------
        self.plot_frame = ttk.LabelFrame(
            main_frame,
            text="Live plot",
            padding=10
        )
        self.plot_frame.grid(row=0, column=1, sticky="nsew")

        self.plot_frame.columnconfigure(0, weight=1)
        self.plot_frame.rowconfigure(1, weight=1)
        self.plot_frame.rowconfigure(0, weight=0)  # dropdown
        self.plot_frame.rowconfigure(1, weight=1)  # plot


                # -------- Plot mode selector (dropdown) --------
        self.plot_mode = tk.StringVar(value="Force vs Displacement")

        self.plot_selector = ttk.Combobox(
            self.plot_frame,
            textvariable=self.plot_mode,
            state="readonly",
            values=[
                "Force vs Displacement",
                "Force vs Time",
                "Displacement vs Time"
            ]
        )

        self.plot_selector.grid(row=0, column=0, sticky="w", pady=(0, 5))


    def ui_setup_tab2(self):

        header_tab2 = ttk.Frame(self.tab2, padding=10)
        header_tab2.grid(row=0, column=0, sticky="ew")

        for col in range(4):
            header_tab2.columnconfigure(col, weight=1)

        header_0_0 = ttk.Label(header_tab2, text="Bearing disassembly logging system")
        header_0_0.grid(row=0, column=0, sticky="w")

        self.header_0_1 = ttk.Button(header_tab2, text="Choose file")
        self.header_0_1.grid(row=0, column=1, sticky="w")

        self.header_0_2 = ttk.Button(header_tab2, text="Choose folder")
        self.header_0_2.grid(row=0, column=2, sticky="w")

        self.header_0_3 = ttk.Label(header_tab2, text="No file selected")
        self.header_0_3.grid(row=0, column=3)

        self.header_1_0 = ttk.Checkbutton(header_tab2, text="Compare plots", variable=self.compare)
        self.header_1_0.grid(row=1, column=0)

        content = ttk.Frame(self.tab2, padding=10)
        content.grid(row=1, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)

        self.content_0 = ttk.LabelFrame(content, text="Visualise data", padding=10)
        self.content_0.grid(row=0, column=0, sticky="nsew")

        self.content_0.columnconfigure(0, weight=1)
        self.content_0.rowconfigure(0, weight=1)
        self.content_0.rowconfigure(1, weight=1)
        self.content_0.rowconfigure(2, weight=1)

                # Placeholder 1: Force vs Displacement
        self.placeholder_force_displacement = ttk.Label(
            self.content_0,
            text="Force vs Displacement",
            background="#f2f2f2",
            foreground="gray",
            anchor="center"
        )
        self.placeholder_force_displacement.grid(row=0, column=0, sticky="nsew", pady=5)

        # Placeholder 2: Force vs Time
        self.placeholder_force_time = ttk.Label(
            self.content_0,
            text="Force vs Time",
            background="#f2f2f2",
            foreground="gray",
            anchor="center"
        )
        self.placeholder_force_time.grid(row=1, column=0, sticky="nsew", pady=5)

        # Placeholder 3: Displacement vs Time
        self.placeholder_displacement_time = ttk.Label(
            self.content_0,
            text="Displacement vs Time",
            background="#f2f2f2",
            foreground="gray",
            anchor="center"
        )
        self.placeholder_displacement_time.grid(row=2, column=0, sticky="nsew", pady=5)



    # -------- Items to be used by the callback functions to send the respective serial command to ESP32
    def get_ui_items_tab1(self):
        return {
            "btn_inner": self.btn_inner,
            "btn_outer": self.btn_outer,
            "btn_manual_height": self.btn_manual_height,
            "btn_engage_grip": self.btn_engage_grip,
            "plot_frame": self.plot_frame,
            "chosen_mounting": self.chosen_mounting, 
            "btn_start_extraction": self.btn_start_extraction,
            "choose_plot": self.plot_mode
        }
    



   # Return controls for tab2
    def get_ui_items_tab2(self):
        return {
            "file_button": self.header_0_1,
            "folder_button": self.header_0_2,
            "label": self.header_0_3,
            "checkbox": self.header_1_0,
            "frame": self.content_0,
            "comp": self.compare, 
            "placeholder_force_displacement": self.placeholder_force_displacement,
            "placeholder_force_time": self.placeholder_force_time,
            "placeholder_displacement_time": self.placeholder_displacement_time
        }        


