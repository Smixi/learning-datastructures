import pytest


@pytest.fixture()
def test_viz_dot():
    return "graph TestGraph {\n\t1 [label=Node1]\n\t2 [label=Node2]\n\t1 -- 2 [label=TestLink]\n\t1 -- 1 [label=None]\n}\n"


@pytest.fixture()
def test_multigraph_viz_dot():
    return "graph TestGraph {\n\t1 [label=Node1]\n\t2 [label=Node2]\n\t1 -- 2 [label=TestLink]\n\t1 -- 2 [label=TestLink2]\n\t1 -- 1 [label=None]\n}\n"


@pytest.fixture()
def test_multigraph_directed_viz_dot():
    return "digraph TestGraph {\n\t1 [label=Node1]\n\t2 [label=Node2]\n\t1 -> 2 [label=TestLink]\n\t1 -> 2 [label=TestLink2]\n\t1 -> 1 [label=TestLink3]\n\t2 -> 1 [label=TestLink4]\n}\n"
