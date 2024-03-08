import math
with open("prompt.txt", 'r') as file:
    prompt = file.read()

def cout(freq: dict, filename: str, mode: str):
    global prompt
    block = "|"
    output = ""
    maxlen = 0
    maxval = 0
    for key in freq.keys():
        if len(key) > maxlen:
            maxlen = len(key)
    for val in freq.values():
        if val > maxval:
            maxval = val
    ratio = maxval/50
    for key, value in freq.items():
        output = output + str(key) + " "*(maxlen - len(str(key))) + ": " + block*(math.ceil(value/ratio)) + f" ({str(value)})" + "\n"
    prompt = prompt.replace("$filename", filename)
    prompt = prompt.replace("$status", "SUCCESS" if len(freq) > 0 else "FAIL")
    prompt = prompt.replace("$mode", mode)
    print(prompt)
    print(output)
