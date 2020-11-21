import pyyed

g = pyyed.Graph()

n0 = g.add_node("node0")
group1 = g.add_group("main1")
n11 = group1.add_node("node11")
group12 = group1.add_group("sub12")
n121 = group12.add_node("node121")
group122 = group12.add_group("sub122")

g.write_graph('test.2.graphml')
