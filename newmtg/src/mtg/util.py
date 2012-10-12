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

'''
Different utilities such as plot2D, plot3D, and so on...
'''

from openalea.mtg import *
from openalea.mtg.traversal import *

def mtg_plot(g, scales=1):
    import pydot

    uniq_scales = set(g._scale.values())

    #cluster2.set_bgcolor('#000fff')
    #pydot_graph = pydot.graph_from_edges(((f(x), f(y)) for x, y in g.iteredges(scale=scale)))
    callgraph = pydot.Dot(graph_type='digraph',fontname="Verdana")

    label = g.property('label')
    scale = g._scale

    for s in uniq_scales:
        print s


    #cluster2 = pydot.Cluster('U2')
    #cluster2.add_edge(pydot.Edge('I4', 'I5'))
    #callgraph.add_subgraph(cluster2)
    #callgraph.write_png('cluster.png')
    #if label:
    #    f = lambda id: label.get(id, str(id))
    #else:
    #    f = str

    callgraph.write_png('cluster.png')



def plot2d(g, image_name, scale=None, orientation=90 ):
    """Compute an image of the tree via graphviz.

    :Parameters:

        - `g` (int) : an MTG object
        - `image_name` (str) : output filename e.g. test.png

    :Optional parameters:

        - `scale` (int): represents the MTG's scale to look at (default max)
        - `orientation` (int): orientation angle (default 90)

    """
    import pydot
    if scale is None:
        scale = max(g.scales_iter())
    label = g.property('label')
    edges = g.iteredges(scale=scale)

    if label:
        f = lambda id: label.get(id, str(id))
    else:
        f = str
    pydot_graph = pydot.graph_from_edges(((f(x), f(y)) for x, y in g.iteredges(scale=scale)))

    # Attributes
    pydot_graph.set('orientation', orientation)

    ext = os.path.splitext(image_name)[1].strip('.')
    return pydot_graph.write(image_name, prog='dot',format=ext)


def plot3d( g, scale=None ):
    """
    Compute a 3d view of the MTG in a simple way:
      * sphere for the nodes and thin cylinder for the edges.
    """
    import openalea.plantgl.all as pgl

    if scale is None:
        scale = max(g.scales())
    
    # Vertex are sphere of radius 1/2
    # edge are cylinder of radius 1/6 and length 3
    points = {}
    edges = {}
    edge_type = g.property('edge_type')

    root_id = g.roots_iter(scale=scale).next()
    for vid in pre_order(g, root_id):
        parent = g.parent(vid)
        if parent is None:
            points[vid] = (0,0,0)
            edges = (0,0,3)
        else:
            et = edge_type[vid]
