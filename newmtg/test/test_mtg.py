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

def test_mtg_api():
    mtg = MTG()
    
    root = mtg.root
    assert root is not None
    assert root == 0, 'default root id (%d) is not 0'%root

    # scale 1
    root1 = mtg.add_component(root)
    v1 = mtg.add_child(root1)
    v2 = mtg.add_child(root1)
    v3 = mtg.add_child(root1)
    v4 = mtg.add_child(v1)
    v5 = mtg.add_child(v1)
    
    assert mtg.complex(root1) == root
    assert mtg.complex(v1) == root
    assert mtg.complex(v2) == root
    assert mtg.complex(v3) == root
    assert mtg.complex(v4) == root
    assert mtg.complex(v5) == root

    assert mtg.parent(v5) == v1
    assert mtg.parent(v4) == v1
    assert mtg.parent(v3) == root1
    assert mtg.parent(v2) == root1
    assert mtg.parent(v1) == root1

    assert [v1,v2,v3] == list(mtg.children(root1))
    assert [v4,v5] == list(mtg.children(v1))
    assert list(mtg.children(v2)) == list(mtg.children(v3)) == list(mtg.children(v4)) == list(mtg.children(v5)) == []

    assert len(mtg) == 7, 'len(mtg) == %d'%len(mtg)

def test_api2():
    mtg = MTG()
    root = mtg.root
    # scale 1
    root1 = mtg.add_component(root)
    v1 = mtg.add_child(root1)
    v2 = mtg.add_child(root1)
    v3 = mtg.add_child(root1)
    v4 = mtg.add_child(v1)
    v5 = mtg.add_child(v1)

    assert mtg.nb_components(root) == 6, "nb_components = %d"%(mtg.nb_components(root))
    assert set([root1, v1, v2, v3, v4, v5]) == set(mtg.components(root))
    assert mtg.nb_components(root1) == mtg.nb_components(v1) == mtg.nb_components(v2) == 0
    

def test_mtg_edition():
    mtg = MTG()
    root = mtg.root
    
    # scale 1, 2
    root1 = mtg.add_component(root)
    root2 = mtg.add_component(root1)
    v12 = mtg.add_child(root2)
    v22 = mtg.add_child(v12)

    v32, v32_complex = mtg.add_child_and_complex(v22)

    assert len(mtg) == 7
    assert v32 in mtg.children(v22)
    assert v32_complex in mtg.children(root1)


def test_mtg_random():
    g = MTG()
    root = g.root
    
    root1 = g.add_component(root)
    root1 = g.add_component(root1)
    vid = random_tree(g, root1, nb_vertices=18)

    v1, complex1 = g.add_child_and_complex(vid)
    vid = random_tree(g, v1, nb_vertices=18)

    v1, complex1 = g.add_child_and_complex(vid)
    vid = random_tree(g, v1, nb_vertices=18)
    assert len(g)==61
    
def test_api3():
    ''' Test clear function. '''
    mtg = MTG()
    assert len(mtg) == 1, 'len(mtg) == %d'%len(mtg)
    v1 = mtg.add_component(mtg.root)
    mtg.clear()
    assert len(mtg) == 1, 'len(mtg) == %d'%len(mtg)

    v2 = mtg.add_component(mtg.root)
    assert v1 == v2

def test_traversal():
    mtg = MTG()
    mtg = simple_tree(mtg, mtg.root)
    
    s1 = set(pre_order(mtg, mtg.root))
    s2 = set(post_order(mtg, mtg.root))
    assert len(mtg) == len(s1) == len(s2)
    assert s1 == s2

def test_components():
    g = MTG() # root = 0
    r1 = g.add_component(g.root) # scale= 1, v=1
    r2 = g.add_component(r1) # scale= 1, v=2
    v, c  = g.add_child_and_complex(r2, edge_type='+')
    v, c  = g.add_child_and_complex(r2)
    v1, c1  = g.add_child_and_complex(v, edge_type='+')
    v = g.add_child(v)
    v1, c1  = g.add_child_and_complex(v, edge_type='+')
    v = g.add_child(v)
    

def test_properties():
    mtg = MTG()
    root = mtg.root
    
    root1 = mtg.add_component(root)
    vid = random_tree(mtg, root1, nb_vertices=18)
    v1, complex1 = mtg.add_child_and_complex(vid)
    vid = random_tree(mtg, v1, nb_vertices=18)
    v1, complex1 = mtg.add_child_and_complex(vid)
    vid = random_tree(mtg, v1, nb_vertices=18)

    assert 'edge_type' in mtg.property_names()
    assert len(mtg.property('edge_type')) == 18*3, \
           'len(mtg.property("edge_type")) == %d'%len(mtg.property('edge_type'))

def test_edition():
    s = '/A/a<b\<B/c[+d[+e<f][+g]]\<D/h\<C/i[+j<k][+l<m]\\\\'
    
    mtg = multiscale_edit(s)

    assert len(mtg) == 18
    assert mtg.nb_scales() == 3

    assert len(set(mtg.vertices(scale=0))) == 1
    assert len(set(mtg.vertices(scale=1))) == 4
    assert len(set(mtg.vertices(scale=2))) == 13

    mtg = fat_mtg(mtg)
    assert len(mtg) == 18
    assert mtg.nb_scales() == 3

    assert len(set(mtg.vertices(scale=0))) == 1
    assert len(set(mtg.vertices(scale=1))) == 4
    assert len(set(mtg.vertices(scale=2))) == 13
    
    assert len(list(iter_mtg(mtg, mtg.root))) == len(mtg)

def test_order():
    s = '/A/a<b<c[+d[+e<f][+g]]<h<i[+j<k][+l<m]'
    mtg = multiscale_edit(s)

def test_iter_mtg():
    g = read_mtg_file('data/test10_agraf.mtg')
    l = list(iter_mtg(g,g.root))
    assert len(l) == len(g)

    l1 = list(iter_mtg2(g,g.root))
    assert len(l1) == len(g)
    assert l == l1

    l2 = list(iter_mtg2(g, 2))
    assert len(l2) == 59

def test_sub_mtg():
    g = read_mtg_file('data/test10_agraf.mtg')
    g1 = g.sub_mtg(2)
    g = g.sub_mtg(2,copy=False)

    assert len(g1) == len(g) == 59

def test_remove_vertex():
    mtg = MTG()
    root = mtg.root
    # scale 1
    root1 = mtg.add_component(root)
    v1 = mtg.add_child(root1)
    v2 = mtg.add_child(root1)
    v3 = mtg.add_child(root1)
    v4 = mtg.add_child(v1)
    v5 = mtg.add_child(v1)
    n = len(mtg)
    mtg.remove_vertex(v5)
    mtg.remove_vertex(v1, reparent_child=True)
    assert len(mtg) == n-2
