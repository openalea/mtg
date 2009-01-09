# -*- python -*-
# -*- coding: utf-8 -*-
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
    sign = 1
    if v2 is None:
        return ancestors(g,v1), sign

    l1= list(ancestors(g,v1))
    l2 = list(ancestors(g,v2))
    s1 = set(l1)
    s2 = set(l2)

    if s1 < s2:
        l1, l2 = l2, l1
        s1, s2 = s2, s1
        v1, v2 = v2, v1
        sign = -1
    elif not s1 > s2:
        # v1 is not an ancestor of v2 (resp v2, v1)
        return iter([]), 0
    
    return iter(l1[:l1.index(v2)]), sign

def edge_type(g,v):
    return g.property('edge_type').get(v)

def topological_path(g,v1, v2=None, edge_type=None):
    p, sign = path(g,v1,v2)
    if sign == 0:
        return None

    if edge_type is None:
        return sum(1 for v in p)
    else: 
        return sum(1 for v in p if edge_type(g,v)==edge_type)
        
def order(g, v1, v2=None):
    return topological_path(g, v1, v2, '+')

def rank(g, v1, v2=None):
    return topological_path(g, v1, v2, '<')

def height(g, v1, v2=None):
    return topological_path(g, v1, v2 )

