import os
import sys
import classes
from console_handler import cout

Modes = classes.Modes()
PluginLoader = classes.PluginLoader()

# Runtime variables
page_size = 10

if "-h" in sys.argv or "--help" in sys.argv or "help" in sys.argv:
    output = []
    output += ["Freqy! Help Panel"]
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
            Modes.filepath = sys.argv[i+1]
    with open(Modes.filepath, 'r', encoding='utf-8') as file:
        Modes.content = file.read()
elif "-t" in sys.argv:
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-t":
            Modes.content = sys.argv[i+1]
    Modes.filepath = f"command argument - {content}"

if "--nocap" in sys.argv:
    Modes.lower = True

if "--page_size" in sys.argv:
    for i in range(len(sys.argv)):
        if sys.argv[i] == "--page_size":
            page_size = int(sys.argv[i+1])

if "-m" in sys.argv:
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-m":
            Modes.mode = sys.argv[i+1]
            
    letters = Modes.callfunc()
    _ = cout(letters, filepath, searchmode, page_size)
    
elif "-p" in sys.argv:
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-p":
            plugin_name = sys.argv[i+1]
            Modes.mode = f"plugin - {plugin_name}"
            plugin = PluginLoader.import_plugin(plugin_name)
            plugin.main(Modes)

if len(sys.argv) == 1:
    print("====================[pyfreq, ver: alpha]====================")
    contentmode = input("file/text: ")
    if contentmode.lower() == "file":
        Modes.filepath = input("File name: ")
        with open(Modes.filepath, 'r', encoding='utf-8') as file:
            Modes.content = file.read()
    elif contentmode.lower() == "text":
        Modes.content = input("Text: ")
        Modes.filepath = f"command argument - {content}"
    modelist = []
    modelist += list(Modes.callfunction.keys())
    for i in os.listdir("plugins"):
        if str(i) != "__init__.py" and i != "__pycache__":
            modelist += [i]
    menu = ""
    for i in range(len(modelist)):
        menu += f"[{i}]. {modelist[i]}\n"
    print(menu)
    Modes.mode = modelist[int(input("Choose mode number"))]
    if Modes.mode not in Modes.callfunction.keys():
        plugin = PluginLoader.import_plugin(Modes.mode)
        letters = plugin.main(Modes)
    else:
        letters = Modes.callfunc()
        
        _ = cout(Modes.result, Modes.filepath, Modes.mode, page_size)