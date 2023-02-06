from typing import Generic, TypeVar, List
from dataclasses import dataclass, field


NodeValue = TypeVar("NodeValue")


@dataclass
class Node(Generic[NodeValue]):
    parent: "Node" = None
    children: List["Node"] = field(default_factory=list)
    value: NodeValue = None

    def is_leaf(self):
        return len(self.children) == 0

    def is_root(self):
        return self.parent is None

    def copy(self):
        return Node(self.parent, self.children)
