from __future__ import division

import threading
from time import *

import numpy as np
from Enums.AudioSynthesizerState import *
from Enums.AudioSynthesizerMode import *
from Enums.ReadingFileModeState import *

from pyaudio import *
from KeyboardBindings import *

try:
    from itertools import izip
except ImportError: # Python 3
    izip = zip
    xrange = range

class AudioSynthesizer:
    """description of class"""

    def __init__(self, allowingLongTones):
            self.keyboardBindings = KeyboardBindings("bindings.xml")
            self.allowLongTones = allowingLongTones
            self.mode = AudioSynthesizerMode.FREESTYLE
            self.audioSynthesizerState = AudioSynthesizerState.SLEEPING
            self.toneDuration = 1.5
            self.p = PyAudio()

    def saveFile(self, filename, text):
        with open(filename, 'w') as file:
            file.write(text)

    def readFile(self, path):
        file = open(path, "r")
        content = file.read()

        for char in content:
            if self.state == ReadingFileModeState.STOPPED:
                file.close()
                return
            while self.state == ReadingFileModeState.ONBREAK or self.audioSynthesizerState == AudioSynthesizerState.PLAYING:  # Waiting for the previous tone to be played
                if self.state == ReadingFileModeState.STOPPED:
                    file.close()
                    return
                pass
            if char in ' ':
                sleep(1)
            else:
                frequency = self.keyboardBindings.getFrequency(char)
                if frequency!=-1:
                    self.playMusicalNote(frequency)
        self.state = ReadingFileModeState.STOPPED
        self.audioSynthesizerState = AudioSynthesizerState.SLEEPING
        file.close()

    def playMusicalNote(self, frequency):
        threading.Thread(target=self.playTone, args=(frequency, self.toneDuration)).start()

    def delayBeforeEachSameTone(self, note):
        debut = time()
        while (time()-debut) < (self.toneDuration/5):   # Why only 20% ?
            pass
        self.tonesState[note] = False

    def playTone(self, frequency, duration, volume=1.0, sample_rate=22050):

        self.audioSynthesizerState = AudioSynthesizerState.PLAYING
        #print(str(frequency) + " Hz")

        # generate samples, note conversion to float32 array
        samples = (np.sin(2 * np.pi * np.arange(sample_rate * duration) * frequency / sample_rate)).astype(np.float32)

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        stream = self.p.open(format=paFloat32,
                        channels=1,
                        rate=sample_rate,
                        output=True)

        # play. May repeat with different volume values (if done interactively)
        stream.write(volume * samples)

        stream.stop_stream()
        stream.close()

        self.audioSynthesizerState = AudioSynthesizerState.SLEEPING

