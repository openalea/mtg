# -*- python -*-
#
#       OpenAlea.mtg
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.pradal.at.cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

import traversal
def layout2d(g, vid=None, origin=(0,0), property_name='position'):
	""" Compute 2d coordinates for each vertex.

	This method compute a 2D layout of a tree or a MTG at a specific scale.
	This will allow to plot tree in matplotlib for instance. 
	
    :Usage:

    .. code-block:: python

        >>> g.reindex()
        >>> g1 = g.reindex(copy=True)
        >>> mymap = dict(zip(list(traversal.iter_mtg2(g,g.root)), range(len(g))))
        >>> g2 = g.reindex(mapping=mymap, copy=True)

    :Optional Parameters:

        - `origin` : a 2D point for the root of the tree.
        - `property` (str) : Name of the property storing the 2D coordinates.

    :Returns:	

        - a MTG
	"""
	if vid is None:
		vid = g.root
		if hasattr(g, 'max_scale'):
			vid = g.component_roots_at_scale_iter(g.root, g.max_scale()).next()

	# Algorithm
	# 1. the y is defined by the Height of a node
	# 2. The x is computed using non intersecting bounding box

	y= {}
	vtxs = traversal.pre_order2(g,vid)
	vtxs.next()
	y[vid] = origin[1]
	for v in vtxs:
		y[v] = y[g.parent(v)]+1

	bbox = {}
	for v in traversal.post_order2(g,vid):
		children = g.children(v)
		if not children:
			bbox[v] = 1
		else:
			has_successor = sum(1 for cid in children if g.edge_type(cid)=='<') 
			bbox[v] = sum(bbox[cid] for cid in children)
			if not has_successor:
				bbox[v]+=1

	x ={}
	vtxs = traversal.pre_order2(g,vid)
	x[vid] = bbox[vid]/2

	for v in vtxs:
		_width = bbox[v]
		kids = g.children(v)
		successor = [cid for cid in kids if g.edge_type(cid)=='<']
		ramifs = [cid for cid in kids if g.edge_type(cid)=='+']
		_min = x[v]-1; _max = x[v]+1  
		for cid in successor:
			_x = x[cid] = x[v]
			width = bbox[cid]/2
			_min = _x-width-1
			_max = _x+width+1
		n = len(ramifs)/2
		for rid in reversed(ramifs[:n]):
			width = bbox[rid]
			_min -= width
			x[rid] = _min + width/2 
		for rid in ramifs[n:]:
			width = bbox[rid]
			x[rid] = _max + width/2 
			_max += width

	# TODO: The tree s not well proportionned becase we impose a constraint that the 
	# < is aligned to its parent

	position = dict((k, (x[k],y[k])) for k in y)
	g.properties()[property_name] = position

	return g


