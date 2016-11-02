from .base import *

class ColorNodes(NodeAnnotator):
    def __init__(self, nodes, fillcolor=None, color=None):
        super(ColorNodes, self).__init__()
        self.nodes = nodes
        self.fillcolor = fillcolor
        self.color = color
    
    def annotate_node(self, node):
        if node.obj in self.nodes:
            node.style = 'filled'
            if self.fillcolor:
                node.fillcolor = self.fillcolor
            if self.color:
                node.color = self.color
