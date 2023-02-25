from typing import Generic, TypeVar, Optional, List
from typing_extensions import Self
from dataclasses import dataclass, field
from sortedcontainers import SortedSet, SortedDict

NodeKey = TypeVar("NodeKey")
NodeValue = TypeVar("NodeValue")

GenericEntry = Generic[NodeKey, NodeValue]

@dataclass
class BTreeEntry(GenericEntry):
    key: NodeKey
    value: NodeValue

    def __hash__(self) -> int:
        return self.key.__hash__()

    def _get_key(self, entry_or_value: "BTreeEntry" | NodeKey):
        if isinstance(entry_or_value, BTreeEntry):
            return entry_or_value.key
        return entry_or_value

    def __eq__(self, other: "BTreeEntry" | NodeKey):
        return self.key == self._get_key(other)

    def __lt__(self, other: "BTreeEntry" | NodeKey):
        return self.key < self._get_key(other)
    
    def __gt__(self, other: "BTreeEntry" | NodeKey):
        return self.key > self._get_key(other)

    def __ge__(self, other: "BTreeEntry" | NodeKey):
        return self.key >= self._get_key(other)

    def __le__(self, other: "BTreeEntry" | NodeKey):
        return self.key <= self._get_key(other)

@dataclass
class BTreeNode(GenericEntry):
    children: SortedSet[Self] = field(default_factory=SortedSet)
    entries: SortedDict[NodeKey, BTreeEntry] = field(default_factory=SortedDict)
    order: int = 2

    def get_child(self, key: NodeKey) -> "BTreeNode":
        """Get the child node that could contains the key"""
        if len(self.entries) == 0:
            raise ValueError("Node is empty")
        index = self.entries.bisect(key)
        return self.children[index]

    def is_leaf(self):
        return len(self.children) == 0
    
    def is_full(self):
        return len(self.entries) == self.order * 2 - 1

    def __getitem__(self, index: NodeKey) -> BTreeEntry:
        return self.entries[index]

    def __setitem__(self, index: NodeKey, value: BTreeEntry):
        self.entries[index] = value

    def __contains__(self, item_or_key: "BTreeEntry" | NodeKey):
        return item_or_key in self.entries

    def _get_entry(self, entry_or_key: "BTreeNode" | NodeKey | BTreeEntry):
        if isinstance(entry_or_key, BTreeNode):
            return entry_or_key.entries.values()[0]
        return entry_or_key

    def split(self):
        left_node = BTreeNode(order=self.order)
        left_node.children.update(self.children.islice(stop=self.order // 2))
        right_node = BTreeNode(order=self.order)
        right_node.children.update(self.children.islice(start=self.order // 2 + 1))
        left_node.entries.update({key: self.entries[key] for key in self.entries.islice(stop=self.order // 2)})
        right_node.entries.update({key: self.entries[key] for key in self.entries.islice(start=self.order // 2 + 1)})
        _, separator_entry = self.entries.popitem(index=self.order // 2)
        return left_node, separator_entry, right_node

    def __eq__(self, other: "BTreeNode" | NodeKey | BTreeEntry):
        return self.entries.values()[0] == self._get_entry(other)

    def __lt__(self, other: "BTreeNode" | NodeKey | BTreeEntry):
        return self.entries.values()[0] < self._get_entry(other)
    
    def __gt__(self, other: "BTreeNode" | NodeKey | BTreeEntry):
        return self.entries.values()[0] > self._get_entry(other)

    def __ge__(self, other: "BTreeNode" | NodeKey | BTreeEntry):
        return self.entries.values()[0] >= self._get_entry(other)

    def __le__(self, other: "BTreeNode" | NodeKey | BTreeEntry):
        return self.entries.values()[0] <= self._get_entry(other)

    def __hash__(self) -> int:
        return hash(None) if len(self.entries) == 0 else hash(self.entries.values()[0])