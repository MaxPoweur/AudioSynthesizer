import threading
from tkinter import *

from Enums.ButtonState import *


class View(Frame):

    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""

    def __init__(self, window, master):

        self.master = master

        self.window = window
        #width = 768, height = 576,

        self.workspace = Frame(window, borderwidth=2, bg="#E1DDDD")

        self.frameWorkspace = Frame(self.window, padx=20, pady=20)
        self.frameWorkspace.grid(row=0, column=0, padx=20, pady=20)

        self.stateColorButton = "#5E3F6F"
        self.stateColorActiveButton = "#8C567E"
        self.modeColorButton = "#90AA90"
        self.modeColorActiveButton = "#A52B2B"
        self.disabledButton = "#BAB5B5"

        self.buttonsMask = "111111"

        self.playButton = Label(self.frameWorkspace, text="Play", fg="white", relief=GROOVE)
        self.playButton.grid(row=0, column=0, ipadx = 10, ipady = 10, padx=10)

        self.breakButton = Label(self.frameWorkspace, text="Break", fg="white", relief=GROOVE)
        self.breakButton.grid(row=0, column=1, ipadx = 10, ipady = 10, padx=10)

        self.stopButton = Label(self.frameWorkspace, text="Stop", fg="white", relief=GROOVE)
        self.stopButton.grid(row=0, column=2, ipadx = 10, ipady = 10, padx=10)

        self.saveFileButton = Label(self.frameWorkspace, text="Save", fg="white", relief=GROOVE)

        self.frameSelectionMode = Frame(self.window, padx=20, pady=20)
        self.frameSelectionMode.grid(row=1, column=0, padx=20, pady=20)

        self.freestyleButton = Label(self.frameSelectionMode, text="Freestyle", fg="#FBFCFB", relief=GROOVE)
        self.freestyleButton.grid(row=1, column=2, ipadx = 10, ipady = 10, padx=10)

        self.readingFileButton = Label(self.frameSelectionMode, text="Read file", fg="#FBFCFB", relief=GROOVE)
        self.readingFileButton.grid(row=1, column=3, ipadx = 10, ipady = 10, padx=10)

        self.recordButton = Label(self.frameSelectionMode, text="Record", fg="#FBFCFB", relief=GROOVE)
        self.recordButton.grid(row=1, column=4, ipadx = 10, ipady = 10, padx=10)

        self.stateButtons = {self.playButton: ButtonState.DISABLED, self.breakButton: ButtonState.DISABLED,
                             self.stopButton: ButtonState.DISABLED, self.saveFileButton: ButtonState.DISABLED}

        self.modeButtons = {self.freestyleButton: ButtonState.ACTIVE, self.readingFileButton: ButtonState.NORMAL,
                            self.recordButton: ButtonState.NORMAL}


        self.updateThread = threading.Thread(target=self.update, args=())
        self.updateThread.daemon = True
        self.updateThread.start()

    def updateButtonState(self, widget, state):
        if widget in self.stateButtons:
            self.stateButtons[widget] = state
        elif widget in self.modeButtons:
            self.modeButtons[widget] = state

    def getButtonState(self, widget):
        if widget in self.stateButtons:
            return self.stateButtons[widget]
        elif widget in self.modeButtons:
            return self.modeButtons[widget]

    def update(self):
        while True:
            for button in self.stateButtons:
                if self.stateButtons[button] == ButtonState.NORMAL:
                    button["bg"] = self.stateColorButton
                    button.bind("<1>", self.master.callbackButton)
                    button.bind("<Enter>", self.buttonHover)
                    button.bind("<Leave>", self.buttonLeave)
                elif self.stateButtons[button] == ButtonState.ACTIVE:
                    button["bg"] = self.stateColorActiveButton
                    button.bind("<1>", self.master.callbackButton)
                    button.bind("<Enter>", self.buttonHover)
                    button.bind("<Leave>", self.buttonLeave)
                elif self.stateButtons[button] == ButtonState.DISABLED:
                    button["bg"] = self.disabledButton
                    button.bind("<1>", lambda e: None)
                    button.bind("<Enter>", lambda e: None)
                    button.bind("<Leave>", lambda e: None)

            for button in self.modeButtons:
                if self.modeButtons[button] == ButtonState.NORMAL:
                    button["bg"] = self.modeColorButton
                    button.bind("<1>", self.master.callbackButton)
                    button.bind("<Enter>", self.buttonHover)
                    button.bind("<Leave>", self.buttonLeave)
                elif self.modeButtons[button] == ButtonState.ACTIVE:
                    button["bg"] = self.modeColorActiveButton
                    button.bind("<1>", self.master.callbackButton)
                    button.bind("<Enter>", self.buttonHover)
                    button.bind("<Leave>", self.buttonLeave)
                elif self.modeButtons[button] == ButtonState.DISABLED:
                    button["bg"] = self.disabledButton
                    button.bind("<1>", lambda e: None)
                    button.bind("<Enter>", lambda e: None)
                    button.bind("<Leave>", lambda e: None)

    def bindings(self):
        # hover styles

        self.freestyleButton.bind('<Enter>', self.buttonHover)
        self.readingFileButton.bind('<Enter>', self.buttonHover)
        self.recordButton.bind('<Enter>', self.buttonHover)
        self.playButton.bind('<Enter>', self.buttonHover)
        self.breakButton.bind('<Enter>', self.buttonHover)
        self.stopButton.bind('<Enter>', self.buttonHover)
        self.saveFileButton.bind('<Enter>', self.buttonHover)

        self.freestyleButton.bind('<Leave>', self.buttonLeave)
        self.readingFileButton.bind('<Leave>', self.buttonLeave)
        self.recordButton.bind('<Leave>', self.buttonLeave)
        self.playButton.bind('<Leave>', self.buttonLeave)
        self.breakButton.bind('<Leave>', self.buttonLeave)
        self.stopButton.bind('<Leave>', self.buttonLeave)
        self.saveFileButton.bind('<Leave>', self.buttonLeave)

        # click callbacks

        self.freestyleButton.bind('<1>', self.master.callbackButton)
        self.readingFileButton.bind('<1>', self.master.callbackButton)
        self.recordButton.bind('<1>', self.master.callbackButton)
        self.playButton.bind('<1>', self.master.callbackButton)
        self.breakButton.bind('<1>', self.master.callbackButton)
        self.stopButton.bind('<1>', self.master.callbackButton)
        self.saveFileButton.bind('<1>', self.master.callbackButton)

    def buttonHover(self, event):   # We just darken the button color
        if self.getButtonState(event.widget) == ButtonState.ACTIVE:
            self.updateButtonState(event.widget, ButtonState.ACTIVEANDHOVER)
        else:
            self.updateButtonState(event.widget, ButtonState.HOVER)

        newIntColor = int(event.widget["bg"][1:], 16) # Convert the HTML Color (hex) to integer
        newIntColor = newIntColor - int(self.buttonsMask, 16)  # Apply a mask to the current HTML color
        newHexColor = hex(newIntColor)[2:] # Convert the Int to Hex Color
        event.widget["bg"] = "#"+str(newHexColor)

    def buttonLeave(self, event):   # We just lighten the button color
        if self.getButtonState(event.widget) == ButtonState.ACTIVEANDHOVER:
            self.updateButtonState(event.widget, ButtonState.ACTIVE)
        newIntColor = int(event.widget["bg"][1:], 16) # Convert the HTML Color (hex) to integer
        newIntColor = newIntColor + int(self.buttonsMask, 16)  # Apply a mask to the current HTML color
        newHexColor = hex(newIntColor)[2:] # Convert the Int to Hex Color
        event.widget["bg"] = "#"+str(newHexColor)

    def hideButton(self, widget):
        widget.grid_forget()

    def visibleButton(self, widget):
        widget.grid(row=0, column=3, ipadx = 10, ipady = 10, padx=10)