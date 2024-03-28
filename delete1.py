# Set up a BTree to allow testing of delete functionality in REPL.
from BTree import BTree
import random


if __name__ == '__main__':
    tree = BTree()
    [tree.insert(i) for i in random.sample(range(0, 10), 10)]
    tree.display()
    breakpoint()
