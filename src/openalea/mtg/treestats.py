# -*- coding: utf-8 -*-
# -*- python -*-
#
#       OpenAlea.mtg.stat
#
#       Copyright 2008-2009 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.pradal.at.cirad.fr>
#                       Thomas Cokelaer <thomas.cokelaer@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
''' This module implements methods to create statistical sequences from an MTG.

:Principles:
    

:Algorithm:


:Examples:


:TODO: 
    - Extract sequence identifier as a property and add it as input of the sequence
    - explicit identifier for sequence (e.g. year of growth or date of observation)

'''
from itertools import chain

from openalea.tree_statistic.trees import etrees
from openalea.mtg import algo
from openalea.mtg.traversal import pre_order2_with_filter

def extract_trees(g, scale, visitor=None, variable_funcs=[], variable_names=[], **kwds):
    ''' Extract a tree from an MTG.

    :Parameters:

    - `g`: an MTG
    - `scale`: the scale at which trees are to be extracted
    - `visitor`: function of vids to decide which vertices are not added to the tree
    - `variable_funcs`: a list of functions to compute each property
    - `variable_names`: a list property names

    :Return:

    - a Trees object from the openalea.tree_statistic.trees module
    If variable_funcs is empty and variable_names is not empty,
    variable_names will be used to define the properties.
    If both variable_funcs and variable_names are empty,
    the MTG property_names will be used to define the properties.

    :Example:

    ::

    '''
    # used default mtg properties if no particular properties are given
    if len(variable_funcs) == 0:
        if len(variable_names) == 0:
            # use g.properties
            for p in g.property_names():
                if p not in ['label', 'edge_type'] and not p.startswith('_'):
                    variable_funcs += [lambda vid: g.property(p).get(vid)]
                    variable_names += [str(p)]
        else:
            # use g.properties in variable_names
            property_names = [s for s in g.property_names()]
            for p in variable_names:
                if not(p in property_names):
                    msg = "Property " + str(p) + " not present in MTG"
                    raise ValueError(msg)
                else:
                    variable_funcs += [lambda vid: g.property(p).get(vid)]
    elif len(variable_names) == 0:
        for p in range(len(variable_funcs)):
            variable_names += ["Variable" + str(p)]

    # list of roots
    roots = g.roots(scale=scale)
    # Some vertices may be descendants of roots, not be filtered,
    # but have their parent filtered. Thus, they should be considered
    # as roots
    if visitor is None:
        visitor = lambda v: True

    roots = [v for v in g.vertices(scale=scale) if visitor(v) and (not(g.parent(v) and visitor(g.parent(v))))]


    def props(vid):
        '''Extract the properties for the Tree.'''
        return [ f(vid) for f in variable_funcs]

    def build_tree(vids):
        """Build a Tree from a list of vertices"""
        root = vids[0]
        nb_vertices = len(vids)
        tree_root = 0
        mtg2tree = {}
        t = etrees.Tree(props(root), nb_vertices, tree_root)

        # Root management
        for vid in vids:
            edge_type = g.edge_type(vid)
            v = t.AddVertex(props(vid))
            mtg2tree[vid] = v
            if vid != root:
                t.AddEdge(mtg2tree[g.parent(vid)],v, edge_type)
        return t, mtg2tree

    trees = []
    mappings = [] # List of mapping between Tree id and MTG id
    for vid_root in roots:
        l = list(pre_order2_with_filter(g, vid_root, pre_order_filter=visitor))
        lf = [v for v in l if visitor(v) and g.scale(v) == scale]
        if lf:
            t, m = build_tree(lf)
            trees.append(t)
            mappings.append(m)

    forest = etrees.Trees(trees, attribute_names=variable_names)
    forest._SetMTGVidDictionary(mappings)

    return forest


