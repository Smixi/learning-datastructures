from ..binary.binary_search_tree import BinarySearchNode


def test_binary_search_tree_insert_right_only():
    root = BinarySearchNode(key=0)
    root.insert(1)
    root.insert(2)
    root.insert(3)
    leaf = root.insert(4)

    assert root.right_child.right_child.right_child.right_child is leaf


def test_binary_search_tree_insert_left_only():
    root = BinarySearchNode(key=4)
    root.insert(3)
    root.insert(2)
    root.insert(1)
    leaf = root.insert(0)

    assert root.left_child.left_child.left_child.left_child is leaf


def test_binary_search_tree_insert_mixed():
    root = BinarySearchNode(key=4)
    root.insert(2)
    root.insert(3)
    root.insert(1)
    root.insert(5)

    for node, expected in [
        (root, 4),
        (root.left_child, 2),
        (root.right_child, 5),
        (root.left_child.left_child, 1),
        (root.left_child.right_child, 3),
    ]:
        assert node.key == expected
