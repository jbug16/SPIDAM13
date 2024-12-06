import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controller import (
    model,
    load_audio,
    combine_plots,
    export_plot,
    analyze_audio,
    initialize_vars,
    plot_data,
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
        load_button = tk.Button(self.root, text="Load Audio File", command=load_audio)
        load_button.pack(pady=10)

        # Analyze Button
        analyze_button = tk.Button(self.root, text="Analyze Audio", command=self.analyze_audio_and_plot)
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

        # Plot Frames
        self.rt60_frame = tk.Frame(self.root, height=300)
        self.rt60_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.waveform_frame = tk.Frame(self.root, height=300)
        self.waveform_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    def visualize_in_gui(self, fig, canvas_frame):
        """Embed Matplotlib figure into a Tkinter frame."""
        for widget in canvas_frame.winfo_children():
            widget.destroy()  # Clear previous canvas

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def analyze_audio_and_plot(self):
        """Perform audio analysis and plot results in the GUI."""
        # Ensure the audio file is loaded and analyze
        analyze_audio()

        # Plot RT60 data
        rt60_data = {
            "Low": {"x": model.time, "y": model.rt60[0]},
            "Mid": {"x": model.time, "y": model.rt60[1]},
            "High": {"x": model.time, "y": model.rt60[2]},
        }
        rt60_fig = plot_data(rt60_data, plot_type="line", title="RT60 Over Time", x_label="Time (s)", y_label="RT60 (s)")
        self.visualize_in_gui(rt60_fig, self.rt60_frame)

        # Plot waveform data
        waveform_data = {"x": model.time, "y": model.channels}
        waveform_fig = plot_data(waveform_data, plot_type="line", title="Waveform", x_label="Time (s)", y_label="Amplitude")
        self.visualize_in_gui(waveform_fig, self.waveform_frame)