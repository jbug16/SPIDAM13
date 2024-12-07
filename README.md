# SPIDAM (Sound Processing, Integration, and Data Analysis Model)

SPIDAM is a graphical user interface (GUI)-based tool for working with audio files, visualizing sound data, and performing various sound analysis operations. The application uses Python with Tkinter for the GUI, Matplotlib for plotting, and other external libraries for audio processing.

## Features

- **Load Audio Files**: Users can load audio files in `.wav` format.
- **Display Waveforms**: Display waveforms of audio data.
- **RT60 Calculation**: Graphical representation of the RT60 (Reverberation Time) based on the loaded audio file.
- **Graph Export**: Export plots of waveforms and RT60 graphs as image files.
- **Resonance & Duration Display**: View key audio properties, such as resonance and duration, directly within the application.
- **Multi-Select Frequency Selection**: Option to select different frequency bands (e.g., Low Freq, Mid Freq, High Freq) to graph specific sound characteristics.

## Installation

To run SPIDAM, you will need Python installed along with the required dependencies. You can install the dependencies using `pip`:

```bash
pip install pydub scipy matplotlib numpy
