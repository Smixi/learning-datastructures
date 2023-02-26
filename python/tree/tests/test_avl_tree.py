from ..binary.avl import AVLTree


def test_avl_tree_insert_left_rotate():
    avl = AVLTree()
    node1 = avl.insert(1)
    node2 = avl.insert(2)
    node3 = avl.insert(3)

    assert avl.root is node2
    assert node1 is node2.left_child
    assert node3 is node2.right_child
    assert node1.left_child is None
    assert node1.right_child is None


def test_avl_tree_insert_right_rotate():
    avl = AVLTree()
    node1 = avl.insert(3)
    node2 = avl.insert(2)
    node3 = avl.insert(1)

    assert avl.root is node2
    assert node1 is node2.right_child
    assert node3 is node2.left_child
    assert node1.left_child is None
    assert node1.right_child is None
    assert node3.left_child is None
    assert node3.right_child is None


def test_avl_tree_insert_left_right_rotate():
    avl = AVLTree()
    node1 = avl.insert(1)
    node2 = avl.insert(3)
    node3 = avl.insert(2)

    assert avl.root is node3
    assert node2 is node3.right_child
    assert node1 is node3.left_child
    assert node1.left_child is None
    assert node1.right_child is None
    assert node2.left_child is None
    assert node2.right_child is None


def test_avl_tree_insert_right_left_rotate():
    avl = AVLTree()
    node1 = avl.insert(3)
    node2 = avl.insert(1)
    node3 = avl.insert(2)

    assert avl.root is node3
    assert node1 is node3.right_child
    assert node2 is node3.left_child
    assert node1.left_child is None
    assert node1.right_child is None
    assert node2.left_child is None
    assert node2.right_child is None


def test_avl_tree_delete():
    avl = AVLTree()
    avl.insert(1)
    avl.insert(2)
    avl.insert(3)
    avl.delete(3)

    assert avl.root.right_child is None


def test_avl_tree_delete_left_rotate():
    avl = AVLTree()
    avl.insert(2)
    avl.insert(1)
    node = avl.insert(3)
    avl.insert(4)
    avl.delete(1)

    assert avl.root is node


def test_avl_tree_delete_right_rotate():
    avl = AVLTree()
    avl.insert(3)
    node = avl.insert(2)
    avl.insert(1)
    avl.insert(4)
    avl.delete(4)

    assert avl.root is node


def test_avl_tree_delete_intermediate():
    avl = AVLTree()
    avl.insert(3)
    node = avl.insert(2)
    avl.insert(1)
    avl.insert(4)
    avl.insert(5)
    avl.delete(4)

    assert avl.root is node


def test_avl_tree_delete_intermediate2():
    avl = AVLTree()
    avl.insert(3)
    node = avl.insert(2)
    avl.insert(1)
    avl.insert(5)
    avl.insert(0)
    avl.insert(6)
    avl.insert(4)
    avl.delete(5)

    assert avl.root is node
