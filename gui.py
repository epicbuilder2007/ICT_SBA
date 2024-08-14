import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import os
import classes
Modes = classes.Modes()
Sort = classes.Sort()
PluginLoader = classes.PluginLoader()
import matplotlib.pyplot as mapo # mapo tofu lol

# Runtime Variables
plugin = False
name = "Freqy! Beta 0.2.5"


def import_file():
    Modes.filepath = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select a file...",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))
    with open(Modes.filepath, 'rb') as file:
        Modes.content = file.read().decode('ascii', 'ignore')
        logbox.addtext("[gui.import_file - INFO] Imported file " + Modes.filepath)


def lowercasefunc():
    Modes.lower = lowercase.state.get()
    logbox.addtext("[lowercasefunc - INFO] -lower flag " + ("ENABLED" if Modes.lower else "DISABLED"))


def EoSSelChange(event):
    global plugin
    selected = englishorspanish.curselection()
    if len(selected) > 0:
        if selected[0] == 0:
            modeselection['values'] = list(Modes.callfunction.keys())
            plugin = False
            logbox.addtext("[EoSSelChange - INFO] Mode selection changed to: Built-in Modes")
        else:
            modeselection['values'] = PluginLoader.list_plugins()
            plugin = True
            logbox.addtext("[EoSSelChange - INFO] Mode selection changed to: Plugins")

def MSSelChange(event):
    Modes.mode = str(modeselection.get())
    logbox.addtext("[MSSelChange - INFO] Set operation mode to: " + Modes.mode)


def Submit():
    if Modes.filepath == "":
        Modes.content = textbox.get()
        Modes.filepath = "Text Input"
    logbox.addtext(f"Program activated with parameters: \n - file/text: {Modes.filepath if Modes.filepath != '' else Modes.content} \n - mode: {('PLUGIN ' if plugin else '') + Modes.mode} \n - lowercase only: {str(Modes.lower)}")
    textbox.delete(0, 'end')
    if plugin:
        imported = PluginLoader.import_plugin(Modes.mode)
        imported.main(Modes)
    else:
        print(Modes.callfunction)
        Modes.callfunc()
        final = Sort.heapsort(Modes.result)
        fig = mapo.figure(figsize=(len(list(final.keys()))*0.3, 5))
        mapo.bar(list(final.keys()), list(final.values()), color="blue", width=0.25)
        mapo.xlabel(Modes.mode)
        mapo.ylabel("Frequency")
        fig.tight_layout()
        mapo.show()
    Modes.clear()


# this class is declared here so I don't have to import tkinter when I don't have to.
class CoreInterfaceElements:

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
            self.state = tk.BooleanVar()
            super().__init__(parent, text=name, command=func, variable=self.state)

    class LogBox(ScrolledText):
        def __init__(self, parent, width, height):
            super().__init__(parent, width=width, height=height)
            self.insert(tk.END, f"{name} - Log started")
            self.config(state='disabled')
        def addtext(self, string):
            self.config(state='normal')
            self.insert(tk.END, "\n\n" + string)
            self.config(state='disabled')


if __name__ == "__main__":
    main = tk.Tk()
    main.geometry('600x400')
    main.title(name)
    main.columnconfigure(index=0, weight=2)
    main.columnconfigure(index=1, weight=1)

    # Step 1

    import_label = CoreInterfaceElements.CoreLabel(main)
    import_label.text("1. Import a file or enter a string.")
    import_label.grid(column=0, row=0)

    import_button = CoreInterfaceElements.CoreButton(main, import_file)
    import_button.text("Import File...")
    import_button.grid(column=1, row=0)

    textbox = tk.Entry(main, textvariable=tk.StringVar())
    textbox.grid(column=0, row=1)

    lowercase = CoreInterfaceElements.CoreCheckbox(main, "Force All Lowercase", lowercasefunc)
    lowercase.grid(column=1, row=1)

    # Step 2

    modeselectlabel = CoreInterfaceElements.CoreLabel(main)
    modeselectlabel.text("2. Choose a mode or plugin to use.")
    modeselectlabel.grid(column=0, row=2)

    englishorspanish = CoreInterfaceElements.CoreListBox(main, ["Built-in Modes", "Plugins"])
    englishorspanish.grid(column=1, row=3)
    englishorspanish.bind('<<ListboxSelect>>', EoSSelChange)

    modeselection = CoreInterfaceElements.CoreDropList(main, ["placeholder"])
    modeselection.grid(column=0, row=3)
    modeselection.bind('<<ComboboxSelected>>', MSSelChange)

    # Submit Form

    submit = CoreInterfaceElements.CoreButton(main, Submit)
    submit.text("Generate Graph!")
    submit.grid(column=0, row=4)

    # Logs
    logbox = CoreInterfaceElements.LogBox(main, width=50, height=10)
    logbox.grid(column=0, row=6, pady=10, )

    # Start Program
    main.mainloop()
