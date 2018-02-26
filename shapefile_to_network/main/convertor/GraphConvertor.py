from shapely.geometry import shape
from shapely.ops import unary_union
import fiona
import networkx as nx
import itertools
from haversine import haversine
from GraphSimplify import GraphSimplify
from MultiDiGraphConvertor import MultiDiToSimple

class GraphConvertor:

    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir


    '''
        @input:     The path of the shapefile which need to be converted to network
        @output:    Returns the MultiDigraph created from the shapefile

        This function read the shapefile of the road network and convert it into graph by iterating through the lat, lon
        from the shapefile.
    '''


    def shape_convertor(self):
        geoms = [shape(feature['geometry']) for feature in fiona.open(self.input_file)]
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


    def create_vertex_file(self, g):
        vertex = g.nodes
        output = open(self.output_dir + '/vertex.csv', 'w')
        output.write('Unique Id; Longitude; Latitude\n')

        count = 1
        for v in vertex:
            output.write(str(count) + ';' + str(round(v[0], 6)) + ';' + str(round(v[1], 6)) + '\n')
            count += 1


    '''
        @input:     The Graph and directory

        This function writes the graph in form of shape file to the given directory
    '''


    def create_edges_vertex_shape(self, g):
        nx.write_shp(g, self.output_dir + '/New Shape/')


    '''
        @input:     The Graph and the path

        This function iterate over the edges of the graph and write it into the file defined by the path
    '''


    def create_edges_file(self, g):
        output = open(self.output_dir + '/edges.csv', 'w')
        output.write('Starting Coordinate; End Coordinate; True Distance(km) \n')

        for edge in g.edges:
            distance = g.get_edge_data(edge[0], edge[1])[0]['weight']
            start_coor = [round(elem, 6) for elem in list(edge[0])]
            end_coor = [round(elem, 6) for elem in list(edge[1])]
            output.write(str(start_coor) + ';' + str(end_coor) + ';' + str(distance) + '\n')


    '''
        @input:     path of the shape file and the output for saving clean network
        @output:    Cleaned network

        This function read the input shape file and convert it into network for cleaning. After converting it simplify the
        graph by calling simplify_graph() and write the cleaned network in form of shapefiles
    '''


    def graph_convertor(self):
        G = self.shape_convertor()
        print "Number of Nodes in the graph, ", len(G.nodes)
        simplify_graph = GraphSimplify(G)
        new_G = simplify_graph.simplify_graph()

        print "Number of Nodes after simplifying, ", len(new_G.nodes)
        self.create_vertex_file(new_G)
        self.create_edges_file(new_G)

        multiDi_to_simple = MultiDiToSimple(new_G)
        new_simple_graph = multiDi_to_simple.convert_MultiDi_to_Simple()
        self.create_edges_vertex_shape(new_simple_graph)

        return new_G

