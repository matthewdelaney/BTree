from BTree import BTree

tree = BTree()
for x in [10, 20, 30, 40, 50, 60, 70, 80, 120, 130, 140]:
    tree.insert(x)

tree.insert(100)
tree.display()
tree.insert(110)
tree.display()

