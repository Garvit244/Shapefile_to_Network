from shapely.geometry import shape
from shapely.ops import unary_union
import fiona
import networkx as nx
import itertools
from haversine import haversine
from GraphSimplify import simplify_graph
from MultiDiGraphConvertor import convert_MultiDi_to_Simple
from BufferedGraph import *

'''
    @input:     The path of the shapefile which need to be converted to network
    @output:    Returns the MultiDigraph created from the shapefile

    This function read the shapefile of the road network and convert it into graph by iterating through the lat, lon
    from the shapefile.
'''


def shape_convertor(path):
    geoms = [shape(feature['geometry']) for feature in fiona.open(path)]
    res = unary_union(geoms)
    G = nx.MultiDiGraph()
    for line in res:
        for seg_start, seg_end in itertools.izip(list(line.coords), list(line.coords)[1:]):
            start = (round(seg_start[1], 6), round(seg_start[0], 6))
            end = (round(seg_end[1], 6), round(seg_end[0], 6))
            G.add_edge(start, end, weight=haversine(start, end))
    return G


'''
    @input:     The Graph and the path

    This function read the Graph, iterate over the list of nodes in the graph and save it into file defined by path
'''


def create_vertex_file(g, path):
    vertex = g.nodes
    output = open(path, 'w')
    output.write('Unique Id; Longitude; Latitude\n')

    count = 1
    for v in vertex:
        output.write(str(count) + ';' + str(round(v[0], 6)) + ';' + str(round(v[1], 6)) + '\n')
        count += 1


'''
    @input:     The Graph and directory

    This function writes the graph in form of shape file to the given directory
'''


def create_edges_vertex_shape(g, folder):
    nx.write_shp(g, folder)


'''
    @input:     The Graph and the path

    This function iterate over the edges of the graph and write it into the file defined by the path
'''


def create_edges_file(g, file_name):
    output = open(file_name, 'w')
    output.write('Starting Coordinate; End Coordinate; True Distance(km) \n')

    for edge in g.edges:
        distance = g.get_edge_data(edge[0], edge[1])[0]['weight']
        start_coor = [round(elem, 6) for elem in list(edge[0])]
        end_coor = [round(elem, 6) for elem in list(edge[1])]
        output.write(str(start_coor) + ';' + str(end_coor) + ';' + str(distance) + '\n')


'''
    @input:     path of the shape file and the output for saving clean network
    @output:    Cleaned network

    This function read the input shape file and conver it into network for cleaning. After converting it simplify the
    graph by calling simplify_graph() and write the cleaned network in form of shapefiles
'''


def graph_convertor(input_file, output_dir):
    G = shape_convertor(input_file)
    new_G = simplify_graph(G)

    create_vertex_file(new_G, output_dir + '/vertex.csv')
    create_edges_file(new_G, output_dir + '/edges.csv')

    new_simple_graph = convert_MultiDi_to_Simple(new_G)
    create_edges_vertex_shape(new_simple_graph, output_dir + '/New Shape/')

    return new_G
