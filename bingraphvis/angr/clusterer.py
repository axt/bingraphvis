
from ..base import *
import networkx as nx 
import angr
import itertools


class AngrCallstackKeyClusterer(Clusterer):
    def __init__(self, visible=True):
        super(AngrCallstackKeyClusterer, self).__init__()
        self.visible = visible

    def cluster(self, graph):
        
        for node in graph.nodes:
            key = node.obj.callstack_key
            cluster = graph.get_cluster(key)
            if not cluster:
                cluster = graph.create_cluster(key, visible=self.visible)
            cluster.add_node(node)

        # merge by jump edges
        jgraph = nx.DiGraph()
        for e in graph.edges:
            if e.src.cluster and e.dst.cluster and e.src.cluster != e.dst.cluster:
                if  e.meta['jumpkind'] == 'Ijk_Boring':
                    jgraph.add_edge(e.src.cluster.key, e.dst.cluster.key)
        
        for n in jgraph.nodes():
            in_edges = jgraph.in_edges(n)
            if len(in_edges) == 1:
                s,t = in_edges[0]
                scluster = graph.get_cluster(s)
                for n in graph.nodes:
                    if n.cluster.key == t:
                        n.cluster.remove_node(n)
                        scluster.add_node(n)

        # build cluster hierarchy
        cgraph = nx.DiGraph()
        for e in graph.edges:
            if e.src.cluster and e.dst.cluster and e.src.cluster != e.dst.cluster:
                if  e.meta['jumpkind'] == 'Ijk_Call':
                    cgraph.add_edge(e.src.cluster.key, e.dst.cluster.key)
                
        for n in cgraph.nodes():
            in_edges = cgraph.in_edges(n)
            if len(in_edges) == 1:
                s,t = in_edges[0]
                scluster = graph.get_cluster(s)
                tcluster = graph.get_cluster(t)
                tcluster.parent = scluster
                
