from typing import TypeVar, Generic, Dict, Hashable
from graphviz import Graph

NV = TypeVar('NV')
EV = TypeVar('EV')

class UndirectedGraph(Generic[NV, EV]):
    """Graph implementation using hashable object and adjacency dict."""
    
    def __init__(self) -> None:
        super().__init__()
        self.nodes: Dict[Hashable, NV] =  dict()
        self.links: Dict[Hashable, Dict[Hashable, EV]] = dict()

    def add_node(self, node: Hashable, value: NV=None) -> None:
        """Add node to the graph. If the node already exist update the node value.
        
        The None value cannot be used in our implementation to avoid any confusion (None is an hashable).

        Args:
            node (Hashable): The node to add to the graph.
            value (_type_): The value you want to associate to this node. This can be used to put attribute to describe the node

        Raises:
            ValueError: When you try to add a None value to the graph
        """
        if node is None:
            raise ValueError("None value cannot be used as a Node")
        if node in self.nodes:
            # Update the node value
            self.nodes[node] = value
        else:
            self.nodes[node] = value
            # We initialize the entry in the adjency dict for this node.
            self.links[node] = {}

    def remove_node(self, node: Hashable):
        """Remove a node from the graph. This will delete all links associated to it.

        Args:
            node (Hashable): The node to remove from the graph

        Raises:
            ValueError: When the node is not in the graph
        """        
        if node not in self.nodes:
            raise ValueError("The given node is not in the graph")
        # Delete the node
        del self.nodes[node]
        # Delete all links which contains this node
        connected_nodes = self.links[node]
        for connected_node in connected_nodes:
            del self.links[connected_node][node]
        del self.links[node]
        
    def add_link(self, node1: Hashable, node2: Hashable, link_value: EV = None, node1_value: NV = None, node2_value: NV = None):
        """Add a link to the graph. If a node is not part of the graph yet, it will be created with the given node value.
        If the node already exists, the node value will not be updated.

        Args:
            node1 (Hashable): _description_
            node2 (Hashable): _description_
            link_value (EV): _description_
            node1_value (NV, optional): _description_. Defaults to None.
            node2_value (_type_, optional): _description_. Defaults to NV.
        """
        # Check that each node exists first.
        if node1 not in self.nodes:
            self.add_node(node1, node1_value)
        if node2 not in self.nodes:
            self.add_node(node2, node2_value)
        
        # Add the link in the adjency dict for both node.
        self.links[node1][node2] = link_value
        self.links[node2][node1] = link_value

    def remove_link(self, node1: Hashable, node2: Hashable):
        """Remove the link of the graph. Each node must exist in the graph.

        Args:
            node1 (Hashable): First node of the link
            node2 (Hashable): Second node of the link

        Raises:
            ValueError: The first node in not in the graph
            ValueError: The second node is not in the graph
        """        
        if node1 not in self.nodes:
            raise ValueError("First node of the given link is not in the graph")
        if node2 not in self.nodes:
            raise ValueError("Second node of the given link is not in the graph")
        del self.links[node1][node2]
        if node1 != node2: # A link can connect the node to itself, but we can't delete it twice.
            del self.links[node2][node1]

    def render(self, filename: str, graph_name: str, format: str = "svg"):
        """Render a graph to the fileformat yout want, with the given filename

        Args:
            filename (str): Filename for the rendered
            graph_name (str): The name of the graph to be rendered
            format (str, optional): File format of the graph. Defaults to "svg". Supported format are available [here](https://graphviz.org/docs/outputs/)
        """
        dot = Graph(graph_name, format=format)

        for node, node_value in self.nodes.items():
            dot.node(str(node), str(node_value))
        
        added_links = set()

        for source_node, dest_nodes in self.links.items():
            for dest_node, link_value in dest_nodes.items():
                # Check the link is 
                if (dest_node, source_node) in added_links:
                    continue
                added_links.add((source_node, dest_node))
                dot.edge(str(source_node), str(dest_node) , label=str(link_value))
        dot.render(filename)