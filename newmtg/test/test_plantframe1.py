from openalea.mtg.io import *
import openalea.mtg.plantframe as plantframe
import openalea.mtg.algo as algo 
from openalea.mtg import aml, dresser

from time import clock
from collections import defaultdict

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

    # axes are linear and diameter are defined on axes.
    assert len(pf.top_diameter) == 16
    assert len(pf.bottom_diameter) == 16
    
    for v in g.vertices(scale=3):
        assert pf.is_linear(g, v)
    
    diameters = pf.algo_diameter()
    assert len(diameters) == g.nb_vertices(scale=4)
    
    length = pf.algo_length()

    return pf

def __test2():
    fn = r'data/hetre.mtg'

    g = read_mtg_file(fn)
    param = dresser.DressingData()

    et = g.property('edge_type')
    split_axe = lambda v: et.get(v) == '+' 

    pf = plantframe.PlantFrame(g, Axe=split_axe, DressingData=param)

    diameters = pf.algo_diameter()
    length = pf.algo_length()
    
    
    return pf

def test3():
    fn = r'data/test12_wij10.mtg'
    drf = r'data/wij10.drf'

    g = read_mtg_file(fn)
    dressing_data = dresser.dressing_data_from_file(drf)

    et = g.property('edge_type')
    split_axe = lambda v: et.get(v) == '+' 

    pf = plantframe.PlantFrame(g, Axe=split_axe, 
                               DressingData=dressing_data)

    diameters = pf.algo_diameter()
    length = pf.algo_length()
    
    
    return pf



def test4():
    fn = r'data/test9_noylum2.mtg'
    drf = r'data/walnut.drf'

    t=clock()

    g = read_mtg_file(fn)

    t1=clock(); t, dt = t1, t1-t
    print 'readmtg in ', dt 

    topdia = lambda x: g.property('TopDia').get(x)

    dressing_data = dresser.dressing_data_from_file(drf)
    pf = plantframe.PlantFrame(g, 
                               TopDiameter=topdia, 
                               DressingData = dressing_data)
    pf.propagate_constraints()

    t1=clock(); t, dt = t1, t1-t
    print 'empty plantframe in ', dt 

    diameters = pf.algo_diameter()

    t1=clock(); t, dt = t1, t1-t
    print 'diameter in ', dt 

    axes = plantframe.compute_axes(g,3, pf.points, pf.origin)
    axes[0][0].insert(0,pf.origin)

    t1=clock(); t, dt = t1, t1-t
    print 'points in ', dt 

    scene=plantframe.build_scene(pf.g, pf.origin, axes, pf.points, diameters, 10000)

    t1=clock(); t, dt = t1, t1-t
    print 'scene in ', dt 
    return scene, pf

def test5():
    fn = r'data/test10_agraf.mtg'
    drf = r'data/agraf.drf'

    t=clock()

    g = read_mtg_file(fn)

    t1=clock(); t, dt = t1, t1-t
    print 'readmtg in ', dt 

    topdia = lambda x: g.property('TopDia').get(x)

    dressing_data = dresser.dressing_data_from_file(drf)
    pf = plantframe.PlantFrame(g, 
                               TopDiameter=topdia, 
                               DressingData = dressing_data)
    pf.propagate_constraints()

    t1=clock(); t, dt = t1, t1-t
    print 'empty plantframe in ', dt 

    diameters = pf.algo_diameter()

    t1=clock(); t, dt = t1, t1-t
    print 'diameter in ', dt 

    root = g.roots_iter(scale=g.max_scale()).next()
    axes = plantframe.compute_axes(g,root, pf.points, pf.origin)
    axes[0][0].insert(0,pf.origin)

    t1=clock(); t, dt = t1, t1-t
    print 'points in ', dt 

    scene=plantframe.build_scene(pf.g, pf.origin, axes, pf.points, diameters, 10000, option='cylinder')

    t1=clock(); t, dt = t1, t1-t
    print 'scene in ', dt 

    return scene, pf

def walnut():
    fn = r'data/test9_noylum2.mtg'
    drf = r'data/walnut.drf'

    g = read_mtg_file(fn)

    topdia = lambda x: g.property('TopDia').get(x)

    dressing_data = dresser.dressing_data_from_file(drf)
    pf = plantframe.PlantFrame(g, 
                               TopDiameter=topdia, 
                               DressingData = dressing_data)
    pf.propagate_constraints()

    return pf

   
def test_colors():
    pf = walnut()
    axes = plantframe.compute_axes(pf.g,3, pf.points, pf.origin)
    axes[0][0].insert(0,pf.origin)
    diameters = pf.algo_diameter()

    g = pf.g
    colors =defaultdict(lambda x: (0,255,0), 
        zip(range(8), [ ((i&2**0)*255, ((i&2**1)>>1)*255, ((i&2**2)>>2)*255) for i in range(8)])) 
    def my_color(vid):
        return colors[g.order(vid)]

    scene=plantframe.build_scene(pf.g, pf.origin, axes, pf.points, diameters, 10000, option='cylinder', colors = my_color)
    return scene









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
        vr = g.component_roots_at_scale_iter(root,scale=2).next()
        h = aml.Height(vr)
        lv = [v for v in algo.trunk(g,vr, RestrictedTo='SameComplex', ConatinedIn=root) if v in pf.length]
        P.plot([aml.Height(v)-h for v in lv], [pf.length.get(v) for v in lv], 'o-')
        #lengths.append([pf.length.get(v) for v in lv if v in pf.length])


    #n, bins, patches = P.hist( lengths, 4, histtype='bar')
    
    return lengths
    # Compute a reference axis


