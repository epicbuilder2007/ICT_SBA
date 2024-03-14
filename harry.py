for i in range(1, 8):
    with open(f"hp{i}.txt", 'r', encoding='utf-8') as file:
        content = file.read().split("\n")
    offset = 0
    for j in range(len(content)):
        if " - J.K. Rowling" in content[j-offset] or content[j-offset] == '':
            del content[j-offset]
            offset += 1
    with open(f"hp{i}.txt", 'w', encoding='utf-8') as writefile:
        writefile.write("\n".join(content))