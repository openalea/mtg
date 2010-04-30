from openalea.mtg.mtg import *
from openalea.mtg import aml

def setup_func():
    g= aml.MTG('data/test7.mtg')

def test1():
    g= aml.MTG('data/test7.mtg')
    print list(g.property_names())
    for v in g.vertices():
        n = g.node(v)
        print n.edge_type()
        print n.label
        print n._line
        print n.parent(), n.complex()
        print n.scale()
        print n.XX, n.YY, n.ZZ
