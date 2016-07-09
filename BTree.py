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

    def delete(self, key):
        # Get index of key to remove if it's in this node
        try:
            idx = self.keys.index(key)
        except:
            found = False
            # Key isn't in this node so find appropriate key and recurse down
            for i, k in enumerate(self.keys):
                if k > key:
                    print "Found"
                    found = True
                    underflow = self.children[i].delete(key)
                    break

            if not found:
                print "Not found"
                i = len(self.children)-1
                underflow = self.children[len(self.children)-1].delete(key)

            if underflow:
                print "TODO: Handle underflow"
                # TODO: Handle underflow
                if i-1 >= 0 and len(self.children[i-1].keys) > minSize:
                    print "Left sibling has sufficient children"
                    # Move keys[i] into underflowing child
                    # print self.keys[i-1]
                    self.children[i].insert(self.keys[i-1])
                    # Move largest value of left sibling into keys[i]
                    # print self.children[i-1].keys
                    self.keys[i-1] = self.children[i-1].keys[len(self.children[i-1].keys)-1]
                    self.children[i-1].delete(self.keys[i-1])
                elif i+1 < len(self.children) and len(self.children[i+1].keys) > minSize:
                    print "Right sibling has sufficient children"
                    print self.keys[i]
                    self.children[i].insert(self.keys[i])
                    print self.children[i+1].keys
                    self.keys[i] = self.children[i+1].keys[0]
                    self.children[i+1].delete(self.keys[i])
                else:
                    print "Neither sibling has sufficient children"


        else:
            # Key is in this node so remove it and handle underflow if necessary
            # - First get left and right child node references
            lenChildren = len(self.children)

            if idx < lenChildren:
                left = self.children[idx]
            if idx+1 < lenChildren:
                right = self.children[idx+1]
            # - Remove the key
            self.keys.remove(key)

            # Return whether or not we caused an underflow
            return len(self.keys) < minSize

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
                print "(root) TODO: Handle underflow"

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
