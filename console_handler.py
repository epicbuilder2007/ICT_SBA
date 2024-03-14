with open("prompt.txt", 'r') as file:
    prompt = file.read()

def ascdictsort(unsorted: dict):
    unsorted = {k: v for k, v in unsorted.items()}
    sorted_dict = {k: v for k, v in sorted(unsorted.items(), key=lambda item: item[1], reverse=True)}
    return sorted_dict

def cout(freq: dict, filename: str, mode: str):
    global prompt
    block = "|"
    output = ""
    freq = ascdictsort(freq)
    maxlen = 0
    maxval = list(freq.values())[0]
    for key, val in freq.items():
        if len(key) > maxlen:
            maxlen = len(key)
        # if val > maxval:
            # maxval = val
    ratio = maxval/50
    for key, value in freq.items():
        output = output + str(key) + " "*(maxlen - len(str(key))) + ": " + block*(int(value/ratio)) + f" ({str(value)})" + "\n"
    prompt = prompt.replace("$filename", filename)
    prompt = prompt.replace("$status", "SUCCESS" if len(freq) > 0 else "FAIL")
    prompt = prompt.replace("$mode", mode)
    print(prompt)
    print(output)
    return 0