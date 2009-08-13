# -*- python -*-
# -*- coding: utf-8 -*-
#
#       OpenAlea.mtg
#
#       Copyright 2008-2009 INRIA - CIRAD - INRA  
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

'''
Implementation of a set of algorithms for the MTG datastructure
'''

__docformat__ = "restructuredtext"

import traversal

def ancestors(g, v1, **kwds):
    " Return the vertices from v1 to the root. "
    v = v1
    while v is not None:
        yield v
        v = g.parent(v)

def path(g, v1, v2=None):
    """
    Compute the vertices between v1 and v2.
    If v2 is None, return the path between v1 and the root.
    Otherelse, return the path between v1 and v2.
    If the graph is oriented from v1 to v2, sign is positive.
    Else, sign is negative.
    """
    sign = 1
    if v2 is None:
        return ancestors(g,v1), sign

    l= list(ancestors(g,v2))
    try: 
        index = l.index(v1)
    except ValueError:
        l = list(ancestors(g,v1))
        try:
            index = l.index(v2)
            sign = -1
        except ValueError:
            return iter([]), 0

    return reversed(l[:index]), sign

def edge_type(g,v):
    return g.property('edge_type').get(v)

def topological_path(g,v1, v2=None, edge=None):
    p, sign = path(g,v1,v2)
    if sign == 0:
        return None

    if edge is None:
        return sum(1 for v in p), sign
    else: 
        return sum(1 for v in p if edge_type(g,v)==edge), sign
        
def order(g, v1, v2=None):
    return topological_path(g, v1, v2, '+')[0]

def alg_rank(g, v1, v2=None):
    p, sign = path(g,v1,v2)
    count = 0
    for v in p:
        if edge_type(g,v) == '<':
            count+=1
        else:
            break
    return count*sign

def rank(g, v1, v2=None):
    return abs(alg_rank(g,v1,v2))

def height(g, v1, v2=None):
    return topological_path(g, v1, v2 )[0]-1

def alg_order(g, v1, v2=None):
    p, s = topological_path(g, v1, v2, '+')
    if p is not None:
        return p*s


def alg_height(g, v1, v2=None):
    p, s = topological_path(g, v1, v2)
    if p is not None:
        return p*s

def father(g, vid, scale=-1, **kwds):
    """
    See aml.Father function.
    """
    edge_type = g.property('edge_type')

    et = kwds.get('EdgeType','*')
    rt = kwds.get('RestrictedTo', 'NoRestriction')
    ci = kwds.get('ContainedIn')

    current_scale = g.scale(vid)
    if scale <= 0 or scale == current_scale:
        p = g.parent(vid)
    elif scale < current_scale:
        vid = g.complex_at_scale(vid)
        p = g.parent(vid)
    else:
        vid = g.component_roots_at_scale(vid, scale=scale).next()
        p = g.parent(vid)

    if et != '*':
        if edge_type.get(vid) != et:
            return None


    if rt != 'NoRestriction':
        if rt == 'SameComplex':
            if g.complex(p) != g.complex(vid):
                return None
        elif rt == 'SameAxis':
            if edge_type[vid] == '+':
                return None

    if ci is not None:
        c_scale = g.scale(ci)
        if g.complex_at_scale(vid, scale=c_scale) != g.complex_at_scale(p, scale=c_scale) != ci:
            return None
        
    return p

def successor(g, vid, **kwds):
    """
    TODO: see aml.Successor doc string.
    """
    edge_type = g.property('edge_type')

    rt = kwds.get('RestrictedTo', 'NoRestriction')
    ci = kwds.get('ContainedIn')

    son = None
    for v in g.children(vid):
        if edge_type.get(v) == '<':
            son = v
            break
    else:
        return None

    if rt == 'SameComplex':
        if g.complex(son) != g.complex(vid):
            return None

    if ci is not None:
        c_scale = g.scale(ci)
        if g.complex_at_scale(vid, scale=c_scale) != g.complex_at_scale(son, scale=c_scale) != ci:
            return None

    return son

    
def predecessor(g, vid, **kwds):
    return father(g, vid, **kwds)

def root(g, vid, RestrictedTo='NoRestriction', ContainedIn=None):
    """
    TODO: see aml.Root doc string.
    """
    edge_type = g.property('edge_type')

    rt = RestrictedTo
    ci = ContainedIn

    v_current = vid
    for v in ancestors(g, vid):
        if rt == 'SameComplex':
            if g.complex(v) != g.complex(vid):
                break
        v_current = v

    return v_current


def location(g, vid, **kwds):
    """TODO: see doc aml.Location.
    """
    scale = kwds.get('Scale')
    ci = kwds.get('ContainedIn')

    if not scale or scale < 0:
        scale = g.max_scale()

    current_scale = g.scale(vid)
    return father(g, vid, scale=scale, ContainedIn=ci)


def sons(g, vid, **kwds):
    """TODO: see doc aml.sons.
    """
    et = kwds.get('EdgeType','*')
    rt = kwds.get('RestrictedTo', 'NoRestriction')
    ci = kwds.get('ContainedIn')
    scale = kwds.get('Scale')

    edge_type = g.property('edge_type')

    current_scale = g.scale(vid)
    if not scale or scale < 0:
        scale = current_scale
    
    if scale < current_scale:
        vid = g.complex_at_scale(vid, scale = scale)
    elif scale > current_scale:
        vid = g.component_roots_at_scale(vid, scale=scale).next()
    children = g.children(vid)
    
    if et != '*':
        children = (v for v in children if edge_type[v] == et)
    if ci is not None:
        c_scale = g.scale(ci)
        children = (v for v in children if g.complex_at_scale(v) == ci)

    return list(children)

def full_ancestors(g, v1, **kwds):
    " Return the vertices from v1 to the root. "
    edge_type = g.property('edge_type')
    et = kwds.get('EdgeType','*')
    rt = kwds.get('RestrictedTo', 'NoRestriction')
    ci = kwds.get('ContainedIn')

    v = v1
    if ci is not None:
        c_scale = g.scale(ci)

    while v is not None:
        if et != '*' and edge_type.get(v) != et:
            break

        if rt == 'SameComplex':
            if g.complex(v) != g.complex(v1):
                break
        elif rt == 'SameAxis':
            if edge_type.get(v) == '+':
                break
        if ci and g.complex_at_scale(v, scale=c_scale) != ci:
            break
        yield v
        v = g.parent(v)

def axis(g, vtx_id, scale=-1, **kwds):
    """TODO: see aml doc
    """
    edge_type = g.property('edge_type')

    rt = kwds.get('RestrictedTo', 'NoRestriction')
    ci = kwds.get('ContainedIn')

    for v in ancestors(g, vtx_id):
        if edge_type.get(v) == '+':
            break
    return local_axis(g, v, scale=scale, **kwds)

                
def descendants(g, vtx_id, scale=-1, **kwds):
    """TODO: see aml doc
    """
    edge_type = g.property('edge_type')

    et = kwds.get('EdgeType','*')
    rt = kwds.get('RestrictedTo', 'NoRestriction')
    ci = kwds.get('ContainedIn')

    if ci is not None:
        c_scale = g.scale(ci)

    vtx_id = vertex_at_scale(g, vtx_id, scale)

    v = vtx_id

    if rt == 'SameComplex':
        complex = g.complex(vtx_id)

    def visitor(v):
        if et in ['<', '+'] and et != edge_type.get(v, et):
            return False
        if rt == 'SameComplex':
            if g.complex(v) != complex:
                return False
        elif rt == 'SameAxis' and edge_type.get(v) == '+':
                return False

        if ci and g.complex_at_scale(v, scale=c_scale) != ci:
            return False
        return True


    return traversal.pre_order_with_filter(g, vtx_id, pre_order_filter=visitor)
        
def extremities(g, vid, **kwds):
    """ TODO see aml doc
    Implement the method more efficiently...
    """
    vertices = set(descendants(g,vid, **kwds))
    for v in vertices:
        if g.is_leaf(v):
            yield v
        else:
            for vtx in g.children(v):
                if vtx in vertices:
                    break
            else:
                yield v

def local_axis(g, vtx_id, scale=-1, **kwds):
    """ 
    Return a sequence of vertices connected by '<' edges. 
    The first element of the sequence is vtx_id.
    """

    edge_type = g.property('edge_type')

    et = kwds.get('EdgeType','*')
    rt = kwds.get('RestrictedTo', 'NoRestriction')
    ci = kwds.get('ContainedIn')

    vtx_id = vertex_at_scale(g, vtx_id, scale)

    if ci is not None:
        c_scale = g.scale(ci)

    
    v = vtx_id
    while v is not None:
        yield v
        vtx = v; v = None
        for vid in g.children(vtx):
            if edge_type.get(vid) == '<':
                v = vid

                if rt == 'SameComplex':
                    if g.complex(v) != g.complex(vtx_id):
                        v = None
                if ci and g.complex_at_scale(v, scale=c_scale) != ci:
                    v = None

def vertex_at_scale(g, vtx_id, scale):
    if scale <= 0:
        return vtx_id

    current_scale = g.scale(vtx_id)
    if scale < current_scale:
        vtx_id = g.complex_at_scale(vtx_id, scale=scale)
    elif scale > current_scale:
        vtx_id = g.component_roots_at_scale(vtx_id, scale=scale).next()
    return vtx_id

def trunk(g, vtx_id, scale=-1, **kwds):

    rt = kwds.get('RestrictedTo', 'NoRestriction')
    ci = kwds.get('ContainedIn')

    vtx_id = vertex_at_scale(g, vtx_id, scale)

    v = root(g, vtx_id, RestrictedTo=rt, ContainedIn=ci)

    return local_axis(g, v, scale, **kwds)
