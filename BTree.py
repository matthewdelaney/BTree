import json

maxSize = 3
minSize = maxSize//2
spaces = 0

excess_keys = []

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

            return len(self.keys) > maxSize
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
                medianIndex = len(overflowingChild.keys)//2
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
        global excess_keys
        # Get index of key to remove if it's in this node
        try:
            idx = self.keys.index(key)
        except:
            found = False
            # Key isn't in this node so find appropriate key and recurse down
            for i, k in enumerate(self.keys):
                if k > key:
                    found = True
                    underflow = self.children[i].delete(key)
                    break

            if not found:
                i = len(self.children)-1
                underflow = self.children[len(self.children)-1].delete(key)

            if underflow:
                if i-1 >= 0 and len(self.children[i-1].keys) > minSize:
                    # Move keys[i] into underflowing child
                    self.children[i].insert(self.keys[i-1])
                    # Move largest value of left sibling into keys[i]
                    self.keys[i-1] = self.children[i-1].keys[len(self.children[i-1].keys)-1]
                    self.children[i-1].delete(self.keys[i-1])
                elif i+1 < len(self.children) and len(self.children[i+1].keys) > minSize:
                    self.children[i].insert(self.keys[i])
                    self.keys[i] = self.children[i+1].keys[0]
                    self.children[i+1].delete(self.keys[i])
                else:
                    if i-1 >= 0:
                        # Insert predecessor key into its left child then
                        self.children[i-1].insert(self.keys[i-1])

                        # move all keys and children from self.children[i] (the underflowed node)
                        # into the same left child as above
                        self.children[i-1].keys = self.children[i-1].keys + self.children[i].keys
                        self.children[i-1].children = self.children[i-1].children + self.children[i].children

                        # remove it from self.keys and shift everything after
                        # it back one place.
                        for j in range(i-1, len(self.keys)-1):
                            self.keys[j] = self.keys[j+1]

                        self.keys.remove(self.keys[len(self.keys)-1])

                        # Do the same with the children except
                        # we aren't overwriting the one we inserted into
                        # at the start of this branch
                        for j in range(i, len(self.children)-1):
                            self.children[j] = self.children[j+1]
                        
                        # Remove last child which will not have been overwritten
                        # by the loop above
                        self.children.remove(self.children[len(self.children)-1])
                    else:
                        # Insert key into right child then
                        self.children[i+1].insert(self.keys[i])

                        # move all keys and children from self.children[i] (the underflowed node)
                        # into the same left child as above
                        self.children[i+1].keys = self.children[i].keys + self.children[i+1].keys
                        self.children[i+1].children = self.children[i].children + self.children[i+1].children

                        # Remove it from self.keys and shift everything after
                        # it back one place.
                        for j in range(i, len(self.keys)-1):
                            self.keys[j] = self.keys[j+1]

                        self.keys.remove(self.keys[len(self.keys)-1])

                        # Do the same with the children except
                        # we aren't overwriting the one we inserted into
                        # at the start of this branch
                        for j in range(i, len(self.children)-1):
                            self.children[j] = self.children[j+1]
                        
                        # Remove last child which will not have been overwritten
                        # by the loop above
                        self.children.remove(self.children[len(self.children)-1])

                    # Indicate whether or not we caused an underflow in this
                    # node
                    return len(self.keys) < minSize

        else:
            # Key is in this node so remove it and handle underflow if necessary
            # - First get left and right child node references
            lenChildren = len(self.children)

            left = None
            right = None

            if idx < lenChildren:
                left = self.children[idx]
            if idx+1 < lenChildren:
                right = self.children[idx+1]

            # - Remove the key
            self.keys.remove(key)

            # TODO: Handle moving children
            if left and right:
                lenLeft = len(left.keys)
                lenRight = len(right.keys)

                if lenLeft + lenRight <= maxSize:
                    # Left child can absorb right child

                    # Append keys from right child into left child
                    for k in right.keys:
                        left.keys.append(k)

                    # Append children from right child into left child
                    for c in right.children:
                        left.children.append(c)

                    self.children.remove(right)

                    # Are there too many children in left? There might be because a node of order N can have N+1 children
                    if len(left.children) > maxSize + 1:
                        for k in left.children[maxSize+1].keys:
                            left.children[maxSize].keys.append(k)
                        del left.children[maxSize+1]
                        # TODO: What if the right-most child has children?
                        right_most_child_overflow = len(left.children[-1].keys) > maxSize
                        if right_most_child_overflow:
                            excess_keys = left.children[-1].keys[maxSize:]
                            left.children[-1].keys = [k for k in left.children[-1].keys if k not in excess_keys]
                else:
                    # Not enough space in left child. Append to right child and choose a
                    # median value. Insert the median value into self.keys

                    temp = left.keys + right.keys
                    new_median_key = temp[len(temp)//2]
                    underflow = False

                    if new_median_key in left.keys:
                        underflow = left.delete(new_median_key)
                    else:
                        underflow = right.delete(new_median_key)
                    self.keys.append(new_median_key)
                    self.keys.sort()
                    # TODO: Handle underflow                    
                    if underflow:
                        print('UNHANDLED UNDERFLOW')

            # Return whether or not we caused an underflow
            return len(self.keys) < minSize

    def display(self):
        global spaces

        print("%s Leaf" % genSpaces() if self.isLeaf else "%s Non-leaf" % (genSpaces()))
        print("%s %s" % (genSpaces(), self.keys))

        for i, c in enumerate(self.children):
            print("%s Child(%d)->" % (genSpaces(), i))
            spaces += 1
            c.display()

        if spaces > 0:
            spaces -= 1

    def json(self):
        result = []
        for i, c in enumerate(self.children):
            result.append(c.json())

        return [k for k in self.keys] + result
            
            
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
                self._split_root(True)
        else:
            overflow = self.root.insert(key)

            if overflow:
                self._split_root(False)

    def delete(self, key):
        global excess_keys
        if self.root.isLeaf:
            self.root.keys.remove(key)
        else:
            underflow = self.root.delete(key)
            if underflow:
                # Deal with underflow
                if len(self.root.keys) == 0:
                    self.root = self.root.children[0]
        # TODO: This assumes that this only happens at the end
        # of a delete-call. If it can happen /during/ the
        # sequence of recursive delete calls then this
        # global variable approach will probably not work
        if len(excess_keys) > 0:
            for k in excess_keys:
                self.insert(k)
            excess_keys = []

    def display(self):
        self.root.display()

    def json(self):
        return json.dumps(self.root.json())
        
    def _split_root(self, is_leaf):
        newRoot = BTreeNode(False)
        medianIndex = len(self.root.keys)//2
        median = self.root.keys[medianIndex]
        first = BTreeNode(is_leaf)
        first.keys = self.root.keys[0:medianIndex]
        if not is_leaf:
            first.children = self.root.children[0:medianIndex+1]
        second = BTreeNode(is_leaf)
        second.keys = self.root.keys[medianIndex+1:len(self.root.keys)]
        if not is_leaf:
            second.children = self.root.children[medianIndex+1:len(self.root.children)]
        newRoot.children.append(first)
        newRoot.children.append(second)
        newRoot.keys.append(median)
        self.root = newRoot


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

