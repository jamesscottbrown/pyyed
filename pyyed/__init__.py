import sys
import xml.etree.cElementTree as ET

node_shapes = ["rectangle", "rectangle3d", "roundrectangle", "diamond", "ellipse",
               "fatarrow", "fatarrow2", "hexagon", "octagon", "parallelogram",
               "parallelogram2", "star5", "star6", "star6", "star8", "trapezoid",
               "trapezoid2", "triangle", "trapezoid2", "triangle"]

line_types = ["line", "dashed", "dotted", "dashed_dotted"]
font_styles = ["plain", "bold", "italic", "bolditalic"]

label_alignments = ['left', 'center', 'right']

arrow_types = ["none", "standard", "white_delta", "diamond", "white_diamond", "short",
               "plain", "concave", "convex", "circle", "transparent_circle", "dash",
               "skewed_dash", "t_shape", "crows_foot_one_mandatory",
               "crows_foot_many_mandatory", "crows_foot_many_optional", "crows_foot_one",
               "crows_foot_many", "crows_foot_optional"]


class Group:
    def __init__(self, group_id, parent_graph, label=None, label_alignment="center", shape="rectangle",
                 closed="false", font_family="Dialog", underlined_text="false",
                 font_style="plain", font_size="12", fill="#FFCC00", transparent="false",
                 edge_color="#000000", edge_type="line", edge_width="1.0", height=False,
                 width=False, x=False, y=False):

        self.label = label
        if label is None:
            self.label = group_id

        self.group_id = group_id
        self.nodes = {}
        self.parent_graph = parent_graph

        # node shape
        if shape not in node_shapes:
            raise RuntimeWarning("Node shape %s not recognised" % shape)
        self.shape = shape

        self.closed = closed

        # label formatting options
        self.font_family = font_family
        self.underlined_text = underlined_text

        if font_style not in font_styles:
            raise RuntimeWarning("Font style %s not recognised" % font_style)

        if label_alignment not in label_alignments:
            raise RuntimeWarning("Label alignment %s not recognised" % label_alignment)

        self.font_style = font_style
        self.font_size = font_size

        self.label_alignment = label_alignment

        self.fill = fill
        self.transparent = transparent

        self.geom = {}
        if height:
            self.geom["height"] = height
        if width:
            self.geom["width"] = width
        if x:
            self.geom["x"] = x
        if y:
            self.geom["y"] = y

        self.edge_color = edge_color
        self.edge_width = edge_width

        if edge_type not in line_types:
            raise RuntimeWarning("Edge type %s not recognised" % edge_type)

        self.edge_type = edge_type

    def add_node(self, node_name, **kwargs):
        if node_name in self.nodes.keys():
            raise RuntimeWarning("Node %s already exists" % node_name)

        self.nodes[node_name] = Node(node_name, **kwargs)
        self.parent_graph.nodes_in_groups.append(node_name)

    def convert(self):
        node = ET.Element("node", id=self.group_id)
        node.set("yfiles.foldertype", "group")
        data = ET.SubElement(node, "data", key="data_node")

        # node for group
        pabn = ET.SubElement(data, "y:ProxyAutoBoundsNode")
        r = ET.SubElement(pabn, "y:Realizers", active="0")
        group_node = ET.SubElement(r, "y:GroupNode")

        if self.geom:
            ET.SubElement(group_node, "y:Geometry", **self.geom)

        ET.SubElement(group_node, "y:Fill", color=self.fill, transparent=self.transparent)

        ET.SubElement(group_node, "y:BorderStyle", color=self.edge_color,
                      type=self.edge_type, width=self.edge_width)

        label = ET.SubElement(group_node, "y:NodeLabel", modelName="internal",
                              modelPosition="t",
                              fontFamily=self.font_family, fontSize=self.font_size,
                              underlinedText=self.underlined_text,
                              fontStyle=self.font_style,
                              alignment=self.label_alignment)
        label.text = self.label

        ET.SubElement(group_node, "y:Shape", type=self.shape)

        ET.SubElement(group_node, "y:State", closed=self.closed)

        graph = ET.SubElement(node, "graph", edgedefault="directed", id=self.group_id)

        for node_id in self.nodes:
            n = self.nodes[node_id].convert()
            graph.append(n)

        return node
        # ProxyAutoBoundsNode crap just draws bar at top of group


class Node:
    def __init__(self, node_name, label=None, label_alignment="center", shape="rectangle", font_family="Dialog",
                 underlined_text="false", font_style="plain", font_size="12",
                 shape_fill="#FF0000", transparent="false", edge_color="#000000",
                 edge_type="line", edge_width="1.0", height=False, width=False, x=False,
                 y=False, node_type="ShapeNode", UML=False):

        self.label = label
        if label is None:
            self.label = node_name

        self.node_name = node_name

        self.node_type = node_type
        self.UML = UML

        # node shape
        if shape not in node_shapes:
            raise RuntimeWarning("Node shape %s not recognised" % shape)

        self.shape = shape

        # label formatting options
        self.font_family = font_family
        self.underlined_text = underlined_text

        if font_style not in font_styles:
            raise RuntimeWarning("Font style %s not recognised" % font_style)

        if label_alignment not in label_alignments:
            raise RuntimeWarning("Label alignment %s not recognised" % label_alignment)

        self.font_style = font_style
        self.font_size = font_size

        self.label_alignment = label_alignment

        # shape fill
        self.shape_fill = shape_fill
        self.transparent = transparent

        # edge options
        self.edge_color = edge_color
        self.edge_width = edge_width

        if edge_type not in line_types:
            raise RuntimeWarning("Edge type %s not recognised" % edge_type)

        self.edge_type = edge_type

        # geometry
        self.geom = {}
        if height:
            self.geom["height"] = height
        if width:
            self.geom["width"] = width
        if x:
            self.geom["x"] = x
        if y:
            self.geom["y"] = y

    def convert(self):

        node = ET.Element("node", id=str(self.node_name))
        data = ET.SubElement(node, "data", key="data_node")
        shape = ET.SubElement(data, "y:" + self.node_type)

        if self.geom:
            ET.SubElement(shape, "y:Geometry", **self.geom)
        # <y:Geometry height="30.0" width="30.0" x="475.0" y="727.0"/>

        ET.SubElement(shape, "y:Fill", color=self.shape_fill,
                      transparent=self.transparent)

        ET.SubElement(shape, "y:BorderStyle", color=self.edge_color, type=self.edge_type,
                      width=self.edge_width)

        label = ET.SubElement(shape, "y:NodeLabel", fontFamily=self.font_family,
                              fontSize=self.font_size,
                              underlinedText=self.underlined_text,
                              fontStyle=self.font_style,
                              alignment=self.label_alignment)
        label.text = self.label

        ET.SubElement(shape, "y:Shape", type=self.shape)

        if self.UML:
            UML = ET.SubElement(shape, "y:UML")  

            attributes = ET.SubElement(UML, "y:AttributeLabel", type=self.shape)  
            attributes.text = self.UML["attributes"]

            methods = ET.SubElement(UML, "y:MethodLabel", type=self.shape)  
            methods.text = self.UML["methods"]

            stereotype = self.UML["stereotype"] if "stereotype" in self.UML else ""
            UML.set("stereotype", stereotype)

        return node


class Edge:
    def __init__(self, node1, node2, label="", arrowhead="standard", arrowfoot="none",
                 color="#000000", line_type="line", width="1.0"):
        self.node1 = node1
        self.node2 = node2
        self.edge_id = "%s_%s" % (node1, node2)

        self.label = label

        if arrowhead not in arrow_types:
            raise RuntimeWarning("Arrowhead type %s not recognised" % arrowhead)

        self.arrowhead = arrowhead

        if arrowfoot not in arrow_types:
            raise RuntimeWarning("Arrowfoot type %s not recognised" % arrowfoot)

        self.arrowfoot = arrowfoot

        if line_type not in line_types:
            raise RuntimeWarning("Line type %s not recognised" % line_type)

        self.line_type = line_type

        self.color = color
        self.width = width

    def convert(self):
        edge = ET.Element("edge", id=str(self.edge_id), source=str(self.node1), target=str(self.node2))
        data = ET.SubElement(edge, "data", key="data_edge")
        pl = ET.SubElement(data, "y:PolyLineEdge")

        ET.SubElement(pl, "y:Arrows", source=self.arrowfoot, target=self.arrowhead)
        ET.SubElement(pl, "y:LineStyle", color=self.color, type=self.line_type,
                      width=self.width)

        if self.label:
            ET.SubElement(pl, "y:EdgeLabel").text = self.label

        return edge


class Graph:
    def __init__(self, directed="directed", graph_id="G"):

        self.nodes_in_groups = []
        self.nodes = {}
        self.edges = {}

        self.directed = directed
        self.graph_id = graph_id

        self.groups = {}

        self.graphml = ""

    def construct_graphml(self):
        # xml = ET.Element("?xml", version="1.0", encoding="UTF-8", standalone="no")

        graphml = ET.Element("graphml", xmlns="http://graphml.graphdrawing.org/xmlns")
        graphml.set("xmlns:java", "http://www.yworks.com/xml/yfiles-common/1.0/java")
        graphml.set("xmlns:sys",
                    "http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0")
        graphml.set("xmlns:x", "http://www.yworks.com/xml/yfiles-common/markup/2.0")
        graphml.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        graphml.set("xmlns:y", "http://www.yworks.com/xml/graphml")
        graphml.set("xmlns:yed", "http://www.yworks.com/xml/yed/3")
        graphml.set("xsi:schemaLocation",
                    "http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd")

        node_key = ET.SubElement(graphml, "key", id="data_node")
        node_key.set("for", "node")
        node_key.set("yfiles.type", "nodegraphics")

        edge_key = ET.SubElement(graphml, "key", id="data_edge")
        edge_key.set("for", "edge")
        edge_key.set("yfiles.type", "edgegraphics")

        graph = ET.SubElement(graphml, "graph", edgedefault=self.directed,
                              id=self.graph_id)

        for node_id in self.nodes:
            node = self.nodes[node_id].convert()
            graph.append(node)

        for group_id in self.groups:
            node = self.groups[group_id].convert()
            graph.append(node)

        for edge_id in self.edges:
            edge = self.edges[edge_id].convert()
            graph.append(edge)

        self.graphml = graphml

    def write_graph(self, filename):
        self.construct_graphml()
        tree = ET.ElementTree(self.graphml)
        tree.write(filename)

    def get_graph(self):
        self.construct_graphml()
        # Py2/3 sigh.
        if sys.version_info.major < 3:
            return ET.tostring(self.graphml, encoding='UTF-8')
        else:
            return ET.tostring(self.graphml, encoding='UTF-8').decode()

    def add_node(self, node_name, **kwargs):
        if node_name in self.nodes.keys():
            raise RuntimeWarning("Node %s already exists" % node_name)

        self.nodes[node_name] = Node(node_name, **kwargs)

    def add_edge(self, node1, node2, label="", arrowhead="standard", arrowfoot="none",
                 color="#000000", line_type="line",
                 width="1.0"):
        # pass node names, not actual node objects

        existing_entities = self.nodes_in_groups
        existing_entities.extend(self.nodes.keys())
        existing_entities.extend(self.groups.keys())

        if node1 not in existing_entities:
            self.nodes[node1] = Node(node1)

        if node2 not in existing_entities:
            self.nodes[node2] = Node(node2)

        edge = Edge(node1, node2, label, arrowhead, arrowfoot, color, line_type, width)
        self.edges[edge.edge_id] = edge

    def add_group(self, group_id, **kwargs):
        self.groups[group_id] = Group(group_id, self, **kwargs)
        return self.groups[group_id]
