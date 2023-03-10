from typing import Generic, TypeVar, Optional
from typing_extensions import Self
from dataclasses import dataclass

NodeKey = TypeVar("NodeKey")
NodeValue = TypeVar("NodeValue")


@dataclass
class BinarySearchNode(Generic[NodeKey, NodeValue]):
    parent: Optional["BinarySearchNode"] = None
    left_child: Optional["BinarySearchNode"] = None
    right_child: Optional["BinarySearchNode"] = None
    key: NodeKey = None
    value: NodeValue = None

    def __iter__(self):
        # Walking through the tree in order
        if self.left_child:
            for node in self.left_child:
                yield node
        yield self
        if self.right_child:
            for node in self.right_child:
                yield node

    def is_leaf(self):
        return (self.left_child is None) and (self.right_child is None)

    def is_root(self):
        return self.parent is None

    def insert(
        self, key: NodeKey, value: NodeValue | None = None
    ) -> "BinarySearchNode":
        if key == self.key:
            return self
        if key < self.key:
            if self.left_child is None:
                self.left_child = BinarySearchNode(self, key=key, value=value)
                return self.left_child
            else:
                return self.left_child.insert(key, value)
        else:
            if self.right_child is None:
                self.right_child = BinarySearchNode(self, key=key, value=value)
                return self.right_child
            else:
                return self.right_child.insert(key, value)

    def get_most_left(self) -> "BinarySearchNode":
        return self if self.left_child is None else self.left_child.get_most_left()

    def get_most_right(self) -> "BinarySearchNode":
        return self if self.right_child is None else self.right_child.get_most_right()

    def has_successor(self) -> bool:
        return (self.right_child is not None) or self.is_left_child()

    def has_predecessor(self) -> "BinarySearchNode":
        return (self.left_child is not None) or self.is_right_child()

    def get_successor(self) -> "BinarySearchNode":
        if self.right_child is not None:
            return self.right_child.get_most_left()
        return self.parent

    def get_predecessor(self) -> "BinarySearchNode":
        if self.left_child is not None:
            return self.left_child.get_most_right()
        return self.parent

    def is_left_child(self):
        return self.parent.left_child is self if self.parent is not None else False

    def is_right_child(self):
        return self.parent.right_child is self if self.parent is not None else False

    def delete(self, key: NodeKey) -> Self | None:
        """Return the node that replace the deleted node. None if is a leaf or not found"""
        node = self.search(key)
        if node is None:
            return None
        if node.is_leaf():
            if not node.is_root():
                if node.is_left_child():
                    node.parent.left_child = None
                    del node
                else:
                    node.parent.right_child = None
                    del node
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
            del node
            return child

        # Two children
        # It always have a successor, because right child always exists !
        successor = node.get_successor()
        # update node
        node.key = successor.key
        node.value = successor.value

        # We update parent relationship to grandchild.
        if successor.is_left_child():
            successor.parent.left_child = successor.right_child
        else:
            successor.parent.right_child = successor.right_child

        del successor
        return node

    def search(self, key: NodeKey) -> Self | None:
        if key == self.key:
            return self
        if key < self.key:
            return self.left_child.search(key) if self.left_child is not None else None
        else:
            return (
                self.right_child.search(key) if self.right_child is not None else None
            )

    def key_exists(self, key: NodeKey):
        return self.search(key) is not None
