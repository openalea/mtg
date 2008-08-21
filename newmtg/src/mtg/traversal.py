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

################################################################################
# Tree  and MTG Traversals
################################################################################

def pre_order(tree, vtx_id, complex=None):
    ''' 
    Traverse a tree in a prefix way.
    (root then children)

    This is a non recursive implementation.
    '''
    if complex is not None and tree.complex(vtx_id) != complex:
        return

    yield vtx_id
    for vid in tree.children(vtx_id):
        if complex is not None and tree.complex(vid) != complex:
            continue
        for node in pre_order(tree, vid, complex):
            yield node
    
def post_order(tree, vtx_idcomplex=None):
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
  This is usefull for printing, cmputing or storing vertices 
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



def pre_order_scale(mtg, vtx_id):
    yield vtx_id
    for vid in mtg.components(vtx_id):
        for node in pre_order_scale(mtg, vid):
            yield node

iter_mtg = pre_order_scale

