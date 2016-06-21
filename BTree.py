maxSize = 3
minSize = maxSize/2
spaces = 0

def genSpaces():
    result = ""

    for i in range(0, spaces):
        result += "    "

    return result

class BTreeNode:
    def __init__(self, isLeaf):
        self.keys = []
        self.children = []
        self.isLeaf = isLeaf

    def insert(self, key):
        # Am I a leaf?
        if self.isLeaf:
            # I am, so insert value and return whether or not I caused an overflow
            inserted = False
            for i, k in enumerate(self.keys):
                if k > key:
                    self.keys.insert(i, key)
                    inserted = True
                    break

            if not inserted:
                self.keys.append(key)

            if len(self.keys) > maxSize:
                return True
            else:
                return False
        else:
            # I'm not, so recurse down and see if overflow flag comes back (and handle it if it's True)
            inserted = False
            overflow = False

            for i, k in enumerate(self.keys):
                if k > key:
                    overflow = self.children[i].insert(key)
                    inserted = True
                    break

            if not inserted:
                overflow = self.children[len(self.children)-1].insert(key)

            if overflow:
                # The child we just inserted into overflowed
                # Find it and store its index
                for i, c in enumerate(self.children):
                    if len(c.keys) > maxSize:
                        overflowingChild = c
                        overflowingChildIndex = i
                        break
                        
                # Get the new median value
                medianIndex = len(overflowingChild.keys)/2
                median = overflowingChild.keys[medianIndex]

                # Get split children
                first = BTreeNode(overflowingChild.isLeaf)
                first.keys = overflowingChild.keys[0:medianIndex]
                first.children = overflowingChild.children[0:medianIndex+1]
                second = BTreeNode(overflowingChild.isLeaf)
                second.keys = overflowingChild.keys[medianIndex+1:len(c.keys)]
                second.children = overflowingChild.children[medianIndex+1:len(overflowingChild.children)]
                self.children[overflowingChildIndex] = first
                self.children.insert(overflowingChildIndex+1, second)

                # I should get the new median and I'll return whether or not I overflowed
                # self.keys.append(median)
                medianInserted = False
                for i, k in enumerate(self.keys):
                    if k > median:
                        self.keys.insert(i, median)
                        medianInserted = True
                        break

                if not medianInserted:
                    self.keys.append(median)

                return len(self.keys) > maxSize

            return False

    def display(self):
        global spaces

        print "%s Leaf" % (genSpaces()) if self.isLeaf else "%s Non-leaf" % (genSpaces())
        print "%s %s" % (genSpaces(), self.keys)

        for i, c in enumerate(self.children):
            print "%s Child(%d)->" % (genSpaces(), i)
            spaces += 1
            c.display()

        spaces -= 1

class BTree:
    def __init__(self):
        self.root = BTreeNode(True)

    def insert(self, key):
        if self.root.isLeaf:
            inserted = False

            for i, k in enumerate(self.root.keys):
                if k > key:
                    self.root.keys.insert(i, key)
                    inserted = True
                    break

            if not inserted:
                self.root.keys.append(key)

            if len(self.root.keys) > maxSize:
                newRoot = BTreeNode(False)
                medianIndex = len(self.root.keys)/2
                median = self.root.keys[medianIndex]
                first = BTreeNode(True)
                first.keys = self.root.keys[0:medianIndex]
                second = BTreeNode(True)
                second.keys = self.root.keys[medianIndex+1:len(self.root.keys)]
                newRoot.children.append(first)
                newRoot.children.append(second)
                newRoot.keys.append(median)
                self.root = newRoot
        else:
            overflow = self.root.insert(key)

            if overflow:
                newRoot = BTreeNode(False)
                medianIndex = len(self.root.keys)/2
                median = self.root.keys[medianIndex]
                first = BTreeNode(False)
                first.keys = self.root.keys[0:medianIndex]
                first.children = self.root.children[0:medianIndex+1]
                second = BTreeNode(False)
                second.keys = self.root.keys[medianIndex+1:len(self.root.keys)]
                second.children = self.root.children[medianIndex+1:len(self.root.children)]
                newRoot.children.append(first)
                newRoot.children.append(second)
                newRoot.keys.append(median)
                self.root = newRoot

    def delete(self, key):
        if self.root.isLeaf:
            self.root.keys.remove(key)
        else:
            underflow = self.root.delete(key)
            if underflow:
                # Deal with underflow

    def display(self):
        self.root.display()

if __name__ == "__main__":
    tree = BTree()
    tree.insert(2000)
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    tree.insert(40)
    tree.insert(50)
    tree.insert(60)
    tree.insert(70)
    tree.insert(80)
    tree.insert(90)
    tree.insert(100)
    tree.insert(110)
    tree.insert(120)
    tree.insert(130)
    tree.insert(11)
    tree.insert(25)
    tree.display()
