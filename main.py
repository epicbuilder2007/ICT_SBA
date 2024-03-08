import sys
from console_handler import *

filepath = "file.txt"
if "-f" in sys.argv:
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-f":
            filepath = sys.argv[i+1]

    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
elif "-t" in sys.argv:
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-t":
            content = sys.argv[i+1]
    filepath = f"command argument: {content}"
else:
    raise Exception("Error: No input mode is selected.")


class mode:
    def __init__(self):
        self.callfunction = {self.alphawords: "alphawords",
                             self.numeric: "numeric",
                             self.all: "all",
                             self.alpha: "alpha",
                             self.alphanumeric: "alphanumeric",
                             self.text_info: "text_info"
                             }

    def callfunc(self, freqmode: str, content):
        for key, value in self.callfunction.items():
            if value == freqmode:
                letter = key(content)
                return letter

        raise Exception(f"mode {freqmode} does not exist.")

    def alphawords(self, content: str):
        primary = content.split(" ")
        wordlist = []
        for i in range(len(primary)):
            wordlist += primary[i].split("\n")
        for i in range(len(wordlist)):
            sep_word = list(wordlist[i])
            offset = 0
            for j in range(len(sep_word)):
                if not sep_word[j-offset].isalpha():
                    del sep_word[j-offset]
                    offset += 1
            if len(sep_word) > 0:
                wordlist[i] = "".join(sep_word)

        frequency = {}
        for i in wordlist:
            if i.lower() not in frequency:
                frequency[i.lower()] = 1
            else:
                frequency[i.lower()] += 1

        if '' in frequency:
            del frequency['']
        return frequency

    def numeric(self, content: str):
        frequency = {}
        for i in content:
            if i.isnumeric():
                if i not in frequency:
                    frequency[i] = 1
                else:
                    frequency[i] += 1
        return frequency

    def all(self, content: str):
        frequency = {}
        for i in content:
            if i not in frequency:
                frequency[i] = 1
            else:
                frequency[i] += 1
        return frequency

    def alpha(self, content: str):
        frequency = {}
        for i in content:
            if i.isalpha():
                if i.lower() not in frequency:
                    frequency[i.lower()] = 1
                else:
                    frequency[i.lower()] += 1
        return frequency

    def alphanumeric(self, content: str):
        frequency = {}
        for i in content:
            if i.isalpha() or i.isnumeric():
                if i not in frequency:
                    frequency[i] = 1
                else:
                    frequency[i] += 1
        return frequency

    def text_info(self, content: str):
        info = {}
        info["word count"] = sum(list(self.alphawords(content).values()))
        info["character count"] = len(content)
        info["paragraph count"] = sum([1 if content.split("\n")[i] != '' else 0 for i in range(len(content.split("\n")))])
        return info

searchmode = "all"
if "-m" in sys.argv:
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-m":
            searchmode = sys.argv[i+1]
    modes = mode()
    letters = modes.callfunc(searchmode, content)
elif "-p" in sys.argv:
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-p":
            plugin_name = sys.argv[i+1]
    plugin = __import__(f"plugins.{plugin_name}", globals(), locals(), [''], 0)
    letters = plugin.main(content, mode)
    searchmode = f"plugin: {plugin_name}"
else:
    raise Exception("Error: No mode/plugin selected.")

cout(letters, filepath, searchmode)