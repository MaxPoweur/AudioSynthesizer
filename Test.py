from lxml import etree
tree = etree.parse("bindings.xml")
letters = list()
notes = list()
for letter in tree.xpath("/keyboardBindings/gamme/binding/letter"):
    letters.append(letter.text)
for note in tree.xpath("/keyboardBindings/gamme/binding/note"):
    notes.append(note.text)

bindings = dict(zip(letters, notes))
print(bindings)