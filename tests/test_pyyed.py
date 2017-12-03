import pyyed


def test_graph_added_node_has_default_fill():
    g = pyyed.Graph()
    g.add_node('N1')
    assert "#FF0000" == g.nodes['N1'].shape_fill


def test_graph_added_node_keeps_custom_fill():
    g = pyyed.Graph()
    g.add_node('N1', shape_fill="#99CC00")
    assert "#99CC00" == g.nodes['N1'].shape_fill


def test_node_properties_after_nodes_and_edges_added():

    g = pyyed.Graph()    

    g.add_node('foo',  shape="ellipse")
    g.add_node('foo2', shape="roundrectangle", font_style="bolditalic")    

    g.add_edge('foo1', 'foo2')
    g.add_node('abc', shape="triangle", font_style="bold")    

    assert g.nodes["foo"].shape == "ellipse"
    assert g.nodes["foo"].font_style == "plain"

    assert g.nodes["foo2"].shape == "roundrectangle"
    assert g.nodes["foo2"].font_style == "bolditalic"

    assert g.nodes["abc"].shape == "triangle"
    assert g.nodes["abc"].font_style == "bold"
