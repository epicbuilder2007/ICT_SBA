with open("prompt.txt", 'r') as file:
    prompt = file.read()

def cout(freq: dict, filename: str):
    global prompt
    block = "|"
    output = ""
    maxlen = 0
    for key in freq.keys():
        if len(key) > maxlen:
            maxlen = len(key)
    for key, value in freq.items():
        output = output + str(key) + " "*(maxlen - len(str(key))) + ": " + block*(int(value)+1) + f" ({str(value)})" + "\n"
    prompt = prompt.replace("$filename", filename)
    prompt = prompt.replace("$status", "SUCCESS" if len(freq) > 0 else "FAIL")
    print(prompt)
    print(output)