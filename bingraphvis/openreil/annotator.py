
from ..base import *
import pyopenreil

class OpenreilColorEdgesAsm(EdgeAnnotator):
    EDGECOLOR_CONDITIONAL_TRUE  = 'green'
    EDGECOLOR_CONDITIONAL_FALSE = 'red'
    EDGECOLOR_UNCONDITIONAL     = 'blue'
    EDGECOLOR_CALL              = 'black'
    EDGECOLOR_RET               = 'grey'
    EDGECOLOR_UNKNOWN           = 'yellow'

    def __init__(self):
        super(OpenreilColorEdgesAsm, self).__init__()


    def annotate_edge(self, edge):
        if 'asm' in edge.src.content:
            last = edge.src.content['asm']['data'][-1]

            if last['mnemonic']['content'].find('jmp') == 0:
                edge.color = self.EDGECOLOR_UNCONDITIONAL
            elif last['mnemonic']['content'].find('j') == 0:
                try:
                    if int(last['operands']['content'],16) + last['_addr'] == edge.dst.obj.item.ir_addr[0]:
                        edge.color = self.EDGECOLOR_CONDITIONAL_TRUE
                    else:
                        edge.color = self.EDGECOLOR_CONDITIONAL_FALSE
                except Exception, e:
                    #TODO warning
                    edge.color = self.EDGECOLOR_UNKNOWN
            else:
                edge.color = self.EDGECOLOR_UNCONDITIONAL
                edge.style = 'dashed'
