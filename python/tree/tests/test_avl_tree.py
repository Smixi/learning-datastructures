from ..binary.avl import AVLTree


def test_avl_tree_insert():
    avl = AVLTree()
    avl.insert(1)
    avl.insert(2)
    avl.insert(3)

    assert avl.root.key == 2
