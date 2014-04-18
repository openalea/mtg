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

from openalea.mtg.tree import *
from openalea.mtg.traversal import *

def check(tree):
    """ Traverse the tree to see if all the children have at most one parent.
    TODO
    """

    parents = tree._parent
    kids = tree._children

    sons = set(v for v in l for l in kids.itervalues()) 
    vtx = set(v for v in parents.itervalues() if v is not None)



def test_tree_api():
    tree = Tree()
    
    root = tree.root
    assert root is not None
    assert root == 0, 'default root id (%d) is not 0'%root

    # scale 1
    v1 = tree.add_child(root)
    v2 = tree.add_child(v1)
    assert len(tree) == 3

    v3 = tree.insert_parent(v2)
    assert len(tree) == 4

    tree.replace_parent(v2,v1)
    assert len(tree) == 4
    

