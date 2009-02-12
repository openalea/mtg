
import os, sys

from openalea.mtg import *


g = MTG()
v = random_tree(g, g.root, 5, 1000)
g = random_mtg(g, 5)

# Question
# order: 

def ancestors(g, v1):
    " Return the vertices from v1 to the root. "
    v = v1
    while v is not None:
        yield v
        v = g.parent(v)

def path(g, v1, v2=None):
    if v2 is None:
        return ancestors(g,v1)

    l1= list(ancestors(g,v1))
    l2 = list(ancestors(g,v2))
    s1 = set(l1)
    s2 = set(l2)

    if s1 < s2:
        l1, l2 = l2, l1
        s1, s2 = s2, s1
        v1, v2 = v2, v1
    elif not s1 > s2:
        # v1 is not an ancestor of v2 (resp v2, v1)
        return iter([])
    
    return iter(l1[:l1.index(v2)])

def edge_type(g,v):
    return g.property('edge_type').get(v)

def order(g, v1, v2=None):
    return sum(1 for v in path(g,v1,v2) if edge_type(g,v)=='+')

def rank(g, v1, v2=None):
    return sum(1 for v in path(g,v1,v2) if edge_type(g,v)=='<')

def height(g, v1, v2=None):
    return sum(1 for v in path(g,v1,v2))
