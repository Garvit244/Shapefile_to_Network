'''
    This module is used to clean all the intermediate nodes from the MultiDiGraph
    1. All the intermediate nodes of degree 2 which is just a curve or bend in the graph will be removed

    @input:     MultiDiGraph
    @output:    MultiDiGraph
'''

def is_intermediate_node(G, node):
    neighbours = set(list(G.predecessors(node)) + list(G.successors(node)))
    d = G.degree(node)

    if node in neighbours:
        return True
    elif G.in_degree(node) == 0 or G.out_degree(node) == 0:
        return True
    elif not (len(neighbours) == 2 and d == 2):
        return True
    else:
        return False


def find_path(G, start_node, endnode_list, path):
    for succesor in G.successors(start_node):
        if succesor not in path:
            path.append(succesor)
            if succesor not in endnode_list:
                path = find_path(G, succesor, endnode_list, path)
            else:
                return path

    if (path[-1] not in endnode_list) and (path[0] in G.successors(path[-1])):
        path.append(path[0])
    return path


def simplify_graph(G):
    # Remove nodes of degree one/ isolated nodes
    # Cluster group of points into single point

    # Remove intermediate nodes
    non_intermediate_node = set()
    for node in G.nodes():
        if is_intermediate_node(G, node):
            non_intermediate_node.add((node))

    uncleaned_path = []
    for node in non_intermediate_node:
        for successor in G.successors(node):
            if successor not in non_intermediate_node:
                path = find_path(G, successor, non_intermediate_node, path=[node, successor])
                uncleaned_path.append(path)

    nodes_to_remove = []
    edges_to_build = []

    for path in uncleaned_path:
        nodes_to_remove.extend(path[1:-1])
        total_distance = 0
        for index in range(1, len(path)):
            total_distance += (G.get_edge_data(path[0], path[1])[0]['weight'])

        edges_to_build.append({'start': path[0], 'end': path[-1], 'distance': total_distance})

    G.remove_nodes_from(nodes_to_remove)

    for edge in edges_to_build:
        G.add_edge(edge['start'], edge['end'], weight=edge['distance'])

    return G