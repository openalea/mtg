# -*- coding: utf-8 -*-
# -*- python -*-
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

################################################################################
# Tree  and MTG Traversals
################################################################################

def pre_order(tree, vtx_id, complex=None, visitor_filter=None):
    ''' 
    Traverse a tree in a prefix way.
    (root then children)

    This is a non recursive implementation.
    '''
    if complex is not None and tree.complex(vtx_id) != complex:
        return

    edge_type = tree.property('edge_type')

    # 1. select first '+' edges
    successor = []
    yield vtx_id
    for vid in tree.children(vtx_id):
        if complex is not None and tree.complex(vid) != complex:
            continue
        if edge_type.get(vid) == '<':
            successor.append(vid)
            continue

        if visitor_filter and not visitor_filter.pre_order(tree, vid):
            continue

        for node in pre_order(tree, vid, complex):
            yield node

        if visitor_filter:
            visitor_filter.post_order(vid)


    # 2. select then '<' edges
    for vid in successor:
        for node in pre_order(tree, vid, complex):
            yield node
    
def post_order(tree, vtx_id, complex=None):
    ''' 
    Traverse a tree in a postfix way.
    (from leaves to root)
    '''
    if complex is not None and tree.complex(vtx_id) != complex:
        return
    for vid in tree.children(vtx_id):
        if complex is not None and tree.complex(vid) != complex:
            continue
        for node in post_order(tree, vid):
            yield node
    yield vtx_id

def traverse_tree(tree, vtx_id, visitor):
  ''' 
  Traverse a tree in a prefix or postfix way.
  
  We call a visitor for each vertex.
  This is usefull for printing, computing or storing vertices 
  in a specific order. 
  
  See boost.graph.
  '''

  yield visitor.pre_order(vtx_id)

  for v in tree.children(vtx_id):
     for res in traverse_tree(tree, v, visitor):
        yield res

  yield visitor.post_order(vtx_id)


class Visitor(object):
  ''' Used during a tree traversal. '''

  def pre_order(self, vtx_id): 
     pass

  def post_order(self, vtx_id): 
     pass


# old implementation
# Problem is the traversal traverse complex before components.
# def iter_mtg(mtg, vtx_id):
#     yield vtx_id
#     for vid in mtg.components(vtx_id):
#         for node in iter_mtg(mtg, vid):
#             yield node

def iter_scale(g, vtx_id, visited):
    if vtx_id is not None and vtx_id not in visited:
        for v in iter_scale(g, g._complex.get(vtx_id), visited):
            yield v
        visited[vtx_id] = True
        yield vtx_id

def iter_mtg(mtg, vtx_id):
    visited = {}
    loc = vtx_id
    while mtg._components.get(loc):
        loc = mtg._components[loc][0]
    vtx_id = loc

    for vid in pre_order(mtg, vtx_id):
        for node in iter_scale(mtg, vid, visited):
            yield node
        
def topological_sort(tree, vtx_id, visited = None):
    ''' 
    Topolofgical sort of a directed acyclic graph.

    This is a non recursive implementation.
    '''
    if visited is None:
        visited = {}

    yield vtx_id
    visited[vtx_id] = True
    for vid in g.out_neighbors(vtx_id):
        if vid in visited:
            continue
        for node in topological_sort(g, vid, visited):
            yield node

def pre_order_with_filter(tree, vtx_id, pre_order_filter=None, post_order_visitor=None):
    ''' 
    Traverse a tree in a prefix way.
    (root then children)

    This is a non recursive implementation.
    
    TODO: make the naming and the arguments more consistent and user friendly.
    pre_order_filter is a functor which has to return a boolean.
    If the return value is False, the vertex is not visited.
    Otherelse, some computation can be done.

    The post_order_visitor is used to execute, store, compute a function when the 
    tree rooted on the vertex has been visited.
    
    '''
    if pre_order_filter and not pre_order_filter(vtx_id):
        return

    edge_type = tree.property('edge_type')

    # 1. select first '+' edges
    successor = []
    yield vtx_id
    for vid in tree.children(vtx_id):
        if edge_type.get(vid) == '<':
            successor.append(vid)
            continue

        for node in pre_order_with_filter(tree, vid, pre_order_filter, post_order_visitor):
            yield node


    # 2. select then '<' edges
    for vid in successor:
        for node in pre_order_with_filter(tree, vid, pre_order_filter, post_order_visitor):
            yield node

    if post_order_visitor:
        post_order_visitor(vtx_id)
