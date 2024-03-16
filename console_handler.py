with open("prompt.txt", 'r') as file:
    prompt = file.read()

def ascdictsort(unsorted: dict):
    unsorted = {k: v for k, v in unsorted.items()}
    sorted_dict = {k: v for k, v in sorted(unsorted.items(), key=lambda item: item[1], reverse=True)}
    return sorted_dict

def ceil(num):
    num = num + 1 if num - int(num) > 0 else num
    return int(num)

def cout(freq: dict, filename: str, mode: str, page_size: int):
    global prompt
    block = "|"
    output = ""
    if '' in freq:
        del freq['']
    freq = ascdictsort(freq)
    maxlen = 0
    maxval = list(freq.values())[0]
    for key, val in freq.items():
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
        output = output + str(key) + " "*(maxlen - len(str(key))) + ": " + block*(int(value/ratio)) + f" ({str(value)})" + "\n"
        count += 1
        if count == page_size:
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