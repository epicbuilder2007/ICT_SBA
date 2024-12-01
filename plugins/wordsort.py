import time
import tracemalloc
def main(Modes, Sort, ConsoleHandler):
    sort = Sort
    Modes.filepath = r"test files\hp1.txt"
    print(Modes.filepath)
    # directly call the words function
    temp = Modes.words()

    # find max len
    maxlen = 0
    for i in temp:
        if len(i) > maxlen:
            maxlen = len(i)

    # pad words with reference to maxlen, change words in temp to numbers and cache repeating words
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    cache = {}
    translated = []
    for i in temp:
        word = i + " " * (maxlen - len(i))
        if i not in cache:
            num = 0
            multi = 0
            rev = word[::-1]
            for l in rev:
                if l.lower() in alphabet:
                    num += (ord(l.lower()) - 95) * (27 ** multi)
                    multi += 1
                elif l == " ":
                    num += (27 ** multi)
                    multi += 1
            cache[i] = num
        else:
            num = cache[i]
        translated += [num]

    """# sort with quicksort algorithm
    val, key = sort.quicksort(translated, temp)
    print(val[::-1])
    print(key[::-1])"""

    # weave translated and temp into dict and send to heapsort for testing
    foo = {}
    for i in range(len(translated)):
        foo[temp[i]] = translated[i]

    start = time.perf_counter()
    returndict = sort.heapsort(foo)
    print(list(returndict.keys())[::-1])
    print("heapsort: " + str(time.perf_counter() - start))
