from tkinter import filedialog
import os
import wave
from SPIDAM_model import Model
import matplotlib.pyplot as plt

# Global StringVars to share state with the GUI
file_name = None
duration = None

# Reference Model
model = Model()

def initialize_vars(fn_var, dur_var):
    global file_name, duration
    file_name = fn_var
    duration = dur_var

def load_audio():
    # Open directory
    file = filedialog.askopenfilename(
        initialdir="/",
        title="Select a File",
        filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.flac"), ("All files", "*.*")]
    )

    # Return early if file not selected
    if not file:
        file_name.set("No file selected")
        duration.set("Duration: N/A")
        return

    # Set file for Model
    model.original_file = file

    try:
        # Try to convert to .wav
        model.to_wav()

        # Get file name
        file_name.set(os.path.basename(file))
    
        # Get duration
        with wave.open(file, 'rb') as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            dur = frames / float(rate)
            duration.set(f"Duration: {dur:.2f} seconds")
    except wave.Error as e:
        print(f"Wave error: {e}")  # Log wave-specific errors
        duration.set("Duration: N/A")
    except Exception as e:
        print(f"General error: {e}")  # Log general errors
        duration.set("Duration: N/A")

def analyze_audio():
    # Check if file has been loaded first
    if not hasattr(model, "original_file") or not model.original_file:
        print("No file loaded for analysis.")
        return

    try:
        # Load and preprocess data
        model.preprocess_data(model.original_file)
        model.get_data()
        model.get_waveform_data()
        model.get_spec_data()

        # Calculate RT60 and other metrics
        model.find_rt60()
        model.time = model.time if isinstance(model.time, list) else [0, 0.1, 0.2]  # Fallback for `time`
        model.rt60 = [
            band if isinstance(band, list) else [0 for _ in model.time]
            for band in model.rt60
        ]

        # Debug prints
        print("Time data:", model.time)
        print("RT60 data (Low):", model.rt60[0])
        print("RT60 data (Mid):", model.rt60[1])
        print("RT60 data (High):", model.rt60[2])
    except Exception as e:
        print(f"Error during analysis: {e}")

def plot_data(data, plot_type="line", title="", x_label="", y_label=""):
    fig, ax = plt.subplots()
    for label, series in data.items():
        if plot_type == "line":
            if not all(isinstance(x, (int, float)) for x in series["x"]):
                raise ValueError(f"Non-numeric X data for {label}: {series['x']}")
            if not all(isinstance(y, (int, float)) for y in series["y"]):
                raise ValueError(f"Non-numeric Y data for {label}: {series['y']}")
            ax.plot(series["x"], series["y"], label=label)
    
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend()
    
    return fig

def combine_plots():
    return

def export_plot():
    return