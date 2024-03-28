from BTree import BTree

tree = BTree()
for x in range(10, 150, 10):
    tree.insert(x)
tree.display()
breakpoint()
tree.delete(90)
tree.display()
breakpoint()
