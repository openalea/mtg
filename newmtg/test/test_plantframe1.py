from openalea.mtg.io import *
import openalea.mtg.plantframe as plantframe
import openalea.mtg.algo as algo 
from openalea.mtg import aml

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

def test2():
    fn = r'data/hetre.mtg'

    g = read_mtg_file(fn)
    pf = plantframe.PlantFrame(g)

    aml.Activate(g)
    
    return g, pf
   

def fun3():
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.mlab as mlab
    import matplotlib.ticker as ticker
    import pylab as P

    g, pf = test2()
    P.figure()

    lengths = []
    for root in g.vertices(scale=1):
        vr = g.component_roots_at_scale(root,scale=2).next()
        h = aml.Height(vr)
        lv = [v for v in algo.trunk(g,vr, RestrictedTo='SameComplex', ConatinedIn=root) if v in pf.length]
        P.plot([aml.Height(v)-h for v in lv], [pf.length.get(v) for v in lv], 'o-')
        #lengths.append([pf.length.get(v) for v in lv if v in pf.length])


    #n, bins, patches = P.hist( lengths, 4, histtype='bar')
    
    return lengths
    # Compute a reference axis


def test_hetre():
    symbols = {'P': 1, 'U': 2}
    code = '/P1/U1<U2/P2/U1'

    g = multiscale_edit(code, symbols)
    assert g.parent(5) != 3
