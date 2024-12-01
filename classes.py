import os


# Class that supplies the program with basic frequency functions
class Modes:
    def __init__(self) -> None:
        self.callfunction = {"words": self.words,
                             "numeric": self.numeric,
                             "all": self.all,
                             "alpha": self.alpha,
                             }
        self.result = {}
        self.lower = False
        self.mode = ""
        self.content = ""
        self.filepath = ""

    def callfunc(self) -> int:
        if self.mode in self.callfunction:
            self.getResult(self.callfunction[self.mode]())
            return 0
        raise Exception(f"mode {self.mode} does not exist.")

    def getResult(self, data: list) -> None:
        for i in data:
            i = i.lower() if self.lower else i
            if i in self.result:
                self.result[i] += 1
            else:
                self.result[i] = 1
        if "" in self.result:
            del self.result[""]

    def clear(self) -> None:
        self.result = {}
        self.content = ""
        self.letters = {}
        self.filepath = ""

    def words(self) -> list:
        # i'll have to assume everything passed is already transformed into ascii
        self.content = self.content.replace("\r", "\n")
        for i in range(128):
            if not (91 > i > 64 or 123 > i > 96 or i in (13, 10, 32)):
                self.content = self.content.replace(chr(i), "")
        self.content = self.content.split("\n")
        wordlist = []

        # convert to a list of words
        for i in self.content:
            wordlist += i.split(" ")
        return wordlist

    def numeric(self) -> list:
        finalstring = ""
        for i in self.content:
            if i.isnumeric():
                finalstring += i
        return list(finalstring)

    def all(self) -> list:
        return list(self.content)

    def alpha(self) -> list:
        finalstring = ""
        for i in self.content:
            if i.isalpha():
                finalstring += i
        return list(finalstring)


# Class that supplies the program with plugin loading capabilities
class PluginLoader:
    def __init__(self) -> None:
        # check if plugins folder exist
        if not os.path.isdir("plugins"):
            os.makedirs("plugins")

        self.PDir = "plugins"

    def import_plugin(self, plugin_name):
        if os.path.exists(f"{self.PDir}/{plugin_name}"):
            plugin = __import__(f"{self.PDir}.{plugin_name[:-3]}", globals(), locals(), [''], 0)
        else:
            raise Warning(f"[PluginLoader.import_plugin WARNING] Plugin with name {plugin_name} not found! Overlooking error...")
        return plugin

    def list_plugins(self) -> list:
        modelist = []
        for i in os.listdir("plugins"):
            if str(i) != "__init__.py" and i != "__pycache__":
                modelist += [i]
        return modelist


class Sort:
    def __init__(self):
        self.increasing = False
        pass
    
    def quicksort(self, unsorted: list, castto: list) -> (list, list):
        pivot = unsorted[0]
        pivotlist = unsorted[0]
        lwing, rwing = [], []
        lcast, rcast = [], []
        for i in range(len(unsorted[1:])):
            if unsorted[i+1] <= pivot:
                rwing += [unsorted[i+1]]
                rcast += [castto[i+1]]
            else:
                lwing += [unsorted[i+1]]
                lcast += [castto[i+1]]
        if not (len(lwing) <= 1 and len(rwing) <= 1):
            if len(lwing) >= 2:
                lwing, lcast = self.quicksort(lwing, lcast)
            if len(rwing) >= 2:
                rwing, rcast = self.quicksort(rwing, rcast)
        sortval = lwing + [pivotlist] + rwing
        sortcast = lcast + [castto[0]] + rcast
        return sortval, sortcast

    def quickdictsort(self, unsorted: dict) -> dict:
        # Thanks, Nelson, for the improvement idea
        # This stores keys to the same value.
        optdict = {}
        for i, v in unsorted.items():
            if v not in optdict:
                optdict[v] = [i]
            else:
                optdict[v] += [i]

        if self.increasing:
            for k, v in optdict.items():
                optdict[k] = -v

        bundled = list(optdict.keys())
        castto = list(optdict.values())

        sortval, sortkey = self.quicksort(bundled, castto)
        ascdict = {}
        for k in range(len(sortkey)):
            for i in range(len(sortkey[k])):
                ascdict[sortkey[k][i]] = sortval[k] if not self.increasing else -sortval[k]
        return ascdict

    def heapsort(self, unsorted: dict) -> dict:
        # Thanks, Nelson, for the improvement idea
        # This stores keys to the same value.
        optdict = {}
        for i, v in unsorted.items():
            if v not in optdict:
                optdict[v] = [i]
            else:
                optdict[v] += [i]

        if self.increasing:
            for k, v in optdict.items():
                optdict[k] = -v

        val = list(optdict.keys())
        key = list(optdict.values())

        def heapify(vals: list, keys: list, n: int, index: int):
            root = index
            l = 2*index + 1
            r = 2*index + 2

            if l < n and vals[l] < vals[root]:
                root = l

            if r < n and vals[r] < vals[root]:
                root = r

            if root != index:
                vals[root], vals[index] = vals[index], vals[root]
                keys[root], keys[index] = keys[index], keys[root]

                heapify(vals, keys, n, root)

        for i in range(len(key)//2 - 1, -1, -1):
            heapify(val, key, len(val), i)

        for i in range(len(key)-1, 0, -1):
            val[0], val[i] = val[i], val[0]
            key[0], key[i] = key[i], key[0]
            heapify(val, key, i, 0)

        # weave back into 1

        ascdict = {}
        for k in range(len(key)):
            for i in range(len(key[k])):
                ascdict[key[k][i]] = val[k] if not self.increasing else -val[k]

        return ascdict


class ConsoleHandler:
    def __init__(self, page_size: int = 10, barchar: str = "|", maxlen: int = 50) -> None:
        self.page_size = page_size
        self.bar_char = barchar
        self.max_len = maxlen

    def barplot(self, keys: [str], values: [int]) -> None:
        topk = 0
        topv = max(values)
        for k in keys:
            if len(k) > topk:
                topk = len(k)

        ratio = self.max_len/topv
        for i in range(0, len(keys), self.page_size):
            upper_bound = i+self.page_size if i+self.page_size < len(keys) else (len(keys)-1)
            for k, v in zip(keys[i:upper_bound], values[i:upper_bound]):
                print(k + " "*(topk-len(k)) + ": " + self.bar_char*round(v*ratio) + f"  ({v})")

            cont = None
            while cont not in ("", "x"):
                cont = input(f"Showing {i+1} - {min(i+10, len(values))} of {len(values)} results. [Enter] for next page, [x] to exit. ")
            if cont == "x":
                break






