
from shapely.geometry import shape
from shapely.ops import unary_union
import fiona
import networkx as nx
import itertools
from haversine import haversine
from GraphSimplify import simplify_graph
from MultiDiGraphConvertor import convert_MultiDi_to_Simple
from BufferedGraph import *

def shape_convertor(path):
    geoms =[shape(feature['geometry']) for feature in fiona.open(path)]
    res = unary_union(geoms)
    G = nx.MultiDiGraph()
    for line in res:
        for seg_start, seg_end in itertools.izip(list(line.coords),list(line.coords)[1:]):
            start = (round(seg_start[1], 6), round(seg_start[0], 6))
            end = (round(seg_end[1], 6), round(seg_end[0], 6))
            G.add_edge(start, end, weight=haversine(start, end))
    return G

def create_vertex_file(G, folder):
    vertex = (G.nodes)
    output = open(folder, 'w')
    output.write('Unique Id; Longitute; Latitute\n')

    count = 1
    for v in vertex:
        output.write(str(count) + ';'+ str(round(v[0], 6)) + ';' + str(round(v[1], 6)) + '\n')
        count += 1

def create_edges_vertex_shape(G, folder):
    nx.write_shp(G, folder )

def create_edges_file(G, file_name):
    output = open(file_name, 'w')
    output.write('Starting Coordinate; End Coordinate; True Distance(km) \n')

    for edge in G.edges:
        distance = G.get_edge_data(edge[0], edge[1])[0]['weight']
        start_coor =  [round(elem, 6) for elem in list(edge[0])]
        end_coor =  [round(elem, 6) for elem in list(edge[1]) ]
        output.write(str(start_coor) + ';' + str(end_coor) + ';' + str(distance) + '\n')

def graph_convertor(input_file, output_dir):
    G = shape_convertor(input_file)
    new_G = simplify_graph(G)

    create_vertex_file(new_G, output_dir + '/vertex.csv')
    create_edges_file(new_G, output_dir + '/edges.csv')

    new_simple_graph = convert_MultiDi_to_Simple(new_G)
    create_edges_vertex_shape(new_simple_graph, output_dir + '/New Shape/')

    return new_G