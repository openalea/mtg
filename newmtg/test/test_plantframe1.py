from openalea.mtg.io import *
from openalea.aml import *

def check(fn):
    g = read_mtg_file(fn)
    g1 = aml.MTG(fn)
    
    assert list(g.vertices()) == VtxList()
    for scale in range(1,g.nb_scales()):
        assert list(g.vertices(scale=scale)) == VtxList(Scale=scale), set(g.vertices(scale=scale)).difference(VtxList(Scale=scale))

    l = VtxList(Scale=g.max_scale())
    for vid in l:
        assert g.parent(vid) == aml.Father(vid), 'vertex %d has not the same parent at scale %d'%(vid, g.max_scale())

    return g

def test1():
    fn = r'data/reconstructed_appletree.mtg'
    g = read_mtg_file(fn)


