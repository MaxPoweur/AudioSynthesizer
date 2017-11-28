from Notes import *
from lxml import etree
class KeyboardBindings:

    def __init__(self, file):
        tree = etree.parse(file)
        letters = list()
        frequences = list()
        for letter in tree.xpath("/keyboardBindings/gamme/binding/letter"):
            letters.append(letter.text)
        for note in tree.xpath("/keyboardBindings/gamme/binding/note"):
            frequences.append(self.calculateFrequency(note.text))
        self.bindings = dict(zip(letters, frequences))

    def calculateFrequency(self, note):
        try:
            if note[0:-1] in Notes.NOTES.keys():
                return Notes.NOTES.get(note[0:-1])*2**int(note[-1:])
            else:
                raise Exception("Error with note format.")
        except ValueError:
            print("Parse error from bindings file.")

    def getFrequency(self, char):
        for letter in self.bindings.keys():
            if char in letter:
                return self.bindings.get(letter)
        return -1