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
        return self.weight <= 1


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
        while parent is not None:
            grandparent = parent.parent
            if not parent.is_balanced():
                self._rebalance(parent)
            # Here we should update the height of the parent.

            parent = grandparent
        return inserted_node

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
        node.parent.left_child = node.left_child
        if node.left_child is not None:
            node.left_child.parent = node.parent
        grandparent = node.parent.parent
        node.parent.parent = node
        node.right_child = node.parent
        node.parent = grandparent
        if grandparent is None:
            self.root = node

    def _rotate_right(self, node: AVLNode):
        if node.is_root():
            return
        node.parent.right_child = node.right_child
        if node.right_child is not None:
            node.right_child.parent = node.parent
        grandparent = node.parent.parent
        node.parent.parent = node
        node.left_child = node.parent
        node.parent = grandparent
        if grandparent is None:
            self.root = node

    def insert(self, key: NodeKey, value: NodeValue | None = None):
        if self.root is None:
            self.root = AVLNode(key=key, value=value)
            return self.root
        else:
            return self._insert_and_balance(key=key, value=value)
