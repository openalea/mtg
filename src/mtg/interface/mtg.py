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

"""
This module provides multiscale tree concepts to form MTG interface.
"""

class MultiscaleTreeConcept(object):
    """
    Multiscale Tree Graph definition.
    """

    def set_root(self, vtx_id):
        '''
        Set the tree root.

        :Parameters:
            - `vtx_id`: The vertex identifier.
        '''
        pass

    def get_root(self): 
        '''
        Return the tree root.

        :Return: vertex identifier
        '''
        pass

    root= property( get_root, set_root )

    def parent(self, vtx_id):
        '''
        Return the parent of `vtx_id`.

        :Parameters:
            - `vtx_id`: The vertex identifier.

        :Return: vertex identifier
        '''
        pass

    def children(self, vtx_id):
        '''
        Return a vertex iterator

        :Parameters:
            - `vtx_id`: The vertex identifier.

        :Return: iter of vertex identifier
        '''

    def nb_children(self, vtx_id):
        '''
        Return the number of children

        :Parameters:
            - `vtx_id`: The vertex identifier.

        :Return: int
        '''

    def is_leaf(self, vtx_id):
        '''
        Test if `vtx_id` is a leaf.

        :Return: bool
        '''

  
