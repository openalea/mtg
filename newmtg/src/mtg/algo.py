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


def ancestors(g, v1):
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

def father(g, vid, scale= -1, **kwds):
    """
    See aml.Father function.
    """
    edge_type = g.property('edge_type')

    et = kwds.get('EdgeType','*')
    rt = kwds.get('RestrictedTo', 'NoRestriction')
    ci = kwds.get('ContainedIn')

    p = g.parent(vid)

    if et != '*':
        if edge_type[vid] != et:
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
        
    if scale != -1:
        p = g.complex_at_scale(p,scale)

    return p

def successor(g, vid, **kwds):
    raise NotImplementedError

def predecessor(g, vid, **kwds):
    raise NotImplementedError


