from tkinter import filedialog
import os
import wave
from SPIDAM_model import Model
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global StringVars to share state with the GUI
file_name = None
duration = None

# Reference Model class
model = Model()

def initialize_vars(fn_var, dur_var):
    global file_name, duration
    file_name = fn_var
    duration = dur_var

def load_file():
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
    
    # Get data
    model.preprocess_data(file)
    model.get_data()

    try:
        # Try to convert to .wav
        model.to_wav()

        # Get file name
        file_name.set(os.path.basename(file))
    
        # Get duration
        duration.set(f"Duration: {model.time} seconds")
    except wave.Error as e:
        print(f"Wave error: {e}")  # Log wave-specific errors
        duration.set("Duration: N/A")
    except Exception as e:
        print(f"General error: {e}")  # Log general errors
        duration.set("Duration: N/A")

def plot_wave(frame):
    # Reset frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Get data needed
    model.get_waveform_data()

    # Create figure
    fig = Figure(figsize=(8, 4), dpi=100)

    # Clear and add subplot
    fig.clf()
    ax = fig.add_subplot(111)

    # Plot
    ax.plot(model.waveform_time, model.signal)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title(f'Waveform of {file_name.get()}')

    # Embed figure into frame
    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

def placeholder_graph(frame):
    # Add an empty graph to the graph frame
    fig = Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title("No data available")
    ax.set_xlabel("N/A")
    ax.set_ylabel("N/A")

    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def analyze_audio():
    return

def combine_plots():
    return

def export_plot():
    return