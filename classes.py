import os
# Class that supplies the program with basic frequency functions
class Modes:
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
    def __init__(self):
        self.head = None

    class node:
        def __init__(self, val, par, left, right, payload):
            self.val = val
            self.parent = par
            self.left = left
            self.right = right
            self.payload = payload

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
                    self.parent.left = self.left
                else:
                    self.parent.right = self.left

                # Then, we change the parent of our child to our parent
                self.left.parent = self.parent

                # Then, we change our parent to our left node
                self.parent = self.left

                # Set our left node to their left node
                self.left = self.parent.left

                # Set our new left node's parent to us
                self.left.parent = self

                # Set right node parent to our new parent node
                self.right.parent = self.parent

                # set parent left to us
                self.parent.left = self

                # we cannot move our right nodes without orphaning the other right node
                # so we need to temporarily save our own right node to a variable
                tempright = self.right

                # then we set our own right node to our parent's right node
                self.right = self.parent.right

                # set parent right node to saved right node
                self.parent.right = tempright

                # set our new right node's parent to our own
                self.right.parent = self
                
            if self.right.val > self.val:
                # Rule 1 is now violated, correct by swapping the positions of right node and current node

                # We do this by first getting our parent node to reference our right node as its child node
                # But first, we have to check which position we are in.
                position = "left" if self.parent.left == self else "right"

                # Then, we link our parent with our child
                if position == "left":
                    self.parent.left = self.right
                else:
                    self.parent.right = self.right

                # Then, we change the parent of our child to our parent
                self.right.parent = self.parent

                # Then, we change our parent to our right node
                self.parent = self.right

                # Set our right node to their right node
                self.right = self.parent.right

                # Set our new right node's parent to us
                self.right.parent = self

                # Set left node parent to our new parent node
                self.left.parent = self.parent

                # set parent right to us
                self.parent.right = self

                # we cannot move our left nodes without orphaning the other left node
                # so we need to temporarily save our own left node to a variable
                templeft = self.left

                # then we set our own left node to our parent's left node
                self.left = self.parent.left

                # set parent left node to saved left node
                self.parent.left = templeft

                # set our new left node's parent to our own
                self.left.parent = self

    def TreeGen(self, dictionary: dict):
        # We assume items inside the dictionary are all payload: value
        # The first key in the dictionary will be our tree head
        keys = list(dictionary.keys())
        self.head = self.node(dictionary[keys[0]], None, None, None, keys[0])
        del keys[0]
        for i in keys:
            # for every entry, we first construct a node
            newnode = self.node(dictionary[i], None, None, None, i)

            cur = self.head
            while newnode.parent is not None:
                # we can express whether it should go left or right by boolean
                right = False if newnode.val <= cur.val else True

                if right:
                    if cur.right is None:
                        cur.right = newnode
                        newnode.parent = cur
                    else:
                        cur = cur.right
                else:
                    if cur.left is None:
                        cur.left = newnode
                        newnode.parent = cur
                    else:
                        cur = cur.left

    # Recursive function that calls repos from the bottom up.
    def heapify(self, node):
        # work our way down to the last branch node
        # this should be done by recursively calling ourselves
        # check if child node is a leaf node
        if node.left is not None:
            if not ((node.left.left is None) and (node.left.right is None)):
                self.heapify(node.left)

        if node.right is not None:
            if not ((node.right.left is None) and (node.right.right is None)):
                self.heapify(node.right)

        node.repos()


# Class that supplies the program with plugin loading capabilities
class PluginLoader:
    def __init__(self):
        # check if plugins folder exist
        if not os.path.isdir("plugins"):
            os.makedirs("plugins")

        self.PDir = "plugins"

    def import_plugin(self, plugin_name):
        if os.path.exists(f"{self.PDir}/{plugin_name}.py"):
            plugin = __import__(f"{self.PDir}.{plugin_name}", globals(), locals(), [''], 0)
        else:
            raise Warning(f"[PluginLoader.import_plugin WARNING] Plugin with name {plugin_name} not found! Overlooking error...")
        return plugin

    def list_plugins(self):
        modelist = []
        for i in os.listdir("plugins"):
            if str(i) != "__init__.py" and i != "__pycache__":
                modelist += [i]
        return modelist
