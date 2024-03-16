import time
start = time.perf_counter()
import sys
from console_handler import *
import string

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
                             self.alphanumeric: "alphanumeric",
                             self.text_info: "text_info"
                             }
        self.result = {}
    def callfunc(self, freqmode: str, content):
        for key, value in self.callfunction.items():
            if value == freqmode:
                letter = key(content)
                return letter

        raise Exception(f"mode {freqmode} does not exist.")

    def getResult(self, data: list):
        result = {}
        for i in data:
            i = i.lower() if lower else i
            if i in result:
                result[i] += 1
            else:
                result[i] = 1
        return result

    def words(self, content: str):
        primary = content.split("\n")
        wordlist = []
        for i in range(len(primary)):
            wordlist += primary[i].split(" ")
        for i in range(len(wordlist)):
            for char in string.punctuation + "’‘“”—•…":
                wordlist[i] = wordlist[i].replace(char, '')
        frequency = self.getResult(wordlist)
        return frequency

    def numeric(self, content: str):
        finalstring = ""
        for i in content:
            if i.isnumeric():
                finalstring += i
        frequency = self.getResult(list(finalstring))
        return frequency

    def all(self, content: str):
        frequency = self.getResult(list(content))
        return frequency

    def alpha(self, content: str):
        finalstring = ""
        for i in content:
            if i.isalpha():
                finalstring += i
        frequency = self.getResult(list(finalstring))
        return frequency

    def alphanumeric(self, content: str):
        finalstring = ""
        for i in content:
            if i.isalpha() or i.isnumeric():
                finalstring += i
        frequency = self.getResult(list(finalstring))
        return frequency

    def text_info(self, content: str):
        info = {}
        info["word count"] = sum(list(self.words(content).values()))
        info["character count"] = len(content)
        info["paragraph count"] = sum([1 if content.split("\n")[i] != '' else 0 for i in range(len(content.split("\n")))])
        return info


if "-h" in sys.argv or "--help" in sys.argv or "help" in sys.argv or len(sys.argv) == 1:
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
else:
    raise Exception("Error: No text input defined.")

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
elif "-p" in sys.argv:
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-p":
            plugin_name = sys.argv[i+1]
            searchmode = f"plugin - {plugin_name}"
    plugin = __import__(f"plugins.{plugin_name}", globals(), locals(), [''], 0)
    letters = plugin.main(content, mode)
else:
    raise Exception("Error: No operation mode defined.")

_ = cout(letters, filepath, searchmode, page_size)

end = time.perf_counter()
print(f"Runtime: {end-start}")