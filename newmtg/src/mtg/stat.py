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
from itertools import chain, ifilter, imap

from openalea.sequence_analysis import *
from openalea.mtg import algo


class InvalidVariable(Exception):
    pass

class InvalidVertex(Exception):
    pass

def check_variables(g, variables):
    props = g.properties()
    for property_name in variables:
        if property_name not in props:
            raise InvalidVariable(property_name)

def check_vids(g, vids):
    for vid in vids:
        if vid not in g:
            raise InvalidVertex(vid)

def property_list(g, vid, variables):
    props = g.properties()
    return [props[variable][vid] for variable in variables] 

def extract_vectors(g, vids, variables=[], **kwds):
    ''' Extract a set of Vectors from an MTG.

    :Parameters:

    - `g`: an MTG
    - `vid`: a list of vertex ids that belong to the MTG
    - `variables`: a list of property names that represent the vectors variables.

    :Return:

    - a Vectors object

    :Example:

    ::

        length = g.property('Length')
        vids = [vid for vid in g.vertices(scale=2) if vid in length]
        vectors = extract_vectors(g, vids, ['Length'])

        # or an equivalent

        length = g.property('Length')
        vids = [vid for vid in g.vertices(scale=2) if vid in length]
        vectors = extract_vectors(g, vids, [length])

    '''
    check_variables(g, variables)
    #check_vids(g, vids)
    vectors = [property_list(g, vid, variables) for vid in vids]
    return Vectors(vectors, Identifiers=vids, **kwds)

def build_sequences(g, vid_sequences, variables=[], **kwds):
    ''' Extract a set of Vectors from an MTG.

    :Parameters:

    - `g`: an MTG
    - `vid_sequences`: a list of list ofvertex ids that belong to the MTG
      Each element of the lsit represents a sequence.
    - `variables`: a list of property names that represent the vectors variables.

    :Return:

    - a Sequence object

    :Example:

    ::

        length = g.property('Length')
        leaves = (vid for vid in g.vertices(scale=g.max_scale()) if g.is_leaf(vid))
        seqs = [list(reversed([vid for vid in algo.ancestors(g, lid) if vid in leaves])) for lid in leaves]

        sequences = build_sequences(g,seqs,['Length'])
    '''
    check_variables(g, variables)
    def predicate(v):
        return all(v in g.properties()[var] for var in variables)
    #check_vids(g, vids)
    vertex_ids = [vids for vids in vid_sequences if bool(vids and filter_sequence(vids,predicate)) ]
    sequences = [[property_list(g, vid, variables) for vid in vids ] for vids in vertex_ids]
    return Sequences(sequences, VertexIdentifiers=vertex_ids)

def extract_sequences(g, variables=[], vid=-1, scale=0, mode='axes', **kwds):
    ''' Implement different strategies to extract a set of vids.

    The different modes are:
        - extremities: seqs from root to leaves.
        - axes: split each sequence when a + is found
    '''
    if scale < 1: 
        scale = g.max_scale()
    if vid < 0:
        vid = g.root
    vids = g.component_roots_at_scale(vid, scale)

    if mode == 'extremities':
        seqs = extract_extremities(g, scale=scale, vid=vid, **kwds)
    else:
        seqs = extract_axes(g, scale=scale, vid=vid, **kwds)

    return build_sequences(g, seqs, variables=variables, **kwds)

def extract_extremities(g, scale=0, **kwds):
    if scale <= 0:
        vid = first_component_root(g,g.root)
        scale = g.scale(vid)

    vids = g.component_roots_at_scale_iter(g.root, scale=scale)
    leaves = chain.from_iterable(algo.extremities(g,vid) for vid in vids)

    seqs = [list(reversed([vid for vid in algo.ancestors(g,lid)])) for lid in leaves]
    return seqs

def extract_axes(g, scale=0, **kwds):
    vid = g.root
    if scale < 1:
        vid = first_component_root(g,g.root)
        scale = g.scale(vid)
    roots = g.component_roots_at_scale(vid, scale=scale)

    # Extract all the vertices with edge_type == '+'
    vids =roots+[vid for vid in g.vertices_iter(scale=scale) if g.edge_type(vid) == '+']
    seqs = [ list(algo.local_axis(g, vid, scale=scale, EdgeType='<')) for vid in vids]
    return seqs

def filter_sequence(seq, pred):
    """ Select a Sequence if only the predicate is true for each element.
    """
    ok = all(imap(pred, seq))
    return ok

def first_component_root(g, vid):

    vids = g.component_roots(vid)
    if vids:
        return first_component_root(g, vids[0])
    else:
        return vid



