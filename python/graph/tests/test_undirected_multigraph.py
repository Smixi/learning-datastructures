from ..undirected_graph.multigraph import AdjacencySetUndirectedMultiGraph
# Test the behavior of the graph

def test_undirect_multigraph_add_node():
    g: AdjacencySetUndirectedMultiGraph[int, str] = AdjacencySetUndirectedMultiGraph()
    g.add_node(1, 1)
    assert g.nodes == {1: 1}

def test_undirect_multigraph_remove_node():
    g: AdjacencySetUndirectedMultiGraph[int, str] = AdjacencySetUndirectedMultiGraph()
    g.add_node(1, 1)
    g.remove_node(1)
    assert g.nodes == {}

def test_undirect_multigraph_add_link():
    g: AdjacencySetUndirectedMultiGraph[int, str] = AdjacencySetUndirectedMultiGraph()
    g.add_node(1,1)
    g.add_link(1,2, "link_1", "LinkValue", node1_value=-1, node2_value=1)
    assert g.links == {1: {2: {"link_1": "LinkValue"}}, 2: {1: {"link_1": "LinkValue"}}}
    assert g.nodes == {1: 1, 2: 1}

def test_undirect_multigraph_add_links():
    g: AdjacencySetUndirectedMultiGraph[int, str] = AdjacencySetUndirectedMultiGraph()
    g.add_node(1,1)
    g.add_link(1,2, "link_1", "LinkValue", node1_value=-1, node2_value=1)
    g.add_link(1,2, "link_2", "AnotherLink", node1_value=-1, node2_value=1)
    assert g.links == {1: {2: {"link_1": "LinkValue", "link_2": "AnotherLink"}}, 2: {1: {"link_1": "LinkValue", "link_2": "AnotherLink"}}}
    assert g.nodes == {1: 1, 2: 1}

def test_undirect_multigraph_remove_links():
    g: AdjacencySetUndirectedMultiGraph[int, str] = AdjacencySetUndirectedMultiGraph()
    g.add_link(1, 2, "link_1")
    g.remove_links(1, 2)
    assert g.links == {1: {}, 2: {}}
    assert g.nodes == {1: None, 2: None}

def test_undirect_multigraph_remove_link_no_remaining():
    g: AdjacencySetUndirectedMultiGraph[int, str] = AdjacencySetUndirectedMultiGraph()
    g.add_link(1, 2, "link_1")
    g.remove_link(1, 2, "link_1")
    assert g.links == {1: {}, 2: {}}
    assert g.nodes == {1: None, 2: None}

def test_undirect_multigraph_remove_link_with_remaining():
    g: AdjacencySetUndirectedMultiGraph[int, str] = AdjacencySetUndirectedMultiGraph()
    g.add_link(1, 2, "link_1")
    g.add_link(1, 2, "link_2")
    g.remove_link(1, 2, "link_1")
    assert g.links == {1: {2: {"link_2": None}}, 2: {1: {"link_2": None}}}
    assert g.nodes == {1: None, 2: None}

def test_undirect_multigraph_remove_node_linked():
    g: AdjacencySetUndirectedMultiGraph[int, str] = AdjacencySetUndirectedMultiGraph()
    g.add_link(1, 2, "link_1")
    g.remove_node(1)
    assert g.links == {2: {}}
    assert g.nodes == {2: None}

def test_undirected_multigraph_render(tmpdir, test_multigraph_viz_dot):
    
    path = tmpdir + "/rendered.dot" 

    g: AdjacencySetUndirectedMultiGraph[int, str] = AdjacencySetUndirectedMultiGraph()
    g.add_link(1, 2, "TestLink", "TestLink", "Node1", "Node2")
    g.add_link(1, 2, "TestLink2", "TestLink2")
    g.add_link(1, 1, "TestLink3")
    
    g.render(path, "TestGraph", "dot")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert content == test_multigraph_viz_dot
    
