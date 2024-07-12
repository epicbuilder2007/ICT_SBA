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
            # Check rule 1.
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

                # Set our left node to their left node
                self.setleft(self.parent.left)
                
                # Set our new left node's parent to us
                self.left.setparent(self)
                
                # Set right node parent to our new parent node
                self.right.setparent(self.parent)
                
                # set parent left to us
                self.parent.setleft(self)
                
                # we cannot move our right nodes without orphaning the other right node
                # so we need to temporarily save our own right node to a variable
                tempright = self.right
                
                # then we set our own right node to our parent's right node
                self.setright(self.parent.right)
                
                # set parent right node to saved right node
                self.parent.setright(tempright)
                
                # set our new right node's parent to our own
                self.right.setparent(self)
                
            elif self.right.val > self.val:
                                # Rule 1 is now violated, correct by swapping the positions of left node and current node

                # We do this by first getting our parent node to reference our left node as its child node
                # But first, we have to check which position we are in.
                position = "left" if self.parent.left == self else "right"

                # Then, we link our parent with our child
                if position == "left":
                    self.parent.setleft(self.right)
                else:
                    self.parent.setright(self.right)

                # Then, we change the parent of our child to our parent
                self.right.setparent(self.parent)

                # Then, we change our parent to our right node
                self.setparent(self.right)

                # Set our right node to their right node
                self.setright(self.parent.right)
                
                # Set our new right node's parent to us
                self.right.setparent(self)
                
                # Set left node parent to our new parent node
                self.left.setparent(self.parent)
                
                # set parent right to us
                self.parent.setright(self)
                
                # we cannot move our left nodes without orphaning the other left node
                # so we need to temporarily save our own left node to a variable
                templeft = self.left
                
                # then we set our own left node to our parent's left node
                self.setleft(self.parent.left)
                
                # set parent left node to saved left node
                self.parent.setleft(templeft)
                
                # set our new left node's parent to our own
                self.left.setparent(self)

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


