"""
    This module is used to clean all the intermediate nodes from the MultiDiGraph
    1. All the intermediate nodes of degree 2 which is just a curve or bend in the graph will be removed

    @input:     MultiDiGraph
    @output:    MultiDiGraph
"""


class GraphSimplify:
    def __init__(self, G):
        self.G = G

    '''
        @input:     The MultiDigraph and the coordinate of node
        @output:    Returns bool

        This function check if the node is intermediate node or not. It get the list of the successors and predecessors of
        the node and check for node with degree one and isolated nodes.

        Return true if its the intermediate node of false if its not
    '''

    def is_intermediate_node(self, node):
        neighbours = set(list(self.G.predecessors(node)) + list(self.G.successors(node)))
        d = self.G.degree(node)

        if node in neighbours:
            return True
        elif self.G.in_degree(node) == 0 or self.G.out_degree(node) == 0:
            return True
        elif not (len(neighbours) == 2 and d == 2):
            return True
        else:
            return False

    '''
        @input:     The MultiDiGraph, start coord, list of non intermediate nodes, list of nodes in path
        @output:    Returns list of nodes in the path from the start coord to then end

        This function will iterate over all the successor of the start coordinate and check if it lies in the path
        If not then check if its the non intermediate node, if not then call this function again till you get the
        non intermediate node.

    '''

    def find_path(self, start_node, endnode_list, path):
        for succesor in self.G.successors(start_node):
            if succesor not in path:
                path.append(succesor)
                if succesor not in endnode_list:
                    path = self.find_path(succesor, endnode_list, path)
                else:
                    return path

        if (path[-1] not in endnode_list) and (path[0] in self.G.successors(path[-1])):
            path.append(path[0])
        return path

    '''
        @input:     The MultiDigraph for simplifying and cleaning
        @output:    Returns cleaned and simplified MultiDigraph

        This function removed all the nodes which are of degree one and intermediate nodes. While removing the intermediate
        nodes it preserve the weight(distance) between edges by adding it to the new edges while removing intermediate node.
    '''

    def simplify_graph(self):
        non_intermediate_node = set()
        for node in self.G.nodes():
            if self.is_intermediate_node(node):
                non_intermediate_node.add(node)

        uncleaned_path = []
        for node in non_intermediate_node:
            for successor in self.G.successors(node):
                if successor not in non_intermediate_node:
                    path = self.find_path(successor, non_intermediate_node, path=[node, successor])
                    uncleaned_path.append(path)

        nodes_to_remove = []
        edges_to_build = []

        for path in uncleaned_path:
            nodes_to_remove.extend(path[1:-1])
            total_distance = 0
            for index in range(1, len(path)):
                total_distance += (self.G.get_edge_data(path[0], path[1])[0]['weight'])

            edges_to_build.append({'start': path[0], 'end': path[-1], 'distance': total_distance})

        self.G.remove_nodes_from(nodes_to_remove)

        for edge in edges_to_build:
            self.G.add_edge(edge['start'], edge['end'], weight=edge['distance'])

        return self.G
