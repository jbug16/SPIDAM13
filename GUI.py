import tkinter as tk
from controller import (
    load_file,
    export_plot,
    initialize_vars,
    plot_wave,
    placeholder_graph,
    update_plot,
    plot_fft
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
        self.res = tk.StringVar(value="Resonance: N/A")

        # Initialize controller variables
        initialize_vars(self.file_name, self.duration, self.rt60, self.res)

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Create a Frame for the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Load File Button
        load_button = tk.Button(button_frame, text="Load Audio File", command=self.load_audio_button)
        load_button.grid(row=0, column=0, pady=10)

        # Multi-select Listbox
        lb = tk.Listbox(button_frame, selectmode=tk.MULTIPLE)
        lb.insert(tk.END, "High Freq (2kHz+)")
        lb.insert(tk.END, "Mid Freq (200-2kHz)")
        lb.insert(tk.END, "Low Freq (20-200 Hz)")
        lb.grid(row=4, column=0, pady=10)

        # Graph button
        graph_button = tk.Button(button_frame, text="Graph RT60", command=lambda: update_plot(self.rt60_graph, lb))
        graph_button.grid(row=5, column=0, pady=10)

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
        
        # Display Resonance
        self.res_label = tk.Label(label_frame, textvariable=self.res)
        self.res_label.grid(row=0, column=3, padx=10)

        # Create a Frame for the graphs
        graph_frame = tk.Frame(self.root)
        graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        # Wave Graphs
        self.wave_graph = tk.Frame(graph_frame)
        self.wave_graph.grid(row=0, column=0, pady=10, sticky="nsew")
        placeholder_graph(self.wave_graph)

        # Wave Export Button
        wave_export_button = tk.Button(graph_frame, text="Export Plot", command=lambda: export_plot(plot_wave(self.wave_graph), f"{self.file_name.get()[:-4]}_wave_exported_plot"))
        wave_export_button.grid(row=1, column=0, pady=10)

        # RT60 Graph
        self.rt60_graph = tk.Frame(graph_frame)
        self.rt60_graph.grid(row=2, column=0, pady=10, sticky="nsew")
        placeholder_graph(self.rt60_graph)

        # RT60 Export Button
        rt60_export_button = tk.Button(graph_frame, text="Export Plot", command=lambda: export_plot(update_plot(self.rt60_graph, lb), f"{self.file_name.get()[:-4]}_rt60_exported_plot"))
        rt60_export_button.grid(row=3, column=0, pady=10)

        # FFT Graph
        self.fft_graph = tk.Frame(graph_frame)
        self.fft_graph.grid(row=4, column=0, pady=10, sticky="nsew")
        placeholder_graph(self.fft_graph)

        # FFT Export Button
        fft_export_button = tk.Button(graph_frame, text="Export Plot", command=lambda: export_plot(plot_fft(self.fft_graph), f"{self.file_name.get()[:-4]}_fft_exported_plot"))
        fft_export_button.grid(row=5, column=0, pady=10)

        # Make sure all graphs fit
        graph_frame.grid_rowconfigure(0, weight=1)
        graph_frame.grid_rowconfigure(2, weight=1)
        graph_frame.grid_rowconfigure(4, weight=1)
        graph_frame.grid_columnconfigure(0, weight=1)

    def load_audio_button(self):
        # Load waveform if file selected
        try:
            load_file()
            plot_wave(self.wave_graph)
            plot_fft(self.fft_graph)
        except Exception:
            placeholder_graph(self.wave_graph)