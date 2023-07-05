import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Shared parameters
line_types = ["line", "dashed", "dotted", "dashed_dotted"]
font_styles = ["plain", "bold", "italic", "bolditalic"]
horizontal_alignments = ['left', 'center', 'right']
vertical_alignments = ['top', 'center', 'bottom']
custom_property_scopes = ["node", "edge"]
custom_property_types = ["string", "int", "double", "boolean"]

def checkValue(parameter_name, value, validValues = None):
    if validValues is not None:
        if value not in validValues:
            raise ValueError("%s '%s' is not supported. Use: '%s'" % (parameter_name, value, "', '".join(validValues)) )

class Label:
    graphML_tagName = None

    def __init__(self, text, height="18.1328125", width= None, 
                    alignment="center",
                    font_family="Dialog", 
                    font_size="12", 
                    font_style="plain",
                    horizontalTextPosition="center",
                    underlined_text = "false",
                    text_color="#000000", 
                    icon_text_gap="4", 
                    horizontal_text_position="center", 
                    vertical_text_position="center", 
                    visible="true",  
                    border_color = None,
                    background_color = None, 
                    has_background_color="false"):  

        #make class abstract
        if type(self) is Label:
            raise Exception('Label is an abstract class and cannot be instantiated directly')

        self._text = text 

        # Initialize dictionary for parameters
        self._params = {}        
        self.updateParam("horizontalTextPosition", horizontal_text_position, horizontal_alignments)
        self.updateParam("verticalTextPosition", vertical_text_position, vertical_alignments)
        self.updateParam("alignment", alignment, horizontal_alignments)
        self.updateParam("fontStyle", font_style, font_styles)


        #TODO: Implement range checks
        self.updateParam("fontFamily", font_family)
        self.updateParam("iconTextGap", icon_text_gap)
        self.updateParam("fontSize", font_size)
        self.updateParam("textColor", text_color)
        self.updateParam("visible", visible.lower(), ["true", "false"])
        self.updateParam("underlinedText" ,underlined_text.lower(), ["true", "false"])
        if background_color:
            has_background_color = "true"
        self.updateParam("hasBackgroundColor", has_background_color.lower(), ["true", "false"])
        self.updateParam("width", width)
        self.updateParam("height", height)
        self.updateParam("borderColor", border_color)
        self.updateParam("backgroundColor", background_color)


    def updateParam(self, parameter_name, value, validValues = None):
        if value is None:
            return False
        checkValue(parameter_name,value,validValues)

        self._params[parameter_name] = value
        return True
    
    def addSubElement(self, shape):
        label = ET.SubElement(shape, self.graphML_tagName, **self._params)
        label.text = self._text

class NodeLabel(Label):
    validModelParams = {
        "internal" : ["t", "b", "c", "l", "r", "tl", "tr", "bl", "br"],
        "corners" : ["nw", "ne", "sw" , "se"],
        "sandwich" : ["n", "s"],
        "sides" : ["n", "e", "s", "w"],
        "eight_pos" : ["n", "e", "s", "w", "nw", "ne", "sw" , "se"]
    }

    graphML_tagName = "y:NodeLabel"

    def __init__(self, text, alignment="center", font_family="Dialog", font_size="12", font_style="plain", height="18.1328125", 
                    horizontalTextPosition="center", underlined_text = "false", icon_text_gap = "4",
                    text_color="#000000", horizontal_text_position="center", vertical_text_position="center", visible="true",  
                    has_background_color="false", width="55.708984375", model_name ="internal", 
                    border_color = None, background_color = None, model_position ="c"):  

        super().__init__(text, height, width, alignment, font_family, font_size, font_style, horizontalTextPosition,
                    underlined_text, text_color, icon_text_gap, horizontal_text_position, vertical_text_position, 
                    visible, border_color, background_color, has_background_color)

        self.updateParam("modelName", model_name, NodeLabel.validModelParams.keys())
        self.updateParam("modelPosition", model_position, NodeLabel.validModelParams[model_name])

class EdgeLabel(Label):

    validModelParams = {
        "two_pos" : ["head","tail"],
        "centered" : ["center"],
        "six_pos" : ["shead", "thead","head","stail", "ttail","tail"],
        "three_center"  : ["center", "scentr", "tcentr"],
        "center_slider" : None,
        "side_slider" : None
    }

    graphML_tagName = "y:EdgeLabel"

    def __init__(self, text, alignment="center", font_family="Dialog", font_size="12", font_style="plain", height="18.1328125", 
                    horizontalTextPosition="center", underlined_text = "false", icon_text_gap = "4",
                    text_color="#000000", horizontal_text_position="center", vertical_text_position="center", visible="true",  
                    has_background_color="false", width="55.708984375", model_name = "centered", model_position = "center",
                    border_color = None, background_color = None, 
                    preferred_placement=None):  
        
        super().__init__(text, height, width, alignment, font_family, font_size, font_style, horizontalTextPosition,
                    underlined_text, text_color, icon_text_gap, horizontal_text_position, vertical_text_position, 
                    visible, border_color, background_color, has_background_color)

        self.updateParam("modelName", model_name, EdgeLabel.validModelParams.keys())
        self.updateParam("modelPosition", model_position, EdgeLabel.validModelParams[model_name])
        self.updateParam("preferredPlacement", preferred_placement)

class CustomPropertyDefinition:

    def __init__(self, scope, name, property_type, default_value):
        """
        scope: [node|edge]
        name: name of the custom property
        property_type: [string|boolean|int|double]
                        boolean: Java keywords [true|false]
        default_value: any above datatype represented as a string
        """
        self.scope = scope
        self.name = name
        self.property_type = property_type
        self.default_value = default_value
        self.id = "%s_%s" % (self.scope, self.name)

    def convert(self):

        custom_prop_key = ET.Element("key", id=self.id)
        custom_prop_key.set("for", self.scope)
        custom_prop_key.set("attr.name", self.name)
        custom_prop_key.set("attr.type", self.property_type)

        return custom_prop_key


class Group:
    validShapes = ["rectangle", "rectangle3d", "roundrectangle", "diamond", "ellipse",
               "fatarrow", "fatarrow2", "hexagon", "octagon", "parallelogram",
               "parallelogram2", "star5", "star6", "star6", "star8", "trapezoid",
               "trapezoid2", "triangle", "trapezoid2", "triangle"]

    def __init__(self, group_id, parent_graph, label=None, label_alignment="center", shape="rectangle",
                 closed="false", font_family="Dialog", underlined_text="false",
                 font_style="plain", font_size="12", fill="#FFCC00", transparent="false",
                 border_color="#000000", border_type="line", border_width="1.0", height=False,
                 width=False, x=False, y=False, custom_properties=None, description="", url="", node_id=None):
        """

        :param group_id:
        :param parent_graph:
        :param label:
        :param label_alignment:
        :param shape:
        :param closed:
        :param font_family:
        :param underlined_text:
        :param font_style:
        :param font_size:
        :param fill:
        :param transparent:
        :param border_color:
        :param border_type:
        :param border_width:
        :param height:
        :param width:
        :param x:
        :param y:
        :param custom_properties:
        :param description:
        :param url:
        :param node_id: If set, will allow a different name than the node_name (to allow duplicates)
        """
        self.label = label
        if label is None:
            self.label = group_id

        self.parent = None
        self.group_id = group_id

        if node_id is not None:
            self.node_id = node_id
        else:
            self.node_id = group_id

        self.nodes = {}
        self.groups = {}
        self.parent_graph = parent_graph
        self.edges = {}
        self.num_edges = 0

        # node shape
        checkValue("shape", shape, Group.validShapes)
        self.shape = shape

        self.closed = closed

        # label formatting options
        self.font_family = font_family
        self.underlined_text = underlined_text
        
        checkValue("font_style", font_style, font_styles)
        self.font_style = font_style
        self.font_size = font_size

        checkValue("label_alignment", label_alignment, horizontal_alignments)
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

        checkValue("border_type",border_type,line_types)
        self.border_type = border_type

        self.description = description
        self.url = url

        # Handle Node Custom Properties
        for name, definition in Node.custom_properties_defs.items():
            if custom_properties:
                for k, v in custom_properties.items():
                    if k not in Node.custom_properties_defs:
                        raise RuntimeWarning("key %s not recognised" % k)
                    if name == k:
                        setattr(self, name, custom_properties[k])
                        break
                else:
                    setattr(self, name, definition.default_value)
            else:
                setattr(self, name, definition.default_value)

    def add_node(self, node_name, **kwargs):
        if self.parent_graph.duplicates:
            node_id = self.parent_graph._next_unique_identifier()
        else:
            if node_name in self.parent_graph.existing_entities:
                raise RuntimeWarning("Node %s already exists" % node_name)
            node_id = node_name

        node = Node(node_name, node_id=node_id, **kwargs)
        node.parent = self
        self.nodes[node_id] = node
        self.parent_graph.existing_entities[node_id] = node
        return node

    def add_group(self, group_id, **kwargs):
        if self.parent_graph.duplicates:
            node_id = self.parent_graph._next_unique_identifier()
        else:
            if group_id in self.parent_graph.existing_entities:
                raise RuntimeWarning("Node %s already exists" % group_id)
            node_id = group_id

        group = Group(group_id, self.parent_graph, node_id=node_id, allow_duplicates=self.duplicates, **kwargs)
        group.parent = self
        self.groups[node_id] = group
        self.parent_graph.existing_entities[node_id] = group
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

    def add_edge_by_obj(self,  node1, node2, **kwargs):
        # pass node names, not actual node objects

        # http://graphml.graphdrawing.org/primer/graphml-primer.html#Nested
        # The edges between two nodes in a nested graph have to be declared in a graph,
        # which is an ancestor of both nodes in the hierarchy.

        if not (self.is_ancestor(node1) and self.is_ancestor(node2)):
            raise RuntimeWarning("Group %s is not ancestor of both %s and %s" % (self.group_id, node1.node_name,
                                                                                 node2.node_name))

        self.parent_graph.num_edges += 1
        kwargs['edge_id'] = str(self.parent_graph.num_edges)
        edge = Edge(node1.node_id, node2.node_id, **kwargs)
        self.edges[edge.edge_id] = edge
        return edge

    def convert(self):
        node = ET.Element("node", id=self.node_id)
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

        if self.url:
            url_node = ET.SubElement(node, "data", key="url_node")
            url_node.text = self.url

        if self.description:
            description_node = ET.SubElement(node, "data", key="description_node")
            description_node.text = self.description

        for node_id in self.nodes:
            n = self.nodes[node_id].convert()
            graph.append(n)

        for group_id in self.groups:
            n = self.groups[group_id].convert()
            graph.append(n)

        for edge_id in self.edges:
            e = self.edges[edge_id].convert()
            graph.append(e)

        # Node Custom Properties
        for name, definition in Node.custom_properties_defs.items():
            node_custom_prop = ET.SubElement(node, "data", key=definition.id)
            node_custom_prop.text = getattr(self, name)

        return node
        # ProxyAutoBoundsNode crap just draws bar at top of group


class Node:

    custom_properties_defs = {}

    validShapes = ["rectangle", "rectangle3d", "roundrectangle", "diamond", "ellipse",
               "fatarrow", "fatarrow2", "hexagon", "octagon", "parallelogram",
               "parallelogram2", "star5", "star6", "star6", "star8", "trapezoid",
               "trapezoid2", "triangle", "trapezoid2", "triangle"]

    def __init__(self, node_name, label=None, label_alignment="center", shape="rectangle", font_family="Dialog",
                 underlined_text="false", font_style="plain", font_size="12",
                 shape_fill="#FF0000", transparent="false", border_color="#000000",
                 border_type="line", border_width="1.0", height=False, width=False, x=False,
                 y=False, node_type="ShapeNode", UML=False,
                 custom_properties=None, description="", url="", node_id=None):
        """

        :param node_name:
        :param label:
        :param label_alignment:
        :param shape:
        :param font_family:
        :param underlined_text:
        :param font_style:
        :param font_size:
        :param shape_fill:
        :param transparent:
        :param border_color:
        :param border_type:
        :param border_width:
        :param height:
        :param width:
        :param x:
        :param y:
        :param node_type:
        :param UML:
        :param custom_properties:
        :param description:
        :param url:
        :param node_id: If set, will allow a different name than the node_name (to allow duplicates)
        """

        self.list_of_labels = []  # initialize list of labels
        if label:
            self.add_label(label, alignment=label_alignment,
                            font_family =  font_family, underlined_text = underlined_text,
                            font_style =  font_style, font_size =  font_size)    
        else:
            self.add_label(node_name, alignment=label_alignment,
                            font_family =  font_family, underlined_text = underlined_text,
                            font_style =  font_style, font_size =  font_size)  

        self.node_name = node_name

        if node_id is not None:
            self.node_id = node_id
        else:
            self.node_id = node_name

        self.node_type = node_type
        self.UML = UML

        self.parent = None

        # node shape
        checkValue("shape", shape, Node.validShapes)
        self.shape = shape
  
        # shape fill
        self.shape_fill = shape_fill
        self.transparent = transparent

        # border options
        self.border_color = border_color
        self.border_width = border_width

        checkValue("border_type", border_type, line_types)
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

        self.description = description
        self.url = url

        # Handle Node Custom Properties
        for name, definition in Node.custom_properties_defs.items():
            if custom_properties:
                for k, v in custom_properties.items():
                    if k not in Node.custom_properties_defs:
                        raise RuntimeWarning("key %s not recognised" % k)
                    if name == k:
                        setattr(self, name, custom_properties[k])
                        break
                else:
                    setattr(self, name, definition.default_value)
            else:
                setattr(self, name, definition.default_value)

    def add_label(self, label_text, **kwargs):
        self.list_of_labels.append(NodeLabel(label_text, **kwargs))
        return self


    def convert(self):

        node = ET.Element("node", id=str(self.node_id))
        data = ET.SubElement(node, "data", key="data_node")
        shape = ET.SubElement(data, "y:" + self.node_type)

        if self.geom:
            ET.SubElement(shape, "y:Geometry", **self.geom)
        # <y:Geometry height="30.0" width="30.0" x="475.0" y="727.0"/>

        ET.SubElement(shape, "y:Fill", color=self.shape_fill,
                      transparent=self.transparent)

        ET.SubElement(shape, "y:BorderStyle", color=self.border_color, type=self.border_type,
                      width=self.border_width)

        for label in self.list_of_labels:
            label.addSubElement(shape)

        ET.SubElement(shape, "y:Shape", type=self.shape)

        if self.UML:
            UML = ET.SubElement(shape, "y:UML", use3DEffect="false")

            attributes = ET.SubElement(UML, "y:AttributeLabel", type=self.shape)
            attributes.text = self.UML["attributes"]

            methods = ET.SubElement(UML, "y:MethodLabel", type=self.shape)
            methods.text = self.UML["methods"]

            stereotype = self.UML["stereotype"] if "stereotype" in self.UML else ""
            UML.set("stereotype", stereotype)

        if self.url:
            url_node = ET.SubElement(node, "data", key="url_node")
            url_node.text = self.url

        if self.description:
            description_node = ET.SubElement(node, "data", key="description_node")
            description_node.text = self.description

        # Node Custom Properties
        for name, definition in Node.custom_properties_defs.items():
            node_custom_prop = ET.SubElement(node, "data", key=definition.id)
            node_custom_prop.text = getattr(self, name)

        return node

    @classmethod
    def set_custom_properties_defs(cls, custom_property):
        cls.custom_properties_defs[custom_property.name] = custom_property


class Edge:
    custom_properties_defs = {}

    arrow_types = ["none", "standard", "white_delta", "diamond", "white_diamond", "short",
               "plain", "concave", "convex", "circle", "transparent_circle", "dash",
               "skewed_dash", "t_shape", "crows_foot_one_mandatory",
               "crows_foot_many_mandatory", "crows_foot_many_optional", "crows_foot_one",
               "crows_foot_many", "crows_foot_optional"]

    def __init__(self, node1, node2, label=None, arrowhead="standard", arrowfoot="none",
                color="#000000", line_type="line", width="1.0", edge_id="",
                label_background_color="", label_border_color="",
                source_label=None, target_label=None,
                custom_properties=None, description="", url=""):
        self.node1 = node1
        self.node2 = node2

        self.list_of_labels = [] # initialize list of labels

        if label:
            self.add_label(label, border_color = label_border_color, background_color = label_background_color)
            
        if not edge_id:
            edge_id = "%s_%s" % (node1, node2)
        self.edge_id = str(edge_id)

        if source_label is not None:
            self.add_label(source_label, model_name="six_pos", model_position="shead", preferred_placement="source_on_edge",
            border_color=label_border_color, background_color = label_background_color)

        if target_label is not None:
            self.add_label(source_label, model_name="six_pos", model_position="shead", preferred_placement="source_on_edge",
            border_color=label_border_color, background_color = label_background_color)


        checkValue("arrowhead", arrowhead, Edge.arrow_types)
        self.arrowhead = arrowhead

        checkValue("arrowfoot", arrowfoot, Edge.arrow_types)
        self.arrowfoot = arrowfoot

        checkValue("line_type", line_type, line_types)
        self.line_type = line_type

        self.color = color
        self.width = width

        self.description = description
        self.url = url

        # Handle Edge Custom Properties
        for name, definition in Edge.custom_properties_defs.items():
            if custom_properties:
                for k, v in custom_properties.items():
                    if k not in Edge.custom_properties_defs:
                        raise RuntimeWarning("key %s not recognised" % k)
                    if name == k:
                        setattr(self, name, custom_properties[k])
                        break
                else:
                    setattr(self, name, definition.default_value)
            else:
                setattr(self, name, definition.default_value)

    def add_label(self, label_text, **kwargs):
        self.list_of_labels.append(EdgeLabel(label_text, **kwargs))
        # Enable method chaining
        return self

    def convert(self):
        edge = ET.Element("edge", id=str(self.edge_id), source=str(self.node1), target=str(self.node2))
        data = ET.SubElement(edge, "data", key="data_edge")
        pl = ET.SubElement(data, "y:PolyLineEdge")

        ET.SubElement(pl, "y:Arrows", source=self.arrowfoot, target=self.arrowhead)
        ET.SubElement(pl, "y:LineStyle", color=self.color, type=self.line_type,
                      width=self.width)

        for label in self.list_of_labels:
            label.addSubElement(pl)
        
        if self.url:
            url_edge = ET.SubElement(edge, "data", key="url_edge")
            url_edge.text = self.url

        if self.description:
            description_edge = ET.SubElement(edge, "data", key="description_edge")
            description_edge.text = self.description

        # Edge Custom Properties
        for name, definition in Edge.custom_properties_defs.items():
            edge_custom_prop = ET.SubElement(edge, "data", key=definition.id)
            edge_custom_prop.text = getattr(self, name)

        return edge
    @classmethod
    def set_custom_properties_defs(cls, custom_property):
        cls.custom_properties_defs[custom_property.name] = custom_property


class Graph:
    def __init__(self, directed="directed", graph_id="G", allow_duplicates=False):
        """

        :param directed:
        :param graph_id:
        :param allow_duplicates: False by default to keep compatibility with past behavior. If True, text in node
        will be different than label to ensure we can add multiple nodes with the same name.
        """

        self.nodes = {}
        self.edges = {}
        self.num_edges = 0
        self.duplicates = allow_duplicates

        # Only used if duplicates = True
        self.num_nodes = 0

        self.directed = directed
        self.graph_id = graph_id
        self.existing_entities = {self.graph_id: self}

        self.groups = {}

        self.custom_properties = []

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

        # Definition: url for Node
        node_key = ET.SubElement(graphml, "key", id="url_node")
        node_key.set("for", "node")
        node_key.set("attr.name", "url")
        node_key.set("attr.type", "string")

        # Definition: description for Node
        node_key = ET.SubElement(graphml, "key", id="description_node")
        node_key.set("for", "node")
        node_key.set("attr.name", "description")
        node_key.set("attr.type", "string")

        # Definition: url for Edge
        node_key = ET.SubElement(graphml, "key", id="url_edge")
        node_key.set("for", "edge")
        node_key.set("attr.name", "url")
        node_key.set("attr.type", "string")

        # Definition: description for Edge
        node_key = ET.SubElement(graphml, "key", id="description_edge")
        node_key.set("for", "edge")
        node_key.set("attr.name", "description")
        node_key.set("attr.type", "string")

        # Definition: Custom Properties for Nodes and Edges
        for prop in self.custom_properties:
            graphml.append(prop.convert())

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

        if self.duplicates:
            node_id = self._next_unique_identifier()
        else:
            if node_name in self.existing_entities:
                raise RuntimeWarning("Node %s already exists" % node_name)
            node_id = node_name

        node = Node(node_name, node_id=node_id, **kwargs)
        self.nodes[node_id] = node
        self.existing_entities[node_id] = node
        return node

    def add_edge(self,  node1_name, node2_name, **kwargs):
        # pass node names, not actual node objects

        self.existing_entities.get(node1_name) or self.add_node(node1_name)
        self.existing_entities.get(node2_name) or self.add_node(node2_name)

        self.num_edges += 1
        kwargs['edge_id'] = str(self.num_edges)
        edge = Edge(node1_name, node2_name, **kwargs)
        self.edges[edge.edge_id] = edge
        return edge

    def add_edge_by_obj(self,  node1, node2, **kwargs):
        # pass node names, not actual node objects


        self.num_edges += 1
        kwargs['edge_id'] = str(self.num_edges)
        edge = Edge(node1.node_id, node2.node_id, **kwargs)
        self.edges[edge.edge_id] = edge
        return edge

    def add_group(self, group_id, **kwargs):
        if self.duplicates:
            node_id = self._next_unique_identifier()
        else:
            if group_id in self.existing_entities:
                raise RuntimeWarning("Node %s already exists" % group_id)
            node_id = group_id

        group = Group(group_id, self, node_id=node_id, **kwargs)
        self.groups[node_id] = group
        self.existing_entities[node_id] = group
        return group

    def define_custom_property(self, scope, name, property_type, default_value):
        if scope not in custom_property_scopes:
            raise RuntimeWarning("Scope %s not recognised" % scope)
        if property_type not in custom_property_types:
            raise RuntimeWarning("Property Type %s not recognised" % property_type)
        if type(default_value) != str:
            raise RuntimeWarning("default_value %s needs to be a string" % default_value)
        custom_property = CustomPropertyDefinition(scope, name, property_type, default_value)
        self.custom_properties.append(custom_property)
        if scope == "node":
            Node.set_custom_properties_defs(custom_property)
        elif scope == "edge":
            Edge.set_custom_properties_defs(custom_property)

    def _next_unique_identifier(self):
        """
        Increment internal counter, then return next identifier not yet used.
        """
        self.num_nodes += 1
        node_id = str(self.num_nodes)

        return node_id