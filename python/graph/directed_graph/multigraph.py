from typing import TypeVar, Generic, Dict, Hashable, Set, Tuple
from graphviz import Digraph

NV = TypeVar('NV')
EV = TypeVar('EV')

NodeId = Hashable
LinkId = Hashable

class AdjacencyDirectedSetMultiGraph(Generic[NV, EV]):
    """Graph implementation using hashable object and adjacency dict."""
    
    def __init__(self) -> None:
        super().__init__()
        self.nodes: Dict[NodeId, NV] =  dict()
        self.links: Dict[NodeId, Dict[NodeId, Dict[LinkId, EV]]] = dict()
        self.reverse_link_lookup: Dict[NodeId, Dict[NodeId, Set[LinkId]]] = dict()

    def add_node(self, node: NodeId, value: NV=None) -> None:
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
        
        if node not in self.nodes:
            # We initialize the entry in the adjency dict for this node.
            self.links[node] = {}
        self.nodes[node] = value
        self.reverse_link_lookup[node] = {}

    def remove_node(self, node: NodeId):
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
        related_links = self.reverse_link_lookup[node]
        for connected_node, link in related_links:
            del self.links[connected_node][link]
        del self.reverse_link_lookup[node]
        del self.links[node]
        
    def add_link(self, node1: NodeId, node2: NodeId, link_id: LinkId, link_value: EV = None, node1_value: NV = None, node2_value: NV = None):
        """Add a link to the graph. If a node is not part of the graph yet, it will be created with the given node value.
        If the node already exists, the node value will not be updated.
        The entry is also added in a lookup set to facilitate deletion.
        Args:
            node1 (NodeId): Source node that take part of the link
            node2 (NodeId): Destination node that take part of the link
            link_id (): Link id. Identify a unique link between node1 and node2.
            link_value (EV): A value stored for this link
            node1_value (NV, optional): In case this node doesn't exists, give it a value. Defaults to None.
            node2_value (_type_, optional): In case this node doesn't exists, give it a value. Defaults to NV.
        """
        # Check that each node exists first.
        if node1 not in self.nodes:
            self.add_node(node1, node1_value)
        if node2 not in self.nodes:
            self.add_node(node2, node2_value)
        
        # Add the link in the adjency dict for the source node. Must ensure the dict indirection exist before hands.
        if node2 not in self.links[node1]:
            self.links[node1][node2] = {}
        self.links[node1][node2][link_id] = link_value
        
        if node1 not in self.reverse_link_lookup[node2]:
            self.reverse_link_lookup[node2][node1] = set()
        self.reverse_link_lookup[node2][node1].add(link_id)
        

    def remove_links(self, node1: NodeId, node2: NodeId):
        """Remove all links of the graph between node1 and node2 (from source to dest). Each node must exist in the graph.

        Args:
            node1 (NodeId): Source node of the link
            node2 (NodeId): Dest node of the link

        Raises:
            ValueError: The first node in not in the graph
            ValueError: The second node is not in the graph
        """        
        if node1 not in self.nodes:
            raise ValueError("First node of the given link is not in the graph")
        if node2 not in self.nodes:
            raise ValueError("Second node of the given link is not in the graph")
        del self.links[node1][node2]
        del self.reverse_link_lookup[node2][node1]
        
    def remove_link(self, node1: NodeId, node2: NodeId, link_id: LinkId):
        """Remove all links of the graph between node1 and node2. Each node must exist in the graph.

        Args:
            node1 (NodeId): First node of the link
            node2 (NodeId): Second node of the link
            link_id (LinkId): The id of the link to remove.
        Raises:
            ValueError: The first node in not in the graph
            ValueError: The second node is not in the graph
        """        
        if node1 not in self.nodes:
            raise ValueError("First node of the given link is not in the graph")
        if node2 not in self.nodes:
            raise ValueError("Second node of the given link is not in the graph")
        del self.links[node1][node2][link_id]
        # Remove key if there is no more item in the dictionnary
        if len(self.links[node1][node2]) == 0:
            del self.links[node1][node2]

        self.reverse_link_lookup[node2][node1].remove(link_id)
        if len(self.reverse_link_lookup[node2][node1]) == 0:
            del self.reverse_link_lookup[node2][node1]

    def render(self, filename: str, graph_name: str, output_format: str = "svg"):
        """Render a graph to the fileformat yout want, with the given filename

        Args:
            filename (str): Filename for the rendered
            graph_name (str): The name of the graph to be rendered
            format (str, optional): File format of the graph. Defaults to "svg". Supported format are available [here](https://graphviz.org/docs/outputs/)
        """
        dot = Digraph(graph_name, format=output_format)

        for node, node_value in self.nodes.items():
            dot.node(str(node), str(node_value))
        
        for source_node, dest_nodes in self.links.items():
            for dest_node, links in dest_nodes.items():
                for link_id, link_value in links.items():
                    dot.edge(str(source_node), str(dest_node) , label=str(link_value))
        dot.render(filename)