from BTree import BTree

if __name__ == "__main__":
    tree = BTree()
    for i in range(0, 7):
        tree.insert(i)
    tree.display()    
