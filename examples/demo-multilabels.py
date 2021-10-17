from __future__ import print_function
import pyyed

g = pyyed.Graph()

# Label class is indeed abstract:
#label = pyyed.Label("test")


g.add_node('foo', label='Center', font_family="Zapfino", width="200", height="200", shape_fill="#FFFFFF", border_type="dotted").add_label(
        'Top', model_position="t", font_family="Courier New", font_style="bold"
    ).add_label(
        'Left', model_name = "internal", model_position="l", font_family="Arial", font_style="italic", text_color= "#FF0000"
    ).add_label(
        'Right', model_name = "internal", model_position="r", font_family="Tahoma", font_style="bold",text_color= "#00FF00"
    ).add_label('Bottom', model_name = "internal", model_position="b", text_color= "#0000FF")



g.add_node('foo2', label="foo2", width="100", height="100").add_label(
        'North-West', model_name = "corners", model_position="nw", font_family="Courier New", font_style="bold"
    ).add_label(
        'North-East', model_name = "corners", model_position="ne", font_family="Arial", font_style="italic", text_color= "#FF0000"
    ).add_label(
        'South', model_name = "sides", model_position="s", font_family="Tahoma", font_style="bold",text_color= "#00FF00"
    ).list_of_labels.pop(0)


g.add_edge('foo', 'foo2', width="3.0", color="#0000FF").add_label(
    "Head", model_name = "two_pos", model_position="head", font_family="Courier New", font_style="bold",text_color= "#FF00FF", 
    background_color="#FFFFFF"
).add_label(
    "Tail", model_name = "two_pos", model_position="tail", font_family="Courier New", font_style="bold",
    background_color="#FFFFFF"
).add_label(
    "Center", model_name = "three_center", model_position="center", font_family="Courier New", font_style="bold",
    background_color="#FFFFFF"
)

g.add_edge('foo', 'foo2', width="3.0", color="#0000FF").add_label(
    "Head", model_name = "two_pos", model_position="head", font_family="Courier New", font_style="bold",text_color= "#FF00FF", 
    background_color="#FFFFFF"
).add_label(
    "Tail2", model_name = "two_pos", model_position="tail", font_family="Courier New", font_style="bold",
    background_color="#FFFFFF"
).add_label(
    "Center2", model_name = "three_center", model_position="center", font_family="Courier New", font_style="bold",
    background_color="#FFFFFF"
)

g.write_graph("demo_multilabel.graphml")