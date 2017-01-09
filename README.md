# yEd Py

A simple Python API to export Networks to [yEd](http://www.yworks.com/en/products_yed_about.html)

A previous project of mine produced diagrams by exporting DOT for GraphViz to render. 
Someone suggested it would be useful to produce diagrams that could be further manipulated and edited, and that their preferred tool would be yEd.

The main file format supported by yEd is [GraphML](http://graphml.graphdrawing.org/) ([GraphML Primer](http://graphml.graphdrawing.org/primer/graphml-primer.html)). 
This is an open standard based on XML, and is supported by Python libraries such as [NetworkX](https://networkx.github.io/).
However, the details of formatting (rather than network topology) are handled by yEd specific extensions to the standard, which are not supported by other libraries.
 
I therefore wrote this library to provide an easy interface that lets you specify how a graph should look, and generates the corresponding yEd graphml file.

## Usage
The interface is similar to that of NetworkX:

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
    
