from __future__ import print_function

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pyyed

g = pyyed.Graph()
g.add_node('Person', shape_fill="#EEEEEE",
           node_type="GenericNode",
           ER={"attributes": ["name", "surname"]})

#This is an entity without any attribut, for which only name will be set
g.add_node('Role', shape_fill="#EEEEEE",
           node_type="GenericNode",
           ER={})

g.add_node('Kind', shape_fill="#EEEEEE",
           node_type="GenericNode",
           ER={'weak':'true'})

# g.add_node('ICar', shape_fill="#EEEEEE",
#            node_type="UMLClassNode",
#            UML={"stereotype": "interface",
#                 "attributes": "",
#                 "methods": "getModel()\ngetManufacturer()\ngetPrice()\nsetPrice()"})

#g.add_node('Vehicle', shape_fill="#EEEEEE", node_type="UMLClassNode")
#g.add_edge('Car', 'Vehicle', arrowhead="white_delta")
#g.add_edge('Car', 'ICar', arrowhead="white_delta", line_type="dashed")
#g.add_node('This is a note', shape_fill="#EEEEEE", node_type="UMLNoteNode")

# print(g.get_graph())

g.write_graph('demo-entity-relation.graphml')
