import networkx as nx

'''
    This module is Used to convert MultiDigraph to Simple Graph
    @input:     MultiDiGraph
    @Output:    Simple Graph
'''


class MultiDiToSimple:
    def __init__(self, G):
        self.G = G

    def convert_MultiDi_to_Simple(self):
        new_G = self.G.to_undirected()

        new_simple_graph = nx.Graph()
        for uv in new_G.edges:
            u_lat = uv[0][0]
            u_lon = uv[0][1]

            v_lat = uv[1][0]
            v_lon = uv[1][1]

            new_start = (u_lat, u_lon)
            new_end = (v_lat, v_lon)
            weight = new_G.get_edge_data(uv[0], uv[1])[0]['weight']
            if new_simple_graph.has_edge(new_start, new_end):
                continue
            else:
                new_simple_graph.add_edge(new_start, new_end, weight=weight)
        return new_simple_graph
