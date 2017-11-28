from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfilename
from win32gui import *

from pynput import keyboard

from AudioSynthesizer import *
from Enums.ButtonState import *
from View import View

from Enums.FreestyleModeState import *
from Enums.ReadingFileModeState import *
from Enums.RecordingModeState import *


class Controller:

    def __init__(self):
        self.window = Tk()
        self.window.title("Synthetiseur audio")
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)
        self.model = AudioSynthesizer(allowingLongTones=True)

        self.view = View(self.window, self)
        self.toSave = ""
        self.keyboardListener = threading.Thread(target=self.keyboardListener, args=())
        self.keyboardListener.daemon = True # makes the thread to get killed when the gui is closed
        self.keyboardListener.start()
        self.updatingGUIThread = threading.Thread(target=self.updateGUI, args=())
        self.updatingGUIThread.daemon = True
        self.updatingGUIThread.start()

        self.window.mainloop()

    def callbackButton(self, event):
        if event.widget["text"]=="Freestyle":
            self.freestyleButton(event)
        elif event.widget["text"]=="Read file":
            self.playfileButton(event)
        elif event.widget["text"]=="Record":
            self.recordButton(event)
        elif event.widget["text"]=="Play":
            self.playButton(event)
        elif event.widget["text"]=="Break":
            self.breakButton(event)
        elif event.widget["text"]=="Stop":
            self.stopButton(event)
        elif event.widget["text"]=="Save":
            self.saveButton(event)

    def freestyleButton(self, event):
        self.model.mode = AudioSynthesizerMode.FREESTYLE
        self.model.state = FreestyleModeState.SLEEPING

    def updateGUI(self):
        while True:
            if self.model.mode == AudioSynthesizerMode.FREESTYLE:
                self.view.updateButtonState(self.view.freestyleButton, ButtonState.ACTIVE)
                self.view.updateButtonState(self.view.readingFileButton, ButtonState.NORMAL)
                self.view.updateButtonState(self.view.recordButton, ButtonState.NORMAL)
                self.view.updateButtonState(self.view.playButton, ButtonState.ACTIVE)
                self.view.updateButtonState(self.view.breakButton, ButtonState.DISABLED)
                self.view.updateButtonState(self.view.stopButton, ButtonState.DISABLED)
                self.view.hideButton(self.view.saveFileButton)

            elif self.model.mode == AudioSynthesizerMode.READINGFILE:
                self.view.updateButtonState(self.view.readingFileButton, ButtonState.ACTIVE)
                self.view.hideButton(self.view.saveFileButton)
                if self.model.state == ReadingFileModeState.ONBREAK: # play on; break active; stop on;
                    self.view.updateButtonState(self.view.playButton, ButtonState.NORMAL)
                    self.view.updateButtonState(self.view.breakButton, ButtonState.ACTIVE)
                    self.view.updateButtonState(self.view.stopButton, ButtonState.NORMAL)
                    self.view.updateButtonState(self.view.freestyleButton, ButtonState.DISABLED)
                    self.view.updateButtonState(self.view.recordButton, ButtonState.DISABLED)

                elif self.model.state == ReadingFileModeState.STOPPED: # play on; break off; stop off;
                    self.view.updateButtonState(self.view.playButton, ButtonState.NORMAL)
                    self.view.updateButtonState(self.view.breakButton, ButtonState.DISABLED)
                    self.view.updateButtonState(self.view.stopButton, ButtonState.ACTIVE)
                    self.view.updateButtonState(self.view.freestyleButton, ButtonState.NORMAL)
                    self.view.updateButtonState(self.view.recordButton, ButtonState.NORMAL)

                elif self.model.state == ReadingFileModeState.READING: # play active;  break on; stop on;
                    self.view.updateButtonState(self.view.playButton, ButtonState.ACTIVE)
                    self.view.updateButtonState(self.view.breakButton, ButtonState.NORMAL)
                    self.view.updateButtonState(self.view.stopButton, ButtonState.NORMAL)
                    self.view.updateButtonState(self.view.freestyleButton, ButtonState.DISABLED)
                    self.view.updateButtonState(self.view.recordButton, ButtonState.DISABLED)

            elif self.model.mode == AudioSynthesizerMode.RECORDING:
                self.view.updateButtonState(self.view.recordButton, ButtonState.ACTIVE)
                self.view.visibleButton(self.view.saveFileButton)
                if self.model.state == RecordingModeState.RECORDING:
                    self.view.updateButtonState(self.view.playButton, ButtonState.ACTIVE)
                    self.view.updateButtonState(self.view.breakButton, ButtonState.NORMAL)
                    self.view.updateButtonState(self.view.stopButton, ButtonState.NORMAL)
                    self.view.updateButtonState(self.view.saveFileButton, ButtonState.DISABLED)
                    self.view.updateButtonState(self.view.freestyleButton, ButtonState.DISABLED)
                    self.view.updateButtonState(self.view.readingFileButton, ButtonState.DISABLED)

                elif self.model.state == RecordingModeState.ONBREAK:
                    self.view.updateButtonState(self.view.playButton, ButtonState.NORMAL)
                    self.view.updateButtonState(self.view.breakButton, ButtonState.ACTIVE)
                    self.view.updateButtonState(self.view.stopButton, ButtonState.NORMAL)
                    if self.toSave != "" :
                        self.view.updateButtonState(self.view.saveFileButton, ButtonState.NORMAL)
                    else:
                        self.view.updateButtonState(self.view.saveFileButton, ButtonState.DISABLED)
                    self.view.updateButtonState(self.view.freestyleButton, ButtonState.DISABLED)
                    self.view.updateButtonState(self.view.readingFileButton, ButtonState.DISABLED)

                elif self.model.state == RecordingModeState.STOPPED:
                    self.view.updateButtonState(self.view.playButton, ButtonState.NORMAL)
                    self.view.updateButtonState(self.view.breakButton, ButtonState.DISABLED)
                    self.view.updateButtonState(self.view.stopButton, ButtonState.ACTIVE)
                    self.view.updateButtonState(self.view.saveFileButton, ButtonState.DISABLED)
                    self.view.updateButtonState(self.view.freestyleButton, ButtonState.NORMAL)
                    self.view.updateButtonState(self.view.readingFileButton, ButtonState.NORMAL)

            sleep(0.05) # pour que ça ne consomme pas trop de CPU mais sans rajouter trop de délais

    def playfileButton(self, event):
        if self.model.mode != AudioSynthesizerMode.READINGFILE \
        or (self.model.mode == AudioSynthesizerMode.READINGFILE and self.model.state == ReadingFileModeState.STOPPED):
            newName = askopenfilename()
            if newName!='':
                self.filename = newName
            if hasattr(self, "filename") and self.filename != "":
                self.model.mode = AudioSynthesizerMode.READINGFILE
                self.model.state = ReadingFileModeState.STOPPED


    def recordButton(self, event):
        self.model.mode = AudioSynthesizerMode.RECORDING
        self.model.state = RecordingModeState.STOPPED

    def playButton(self, event):
        if self.model.mode == AudioSynthesizerMode.READINGFILE and self.model.state != ReadingFileModeState.READING:
            self.model.state = ReadingFileModeState.READING
            if not hasattr(self, 'currentFileReadingThread') or (hasattr(self, 'currentFileReadingThread') and not self.currentFileReadingThread.isAlive()):
                self.currentFileReadingThread = threading.Thread(target=self.model.readFile, args=(self.filename,))
                self.currentFileReadingThread.daemon = True
                self.currentFileReadingThread.start()

        elif self.model.mode == AudioSynthesizerMode.RECORDING:
            self.model.state = RecordingModeState.RECORDING

    def breakButton(self, event):
        if self.model.mode == AudioSynthesizerMode.READINGFILE and self.model.state == ReadingFileModeState.READING:
            self.model.audioSynthesizerState = AudioSynthesizerState.SLEEPING
            self.model.state = ReadingFileModeState.ONBREAK
        elif self.model.mode == AudioSynthesizerMode.RECORDING:
            self.model.audioSynthesizerState = AudioSynthesizerState.SLEEPING
            self.model.state = RecordingModeState.ONBREAK

    def stopButton(self, event):
        if self.model.mode == AudioSynthesizerMode.READINGFILE:
            self.model.audioSynthesizerState = AudioSynthesizerState.SLEEPING
            self.model.state = ReadingFileModeState.STOPPED
        elif self.model.mode == AudioSynthesizerMode.RECORDING:
            self.model.audioSynthesizerState = AudioSynthesizerState.SLEEPING
            self.model.state = RecordingModeState.STOPPED
            self.toSave = ""

    def saveButton(self, event):
        f = asksaveasfile(mode='w', defaultextension=".whynot")
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        f.write(self.toSave)
        f.close()
        self.model.state = RecordingModeState.STOPPED
        self.toSave = ""

    def onClose(self):
        self.model.audioSynthesizerState = AudioSynthesizerState.SLEEPING
        if self.model.mode == AudioSynthesizerMode.READINGFILE:
            self.model.state = ReadingFileModeState.STOPPED
        self.window.quit()
        self.window.destroy()
        exit(0)

    def keyboardListener(self):
        with keyboard.Listener(on_press=self.onPress, on_release=self.onRelease) as listener:
            listener.join()

    def onPress(self, key):
        try:
            if not self.isCurrentActiveWindow():
                return
            canPlayTone = False
            if self.model.mode == AudioSynthesizerMode.FREESTYLE or (self.model.mode == AudioSynthesizerMode.RECORDING and self.model.state==RecordingModeState.RECORDING):
                if self.model.audioSynthesizerState == AudioSynthesizerState.SLEEPING and not self.model.allowLongTones:
                    canPlayTone = True
                elif self.model.allowLongTones:
                    canPlayTone = True

            if canPlayTone:
                if self.model.mode == AudioSynthesizerMode.RECORDING:
                    self.toSave += key.char
                frequency = self.model.keyboardBindings.getFrequency(key.char)
                if frequency != None and frequency!=-1:
                    self.model.playMusicalNote(frequency)
        except Exception:
           print('special key {0} pressed'.format(key))

    def onRelease(self, key): # Callback to 'release' key event
        pass

    def isCurrentActiveWindow(self): # Check if current active window is our audio synthesizer
        return "Synthetiseur audio" == GetWindowText(GetForegroundWindow())

program = Controller()