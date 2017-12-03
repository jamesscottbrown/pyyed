import pyyed


def test_graph_added_node_has_default_fill():
    g = pyyed.Graph()
    g.add_node('N1')
    assert "#FF0000" == g.nodes['N1'].shape_fill


def test_graph_added_node_keeps_custom_fill():
    g = pyyed.Graph()
    g.add_node('N1', shape_fill="#99CC00")
    assert "#99CC00" == g.nodes['N1'].shape_fill
