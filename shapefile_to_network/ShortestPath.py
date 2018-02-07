from shapely.geometry import Point
import networkx as nx
from haversine import haversine
from MultiDiGraphConvertor import convert_MultiDi_to_Simple
from BufferedGraph import *

def assignTuple(G, coord, buffer):
    geometry = Point(coord[1], coord[0])
    new_G = combine_network_buffer(G, geometry, buffer)
    print new_G.nodes
    return list(new_G.nodes)

def find_shortest_paths(G, start_tuple, end_tuple, graph_buffer, point_buffer):
    geometry = Point(start_tuple[1], start_tuple[0])
    start_tuples = assignTuple(G, start_tuple, point_buffer)
    end_tuples = assignTuple(G, end_tuple, point_buffer)

    buffered_graph = combine_network_buffer(G, geometry, graph_buffer)
    nodes = list(buffered_graph.nodes)

    path_dict = {}
    for start_tuple in start_tuples:

        if start_tuple in nodes:
            for end_tuple in end_tuples:
                if end_tuple in nodes:
                    if nx.has_path(buffered_graph, start_tuple, end_tuple) and start_tuple != end_tuple:
                        shortest_distance = nx.dijkstra_path_length(buffered_graph, start_tuple, end_tuple,
                                                                    weight='weight')
                        shortest_path = nx.shortest_path(buffered_graph, start_tuple, end_tuple, weight='weight')
                        print 'Shortest Path: ', shortest_distance
                        path_dict[shortest_distance] = shortest_path

    return path_dict, buffered_graph

def alphaTimesShortestPath(G, alpha, graph_buffer, point_buffer, start_tuple, end_tuple, break_point):
    shortest_paths, buffered_graph = find_shortest_paths(G, start_tuple, end_tuple, graph_buffer, point_buffer)
    totalPaths = 0

    if len(shortest_paths) >= 1:
        shortest_dis = min(shortest_paths.keys())
        shortest_path = shortest_paths[shortest_dis]
        new_start_coord = shortest_path[0]
        new_end_coord = shortest_path[len(shortest_path)-1]

        all_paths = nx.shortest_simple_paths(convert_MultiDi_to_Simple(buffered_graph), source=new_start_coord,
                                             target=new_end_coord, weight='weight')

        flag = True
        path_list = []
        nodes_in_path = []

        for path in all_paths:
            if totalPaths >= break_point:
                break

            total_distance = 0
            for index in range(1, len(path)):
                if nx.has_path(buffered_graph, path[index - 1], path[index]):
                    total_distance += haversine(path[index - 1], path[index])
                    if total_distance > (alpha * shortest_dis):
                        flag = False
                        break

            if flag or (total_distance <= (alpha * shortest_dis)):
                totalPaths += 1
                path_list.append(total_distance)
                nodes_in_path.append(len(path))

            if flag == False:
                break

    return totalPaths