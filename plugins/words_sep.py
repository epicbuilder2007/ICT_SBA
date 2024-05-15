def main(content: str, mode):
    modes = mode()
    words = modes.words(content)
    print(words)
    return 0
