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

'''
from vplants.sequence_analysis import *

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
    print vectors
    return Vectors(vectors, Identifiers=vids, **kwds)

def build_sequences(g, vid_sequences, variables=[], **kwds):
    ''' Extract a set of Vectors from an MTG.

    :Parameters:

    - `g`: an MTG
    - `vid_sequences`: a list of list ofvertex ids that belong to the MTG
      Each element of the lsit represents a sequence.
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
    vertex_ids = [vids for vids in vid_sequences if vids ]
    sequences = [[property_list(g, vid, variables) for vid in vids ] for vids in vertex_ids]
    print sequences
    return Sequences(sequences, VertexIdentifiers=vertex_ids)


