import os
import pydub
from pydub import AudioSegment
import wave
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

class Model:
    def __init__(self):
        self.original_file = None
        self.preprocessed_file = None
        self.freq = None
        self.spec = None
        self.graph_time = None
        self.target_freq = None

        self.time = None
        self.channels = None
        self.res = None
        self.rt60 = None

        self.waveform_time = None
        self.signal = None

        self.sample_rate = None
        self.data = None

        self.db_data = None
    
    # This method converts an audio file to wav type while also loading it
    def to_wav(self):
        filename = self.original_file
        # takes name of file and concatenates .wav
        new_filename = os.path.splitext(filename)[0] + '.wav'
        # load file
        wav_audio = AudioSegment.from_file(filename)
        # exports file as wav
        wav_audio.export(new_filename, format="wav")

    # This method gets rid off any meta while alsos splitting multiple channels into one
    # It also creates information for other fucntions too do calculations with
    def preprocess_data(self, file):
        self.original_file = file
        self.to_wav()
        sof = os.path.splitext(self.original_file)[0] + '.wav'
        # variable for single channel
        original_audio = pydub.AudioSegment.from_file(sof, format="wav")
        new_filename = os.path.splitext(sof)[0] + '_modified.wav'
        self.preprocessed_file = new_filename
        # sets one channel
        mono_audio = original_audio.set_channels(1)
        # export file and removes metadata
        mono_audio.export(new_filename, format="wav", tags={}, )

        # necessary info for calculations in other methods
        filename = self.preprocessed_file
        sample_rate, data = wavfile.read(filename)
        spectrum, freqs, time, _ = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        self.freq = freqs
        self.spec = spectrum
        self.graph_time = time

    # finds the reverb at t60 using other methods we define below
    def find_rt60(self):
        self.rt60 = str(((self.local_rt60(1) + self.local_rt60(2) + self.local_rt60(3)) / 3) - 0.5)

    # gets data about file (time, channels, resonance)
    def get_data(self):
        a = pydub.AudioSegment.from_file(file=self.preprocessed_file, format="wav")
        self.time = str(len(a) / 1000)
        self.channels = str(a.channels)
        self.res = str(a.max)

    # gets waveform data from audio file
    def get_waveform_data(self):
        filename = self.preprocessed_file
        spf = wave.open(filename, "r")
        # get audio from wav file
        self.signal = spf.readframes(-1)
        self.signal = np.fromstring(self.signal, "int16")
        fs = spf.getframerate()
        self.waveform_time = np.linspace(0, len(self.signal) / fs, num=len(self.signal))

    # gets sample rate and data from single channel audio
    def get_spec_data(self):
        filename = self.preprocessed_file
        self.sample_rate, self.data = wavfile.read(filename)

    # finds frequency and calculates the digital signal to decibals
    def check_freq(self, gate):
        # see which frequency to find and save it  to target frequency
        match gate:
            case 1:
                self.target_freq = self.mid_freq(self.freq)
            case 2:
                self.target_freq = self.low_freq(self.freq)
            case 3:
                self.target_freq = self.high_freq(self.freq)
        # index where freq is equal to target freq
        freq_index = np.where(self.freq == self.target_freq)[0][0]
        # find sound data in spectrogram using index
        data_for_frequency = self.spec[freq_index]

        epsilon = 1e-10
        data_for_frequency = data_for_frequency + epsilon
        # signal to db
        db_data = 10 * np.log10(data_for_frequency)
        self.db_data = db_data
        return db_data

    # returns local reverb at t60 using index parameter i
    def local_rt60(self, i):
        db_data = self.check_freq(i)
        # index of max value in decibal data
        max_index = np.argmax(db_data)
        # max value of decibal data
        max_value = db_data[max_index]

        # slice decibal data [max value:]
        modified_db_data = db_data[max_index:]

        # find value and index of max value minus 5 decibals
        max_minus_five = max_value - 5
        max_minus_five = self.closest_value(modified_db_data, max_minus_five)
        index_minus_five = np.where(db_data == max_minus_five)

        # find value and index of max value minus 25 decibals
        max_minus_twenty_five = max_value - 25
        max_minus_twenty_five = self.closest_value(modified_db_data, max_minus_twenty_five)
        index_minus_twenty_five = np.where(db_data == max_minus_twenty_five)

        # calculate rt20 using max value minus 5 and 25 decibal data
        rt20 = (self.graph_time[index_minus_five] - self.graph_time[index_minus_twenty_five])[0]

        # calculate rt60 usisng rt20
        rt60 = 3 * rt20
        rt60 = round(abs(rt60), 2)
        return rt60

    # defines low freq range
    @staticmethod
    def low_freq(freq):
        for i in freq:
            if i > 250:
                break
        return i

    # defines mid freq range
    @staticmethod
    def mid_freq(freq):
        for i in freq:
            if i > 2000:
                break
        return i

    # defines high freq range
    @staticmethod
    def high_freq(freq):
        for i in freq:
            if i > 20000:
                break
        return i

    # calculates the closest value in an array to the value passed as a parameter
    @staticmethod
    def closest_value(array, value):
        # np array
        array = np.asarray(array)
        # absolute value of element wise difference in array, then returns minimum difference's index
        idx = (np.abs(array - value)).argmin()
        # returns the mininmum difference
        return array[idx]