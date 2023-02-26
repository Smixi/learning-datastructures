from ..b_tree.b_tree import BTree
from ..b_tree.b_tree_node import BTreeEntry, BTreeNode


def test_btreenode_split():
    entry1 = BTreeEntry(1, None)
    entry2 = BTreeEntry(2, None)
    entry3 = BTreeEntry(3, None)
    node = BTreeNode(order=2)
    node.entries[entry1] = entry1
    node.entries[entry2] = entry2
    node.entries[entry3] = entry3
    left, separator, right = node.split()
    assert entry1 in left
    assert separator is entry2
    assert entry3 in right


def test_btree_base_insert():
    tree = BTree()
    tree.insert(1, 1)
    tree.insert(2, 2)
    tree.insert(3, 3)
    assert tree.root.entries[1].value == 1
    assert tree.root.entries[2].value == 2
    assert tree.root.entries[3].value == 3


def test_btree_insert_split():
    tree = BTree()
    tree.insert(1, 1)
    tree.insert(2, 2)
    tree.insert(3, 3)
    tree.insert(4, 4)
    assert 2 in tree.root


def test_btree_insert_split_more():
    tree = BTree()
    tree.insert(1, 1)
    tree.insert(2, 2)
    tree.insert(3, 3)
    tree.insert(4, 4)
    tree.insert(5, 5)
    tree.insert(6, 5)
    tree.insert(7, 5)
    tree.insert(8, 5)
    tree.insert(-1, 5)
    tree.insert(-2, 5)
    tree.insert(-3, 5)
    tree.insert(-4, 5)


def test_btree_duplicate():
    tree = BTree()
    tree.insert(1, 1)
    tree.insert(1, 1)
    assert len(tree.root.entries) == 1


def test_btree_search():
    tree = BTree()
    tree.insert(1, 1)
    tree.insert(2, 2)
    tree.insert(3, 3)
    assert tree.search(1).value == 1
    assert tree.search(2).value == 2
    assert tree.search(3).value == 3
    assert tree.search(4) is None


def test_btree_delete_in_root():
    tree = BTree()
    tree.insert(1, 1)
    tree.delete(1)
    assert len(tree.root.entries) == 0
    assert tree.search(1) is None


def test_btree_delete_in_leaf():
    tree = BTree(order=2)
    tree.insert(1, 1)
    tree.insert(2, 2)
    tree.insert(3, 3)
    tree.insert(4, 4)
    tree.delete(3)
    assert tree.search(3) is None


def test_btree_delete_in_leaf_empty_left():
    tree = BTree(order=2)
    tree.insert(1, 1)
    tree.insert(2, 2)
    tree.insert(3, 3)
    tree.insert(4, 4)
    tree.delete(1)
    assert tree.search(1) is None
