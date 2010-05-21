from openalea.mtg.mtg import *
from openalea.mtg import aml
from openalea.mtg.algo import union


def test1():
    g= aml.MTG('data/test7.mtg')
    g1 = g.sub_mtg(g.root)
    assert len(g1) == len(g)
    g2  = union(g,g1)
    assert len(g2) == 2*len(g) -1
