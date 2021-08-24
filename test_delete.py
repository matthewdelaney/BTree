from BTree import BTree

def test_simple_delete():
    tree = BTree()
    for x in range(1, 5):
        tree.insert(x)
    tree.delete(1)
    assert tree.json() == '[3, [2], [4]]'

def test_root_delete():
    tree = BTree()
    for x in range(1, 5):
        tree.insert(x)
    tree.delete(3)
    assert tree.json() == '[1, 2, 4]'

def test_root_delete2():
    tree = BTree()
    for x in range(1, 6):
        tree.insert(x)
    tree.delete(3)
    assert tree.json() == '[4, [1, 2], [5]]'
