
from ..base import *

import networkx

class AngrRemovePathTerminator(Transformer):
    def __init__(self):
        pass
        
    def transform(self, graph):
        remove = []
        for n in graph.nodes:
            
            if hasattr(n.obj, 'is_simprocedure') and n.obj.is_simprocedure and n.obj.simprocedure_name == 'PathTerminator':
                remove.append(n)
        for r in remove:
            graph.remove_node(r)


class AngrRemoveSimProcedures(Transformer):
    def __init__(self):
        pass
        
    def transform(self, graph):
        remove = []
        for n in graph.nodes:
            if n.obj.is_simprocedure:
                remove.append(n)
                cs = []
                for e in graph.edges:
                    if e.dst == n:
                        cs.append(e.src)
                found = False
                for c in cs:
                    for e in graph.edges:
                        if e.src == c and e.dst != n:
                            found = True
                            break
                    if not found:
                        remove.append(c)
        for r in remove:
            graph.remove_node(r)

class AngrFilterNodes(Transformer):
    def __init__(self, node_filter):
        self.node_filter = node_filter
        pass
        
    def transform(self, graph):
        remove = filter(lambda _: not self.node_filter(_), graph.nodes)

        for r in remove:
            graph.remove_node(r)


class AngrRemoveImports(Transformer):
    def __init__(self, project):
        self.project = project
        self.eaddrs = self.import_addrs(project)
        
    def import_addrs(self, project):
        eaddrs=[]
        for _ in project.loader.main_bin.imports.values():
            if _.resolvedby != None:
                eaddrs.append(_.value)
        return set(eaddrs)

    def transform(self, graph):
        remove = []
        for n in graph.nodes:
            if n.obj.addr in self.eaddrs:
                remove.append(n)
                cs = []
                for e in graph.edges:
                    if e.dst == n:
                        cs.append(e.src)
                found = False
                for c in cs:
                    for e in graph.edges:
                        if e.src == c and e.dst != n:
                            found = True
                            break
                    if not found:
                        remove.append(c)
        for r in remove:
            graph.remove_node(r)



class AngrRemoveFakeretEdges(Transformer):
    def __init__(self):
        pass
        
    def transform(self, graph):
        remove = []
        for e in graph.edges:
            if e.meta['jumpkind'] == 'Ijk_FakeRet':
                remove.append(e)
        for r in remove:
            graph.remove_edge(r)

class AngrAddEdges(Transformer):
    def __init__(self, graph, reverse=False, color=None, label=None, style=None, width=None, weight=None):
        self.graph = graph
        self.reverse = reverse
        self.color = color
        self.label = label
        self.style = style
        self.width = width
        self.weight = weight

    def transform(self, graph):
        lookup = {}
        for n in graph.nodes:
            lookup[n.obj] = n
        
        for s,t in self.graph.edges():
            #TODO option to add missing nodes (?)
            try: 
                if self.reverse:
                    ss,tt = lookup[t],lookup[s]
                else:
                    ss,tt = lookup[s],lookup[t]
                
                graph.add_edge(Edge(ss, tt, color=self.color, label=self.label, style=self.style, width=self.width, weight=self.weight))
            except:
                #FIXME WARN
                pass
