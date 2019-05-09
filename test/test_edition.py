from openalea.mtg import *

def my_mtg():
    g = MTG()
    vid = g.add_component(g.root, label='P')
    vid = g.add_component(vid, label='S')
    cid = g.add_child(vid, label='S', edge_type='+')
    cid = g.add_child(vid, label='S', edge_type='+')
    cid = g.add_child(vid, label='S', edge_type='<')       
    return g

def my_mtg_2scales():
    g = MTG()
    # g.add_property("edge_type")
    g.add_component(0, 1)
    g.add_component(1, 2)
    g.add_child(1, 3)
    g.add_child(2, 5)
    g.add_component(3, 5)
    g.node(5).edge_type = "<"
    g.add_child(5, 6)
    g.add_component(3, 6)
    g.node(6).edge_type = "<"
    g.add_child(6, 8)
    g.add_component(3, 8)
    g.node(8).edge_type = "<"
    g.add_child(5, 16)
    g.add_component(3, 16)
    g.node(16).edge_type = "+"
    g.add_child(1, 4)
    g.node(4).edge_type() == "+"
    g.add_child(2, 9)
    g.add_component(4, 9)
    g.node(9).edge_type = "+"
    g.add_child(9, 10)
    g.add_component(4, 10)
    g.node(10).edge_type = "+"
    g.add_child(4, 11)
    g.node(11).edge_type = "+"
    g.add_child(10, 12)
    g.node(12).edge_type = "+"
    g.add_component(11, 12)
    g.add_child(9, 17)
    g.node(17).edge_type = "+"
    g.add_component(4, 17)
    g.add_child(1, 7)
    g.node(7).edge_type = "+"
    g.add_child(2, 13)
    g.add_component(7, 13)
    g.node(13).edge_type = "+"
    g.add_child(13, 14)
    g.add_component(7, 14)
    g.node(14).edge_type = "+"
    g.add_child(14, 15)
    g.add_component(7, 15)
    g.node(15).edge_type = "+"
    # add a property used to add scale
    g.add_property("Y")
    g.node(2).Y = 2010
    for i in [5, 6, 9, 10, 13]:
        g.node(i).Y = 2011
    for i in [8, 12, 14, 15, 16, 17]:
        g.node(i).Y = 2012
        
    return g

def test_insert_scale():
    g = my_mtg()
    
    quotient = lambda v: g.edge_type(v) != '<'

    return g.insert_scale(inf_scale=2, partition=quotient) 

def parent_of_components(g, u):
    """
    Find parent of component root of g
    in g.parent(u) (for connected MTGs)
    """
    c = g.component_roots(u)[0]
    p = g.parent(u)
    if not(p is None):
        p = g.component_roots(p)[0]
        ch = set(g.children(p))
        assert g.complex(p) != u
        path = g.Path(p, c)
        return list(set(path).intersection(ch))[0]
    else:
        return u

def test_insert_scale_from_property():
    g = my_mtg_2scales()
    g_3scales = g.copy()       
    
    def quotient(v, g=g_3scales): 
        if g.parent(v) is None:
            return True
        elif g.complex(v) != g.complex(g.parent(v)):
            return True
        elif g.node(v).Y != g.node(v).parent().Y:
            return True
        else:
            return False
    
    g_3scales.insert_scale(inf_scale=2, partition=quotient, preserve_order=True)
    assert len(g_3scales.scales()) == 4
    assert len(g_3scales.vertices(scale=1)) == len(g.vertices(scale=1))
    assert len(g_3scales.vertices(scale=3)) == len(g.vertices(scale=2))
    assert len(g_3scales.vertices(scale=2)) == 9
    for v in g_3scales.vertices(scale=2):
        c2 = g_3scales.children(v) #children at scale 2
        if len(c2) > 1:
            cpnt = g_3scales.component_roots(v)[0]
            c3 = g_3scales.children(cpnt) #children at scale 3
            cv = [parent_of_components(g_3scales, x) for x in c2]
            msg = "Children inversion at: " + str(v)
            assert cv == c3, msg
    from openalea.mtg.algo import lowestCommonAncestor
    print(lowestCommonAncestor(g, [8, 16]))

def test_remove_scale():
    g = my_mtg()

    quotient = lambda v: g.edge_type(v) != '<'

    g.insert_scale(inf_scale=2, partition=quotient) 
    g, _ = g.remove_scale(scale=2)
    return g

if __name__ == "__main__":
    test_insert_scale()
    test_insert_scale_from_property()
    test_remove_scale()