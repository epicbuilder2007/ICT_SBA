def main(content: str, mode):
    eng_freq = ["e", "t", "a", "o", "i", "n", "s", "r", "h", "d", "l", "u", "c", "m", "f", "y", "w", "g", "p", "b", "v", "k", "x", "q", "j", "z"]
    alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    default_modes = mode()
    letters = default_modes.alpha(content)
    found = False
    for i in eng_freq:
        if not found:
            temp = list(content)
            target = list(letters.keys())[0]
            shift = alphabet.index(target) - alphabet.index(i)
            for j in range(len(temp)):
                if temp[j].isalpha():
                    finalshift = alphabet.index(temp[j]) + shift
                    if finalshift < 0:
                        finalshift = 52 + (finalshift)
                    elif finalshift > 51:
                        finalshift = finalshift - 52

                    temp[j] = alphabet[finalshift].upper() if temp[j].isupper() else alphabet[finalshift].lower()
            confirm = input(f"Does this make sense? {''.join(temp)} (y/n): ")
            if confirm == "y":
                content = "".join(temp)
                found = True
    return {content: 1}


