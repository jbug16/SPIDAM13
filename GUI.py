import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controller import (
    load_file,
    combine_plots,
    export_plot,
    analyze_audio,
    initialize_vars,
    plot_wave
)

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SPIDAM")

        # Set Window Size
        self.root.geometry("800x600")

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
        # Load File Button
        load_button = tk.Button(self.root, text="Load Audio File", command=self.load_audio_button)
        load_button.pack(pady=10)

        # Analyze Button
        analyze_button = tk.Button(self.root, text="Analyze Audio", command=self.analyze_audio_button)
        analyze_button.pack(pady=10)

        # Display File Name
        self.file_label = tk.Label(self.root, textvariable=self.file_name)
        self.file_label.pack(pady=5)

        # Display Duration
        self.duration_label = tk.Label(self.root, textvariable=self.duration)
        self.duration_label.pack(pady=5)

        # Display RT60
        self.rt60_label = tk.Label(self.root, textvariable=self.rt60)
        self.rt60_label.pack(pady=5)

        # Combine Plots Button
        combine_button = tk.Button(self.root, text="Combine Plots", command=combine_plots)
        combine_button.pack(pady=10)

        # Export Button
        export_button = tk.Button(self.root, text="Export Plot", command=export_plot)
        export_button.pack(pady=10)

        # Graphs
        self.wave_graph = tk.Frame(self.root)
        self.wave_graph.pack(pady=10)

    def load_audio_button(self):
        load_file()
        plot_wave(self.wave_graph)
    
    def analyze_audio_button(self):
        analyze_audio()