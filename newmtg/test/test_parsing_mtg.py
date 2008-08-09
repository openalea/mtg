from openalea.mtg.io import *

def test1():
    fn = r'data/mtg1.mtg'
    g = read_mtg_file(fn)
    assert len(g) == 7
    assert g.nb_vertices(scale=1) == 6

def test2():
    fn = r'data/mtg2.mtg'
    g = read_mtg_file(fn)
    assert len(g) == 6
    assert g.nb_vertices(scale=1) == 5

def test3():
    fn = r'data/mtg3.mtg'
    g = read_mtg_file(fn)
    assert len(g) == 13 
    assert g.nb_vertices(scale=1) == 12 

def test4():
    fn = r'data/mtg4.mtg'
    g = read_mtg_file(fn)
    assert len(g) == 47 
    assert g.nb_scales() == 4
    assert g.nb_vertices(scale=1) == 1 
    assert g.nb_vertices(scale=2) == 6 
    assert g.nb_vertices(scale=3) == 39 

def test5():
    fn = r'data/test5_apricot2.mtg'
    g = read_mtg_file(fn)
    assert len(g) == 97 
    assert g.nb_scales() == 5
    assert g.nb_vertices(scale=1) == 1 
    assert g.nb_vertices(scale=2) == 10 
    assert g.nb_vertices(scale=3) == 20 
    assert g.nb_vertices(scale=4) == 65 

