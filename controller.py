from tkinter import filedialog
import os
import wave
from SPIDAM_model import Model
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global StringVars to share state with the GUI
file_ext = None
duration = None

# Reference Model class
model = Model()

def initialize_vars(fn_var, dur_var, rt60_var, res_var):
    global file_ext, duration, rt60, res
    file_ext = fn_var
    duration = dur_var
    rt60 = rt60_var
    res = res_var

def load_file():
    # Open directory
    file = filedialog.askopenfilename(
        initialdir="/",
        title="Select a File",
        filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.flac *.m4a"), ("All files", "*.*")]
    )

    # Return early if file not selected
    if not file:
        file_ext.set("No file selected")
        duration.set("Duration: N/A")
        rt60.set("RT60: N/A")
        res.set("Resonance: N/A")
        return
    
    # Get data
    model.preprocess_data(file)
    model.get_data()

    try:
        # Get file name
        file_ext.set(os.path.basename(file))
    
        # Get duration
        duration.set(f"Duration: {model.time} seconds")

        # Get RT60
        model.find_rt60()
        rt60.set(f"RT60: {model.rt60}")

        # Get res
        res.set(f"Resonance: {model.res}")
    except wave.Error as e:
        print(f"Wave error: {e}")  # Log wave-specific errors
        file_ext.set("No file selected")
        duration.set("Duration: N/A")
        rt60.set("RT60: N/A")
        res.set("Resonance: N/A")
    except Exception as e:
        print(f"General error: {e}")  # Log general errors
        file_ext.set("No file selected")
        duration.set("Duration: N/A")
        rt60.set("RT60: N/A")
        res.set("Resonance: N/A")

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
    ax.set_title(f'Waveform of {file_ext.get()}')

    # Embed figure into frame
    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

    return fig

def placeholder_graph(frame):
    # Add an empty graph to the graph frame
    fig = Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title("No data available")
    ax.set_xlabel("N/A")
    ax.set_ylabel("N/A")

    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def graph_rt60(frame, freq_bands):
    # Reset the frame to clear old plots
    for widget in frame.winfo_children():
        widget.destroy()

    # Get waveform data (assuming model.get_waveform_data is correct)
    model.get_waveform_data()

    # Create a new figure
    fig = Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111)

    # Define a dictionary to map frequency bands to integers
    freq_map = {
        'Low Freq (20-200 Hz)': 1,
        'Mid Freq (200-2kHz)': 2,
        'High Freq (2kHz+)': 3
    }

    # Iterate over the selected frequency bands and plot their RT60 values
    for band in freq_bands:
        rt60_value = model.local_rt60(freq_map[band])
        ax.plot([0, 1], [rt60_value, rt60_value], label=f'RT60 for {band}', linestyle='--')

    # Label and title
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('RT60 (seconds)')
    ax.set_title('RT60 for Selected Frequency Bands')
    ax.legend()

    # Embed the figure into the tkinter frame
    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

    return fig

def update_plot(frame, lb):
    try:
        # Get the selected frequency bands from the Listbox
        selected = [lb.get(i) for i in lb.curselection()]
        print("Selected items:", selected)
        
        # Plot RT60 for the selected frequency bands
        return graph_rt60(frame, selected)
    except Exception as e:
        placeholder_graph(frame)

def export_plot(fig, file_name):
    try:
        # Check if the filename doesn't already have an extension, if not, append .png
        if not file_name.endswith(('.png', '.jpg', '.jpeg', '.pdf', '.svg')):
            file_name += '.png'

        # Check if the file already exists
        if os.path.exists(file_name):
            base, ext = os.path.splitext(file_name)
            counter = 1
            while os.path.exists(file_name):
                file_name = f"{base}_{counter}{ext}"
                counter += 1
        
        fig.savefig(file_name, format=file_name.split('.')[-1])
        print(f"Plot successfully exported to {file_name}.")
    except Exception as e:
        print(f"An error occurred while exporting the plot: {e}")