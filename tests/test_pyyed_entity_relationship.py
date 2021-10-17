import pyyed
import xml.etree.ElementTree as xml

import pytest


def test_er_node_properties_are_set():
    expected_attributes = 'attribute 1\nattribute 2'

    g = pyyed.Graph()

    g.add_node('BigEntity', node_type="GenericNode",
               ER={'attributes': expected_attributes})

    assert g.nodes["BigEntity"].library['ER']["attributes"] == expected_attributes

    graphml = g.get_graph()
#    assertERNode(graphml, 
#                  expected_attributes)


# def assertERNode(graphml, expected_stereotype, expected_attributes, expected_methods):
#     doc = xml.fromstring(graphml)
#     nsmap = {'g': 'http://graphml.graphdrawing.org/xmlns',
#              'y': 'http://www.yworks.com/xml/graphml'
#              }
#     ernode = doc.find(
#         'g:graph/g:node/g:data/y:UMLClassNode/y:UML', namespaces=nsmap)
#     attributes = ernode.find('y:AttributeLabel', namespaces=nsmap)
#     methods = ernode.find('y:MethodLabel', namespaces=nsmap)
# 
#     assert ernode.attrib['stereotype'] == expected_stereotype
#     assert attributes.text == expected_attributes
#     assert methods.text == expected_methods
