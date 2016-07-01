# -*- python -*-
#
#       OpenAlea.mtg
#
#       Copyright 2008-2011 INRIA - CIRAD - INRA  
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
"""This module provides functions to read / write mtg data structure."""


from mtg import *
from tulip import *
tlp.initTulipLib()
tlp.loadPlugins()
from traversal import iter_mtg, iter_mtg_with_filter



def save_tulip(g, name='tulip.tlp', properties=None):
    ''' Save an MTG into a Tulip format.

    :Parameters:
        - `g` is an MTG
        - `name` a file to save the graph

    .. todo::
        All the properties have to be saved like:
            - complex, parent
            - MTG properties
    '''
    nodes = {}
    edges = {}

    # set the label
    root_g = tlp.newGraph()
    tg = tlp.newSubGraph(root_g, 'MTG')

    labels = root_g.getStringProperty('label')
    _label = g.property('label')

    scales = root_g.getIntegerProperty('scale')
    ids = root_g.getIntegerProperty('id')
    complexes = root_g.getIntegerProperty('complex')
    parents = root_g.getIntegerProperty('parent')

    max_scale = g.max_scale()
    
    for vid in g.vertices_iter(scale=max_scale):
        n = tg.addNode()
#X         n.id = vid
        nodes[vid] = n

        labels.setNodeValue(n, _label.get(vid,str(vid)))
        scales.setNodeValue(n, max_scale)
        ids.setNodeValue(n, vid)
        cid = g.complex(vid)
        if cid: 
            complexes.setNodeValue(n, cid)
        pid = g.parent(vid)
        if pid:
            parents.setNodeValue(n, g.parent(vid))
    


    for vid in g.vertices_iter(scale=max_scale):
        pid = g.parent(vid)
        if pid:
            edge = tg.addEdge(nodes[pid], nodes[vid])
            edges[vid] = edge
            labels.setEdgeValue(edge, g.edge_type(vid))

    # create the metanodes by grouping together the components

    #for scale in range(max_scale-1,0,-1):
    scale = max_scale-1
    for vid in g.vertices_iter(scale=scale):
        complex_subgraph = tg.inducedSubGraph([nodes[cid] for cid in g.components_at_scale_iter(vid, scale=max_scale)])
    """
    for scale in range(max_scale-1,0,-1):
        for vid in g.vertices(scale=scale):
            metanode = tg.createMetaNode( [nodes[cid] for cid in g.components(vid)], 
                       False, False)
#X             metanode.id = vid
            nodes[vid] = metanode
            if vid in _label:
                labels.setNodeValue(metanode, _label[vid])
            scales.setNodeValue(metanode, scale)
            ids.setNodeValue(metanode, vid)
            cid = g.complex(vid)
            if cid: 
                complexes.setNodeValue(metanode, cid)
            pid = g.parent(vid)
            if pid:
                parents.setNodeValue(metanode, g.parent(vid))

        for vid in g.vertices(scale=scale):
            pid = g.parent(vid)
            if pid:
                edge = tg.addEdge(nodes[pid], nodes[vid])
                edges[vid] = edge
                labels.setEdgeValue(edge, g.edge_type(vid))


    # create all the trees at each scales
    scale_graph = root_g
    for scale in range(1, max_scale+1):
        scale_graph = tlp.newSubGraph(scale_graph, 'Scale %d'%scale)
        for vid in g.vertices(scale=scale):
            scale_graph.addNode(nodes[vid])
            if vid in edges:
                scale_graph.addEdge(edges[vid])
    """

    # Size: Auto Sizing
#X     viewSize =  root_g.getSizeProperty("viewSize")
#X     root_g.computeSizeProperty('Auto Sizing', viewSize)

    # Layout: Improved Walker
    #   * orientation: up to down (2)

#X     dataSet = tlp.getDefaultPluginParameters("Improved Walker", root_g)
#X     dataSet["orientation"].setCurrent(1)
    # get a reference to the default layout property
#X     viewLayout = root_g.getLayoutProperty("viewLayout")
#X     root_g.computeLayoutProperty("Improved Walker", viewLayout, dataSet)

    # Compute a color based on a metric
#X     viewMetric = root_g.getDoubleProperty("viewMetric")
#X     root_g.computeMetricProperty("Improved Walker", viewLayout, dataSet)

    for p in properties:
        if 'Size' in p:
            my_prop = root_g.getSizeProperty(p)
        elif 'Layout' in p:
            my_prop = root_g.getLayoutProperty(p)
        f = properties[p]
        for vid in g:
            if vid in nodes:
                value = f(g, vid)
                if value:
                    my_prop.setNodeValue(nodes[vid], f(g, vid))


    tlp.saveGraph(root_g,name)


