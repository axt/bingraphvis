from ..base import *
from . import *
from .x86 import *

class AngrVisFactory(object):
    def __init__(self):
        pass

    def default_cfg_pipeline(self, project, asminst=False, vexinst=False, remove_path_terminator=True, color_edges=True, comments=True):
        vis = Vis()
        vis.set_source(AngrCFGSource())
        if remove_path_terminator:
            vis.add_transformer(AngrRemovePathTerminator())
        vis.add_content(AngrCFGHead())
        vis.add_node_annotator(AngrColorSimprocedures())
        if asminst:
            vis.add_content(AngrAsm(project))
            if comments:
                vis.add_content_annotator(AngrCommentsAsm(project))
        if vexinst:
            vis.add_content(AngrVex(project))
            if color_edges:
                vis.add_edge_annotator(AngrColorEdgesVex())
        elif asminst:
            if color_edges:
                vis.add_edge_annotator(AngrColorEdgesAsm())
        return vis

    def default_cg_pipeline(self, kb, verbose=True):
        vis = Vis()
        vis.set_source(AngrKbCGSource())
        vis.add_content(AngrCGHead())
        if verbose:
            vis.add_content(AngrKbFunctionDetails())
        return vis

    def default_common_graph_pipeline(self, type=False):
        vis = Vis()
        vis.set_source(AngrCommonSource())
        vis.add_content(AngrCommonHead())
        if type:
            vis.add_content(AngrCommonTypeHead())
        return vis
    
    
