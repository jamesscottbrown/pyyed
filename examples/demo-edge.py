import pyyed

g = pyyed.Graph()

g.add_node('foo', font_family="Zapfino",x=0,y="50",width=100)
n2=g.add_node('foo2', shape="roundrectangle", font_style="bolditalic",
           underlined_text="true",x="100",y="100",width='100',shape_fill='#ffff00')
n3=g.add_node('n3', shape="roundrectangle", font_style="bolditalic",
           underlined_text="true",x="300",y=300,width='100',shape_fill='#ff0000')


#get first node
n1=g.nodes['foo']
geom1=n1.geom
w1=float(geom1['width'])
#x1=float(geom1['x'])
x1=0
y1=float(geom1['y'])


#add edge simple
g.add_edge('n3', 'foo2',color='#ff0000')
g.add_edge('foo', 'foo2',sx=50,sy=5,color='#3366ff')

#add edge with one point
geom2=n2.geom
w2=float(geom2['width'])
x2=float(geom2['x'])
y2=float(geom2['y'])
paras={"sx": "0",
  "sy": "0.7",
  "tx": str(-w1/2),
  "ty":0,
  'points':((-w1/2+x1,y2)),
  'color':'#3366ff'}
g.add_edge('foo2', 'foo',**paras)

#add egdge with two points
g.add_edge('n3', 'foo',sx=10,sy=2,tx=3,ty=9,points=((400,300),(400,50)),arrowhead="diamond", arrowfoot="circle")

#print(g.get_graph())

    
# Write the graph to a GraphML file
filename="examples/demo-edge.graphml"
with open(filename, "w") as f:
    f.write(g.get_graph())
# Write the graph to a Xml file
with open('examples/demo-edge.xml', "w") as f:
    f.write(g.get_graph())
print(f"Graph has been saved as {filename}")
