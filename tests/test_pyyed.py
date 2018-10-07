import pyyed
import xml.etree.ElementTree as xml


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


def test_uml_node_properties_are_set():
    g = pyyed.Graph()

    expected_attributes = "int foo\nString bar"
    expected_methods = "foo()\nbar()"
    expected_stereotype = "abstract"

    g.add_node('AbstractClass', node_type="UMLClassNode",
               UML={"stereotype": expected_stereotype,
                    "attributes": expected_attributes,
                    "methods": expected_methods})

    assert g.nodes["AbstractClass"].UML["stereotype"] == expected_stereotype
    assert g.nodes["AbstractClass"].UML["attributes"] == expected_attributes
    assert g.nodes["AbstractClass"].UML["methods"] == expected_methods

    graphml = g.get_graph()
    assertUmlNode(graphml, expected_stereotype,
                  expected_attributes, expected_methods)


def test_uml_stereotype_is_optional():
    g = pyyed.Graph()

    expected_attributes = "int foo\nString bar"
    expected_methods = "foo()\nbar()"

    g.add_node('Class', node_type="UMLClassNode",
               UML={"attributes": expected_attributes,
                    "methods": expected_methods})

    assert g.nodes["Class"].UML["methods"] == expected_methods
    assert g.nodes["Class"].UML["attributes"] == expected_attributes

    graphml = g.get_graph()
    assertUmlNode(graphml, "", expected_attributes, expected_methods)


def assertUmlNode(graphml, expected_stereotype, expected_attributes, expected_methods):
    doc = xml.fromstring(graphml)
    nsmap = {'g': 'http://graphml.graphdrawing.org/xmlns',
             'y': 'http://www.yworks.com/xml/graphml'
             }
    umlnode = doc.find(
        'g:graph/g:node/g:data/y:UMLClassNode/y:UML', namespaces=nsmap)
    attributes = umlnode.find('y:AttributeLabel', namespaces=nsmap)
    methods = umlnode.find('y:MethodLabel', namespaces=nsmap)

    assert umlnode.attrib['stereotype'] == expected_stereotype
    assert attributes.text == expected_attributes
    assert methods.text == expected_methods


def test_numeric_node_ids():
    g = pyyed.Graph()
    g.add_node(1, label="Node1")
    g.add_node(2, label="Node2")
    g.add_edge(1,2)

    assert g.nodes[1].label == "Node1"
    assert g.nodes[2].label == "Node2"
    
    node1 = g.edges['1_2'].node1
    node2 = g.edges['1_2'].node2
    
    assert g.nodes[node1].label == "Node1"
    assert g.nodes[node2].label == "Node2"

    assert g.get_graph()