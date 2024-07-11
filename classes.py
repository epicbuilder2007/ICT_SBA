# Class that supplies the program with basic frequency functions
class modes:
    def __init__(self):
        self.callfunction = {self.words: "words",
                             self.numeric: "numeric",
                             self.all: "all",
                             self.alpha: "alpha",
                             }
        self.result = {}
        self.lower = False
        self.mode = ""
        self.content = ""
        self.letters = {}

    def callfunc(self):
        for key, value in self.callfunction.items():
            if value == self.mode:
                self.letters = self.getResult(key())

        raise Exception(f"mode {self.mode} does not exist.")

    def getResult(self, data: list):
        result = {}
        for i in data:
            i = i.lower() if self.lower else i
            if i in result:
                result[i] += 1
            else:
                result[i] = 1
        return result

    def words(self):
        # i'll have to assume everything passed is already transformed into ascii
        for i in range(33, 127):
            if not (91 > i > 64 or 123 > i > 96):
                self.content = self.content.replace(chr(i), "")
        self.content = self.content.replace("\r", "\n")
        self.content = self.content.split("\n")
        wordlist = []

        # convert to a list of words
        for i in self.content:
            wordlist += i.split(" ")
        return wordlist

    def numeric(self):
        finalstring = ""
        for i in self.content:
            if i.isnumeric():
                finalstring += i
        return list(finalstring)

    def all(self):
        return list(self.content)

    def alpha(self):
        finalstring = ""
        for i in self.content:
            if i.isalpha():
                finalstring += i
        return list(finalstring)

# Class that produces a sorted binary tree
class BTree:
    class node:
        def __init__(self, val, par, left, right, payload):
            self.val = val
            self.parent = par
            self.left = left
            self.right = right
            self.payload = payload

        def setleft(self, node):
            pass

        def setright(self, node):
            pass

        def setparent(self, node):
            pass
        def repos(self):
            # Rules for a max heap
            # 1. Everything below a node must be smaller than itself
            # 2. Everything above a node must be larger than itself

            # We first check rule 1.
            if self.left.val > self.val:
                # Rule 1 is now violated, correct by swapping the positions of left node and current node

                # We do this by first getting our parent node to reference our left node as its child node
                # But first, we have to check which position we are in.
                position = "left" if self.parent.left == self else "right"

                # Then, we link our parent with our child
                if position == "left":
                    self.parent.setleft(self.left)
                else:
                    self.parent.setright(self.left)

                # Then, we change the parent of our child to our parent
                self.left.setparent(self.parent)

                # Then, we change our parent to our left node
                self.setparent(self.left)

                # Swap our left node with theirs
                temp = self.left.left
                self.left.setleft()



            if self.right.val > self.val:
                pass

            # Then we check rule 2.
            if self.parent.val < self.val:
                pass


    def TreeGen(self, dictionary: dict):
        # We assume items inside the dictionary are all payload: value
        # The first key in the dictionary will be our tree head
        keys = list(dictionary.keys())
        head = self.node(dictionary[keys[0]], None, None, None, keys[0])
        del keys[0]
        for i in keys:
            # for every entry, we first construct a node
            newnode = self.node(dictionary[i], None, None, None, i)

            cur = head
            while


