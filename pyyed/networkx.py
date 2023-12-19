# Functions to exchange data with networkx

from . import Graph
import networkx

def to_networkx(graph: Graph) -> networkx.Graph:
    '''Convert a pyyed graph to a networkx graph.'''
    # TODO: Autodetect if graph has multi-edges
    match graph.directed:
        case 'directed':
            nx_graph = networkx.DiGraph()
        case 'undirected':
            nx_graph = networkx.Graph()
        case _:
            raise NotImplementedError(f'pyyed graph type "{graph.directed}" is not supported')
    
    # Transfer network structure, but not attributes
    nx_graph.add_nodes_from(graph.nodes.keys())
    nx_graph.add_edges_from([(e.node1, e.node2)
                             for e in graph.edges.values()])

    return nx_graph

def from_networkx(nx_graph: networkx.Graph, update=None) -> Graph:
    '''Convert a networkx graph to a pyyed graph.

    :param update:  If proviede, this pyyed.graph is updated with layout information, instead of creating a new pyyed.graph.
    :returns:  A pyyed graph corresponding to the networkx graph.
    '''
    raise NotImplementedError()
