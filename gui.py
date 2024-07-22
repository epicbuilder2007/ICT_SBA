import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import classes

# Runtime Variables
filepath = ""
content = ""
mode = ""
plugin = False


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
            self.columnconfigure(index=0, weight=1)
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


    class CoreListBox(tk.Listbox):
        def __init__(self, parent, options: list):
            super().__init__(parent, listvariable=tk.Variable(value=options), height=len(options))
    
    class CoreDropList(ttk.Combobox):
        def __init__(self, parent, options: list):
            super().__init__(parent, textvariable=tk.StringVar())
            self['values'] = options
            self['state'] = 'readonly'
    
    class CoreCheckbox(ttk.Checkbutton):
        def __init__(self, parent, name, func):
            super().__init__(parent, text=name, command=func, variable = tk.StringVar())

Modes = classes.Modes()
PluginLoader = classes.PluginLoader()

main = tk.Tk()
main.geometry('600x400')
main.title("Freqy! Beta 0.2.0")
frame = CoreInterfaceElements.CoreFrame(main)
frame.grid_propagate(False)

# Step 1

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

# Step 2

modeselectlabel = CoreInterfaceElements.CoreLabel(frame)
modeselectlabel.text("2. Choose a mode or plugin to use.")
modeselectlabel.grid_propagate(False)
modeselectlabel.grid(column=0, row=2)

englishorspanish = CoreInterfaceElements.CoreListBox(frame, ["Built-in Modes", "Plugins"])
englishorspanish.grid_propagate(True)
englishorspanish.grid(column=1, row=2)

modeselection = CoreInterfaceElements.CoreDropList(frame, ["placeholder"])
modeselection.grid(column=0, row=3)


def EoSSelChange(event):
    selected = englishorspanish.curselection()
    if len(selected) > 0 and selected[0] == 0:
        modeselection['values'] = list(Modes.callfunction.values())
        plugins = False
    else:
        modeselection['values'] = PluginLoader.list_plugins()
        plugin = True


def MSSelChange(event):
    mode = modeselection.get()

englishorspanish.bind('<<ListboxSelect>>', EoSSelChange)
modeselection.bind('<<ComboboxSelected>>', MSSelChange)

# Step 3

additionaloptionslabel = CoreInterfaceElements.CoreLabel(frame)
additionaloptionslabel.text("3. Choose additional flags")
additionaloptionslabel.grid_propagate(False)
additionaloptionslabel.grid(column=0, row=4)

flagframe = CoreInterfaceElements.CoreFrame(frame)
flagframe.grid_propagate(False)

def lowercasefunc():
    Modes.lower = True if lowercase.get() == 1 else False

lowercase = CoreInterfaceElements.CoreCheckbox(frame, "lowercase only", lowercasefunc)
lowercase.grid(column=0, row=6)
flagframe.grid(column=0, row=5)

frame.grid(column=0, row=0)

# Start Program
main.mainloop()
