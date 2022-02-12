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

def test_underflow_first_child():
    tree = BTree()
    for x in range(1, 6):
        tree.insert(x)
    tree.delete(1)
    tree.delete(2)
    assert tree.json() == '[4, [3], [5]]'

def test_underflow_first_child_reverse_order():
    tree = BTree()
    for x in range(1, 6):
        tree.insert(x)
    tree.delete(2)
    tree.delete(1)
    assert tree.json() == '[4, [3], [5]]'

def test_underflow_second_child():
    tree = BTree()
    for x in range(1, 6):
        tree.insert(x)
    tree.delete(4)
    tree.delete(5)
    assert tree.json() == '[2, [1], [3]]' 

def test_underflow_second_child_reverse_order():
    tree = BTree()
    for x in range(1, 6):
        tree.insert(x)
    tree.delete(5)
    tree.delete(4)
    assert tree.json() == '[2, [1], [3]]' 

def test_root_delete_merges_children():
    tree = BTree()
    for x in range(10, 150, 10):
        tree.insert(x)
    import pdb; pdb.set_trace()
    tree.delete(90) # Root
    import pdb; pdb.set_trace()
    assert tree.json() == '[100, [30, 60, [10, 20], [40, 50], [70, 80]], [120, [110], [130, 140]]]' 

def test_root_delete_merges_children2():
    tree = BTree()
    for x in range(10, 130, 10):
        tree.insert(x)
    tree.delete(90) # Root
    assert tree.json() == '[30, 60, 100, [10, 20], [40, 50], [70, 80], [110, 120]]'

def test_root_delete_merges_children3():
    tree = BTree()
    for x in range(10, 160, 10):
        tree.insert(x)
    tree.delete(90) # Root
    assert tree.json() == '[100, [30, 60, [10, 20], [40, 50], [70, 80]], [120, [110], [130, 140]]]' 
