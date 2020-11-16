import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

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
                 border_color="#000000", border_type="line", border_width="1.0", height=False,
                 width=False, x=False, y=False):

        self.label = label
        if label is None:
            self.label = group_id

        self.parent = None
        self.group_id = group_id
        self.nodes = {}
        self.groups = {}
        self.parent_graph = parent_graph
        self.edges = {}
        self.num_edges = 0

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

        self.border_color = border_color
        self.border_width = border_width

        if border_type not in line_types:
            raise RuntimeWarning("Border type %s not recognised" % border_type)

        self.border_type = border_type

    def add_node(self, node_name, **kwargs):
        if node_name in self.parent_graph.existing_entities:
            raise RuntimeWarning("Node %s already exists" % node_name)

        node = Node(node_name, **kwargs)
        node.parent = self
        self.nodes[node_name] = node
        self.parent_graph.existing_entities[node_name] = node
        return node

    def add_group(self, group_id, **kwargs):
        if group_id in self.parent_graph.existing_entities:
            raise RuntimeWarning("Node %s already exists" % group_id)

        group = Group(group_id, self.parent_graph, **kwargs)
        group.parent = self
        self.groups[group_id] = group
        self.parent_graph.existing_entities[group_id] = group
        return group

    def is_ancestor(self, node):
        return node.parent is not None and (
            node.parent is self or self.is_ancestor(node.parent))

    def add_edge(self,  node1_name, node2_name, **kwargs):
        # pass node names, not actual node objects

        node1 = self.parent_graph.existing_entities.get(node1_name) or \
            self.add_node(node1_name)

        node2 = self.parent_graph.existing_entities.get(node2_name) or \
            self.add_node(node2_name)

        # http://graphml.graphdrawing.org/primer/graphml-primer.html#Nested
        # The edges between two nodes in a nested graph have to be declared in a graph,
        # which is an ancestor of both nodes in the hierarchy.

        if not (self.is_ancestor(node1) and self.is_ancestor(node2)):
            raise RuntimeWarning("Group %s is not ancestor of both %s and %s" % (self.group_id, node1_name, node2_name))

        self.parent_graph.num_edges += 1
        kwargs['edge_id'] = str(self.parent_graph.num_edges)
        edge = Edge(node1_name, node2_name, **kwargs)
        self.edges[edge.edge_id] = edge
        return edge

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

        ET.SubElement(group_node, "y:BorderStyle", color=self.border_color,
                      type=self.border_type, width=self.border_width)

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

        for group_id in self.groups:
            n = self.groups[group_id].convert()
            graph.append(n)

        for edge_id in self.edges:
            e = self.edges[edge_id].convert()
            graph.append(e)

        return node
        # ProxyAutoBoundsNode crap just draws bar at top of group


class Node:
    def __init__(self, node_name, label=None, label_alignment="center", shape="rectangle", font_family="Dialog",
                 underlined_text="false", font_style="plain", font_size="12",
                 shape_fill="#FF0000", transparent="false", border_color="#000000",
                 border_type="line", border_width="1.0", height=False, width=False, x=False,
                 y=False, node_type="ShapeNode", UML=False):

        self.label = label
        if label is None:
            self.label = node_name

        self.node_name = node_name

        self.node_type = node_type
        self.UML = UML

        self.parent = None

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

        # border options
        self.border_color = border_color
        self.border_width = border_width

        if border_type not in line_types:
            raise RuntimeWarning("Border type %s not recognised" % border_type)

        self.border_type = border_type

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

        ET.SubElement(shape, "y:BorderStyle", color=self.border_color, type=self.border_type,
                      width=self.border_width)

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
                 color="#000000", line_type="line", width="1.0", edge_id="",
                 label_background_color="", label_border_color="",
                 source_label=None, target_label=None):
        self.node1 = node1
        self.node2 = node2

        if not edge_id:
            edge_id = "%s_%s" % (node1, node2)
        self.edge_id = str(edge_id)

        self.label = label
        self.source_label = source_label
        self.target_label = target_label

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

        self.label_background_color = label_background_color
        self.label_border_color = label_border_color

    def convert(self):
        edge = ET.Element("edge", id=str(self.edge_id), source=str(self.node1), target=str(self.node2))
        data = ET.SubElement(edge, "data", key="data_edge")
        pl = ET.SubElement(data, "y:PolyLineEdge")

        ET.SubElement(pl, "y:Arrows", source=self.arrowfoot, target=self.arrowhead)
        ET.SubElement(pl, "y:LineStyle", color=self.color, type=self.line_type,
                      width=self.width)

        label_color_args = {}
        if self.label_background_color:
            label_color_args["backgroundColor"] = self.label_background_color
        if self.label_border_color:
            label_color_args["lineColor"] = self.label_border_color

        if self.label:
            ET.SubElement(pl, "y:EdgeLabel", **label_color_args).text = self.label

        if self.source_label:
            ET.SubElement(pl, "y:EdgeLabel", modelName="six_pos", modelPosition="shead",
                          preferredPlacement="source_on_edge", **label_color_args).text = self.source_label

        if self.target_label:
            ET.SubElement(pl, "y:EdgeLabel", modelName="six_pos", modelPosition="ttail",
                          preferredPlacement="target_on_edge", **label_color_args).text = self.target_label

        return edge


class Graph:
    def __init__(self, directed="directed", graph_id="G"):

        self.nodes = {}
        self.edges = {}
        self.num_edges = 0

        self.directed = directed
        self.graph_id = graph_id
        self.existing_entities = {self.graph_id: self}

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

        for node in self.nodes.values():
            graph.append(node.convert())


        for node in self.groups.values():
            graph.append(node.convert())

        for edge in self.edges.values():
            graph.append(edge.convert())

        self.graphml = graphml

    def write_graph(self, filename, pretty_print=False):
        self.construct_graphml()

        if pretty_print:
            raw_str = ET.tostring(self.graphml)
            pretty_str = minidom.parseString(raw_str).toprettyxml()
            with open(filename, 'w') as f:
                f.write(pretty_str)
        else:
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
        if node_name in self.existing_entities:
            raise RuntimeWarning("Node %s already exists" % node_name)

        node = Node(node_name, **kwargs)
        self.nodes[node_name]  = node
        self.existing_entities[node_name] = node
        return node

    def add_edge(self,  node1_name, node2_name, **kwargs):
        # pass node names, not actual node objects

        node1 = self.existing_entities.get(node1_name) or \
            self.add_node(node1_name)

        node2 = self.existing_entities.get(node2_name) or \
            self.add_node(node2_name)

        self.num_edges += 1
        kwargs['edge_id'] = str(self.num_edges)
        edge = Edge(node1_name, node2_name, **kwargs)
        self.edges[edge.edge_id] = edge
        return edge

    def add_group(self, group_id, **kwargs):
        if group_id in self.existing_entities:
            raise RuntimeWarning("Node %s already exists" % group_id)

        group = Group(group_id, self, **kwargs)
        self.groups[group_id] = group
        self.existing_entities[group_id] = group
        return group
