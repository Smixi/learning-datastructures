import pytest

@pytest.fixture()
def test_viz_dot():
    return "graph TestGraph {\n\t1 [label=Node1]\n\t2 [label=Node2]\n\t1 -- 2 [label=TestLink]\n\t1 -- 1 [label=None]\n}\n"