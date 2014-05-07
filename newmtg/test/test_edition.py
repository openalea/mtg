from openalea.mtg import *

def my_mtg():
    g = MTG()
    vid = g.add_component(g.root, label='P')
    vid = g.add_component(vid, label='S')
    cid = g.add_child(vid, label='S', edge_type='+')
    cid = g.add_child(vid, label='S', edge_type='+')
    cid = g.add_child(vid, label='S', edge_type='<')       
    return g

def test_insert_scale():
    g = my_mtg()

    quotient = lambda v: g.edge_type(v) != '<'

    return g.insert_scale(inf_scale=2, partition=quotient) 

def test_remove_scale():
    g = my_mtg()

    quotient = lambda v: g.edge_type(v) != '<'

    g.insert_scale(inf_scale=2, partition=quotient) 
    g, _ = g.remove_scale(scale=2)
    return g

