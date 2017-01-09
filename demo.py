from pyyed import *

g = Graph()

g.add_node('foo', font_family="Zapfino")
g.add_node('foo2', shape="roundrectangle", font_style="bolditalic", underlined_text="true")

g.add_edge('foo1', 'foo2')
g.add_node('abc', font_size="72", height="100")

g.add_node('bar', label="Multi\nline\ntext")
g.add_node('foobar', label="""Multi
Line
Text!""")

print g.get_graph()