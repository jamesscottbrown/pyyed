from __future__ import print_function
import pyyed

g = pyyed.Graph()
g.add_node('Car', shape_fill="#EEEEEE",
           node_type="UMLClassNode",
           UML={"attributes": "Model\nManufacturer\nPrice",
                "methods": "getModel()\ngetManufacturer()\ngetPrice()\nsetPrice()"})

g.add_node('ICar', shape_fill="#EEEEEE",
           node_type="UMLClassNode",
           UML={"stereotype": "interface",
                "attributes": "",
                "methods": "getModel()\ngetManufacturer()\ngetPrice()\nsetPrice()"})

g.add_node('Vehicle', shape_fill="#EEEEEE", node_type="UMLClassNode")
g.add_edge('Car', 'Vehicle', arrowhead="white_delta")
g.add_edge('Car', 'ICar', arrowhead="white_delta", line_type="dashed")


g.add_node('This is a note', shape_fill="#EEEEEE", node_type="UMLNoteNode")

# print(g.get_graph())

g.write_graph('demo-uml.graphml')
