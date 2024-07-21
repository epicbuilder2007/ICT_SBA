import tkinter as tk
from tkinter import filedialog
import os
import classes

# Runtime Variables
filepath = ""
content = ""


def import_file():
    global filepath
    global content
    filepath = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select a file...",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))
    with open(filepath, 'rb') as file:
        content = file.read().decode('ascii', 'ignore')


class CoreInterfaceElements:

    class CoreFrame(tk.Frame):
        def __init__(self, parent: tk.Tk):
            parent.update()
            super().__init__(parent, width=parent.winfo_width(), height=parent.winfo_height())
            self.columnconfigure(index=0, weight=2)
            self.columnconfigure(index=0, weight=1)


    class CoreButton(tk.Button):
        def __init__(self, parent, func):
            super().__init__(parent, command=func)

        def text(self, string):
            self.configure(text=string)

    class CoreLabel(tk.Label):
        def __init__(self, parent):
            super().__init__(parent)
            self.configure(font=("Nunito", 12))

        def text(self, string):
            self.configure(text=string)


    class CoreDropList(tk.Listbox):
        def __init__(self, parent, options: list, height):
            super().__init__(parent, listvariable=tk.Variable(value=options), height=height)


Modes = classes.Modes()
PluginLoader = classes.PluginLoader()

main = tk.Tk()
main.geometry('600x400')
main.title("Freqy! Beta 0.2.0")
frame = CoreInterfaceElements.CoreFrame(main)
frame.grid_propagate(False)

import_label = CoreInterfaceElements.CoreLabel(frame)
import_label.text("1. Import a file or enter a string.")
import_label.grid_propagate(False)
import_label.grid(column=0, row=0)

import_button = CoreInterfaceElements.CoreButton(frame, import_file)
import_button.text("Import File...")
import_label.grid_propagate(False)
import_button.grid(column=1, row=0)

textbox = tk.Entry(frame)
textbox.grid(column=0, row=1)
textbox.grid_propagate(True)

modeselectlabel = CoreInterfaceElements.CoreLabel(frame)
modeselectlabel.text("2. Choose a mode or plugin to use.")
modeselectlabel.grid_propagate(False)
modeselectlabel.grid(column=0, row=2)

englishorspanish = CoreInterfaceElements.CoreDropList(frame, ["Built-in Modes", "Plugins"], 2)
englishorspanish.grid_propagate(True)
englishorspanish.grid(column=1, row=2)

modeselection = CoreInterfaceElements.CoreDropList(frame, ["placeholder"], 1)
modeselection.grid(column=0, row=3)


def EoSSelChange(event):
    selected = englishorspanish.curselection()
    if selected[0] == 0:
        modeselection.configure(listvariable=tk.Variable(value=list(Modes.callfunction.values())), height=len(list(Modes.callfunction.values())))
    else:
        modeselection.configure(listvariable=tk.Variable(value=PluginLoader.list_plugins()), height=len(PluginLoader.list_plugins()))


englishorspanish.bind('<<ListboxSelect>>', EoSSelChange)
frame.grid(column=0, row=0)
main.mainloop()
