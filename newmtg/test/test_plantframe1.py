from openalea.mtg.io import *
import openalea.mtg.plantframe as plantframe
import openalea.mtg.algo as algo 
from openalea.mtg import aml, dresser

def test1():
    fn = r'data/test12_wij10.mtg'
    drf = r'data/wij10.drf'

    length = lambda x: g.property('longueur').get(x)
    botdia = lambda x: g.property('diabase').get(x)
    topdia = lambda x: g.property('diasom').get(x)

    g = read_mtg_file(fn)

    dressing_data = dresser.dressing_data_from_file(drf)
    pf = plantframe.PlantFrame(g, Length=length, 
                               TopDiameter=topdia, 
                               BottomDiameter=botdia,
                               DressingData = dressing_data)
    pf.propagate_constraints()

    # axes are linear and diameter are defined on axes.
    assert len(pf.top_diameter) == 16
    assert len(pf.bottom_diameter) == 16
    
    for v in g.vertices(scale=3):
        assert pf.is_linear(g, v)
    
    mtg, new_map = pf.build_mtg_from_radius()
    
    axes = [v for v in mtg.vertices(scale=1) if pf.is_linear(mtg, v)]
    for v in axes:
        assert mtg.order(v) == 1

    diameters = pf.algo_diameter()
    assert len(diameters) == g.nb_vertices(scale=4)
    
    return g, pf, mtg, new_map

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
