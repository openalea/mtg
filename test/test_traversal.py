# -*- python -*-
#
#       OpenAlea.mtg
#
#       Copyright 2008 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.pradal.at.cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

from openalea.mtg.mtg import *
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from time import clock

def test_traversal():
    mtg = MTG()
    t = clock()
    mtg = simple_tree(mtg, mtg.root, nb_vertices=1000)
    t1 = clock()
    print t1-t; t = t1
    
    l1 = list(pre_order(mtg, mtg.root))
    t1 = clock()
    print t1-t; t = t1
    l2 = list(pre_order2(mtg, mtg.root))
    t1 = clock()
    print t1-t; t = t1
    l3 = list(pre_order2_with_filter(mtg, mtg.root))
    t1 = clock()
    print t1-t; t = t1

    assert l1 == l2 
    assert l1 == l3

    s1 = set(l1)
    s2 = set(post_order(mtg, mtg.root))
    assert len(mtg) == len(s1) == len(s2)
    assert s1 == s2

def test_iter_mtg():
    g = read_mtg_file('data/test10_agraf.mtg')
    l = list(iter_mtg(g,g.root))
    assert len(l) == len(g)

    l1 = list(iter_mtg2(g,g.root))
    assert len(l1) == len(g)
    assert l == l1

    l2 = list(iter_mtg2(g, 2))
    assert len(l2) == 59

def test_iter_mtg_nplants():
    g = MTG()

    p1 = g.add_component(g.root)
    a1 = g.add_component(p1)
    simple_tree(g, a1)
    p2 = g.add_component(g.root)
    a2 = g.add_component(p2)
    simple_tree(g, a2)

    print len(list(iter_mtg(g, g.root))), len(g)
    print len(list(iter_mtg2(g, g.root))), len(g)
    print len(list(iter_mtg_with_filter(g, g.root))), len(g)
    print len(list(iter_mtg2_with_filter(g, g.root))), len(g)
    #assert len(list(iter_mtg(g, g.root))) == len(g)
    assert len(list(iter_mtg(g, p1))) ==  22
    assert len(list(iter_mtg(g, p2))) ==  22
    assert len(list(iter_mtg2(g, g.root))) == len(g)
    assert len(list(iter_mtg2(g, p1))) ==  22
    assert len(list(iter_mtg2(g, p2))) ==  22
    assert len(list(iter_mtg_with_filter(g, p1))) ==  22
    assert len(list(iter_mtg_with_filter(g, p2))) ==  22
    assert len(list(iter_mtg_with_filter(g, p1, lambda x:True, None))) ==  22
    assert len(list(iter_mtg_with_filter(g, p2, lambda x : True, None))) ==  22
    assert len(list(iter_mtg2_with_filter(g, p1))) ==  22
    assert len(list(iter_mtg2_with_filter(g, p2))) ==  22
    assert len(list(iter_mtg2_with_filter(g, p1, lambda x:True, None))) ==  22
    assert len(list(iter_mtg2_with_filter(g, p2, lambda x : True, None))) ==  22

