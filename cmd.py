import sys
import classes

# Initialize classes.
Modes = classes.Modes()
PluginLoader = classes.PluginLoader()
ConsoleHandler = classes.ConsoleHandler()
Sort = classes.Sort()

# Initialize variables
name = "Freqy! Beta 0.2.5"

if __name__ == "__main__":
    # Parse arguments
    argv = sys.argv.copy()
    errors = []
    # Get mode/plugin
    if "-m" in argv:
        try:
            Modes.mode = argv[argv.index("-m")+1].lower()
        except Exception as e:
            errors += [e]
    else:
        errors += [Exception("Mode/Plugin is not set.")]

    # get content
    if "-i" in argv:
        try:
            with open(argv[argv.index("-i")+1], 'rb') as file:
                Modes.content = file.read()
                Modes.content = Modes.content.decode("ascii", "ignore")
                Modes.filepath = argv[argv.index("-i")+1]
        except FileNotFoundError:
            Modes.content = argv[argv.index("-i")+1]
            Modes.filepath = "Text Input"
        except Exception as e:
            errors += [e]
    else:
        errors += [Exception("File/Text Input is not set.")]

    # optional flags
    if "--page_size" in argv:
        try:
            ConsoleHandler.page_size = int(argv[argv.index("--page_size") + 1])
        except Exception as e:
            errors += [e]

    if "--bar_char" in argv:
        try:
            if len(argv[argv.index("--bar_char")+1]) == 1:
                ConsoleHandler.bar_char = argv[argv.index("--bar_char")+1]
            else:
                errors += [Exception("Invalid bar chart character")]
        except Exception as e:
            errors += [e]

    if "--max_length" in argv:
        try:
            ConsoleHandler.max_len = int(argv[argv.index("--max_length")+1])
        except Exception as e:
            errors += [e]

    if "--lower" in argv:
        Modes.lower = True
    else:
        Modes.lower = False

    if "--ascending" in argv:
        Sort.increasing = True

    if Modes.mode not in Modes.callfunction.keys():
        if Modes.mode not in PluginLoader.list_plugins():
            errors += [Exception("Invalid mode/plugin name.")]
            raise ExceptionGroup(name + " failed to start with the following error(s):", errors)
        else:
            if len(errors) > 0:
                raise ExceptionGroup(name + " failed to start with the following error(s):", errors)
            plugin = PluginLoader.import_plugin(Modes.mode)
            plugin.main(Modes, Sort, ConsoleHandler)
    else:
        if len(errors) > 0:
            raise ExceptionGroup(name + " failed to start with the following error(s):", errors)
        Modes.callfunc()
        final = Sort.heapsort(Modes.result)
        ConsoleHandler.barplot(list(final.keys()), list(final.values()))


