import pyyed
import xml.etree.ElementTree as xml

import pytest


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


def test_numeric_node_ids():
    g = pyyed.Graph()
    g.add_node(1, label="Node1")
    g.add_node(2, label="Node2")
    g.add_edge(1, 2)

    assert g.nodes[1].label == "Node1"
    assert g.nodes[2].label == "Node2"

    node1 = g.edges['1'].node1
    node2 = g.edges['1'].node2

    assert g.nodes[node1].label == "Node1"
    assert g.nodes[node2].label == "Node2"

    assert g.get_graph()


def test_multiple_edges():
    g = pyyed.Graph()
    g.add_node('a', font_family="Zapfino")
    g.add_node('b', font_family="Zapfino")
    g.add_node('c', font_family="Zapfino")

    g.add_edge('a', 'b')
    g.add_edge('a', 'b')
    g.add_edge('a', 'c')

    e1 = g.edges['1']
    e2 = g.edges['2']
    e3 = g.edges['3']

    assert g.nodes[e1.node1].label == "a"
    assert g.nodes[e1.node2].label == "b"

    assert g.nodes[e2.node1].label == "a"
    assert g.nodes[e2.node2].label == "b"

    assert g.nodes[e3.node1].label == "a"
    assert g.nodes[e3.node2].label == "c"

    assert g.get_graph()


def test_node_already_there_check():

    g = pyyed.Graph()
    g.add_node('a')
    with pytest.raises(RuntimeWarning):
        g.add_node('a')
    with pytest.raises(RuntimeWarning):
        g.add_group('a')

    g = pyyed.Graph()
    g.add_group('a')
    with pytest.raises(RuntimeWarning):
        g.add_node('a')
    with pytest.raises(RuntimeWarning):
        g.add_group('a')

    g = pyyed.Graph()
    g.add_edge('a', 'b')
    with pytest.raises(RuntimeWarning):
        g.add_node('a')
    with pytest.raises(RuntimeWarning):
        g.add_group('a')
    g1 = g.add_group('g1')
    with pytest.raises(RuntimeWarning):
        g1.add_node('a')
    with pytest.raises(RuntimeWarning):
        g1.add_group('a')

    g = pyyed.Graph()
    g1 = g.add_group('g1')
    g1.add_node('a')
    g2 = g.add_group('g2')
    with pytest.raises(RuntimeWarning):
        g.add_node('a')
    with pytest.raises(RuntimeWarning):
        g.add_group('a')
    with pytest.raises(RuntimeWarning):
        g1.add_node('a')
    with pytest.raises(RuntimeWarning):
        g1.add_group('a')
    with pytest.raises(RuntimeWarning):
        g2.add_node('a')
    with pytest.raises(RuntimeWarning):
        g2.add_group('a')


def test_nested_graph_edges():
    g = pyyed.Graph()
    g.add_edge('a', 'b')
    g1 = g.add_group('g1')
    g1n1 = g1.add_node('g1n1')
    g1n1 = g1.add_node('g1n2')
    g2 = g1.add_group('g2')
    g2n1 = g2.add_node('g2n1')
    g2n2 = g2.add_node('g2n2')
    g3 = g1.add_group('g3')
    g3n1 = g3.add_node('g3n1')
    g3n2 = g3.add_node('g3n2')

    assert g.num_edges == 1
    g1.add_edge('g1n1', 'g1n2')
    assert g.num_edges == 2
    g2.add_edge('g2n2', 'g2n2')  # No, that's not a typo
    assert g.num_edges == 3
    g3.add_edge('c', 'd')
    g3.add_edge('c', 'd')
    assert g.num_edges == 5

    g.add_edge('g2n1', 'g2n2')
    g1.add_edge('g2n1', 'g2n2')
    g2.add_edge('g2n1', 'g2n2')
    with pytest.raises(RuntimeWarning):
        g3.add_edge('g2n1', 'g2n2')
    assert g.num_edges == 8

    with pytest.raises(RuntimeWarning):
        g2.add_edge('a', 'b')

    g.add_edge('g1n1', 'g2n2')
    g1.add_edge('g1n1', 'g2n2')
    with pytest.raises(RuntimeWarning):
        g2.add_edge('g1n1', 'g2n2')
    with pytest.raises(RuntimeWarning):
        g3.add_edge('g1n1', 'g2n2')
    assert g.num_edges == 10
