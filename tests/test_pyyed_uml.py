import pyyed
import xml.etree.ElementTree as xml

import pytest


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


