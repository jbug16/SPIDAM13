from tkinter import filedialog
import os
import wave
from SPIDAM_model import Model

# Global StringVars to share state with the GUI
file_name = None
duration = None

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
    model = Model()
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

def combine_plots():
    return

def export_plot():
    return

def analyze_audio():
    return