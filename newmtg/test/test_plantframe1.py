from openalea.mtg.io import *
import openalea.mtg.plantframe as plantframe
import openalea.mtg.algo as algo 
#from openalea.aml import *

# def check(fn):
#     g = read_mtg_file(fn)
#     g1 = aml.MTG(fn)
#     
#     assert list(g.vertices()) == VtxList()
#     for scale in range(1,g.nb_scales()):
#         assert list(g.vertices(scale=scale)) == VtxList(Scale=scale), set(g.vertices(scale=scale)).difference(VtxList(Scale=scale))
# 
#     l = VtxList(Scale=g.max_scale())
#     for vid in l:
#         assert g.parent(vid) == aml.Father(vid), 'vertex %d has not the same parent at scale %d'%(vid, g.max_scale())
# 
#     return g

def test1():
    fn = r'data/test12_wij10.mtg'

    length = lambda x: g.property('longueur').get(x)
    botdia = lambda x: g.property('diabase').get(x)
    topdia = lambda x: g.property('diasom').get(x)

    g = read_mtg_file(fn)

    pf = plantframe.PlantFrame(g, Length=length, TopDiameter=topdia, BottomDiameter=botdia)


    return g, pf
