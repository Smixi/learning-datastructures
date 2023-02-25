from typing import Generic, TypeVar, Optional
from typing_extensions import Self
from dataclasses import dataclass
from functools import cached_property

NodeKey = TypeVar("NodeKey")
NodeValue = TypeVar("NodeValue")


@dataclass
class AVLNode(Generic[NodeKey, NodeValue]):
    parent: Optional["AVLNode"] = None
    left_child: Optional["AVLNode"] = None
    right_child: Optional["AVLNode"] = None
    key: NodeKey = None
    value: NodeValue = None

    def is_left_child(self):
        if self.parent is None:
            return False
        return self.parent.left_child is self  # or self.key < self.parent.key

    def get_parent(self):
        return self.parent

    def get_sibling(self):
        if self.parent is None:
            return None
        if self.is_left_child():
            return self.parent.right_child
        return self.parent.left_child

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return (self.left_child is None) and (self.right_child is None)

    def get_most_left(self) -> "AVLNode":
        return self if self.left_child is None else self.left_child.get_most_left()

    def get_most_right(self) -> "AVLNode":
        return self if self.right_child is None else self.right_child.get_most_right()

    def has_successor(self) -> bool:
        if self.right_child is not None:
            return True
        has_successor = False
        node = self
        while node is not None:
            if node.is_right_child() or node.is_root():
                node = node.parent
            else:
                has_successor = True
                break
        return has_successor

    def has_predecessor(self) -> "AVLNode":
        if self.left_child is not None:
            return True
        has_predecessor = False
        node = self
        while node is not None:
            if node.is_left_child() or node.is_root():
                node = node.parent
            else:
                has_predecessor = True
                break
        return has_predecessor

    def get_successor(self) -> "AVLNode":
        if self.right_child is not None:
            return self.right_child.get_most_left()
        node = self
        while node is not None:
            if node.is_right_child() or node.is_root():
                node = node.parent
            else:
                return node.parent
        return None

    def get_predecessor(self) -> "AVLNode":
        if self.left_child is not None:
            return self.left_child.get_most_right()
        node = self
        while node is not None:
            if node.is_left_child() or node.is_root():
                node = node.parent
            else:
                return node.parent
        return None
    
    def is_left_child(self):
        return self.parent.left_child is self if self.parent is not None else False

    def is_right_child(self):
        return self.parent.right_child is self if self.parent is not None else False

    @property
    def height(self):
        if self.is_leaf():
            return 1
        if self.left_child is None:
            return 1 + self.right_child.height
        if self.right_child is None:
            return 1 + self.left_child.height
        return 1 + max(self.left_child.height, self.right_child.height)

    @property
    def weight(self):
        return (0 if self.right_child is None else self.right_child.height) - (
            0 if self.left_child is None else self.left_child.height
        )

    def is_balanced(self):
        return abs(self.weight) <= 1


class AVLTree(Generic[NodeKey, NodeValue]):
    def __init__(self):
        self.root = None

    def _insert_new_node(
        self, start_node: AVLNode, key: NodeKey, value: NodeValue
    ) -> AVLNode:
        """Recursively try to insert a new node into the tree and return the node if it is inserted."""
        if start_node.key == key:
            return start_node
        if key < start_node.key:
            if start_node.left_child is None:
                start_node.left_child = AVLNode(parent=start_node, key=key, value=value)
                return start_node.left_child
            else:
                return self._insert_new_node(
                    start_node.left_child, key=key, value=value
                )
        else:
            if start_node.right_child is None:
                start_node.right_child = AVLNode(
                    parent=start_node, key=key, value=value
                )
                return start_node.right_child
            else:
                return self._insert_new_node(
                    start_node.right_child, key=key, value=value
                )

    def _insert_and_balance(self, key: NodeKey, value: NodeValue):
        inserted_node = self._insert_new_node(self.root, key=key, value=value)
        if inserted_node is None:
            return None
        parent = inserted_node.parent
        self._rebalance_tree_from_node(parent)
        return inserted_node

    def _rebalance_tree_from_node(self, node: AVLNode):
        while node is not None:
            parent = node.parent
            if not node.is_balanced():
                self._rebalance(node)
            # Here we should update the height of the parent.
            node = parent

    def _rebalance(self, node: AVLNode):
        if node.weight == 2:
            if node.right_child.weight == -1:
                self._rotate_right(node.right_child.left_child)
            self._rotate_left(node.right_child)
        elif node.weight == -2:
            if node.left_child.weight == 1:
                self._rotate_left(node.left_child.right_child)
            self._rotate_right(node.left_child)

    def _rotate_left(self, node: AVLNode):
        if node.is_root():
            return
        node.parent.right_child = node.left_child
        if node.left_child is not None:
            node.left_child.parent = node.parent
        grandparent = node.parent.parent
        if grandparent is None:
            self.root = node
        else:
            if node.parent.is_left_child():
                grandparent.left_child = node
            else:
                grandparent.right_child = node
        node.parent.parent = node
        node.left_child = node.parent
        node.parent = grandparent

    def _rotate_right(self, node: AVLNode):
        if node.is_root():
            return
        node.parent.left_child = node.right_child
        if node.right_child is not None:
            node.right_child.parent = node.parent
        grandparent = node.parent.parent
        if grandparent is None:
            self.root = node
        else:
            if node.parent.is_left_child():
                grandparent.left_child = node
            else:
                grandparent.right_child = node
        node.parent.parent = node
        node.right_child = node.parent
        node.parent = grandparent

    def insert(self, key: NodeKey, value: NodeValue | None = None):
        if self.root is None:
            self.root = AVLNode(key=key, value=value)
            return self.root
        else:
            return self._insert_and_balance(key=key, value=value)

    def delete(self, key: NodeKey) -> Self | None:
        """Return the node that replace the deleted node. None if is a leaf or not found"""
        node = self.search(key)
        if node is None:
            return None
        if node.is_leaf():
            if node.is_root():
                self.root = None
            else:
                if node.is_left_child():
                    node.parent.left_child = None
                if node.is_right_child():
                    node.parent.right_child = None
                self._rebalance_tree_from_node(node.parent)
            return None

        # Only one child
        if (node.left_child is None) or (node.right_child is None):
            child = node.left_child or node.right_child
            child.parent = node.parent

            if not node.is_root():
                if node.is_left_child():
                    node.parent.left_child = child
                elif node.is_right_child():
                    node.parent.right_child = child
                self._rebalance_tree_from_node(node.parent)
            return child

        # Two children
        # It always have a successor, because right child always exists !
        successor = node.get_successor()

        # We update parent relationship to grandchild.
        if successor.is_left_child():
            successor.parent.left_child = successor.right_child
        else:
            successor.parent.right_child = successor.right_child

        if successor.left_child is not None:
            successor.left_child.parent = successor.parent

        # update node child parent
        if node.left_child is not None:
            node.left_child.parent = successor
        if node.right_child is not None:
            node.right_child.parent = successor

        # update successor child parent
        if successor.left_child is not None:
            successor.left_child.parent = successor.parent
        if successor.right_child is not None:
            successor.right_child.parent = successor.parent

        successor.left_child = node.left_child
        successor.right_child = node.right_child
        self._rebalance_tree_from_node(successor)
        return successor

    def _search(self, key: NodeKey, start_node: AVLNode) -> AVLNode | None:
        if key == start_node.key:
            return start_node
        if key < start_node.key:
            return self._search(key, start_node.left_child) if start_node.left_child is not None else None
        else:
            return self._search(key, start_node.right_child) if start_node.right_child is not None else None

    def search(self, key: NodeKey) -> AVLNode | None:
        if self.root is None:
            return None
        return self._search(key, self.root)

    def key_exists(self, key: NodeKey):
        return self.search(key) is not None
