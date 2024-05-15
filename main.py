import time
start = time.perf_counter()
import sys
import os
from console_handler import *

filepath = ""
searchmode = ""
content = ""
letters = ""
lower = False
page_size = 10
class mode:
    def __init__(self):
        self.callfunction = {self.words: "words",
                             self.numeric: "numeric",
                             self.all: "all",
                             self.alpha: "alpha",
                             }
        self.result = {}
        self.lower = False
        self.mode = ""
    def callfunc(self, freqmode: str, content):
        for key, value in self.callfunction.items():
            if value == freqmode:
                letter = self.getResult(key(content))
                return letter

        raise Exception(f"mode {freqmode} does not exist.")

    def getResult(self, data: list):
        result = {}
        for i in data:
            i = i.lower() if self.lower else i
            if i in result:
                result[i] += 1
            else:
                result[i] = 1
        return result

    def words(self, content: str):
        primary = content.split("\n")
        wordlist = []
        for i in primary:
            if i != '':
                para = i.split(" ")
                for j in para:
                    word = list(j)
                    for k in range(len(word)):
                        if not word[k].isalpha():
                            word[k] = ''
                    word = ''.join(word)
                    wordlist += [word]
        return wordlist

    def numeric(self, content: str):
        finalstring = ""
        for i in content:
            if i.isnumeric():
                finalstring += i
        return finalstring

    def all(self, content: str):
        return list(content)

    def alpha(self, content: str):
        finalstring = ""
        for i in content:
            if i.isalpha():
                finalstring += i
        return list(finalstring)
    
    def cout(self, content: dict, filename: str, mode: str, page_size: int):
        cout(content, filename, mode, page_size)
    


if "-h" in sys.argv or "--help" in sys.argv or "help" in sys.argv:
    output = []
    output += ["PyFreq Help Panel"]
    output += ["This is the help menu. You get here with the [-h], [--help] flag, or simply not passing any arguments whatsoever.\n"]
    output += ["Flags:"]
    output += ["[-f <filepath>]: specify file path of file, file needs to be .txt, cannot be used with [-t]."]
    output += ['[-t <string>]: input string of words into the program, cannot be used with [-f]. String must be enclosed in ""']
    output += [f'[-m <{"/".join(list(mode().callfunction.values()))}>]: input mode to be used for processing, cannot be used with [-p]']
    output += ["[-p <plugin name>]: input plugin name to be used for processing, cannot be used with [-m]. do not add file extension."]
    output += ["[--nocap]: all results will be calculated in lower case only."]
    output += ["[--page_size <int>]: specify amount of results to show per page."]
    print("\n".join(output))
    sys.exit(0)

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
    filepath = f"command argument - {content}"

if "--nocap" in sys.argv:
    lower = True

if "--page_size" in sys.argv:
    for i in range(len(sys.argv)):
        if sys.argv[i] == "--page_size":
            page_size = int(sys.argv[i+1])

if "-m" in sys.argv:
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-m":
            searchmode = sys.argv[i+1]
    modes = mode()
    letters = modes.callfunc(searchmode, content)
    _ = cout(letters, filepath, searchmode, page_size)
elif "-p" in sys.argv:
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-p":
            plugin_name = sys.argv[i+1]
            searchmode = f"plugin - {plugin_name}"
    plugin = __import__(f"plugins.{plugin_name}", globals(), locals(), [''], 0)
    plugin.main(content, mode, filepath)

if len(sys.argv) == 1:
    print("====================[pyfreq, ver: alpha]====================")
    contentmode = input("file/text: ")
    if contentmode.lower() == "file":
        filepath = input("File name: ")
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    elif contentmode.lower() == "text":
        content = input("Text: ")
        filepath = f"command argument - {content}"
    modes = mode()
    selectedmode = ""
    modelist = []
    modelist += list(modes.callfunction.values())
    for i in os.listdir("plugins"):
        if str(i) != "__init__.py" and i != "__pycache__":
            modelist += [i]
    menu = ""
    for i in range(len(modelist)):
        menu += f"[{i}]. {modelist[i]}\n"
    print(menu)
    selectedmode = modelist[int(input("Choose mode number"))]
    if selectedmode not in modes.callfunction.values():
        plugin = __import__(f"plugins.{selectedmode}".replace('.py', ''), globals(), locals(), [''], 0)
        letters = plugin.main(content, mode, filepath)
    else:
        letters = modes.callfunc(selectedmode, content)
        _ = cout(letters, filepath, selectedmode, page_size)



end = time.perf_counter()
print(f"Runtime: {end-start}")
