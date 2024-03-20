def main(content: str, _):
    para = content.split("\n")
    words = []
    for i in para:
        if i != '':
            wordlist = i.split(' ')
            for j in range(len(wordlist)):
                word = list(wordlist[j])
                for k in range(len(word)):
                    if not word[k].isalpha():
                        word[k] = ''
                newword = ''.join(word)
                if newword != '':
                    words += [newword]
    print(words)
    return 0