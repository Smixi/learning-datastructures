from .b_tree_node import BTreeEntry, BTreeNode, GenericEntry, NodeKey, NodeValue
from typing import Generic, TypeVar, Optional, List, Tuple, Iterator, cast


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
            separator_entry = cast(BTreeEntry, separator_entry)
            self.root = BTreeNode(order=self.order)
            left_child.parent = self.root
            right_child.parent = self.root
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
                (
                    left_child,
                    separator_entry,
                    right_child,
                ) = child_node.split()
                left_child.parent = node
                right_child.parent = node
                node.children.add(left_child)
                node.children.add(right_child)
                node.entries[separator_entry.key] = separator_entry
                if key < separator_entry.key:
                    node = left_child
                else:
                    node = right_child
        node.entries[key] = BTreeEntry(key=key, value=value)

    def search(self, key: NodeKey) -> Optional[BTreeEntry]:
        node = self.search_node(key)
        if node is None:
            return None
        return node[key]

    def search_node(self, key: NodeKey) -> Optional[BTreeNode]:
        node = self.root
        while True:
            if key in node:
                return node
            if node.is_leaf():
                return None
            node = node.get_child(key)
            if node is None:
                return None

    def _delete_leaf_node_break_property(self, node: BTreeNode, key: NodeKey):
        # Subcase: Deletion will break the BTree property: minimum number of entries + not root
        index = node.parent.children.index(node)
        sibling_node_with_enough_keys = None
        parent = node.parent
        del node.entries[key]
        if index != 0:
            left_sibling = node.parent.children[index - 1]
            if len(left_sibling.entries) > self.order - 1:
                # We can borrow entry from the left sibling
                sibling_node_with_enough_keys = left_sibling
                (
                    sibling_entry_key,
                    sibling_entry,
                ) = sibling_node_with_enough_keys.entries.items()[-1]
                # Replace by the left sibling
                del sibling_node_with_enough_keys.entries[sibling_entry_key]
                parent_key, parent_entry = parent.entries.items()[index]
                del parent.entries[parent_key]
                parent.entries[sibling_entry_key] = sibling_entry
                node.entries[parent_key] = parent_entry
                return
        if (
            index != (len(node.parent.entries))
            and sibling_node_with_enough_keys is None
        ):
            right_sibling = node.parent.children[index + 1]
            if len(right_sibling.entries) > self.order - 1:
                # We can borrow entry from the right sibling
                sibling_node_with_enough_keys = right_sibling
                # Replace by the right sibling
                (
                    sibling_entry_key,
                    sibling_entry,
                ) = sibling_node_with_enough_keys.entries.items()[0]
                del sibling_node_with_enough_keys.entries[sibling_entry_key]
                parent_key, parent_entry = parent.entries.items()[index]
                del parent.entries[parent_key]
                parent.entries[sibling_entry_key] = sibling_entry
                node.entries[parent_key] = parent_entry
                return
        # We need to merge keys of this node with a sibling.
        return

    def _delete_leaf_node(self, node: BTreeNode, key: NodeKey):
        if (len(node.entries) > self.order - 1) or (node is self.root):
            # Subcase: Deletion will not break the BTree property: minimum number of entries or root
            del node.entries[key]
        else:
            self._delete_leaf_node_break_property(node, key)

    def delete(self, key: NodeKey):
        node = self.search_node(key)
        if node is None:
            raise ValueError("Key not found")
        # Case where the node is a leaf.
        node = cast(BTreeNode, node)
        if node.is_leaf():
            self._delete_leaf_node(node, key)
            return
        # Case: this is an internal node.

        # Case:
