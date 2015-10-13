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
    fn = r'data/mtg1.mtg'
    g = check(fn)
    assert len(g) == 7
    assert g.nb_vertices(scale=1) == 6

def test2():
    fn = r'data/mtg2.mtg'
    g = check(fn)
    assert len(g) == 6
    assert g.nb_vertices(scale=1) == 5

def test3():
    fn = r'data/mtg3.mtg'
    g = check(fn)
    assert len(g) == 13 
    assert g.nb_vertices(scale=1) == 12 

def test4():
    fn = r'data/mtg4.mtg'
    g = check(fn)
    assert len(g) == 47 
    assert g.nb_scales() == 4
    assert g.nb_vertices(scale=1) == 1 
    assert g.nb_vertices(scale=2) == 6 
    assert g.nb_vertices(scale=3) == 39 

def test5():
    fn = r'data/mtg51.mtg'
    #g = check(fn)

def test6():
    fn = r'data/test6_apricot2.mtg'
    g = check(fn)
    assert len(g) == 97 
    assert g.nb_scales() == 5
    assert g.nb_vertices(scale=1) == 1 
    assert g.nb_vertices(scale=2) == 10 
    assert g.nb_vertices(scale=3) == 20 
    assert g.nb_vertices(scale=4) == 65 

def test7():
    fn = r'data/test7.mtg'
    g = check(fn)

def test8():
    fn = r'data/test8_boutdenoylum2.mtg'
    g = check(fn)

def test9():
    fn = r'data/test9_noylum2.mtg'
    g = check(fn)

def test10():
    fn = r'data/test10_agraf.mtg'
    g = check(fn)

def test11():
    fn = r'data/test11_wij10.mtg'
    #g = check(fn)

