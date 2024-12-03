import tkinter as tk
from tkinter import filedialog
import os
import wave

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SPIDAM")

        # Set Window Size
        self.root.geometry("800x600")

        # Variables
        self.file_name = tk.StringVar(value="No file selected")
        self.duration = tk.StringVar(value="Duration: N/A")
        self.rt60 = tk.StringVar(value="RT60: N/A")

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Load File Button
        load_button = tk.Button(self.root, text="Load Audio File", command=self.load_audio)
        load_button.pack(pady=10)

        # Analyze Button
        analyze_button = tk.Button(self.root, text="Analyze Audio", command=self.analyze_audio)
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
        combine_button = tk.Button(self.root, text="Combine Plots", command=self.combine_plots)
        combine_button.pack(pady=10)

        # Export Button
        export_button = tk.Button(self.root, text="Export Plot", command=self.export_plot)
        export_button.pack(pady=10)

    def load_audio(self):
        self.file = filedialog.askopenfilename(
            initialdir="/",
            title="Select a File",
            filetypes=[("Audio files", "*.wav"), ("All files", "*.*")]
        )

        # Get duration using wave
        try:
            with wave.open(self.file, 'rb') as wav_file:
                self.file_name.set(os.path.basename(self.file))
        except Exception as e:
            self.file_name.set("No file selected")
        # Get duration using wave
        try:
            with wave.open(self.file, 'rb') as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                duration = frames / float(rate)
                self.duration.set(f"Duration: {duration:.2f} seconds")
        except Exception as e:
            self.duration.set("Duration: N/A")

    def combine_plots(self):
        return

    def export_plot(self):
        return
    
    def analyze_audio(self):
        return