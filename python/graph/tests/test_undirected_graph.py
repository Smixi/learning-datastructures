from ..undirected_graph.adjacency_set import AdjacencySetUndirectedGraph
# Test the behavior of the graph

def test_undirect_graph_add_node():
    g: AdjacencySetUndirectedGraph[int, str] = AdjacencySetUndirectedGraph()
    g.add_node(1, 1)
    assert g.nodes == {1: 1}

def test_undirect_graph_remove_node():
    g: AdjacencySetUndirectedGraph[int, str] = AdjacencySetUndirectedGraph()
    g.add_node(1, 1)
    g.remove_node(1)
    assert g.nodes == {}

def test_undirect_graph_add_link():
    g: AdjacencySetUndirectedGraph[int, str] = AdjacencySetUndirectedGraph()
    g.add_node(1,1)
    g.add_link(1,2, "LinkValue", node1_value=-1, node2_value=1)
    assert g.links == {1: {2: "LinkValue"}, 2: {1: "LinkValue"}}
    assert g.nodes == {1: 1, 2: 1}

def test_undirect_graph_remove_link():
    g: AdjacencySetUndirectedGraph[int, str] = AdjacencySetUndirectedGraph()
    g.add_link(1, 2)
    g.remove_link(1, 2)
    assert g.links == {1: {}, 2: {}}
    assert g.nodes == {1: None, 2: None}

def test_undirect_graph_remove_node_linked():
    g: AdjacencySetUndirectedGraph[int, str] = AdjacencySetUndirectedGraph()
    g.add_link(1, 2)
    g.remove_node(1)
    assert g.links == {2: {}}
    assert g.nodes == {2: None}

def test_undirected_graph_render(tmpdir, test_viz_dot):
    
    path = tmpdir + "/rendered.dot" 

    g: AdjacencySetUndirectedGraph[int, str] = AdjacencySetUndirectedGraph()
    g.add_link(1, 2, "TestLink", "Node1", "Node2")
    g.add_link(1,1)
    
    g.render(path, "TestGraph", "dot")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert content == test_viz_dot
    
