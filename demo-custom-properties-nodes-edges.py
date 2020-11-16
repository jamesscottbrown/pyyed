'''
About: Demo script for utilising the pyyed "Adding Custom Properties for Node and Edge objects" feature.
Version: 0.1
yEd Version: 3.20
python Version: 3.4.3
Author: bockor
Date: 16 Nov 2020
'''

import pyyed_custom_props

g=pyyed_custom_props.Graph()

#Define Node Custom Properties
'''
scope: node
name: name of the custom property
property_type: [string|boolean|int|double]
                boolean: Java keywords [true|false]
default_value: any above datatype represented as a string
'''
g.define_custom_property("node","Population", "int", "0")
g.define_custom_property("node","Unemployment", "double", "0.0")
g.define_custom_property("node","Environmental Engagements", "boolean", "false")
g.define_custom_property("node","Mayor","string", "")

#Define Edge Custom Properties
'''
scope: edge
name: name of the custom property
property_type: [string|boolean|int|double]
                boolean: Java keywords [true|false]
default_value: any above datatype represented as a string
'''
g.define_custom_property("edge","Distance","int", "0")
g.define_custom_property("edge","Availability","double", "100.0")
g.define_custom_property("edge","Toll Free","boolean", "true")
g.define_custom_property("edge","Year of build","string", "")

#Create Nodes
g.add_node('Pasta City', custom_properties={"Population": "13000","Unemployment": "13.7","Environmental Engagements": "true","Mayor" : "Genarro"})
g.add_node('Wurst Stadt', custom_properties={"Population": "25100","Unemployment": "6.2","Mayor" : "Orlowsky"})
g.add_node('Gruyereville', custom_properties={"Population": "29650","Unemployment": "11.8","Environmental Engagements": "true","Mayor" : "Delage"})

#Create Edges
g.add_edge("Pasta City", "Wurst Stadt", label='N666', arrowhead="none", custom_properties={"Year of build": "1974","Distance": "356","Toll Free": "false","Availability": "85.7"})
g.add_edge("Pasta City", "Gruyereville", label='E55', arrowhead="none", custom_properties={"Year of build": "1986","Distance": "1444","Availability": "96.7"})
g.add_edge("Gruyereville", "Wurst Stadt", label='E23', arrowhead="none", custom_properties={"Year of build": "2011","Distance": "740","Toll Free": "false"})

#Write Graph
g.write_graph('intercities.graphml', pretty_print=True)

print(40 * "=")
print("DONE!")
print("")
print("Open the file in yEd now. Click on the nodes and the edges, press F6 and select the 'data' tab to view the custom properties")
print("")
print("Node Custom Properties will show up into the yEd 'Structure View Window'")
print("")
print("All Custom Properties definitions should be populated into the 'Manage Custom Properties Menu'")
print("")
print("To select Nodes & Edges based on Custom Properties open yEd 'Tools Menu' -> 'Select Elements' and define criteria in the 'Nodes' and 'Edges' tabs") 
print(40 * "=")
print("")
