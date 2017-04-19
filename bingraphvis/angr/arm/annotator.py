
from ...base import *

class AngrColorEdgesAsmArm(EdgeAnnotator):
    EDGECOLOR_CONDITIONAL_TRUE  = 'green'
    EDGECOLOR_CONDITIONAL_FALSE = 'red'
    EDGECOLOR_UNCONDITIONAL     = 'blue'
    EDGECOLOR_CALL              = 'black'
    EDGECOLOR_RET               = 'grey'
    EDGECOLOR_UNKNOWN           = 'yellow'

    def __init__(self):
        super(AngrColorEdgesAsmArm, self).__init__()

    def annotate_edge(self, edge):
        if 'jumpkind' in edge.meta:
            jk = edge.meta['jumpkind']
            if jk == 'Ijk_Ret':
                edge.color = self.EDGECOLOR_RET
            elif jk == 'Ijk_FakeRet':
                edge.color = self.EDGECOLOR_RET
                edge.style = 'dotted'
            elif jk == 'Ijk_Call':
                edge.color = self.EDGECOLOR_CALL
            elif jk == 'Ijk_Boring':
                if 'asm' in edge.src.content:
                    last = edge.src.content['asm']['data'][-1]
                    if last['mnemonic']['content'] in ['b', 'bx']:
                        edge.color = self.EDGECOLOR_UNCONDITIONAL
                    elif last['mnemonic']['content'].find('b') == 0:
                        try:
                            if int(last['operands']['content'].replace('#',''),16) == edge.dst.obj.addr:
                                edge.color = self.EDGECOLOR_CONDITIONAL_TRUE
                            else:
                                edge.color = self.EDGECOLOR_CONDITIONAL_FALSE
                        except Exception, e:
                            #TODO warning
                            edge.color = self.EDGECOLOR_UNKNOWN
                    else:
                        edge.color = self.EDGECOLOR_UNCONDITIONAL
                        edge.style = 'dashed'
            else:
                #TODO warning
                edge.color = self.EDGECOLOR_UNKNOWN
