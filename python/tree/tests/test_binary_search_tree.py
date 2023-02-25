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


def test_binary_search_tree_delete_leaf():
    root = BinarySearchNode(key=1)
    root.insert(2)
    node = root.delete(2)

    assert node is None

    root = BinarySearchNode(key=2)
    root.insert(1)
    node = root.delete(1)

    assert node is None


def test_binary_search_delete_non_existent_key():
    root = BinarySearchNode(key=1)
    root.insert(2)
    node = root.delete(10)

    assert node is None


def test_binary_search_tree_delete_root():
    root = BinarySearchNode(key=1)
    node = root.insert(2)
    replaced_node = root.delete(1)

    assert node is replaced_node


def test_binary_search_tree_delete_a_left_child():
    root = BinarySearchNode(key=2)
    root.insert(1)
    node = root.insert(0)
    replaced_node = root.delete(1)
    assert node is replaced_node


def test_binary_search_tree_delete_mid_node():
    root = BinarySearchNode(key=1)
    root.insert(2)
    root.insert(3)
    node = root.delete(2)
    assert node.key == 3


def test_binary_search_tree_exists():
    root = BinarySearchNode(key=1)
    root.insert(2)
    root.insert(3)
    root.insert(4)
    assert root.key_exists(5) is False
    assert root.key_exists(4) is True


def test_binary_search_tree_delete_successor_node():
    root = BinarySearchNode(key=3)
    root.insert(2)
    root.insert(1)
    root.insert(7)
    root.insert(6)
    root.insert(5)

    node = root.delete(7)
    assert node.key == 6

    root = BinarySearchNode(key=3)
    root.insert(2)
    root.insert(1)
    root.insert(7)
    root.insert(5)
    root.insert(6)
    node = root.delete(7)
    assert node.key == 5

    root = BinarySearchNode(key=3)
    root.insert(2)
    root.insert(1)
    root.insert(6)
    root.insert(7)
    root.insert(5)
    node = root.delete(6)
    assert node.key == 7

    root = BinarySearchNode(key=2)
    root.insert(1)
    root.insert(5)
    node = root.insert(4)
    replaced = root.delete(2)
    assert replaced is node


def test_binary_search_tree_successor():
    root = BinarySearchNode(key=3)
    root.insert(2)
    root.insert(1)
    assert root.has_successor() is False

    root = BinarySearchNode(key=2)
    root.insert(1)
    successor = root.insert(3)

    assert root.get_successor() is successor

    root = BinarySearchNode(key=2)
    root.insert(1)
    root.insert(4)
    root.insert(5)
    successor = root.insert(3)
    assert root.get_successor() is successor

    root = BinarySearchNode(key=2)
    leaf = root.insert(1)
    assert leaf.get_successor() is root

    root = BinarySearchNode(key=3)
    root.insert(1)
    leaf = root.insert(2)
    assert leaf.get_successor() is root


def test_binary_search_tree_predecessor():
    root = BinarySearchNode(key=1)
    root.insert(2)
    root.insert(3)
    assert root.has_predecessor() is False

    root = BinarySearchNode(key=2)
    root.insert(3)
    predecessor = root.insert(1)

    assert root.get_predecessor() is predecessor

    root = BinarySearchNode(key=3)
    root.insert(0)
    predecessor = root.insert(2)
    root.insert(1)
    assert root.get_predecessor() is predecessor

    root = BinarySearchNode(key=1)
    node = root.insert(2)
    assert node.get_predecessor() is root


def test_binary_search_tree_is_leaf():
    root = BinarySearchNode(key=1)
    leaf = root.insert(1)
    assert leaf.is_leaf() is True


def test_binary_search_tree_is_root():
    root = BinarySearchNode(key=1)
    leaf = root.insert(1)
    assert root.is_root() is True


def test_binary_search_tree_has_predecessor():
    root = BinarySearchNode(key=1)
    assert root.has_predecessor() is False

    root.insert(-1)
    assert root.has_predecessor() is True


def test_binary_search_tree_has_successor():
    root = BinarySearchNode(key=1)
    assert root.has_successor() is False

    root.insert(2)
    assert root.has_successor() is True
    
    last = root.insert(3)
    assert last.has_successor() is False

    root = BinarySearchNode(key=3)
    root.insert(1)
    node = root.insert(2)
    assert node.has_successor() is True



def test_binary_search_tree_iter():
    root = BinarySearchNode(key=3)
    root.insert(4)
    root.insert(5)
    root.insert(3)
    root.insert(0)
    root.insert(2)
    root.insert(1)

    chain = ""
    for node in root:
        chain += str(node.key)

    assert chain == "012345"
