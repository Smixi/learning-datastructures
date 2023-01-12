from graphviz import Graph
from undirected_graph import UndirectedGraph

def render_undirected_graph(self: UndirectedGraph, filename: str, graph_name: str, format: str = "svg"):
    """Render a graph to the fileformat yout want, with the filename you want.

    Args:
        filename (str): Filename for the rendered
        graph_name (str): The name of the graph to be rendered
        format (str, optional): File format of the graph. Defaults to "svg". Supported format are available [here](https://graphviz.org/docs/outputs/)
    """
    dot = Graph(graph_name, format=format)

    for node, node_value in graph.nodes.items():
        dot.node(str(node), node_value.label)
    
    added_links = set()

    for source_node, dest_nodes in graph.links.items():
        for dest_node, link_value in dest_nodes.items():
            # Check the link is 
            if (dest_node, source_node) in added_links:
                continue
            added_links.add((source_node, dest_node))
            dot.edge(str(source_node), str(dest_node) , label=link_value.label)
    dot.render(filename)