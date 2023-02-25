from .b_tree_node import BTreeEntry, BTreeNode, GenericEntry, NodeKey, NodeValue
from typing import Generic, TypeVar, Optional, List, Tuple, Iterator

class BTree(GenericEntry):
    def __init__(self, order: int = 2):
        self.order = order
        self.root = BTreeNode(order=order)

    def insert(self, key: NodeKey, value: Optional[NodeValue] = None):
        node = self.root
        # Special case for root, if it is full, split it and create a new root
        if key in node:
            node[key].value = value
            return None
        if node.is_full():
            left_child, separator_entry, right_child = node.split()
            self.root = BTreeNode(order=self.order)
            self.root.children.add(left_child)
            self.root.children.add(right_child)
            self.root.entries[separator_entry.key] = separator_entry
            if key < separator_entry.key:
                node = left_child
            else:
                node = right_child
        # Traverse the tree until a leaf is found, splitting nodes as needed
        while not node.is_leaf():
            # Find in which children the key should be inserted
            child_node = node.get_child(key)
            # Check if the key already exists for the child
            if key in child_node:
                child_node[key].value = value
                return None
            if not child_node.is_full():
                node = child_node
            else:
                left_child, separator_entry, right_child,  = child_node.split()
                node.children.add(left_child)
                node.children.add(right_child)
                node.entries[separator_entry.key] = separator_entry
                if key < separator_entry.key:
                    node = left_child
                else:
                    node = right_child
        node.entries[key] = BTreeEntry(key=key, value=value)