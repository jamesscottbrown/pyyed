"""
About: Demo script for using networkx for layout of a graph.
Version: 0.1
yEd Version: 3.23.1
python Version: 3.12.0
Date: 19 Dec 2023
"""

import pyyed
import networkx

g = pyyed.Graph(directed="undirected")

# Create Nodes
g.add_node("Ambridge")
g.add_node("Borchester")
g.add_node("Felpersham")
g.add_node("Meyruelle")
g.add_node("Penny Hassett")
g.add_node("Loxley Barrett")
g.add_node("Darrington")
g.add_node("Hollerton")

# Create Edges
g.add_edge("Ambridge", "Meyruelle")
g.add_edge("Ambridge", "Felpersham")
g.add_edge("Felpersham", "Borchester")
g.add_edge("Penny Hassett","Felpersham")
g.add_edge("Loxley Barrett","Borchester")
g.add_edge("Darrington", "Borchester")
g.add_edge("Hollerton", "Borchester")
g.add_edge("Ambridge", "Darrington")
g.add_edge("Penny Hassett", "Borchester")

# Layout graph
pyyed.layout_graph(g, lambda G: networkx.spring_layout(G, scale=300))

# Write Graph
g.write_graph('demo-layout.graphml', pretty_print=True)

print(40 * "=")
print("""
DONE!

The yEd graph Editor has powerfull layout algorithms, but it gets cumbersome
to always start a yEd session with everything stacked on a single point.

Open the file in yEd now.

Verify that the nodes are not on top of each other.
""")
print(40 * "=")
print("")
