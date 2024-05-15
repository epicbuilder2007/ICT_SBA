import sys
with open("prompt.txt", 'r') as file:
    prompt = file.read()

def quicksort(unsorted: list, castto: list):
    pivot = unsorted[0][0]
    pivotlist = unsorted[0]
    lwing, rwing = [], []
    lcast, rcast = [], []
    for i in range(len(unsorted[1:])):
        if unsorted[i+1][0] <= pivot:
            rwing += [unsorted[i+1]]
            rcast += [castto[i+1]]
        else:
            lwing += [unsorted[i+1]]
            lcast += [castto[i+1]]
    if not (len(lwing) <= 1 and len(rwing) <= 1):
        if len(lwing) >= 2:
            lwing, lcast = quicksort(lwing, lcast)
        if len(rwing) >= 2:
            rwing, rcast = quicksort(rwing, rcast)
    sortval = lwing + [pivotlist] + rwing
    sortcast = lcast + [castto[0]] + rcast
    return sortval, sortcast

def ascdictsort(unsorted: dict):
    # split dict to two lists for sorting
    keys = list(unsorted.keys())
    vals = list(unsorted.values())

    # group same values together, group keys with same values together.
    lastnum = 0
    buffer = []
    keybuf = []
    castto = []
    bundled = []

    for i in range(len(vals)):
        if lastnum != vals[i] and lastnum != 0:
            bundled += [buffer]
            castto += [keybuf]
            buffer = []
            keybuf = []
        
        buffer += [vals[i]]
        keybuf += [keys[i]]
        lastnum = vals[i]

    if len(buffer) > 0:
        bundled += [buffer]
        castto += [keybuf]

    # bundle bundles
    offset = 0
    firstoccur = {}
    for i in range(len(bundled)):
        val = bundled[i-offset][0]
        if str(val) not in firstoccur:
            firstoccur[str(val)] = i-offset
        else:
            bundled[firstoccur[str(val)]] += bundled[i-offset]
            castto[firstoccur[str(val)]] += castto[i-offset]
            del bundled[i-offset]
            del castto[i-offset]
            offset += 1

    # group descending values together.
    offset = 0
    for i in range(len(bundled)-1):
        if bundled[i+1-offset][0] < bundled[i-offset][0]:
            can = True
            for v in range(len(bundled)):
                if bundled[i - offset][0] > bundled[v][-1] > bundled[i + 1 - offset][0]:
                    can = False
                    break
            if can:
                bundled[i-offset] += bundled[i+1-offset]
                castto[i-offset] += castto[i+1-offset]
                del castto[i+1-offset]
                del bundled[i+1-offset]
                offset += 1

    sortval, sortkey = quicksort(bundled, castto)
    ascdict = {}
    for k in range(len(sortkey)):
        for i in range(len(sortkey[k])):
            ascdict[sortkey[k][i]] = sortval[k][i]
    return ascdict

def ceil(num):
    num = num + 1 if num - int(num) > 0 else num
    return int(num)

def cout(freq: dict, filename: str, mode: str, page_size: int):
    global prompt
    block = "|"
    output = r""
    if '' in freq:
        del freq['']
    freq = ascdictsort(freq)
    maxlen = 0
    maxval = list(freq.values())[0]
    for key, val in freq.items():
        key = key if key != "\n" else r"\n"
        if len(key) > maxlen:
            maxlen = len(key)
    ratio = maxval/50
    prompt = prompt.replace("$filename", filename)
    prompt = prompt.replace("$status", "SUCCESS" if len(freq) > 0 else "FAIL")
    prompt = prompt.replace("$mode", mode)
    print(prompt)
    count = 0
    page = 0
    manual_exit = False
    for key, value in freq.items():
        key = key if key != "\n" else r"\n"
        output = output + key + " "*(maxlen - len(str(key))) + ": " + block*(int(value/ratio)) + f" ({str(value)})" + "\n"
        count += 1
        if count == page_size and len(freq.values()) > page_size:
            page += 1
            output += f"\n<Showing: Page {page} of {ceil(len(list(freq.values()))/page_size)}, [Enter] for next page, [x] to exit.>\n"
            print(output)
            if input() == 'x':
                manual_exit = True
                print("exiting...")
                count += 1
            else:
                output = ""
                count = 0
    if not manual_exit:
        page += 1
        output += f"\n<Showing: Page {page} of {ceil(len(list(freq.values()))/page_size)}, end of output, exiting...>\n"
        print(output)
    return 0
