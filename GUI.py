import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controller import (
    load_file,
    combine_plots,
    export_plot,
    analyze_audio,
    initialize_vars,
    plot_wave,
    placeholder_graph
)

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SPIDAM")

        # Set Window Size
        self.root.geometry("800x900")

        # Fullscreen window
        root.state("zoomed")

        # Variables
        self.file_name = tk.StringVar(value="No file selected")
        self.duration = tk.StringVar(value="Duration: N/A")
        self.rt60 = tk.StringVar(value="RT60: N/A")

        # Initialize controller variables
        initialize_vars(self.file_name, self.duration)

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Create a Frame for the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Load File Button
        load_button = tk.Button(button_frame, text="Load Audio File", command=self.load_audio_button)
        load_button.grid(row=0, column=0, pady=10)

        # Analyze Button
        analyze_button = tk.Button(button_frame, text="Analyze Audio", command=self.analyze_audio_button)
        analyze_button.grid(row=1, column=0, pady=10)

        # Combine Plots Button
        combine_button = tk.Button(button_frame, text="Combine Plots", command=combine_plots)
        combine_button.grid(row=2, column=0, pady=10)

        # Export Button
        export_button = tk.Button(button_frame, text="Export Plot", command=export_plot)
        export_button.grid(row=3, column=0, pady=10)

        # Multi-select Listbox
        lb = tk.Listbox(button_frame, selectmode=tk.MULTIPLE)
        lb.insert(tk.END, "High Freq")
        lb.insert(tk.END, "Mid Freq")
        lb.insert(tk.END, "Low Freq")
        lb.grid(row=4, column=0, pady=10)

        def on_select():
            selected = [lb.get(i) for i in lb.curselection()]
            print("Selected items:", selected)

        # Graph button
        button = tk.Button(button_frame, text="Graph", command=on_select)
        button.grid(row=5, column=0, pady=10)

        # Create a Frame for the labels (file name, duration, rt60)
        label_frame = tk.Frame(self.root)
        label_frame.pack(side=tk.TOP, pady=10)

        # Display File Name
        self.file_label = tk.Label(label_frame, textvariable=self.file_name)
        self.file_label.grid(row=0, column=0, padx=10)

        # Display Duration
        self.duration_label = tk.Label(label_frame, textvariable=self.duration)
        self.duration_label.grid(row=0, column=1, padx=10)

        # Display RT60
        self.rt60_label = tk.Label(label_frame, textvariable=self.rt60)
        self.rt60_label.grid(row=0, column=2, padx=10)

        # Create a Frame for the graphs
        graph_frame = tk.Frame(self.root)
        graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        # Graphs
        self.wave_graph = tk.Frame(graph_frame)
        self.wave_graph.pack(side=tk.TOP, pady=10)
        placeholder_graph(self.wave_graph)

        self.rt60_graph = tk.Frame(graph_frame)
        self.rt60_graph.pack(side=tk.TOP, pady=10)
        placeholder_graph(self.rt60_graph)

    def load_audio_button(self):
        load_file()
        plot_wave(self.wave_graph)
    
    def analyze_audio_button(self):
        analyze_audio()