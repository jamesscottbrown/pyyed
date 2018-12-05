from __future__ import print_function
import pyyed

def write_to_file(graph, file_index):
    file_name = "test_graph_%s.graphml" % str(file_index)
    inp = input("\nWould you like to write this data to file: %s? (y/n): " % file_name)
    if "y" in inp.lower():
        file_handle = open(file_name, "w")
        file_handle.write(g.get_graph())
        file_handle.close()
        print("Graph written to %s" % file_name)

g = pyyed.Graph()

g.add_node('foo', font_family="Zapfino")
g.add_node('foo2', shape="roundrectangle", font_style="bolditalic",
           underlined_text="true")

g.add_edge('foo1', 'foo2')
g.add_node('abc', font_size="72", height="100")

g.add_node('bar', label="Multi\nline\ntext")
g.add_node('foobar', label="""Multi
Line
Text!""")

g.add_edge('foo', 'foo1', label="EDGE!", width="3.0", color="#0000FF",
           arrowhead="white_diamond", arrowfoot="standard", line_type="dotted")

print(g.get_graph())
write_to_file(g, 1)

print("\n\n\n")

g = pyyed.Graph()
g.add_node('foo', font_family="Zapfino")

gg = g.add_group("MY_Group", shape="diamond")
gg.add_node('foo2', shape="roundrectangle", font_style="bolditalic",
            underlined_text="true")
gg.add_node('abc', font_size="72", height="100")

g.add_edge('foo2', 'abc')
g.add_edge('foo', 'MY_Group')

print(g.get_graph())
write_to_file(g, 2)


print("\n\n\n")

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

print(g.get_graph())
write_to_file(g, 3)
