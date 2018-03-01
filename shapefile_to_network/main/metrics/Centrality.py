import networkx as nx

'''
    This class is used to calculate some basic metrics over the network like

     degree_centrality      :   number of nodes its connected to
     closeness_centrality   :   reciprocal of sum of shortest path form node u to all other nodes
     communicability        :   sum of closest walk from node u to node v
     load_centrality        :   fraction of all the shortest path passes from that node
     nodes_pagerank         :   ranking of the nodes in the graph g on basis on incoming links
'''


class Centrality:
    def __init__(self, g, weight=None):
        self.g = g
        self.weight = weight

    def metrics(self):
        degree_centrality = nx.degree_centrality(self.g)
        closeness_centrality = nx.closeness_centrality(self.g, distance=self.weight)
        communicability = nx.communicability(self.g)
        load_centrality = nx.load_centrality(self.g, weight=self.weight)
        nodes_pagerank = nx.pagerank(self.g, weight=self.weight)

        return degree_centrality, closeness_centrality, communicability, load_centrality, nodes_pagerank

    '''
        This function is used to find the dispersion between source and target in the network
        @input  :   source and target node in the network
        @output :   dictionary of nodes with dispersion score
    '''

    def nodes_dispersion(self, source, target):
        return nx.dispersion(self.g, u=source, v=target)
