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

'''
Different utilities such as plot2D, plot3D, and so on...
'''

from openalea.mtg import *

def plot2d( mtg, image_name, scale=None ):
    """
    Compute an image of the tree via graphviz.
    """
    import pydot
    if scale is None:
        scale = max(mtg.scales())
    label = mtg.property('label')
    edges = mtg.iteredges(scale=scale)

    g= pydot.graph_from_edges(mtg.iteredges(scale=scale))

    ext= os.path.splitext(image_name)[1].strip('.')
    return g.write(image_name, prog='dot',format=ext)

