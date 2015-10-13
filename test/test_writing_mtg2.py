from openalea.mtg import *
from openalea.mtg.io import *

def mtg1():
    g = MTG()
    a1=g.add_component(g.root, label='A1')
    b1= g.add_component(a1, label='B1')
    b2 = g.add_child(b1, label='B2', edge_type='<')
    b3 = g.add_child(b2, label='B3', edge_type='+')

    a2 = g.add_child(a1, label='A2', edge_type='+')
    b4 = g.add_component(a2)
    b4 = g.add_child(b2, child=b4, label='B4',edge_type='+')
    return g

def test1():
    g = mtg1()
    properties = [(p, 'REAL') for p in g.property_names() if p not in ['edge_type', 'index', 'label']]
    mtg_lines = write_mtg(g,properties)
    f=open('toto.xls','w')
    f.write(mtg_lines)
    f.close()

