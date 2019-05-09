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

import traversal, matrix
from random import random

def layout2d(g, vid=None, origin=(0,0), steps=(4,8), property_name='position'):
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
            vid = next(g.component_roots_at_scale_iter(g.root, g.max_scale()))

	# Algorithm
	# 1. the y is defined by the Height of a node
	# 2. The x is computed using non intersecting bounding box

    x_step, y_step = steps

    y= {}
    vtxs = traversal.pre_order2(g,vid)
    next(vtxs)
    y[vid] = origin[1]
    for v in vtxs:
        y[v] = y[g.parent(v)]+y_step

    bbox = {}
    for v in traversal.post_order2(g,vid):
        children = g.children(v)
        if not children:
            bbox[v] = 2*x_step
        else:
            has_successor = [cid for cid in children if g.edge_type(cid)=='<']
            # 2 is for symmetry
            bbox[v] = sum(bbox[cid] for cid in children)
            if not has_successor:
                bbox[v]+=2*x_step

    x ={}
    vtxs = traversal.pre_order2(g,vid)
    x[vid] = int(bbox[vid]/2.)

    for v in vtxs:
        _width = bbox[v]
        kids = g.children(v)
        successor = [cid for cid in kids if g.edge_type(cid)=='<']
        ramifs = [cid for cid in kids if g.edge_type(cid)=='+']
        _min = x[v]; _max = x[v]
        for cid in successor:
            _x = x[cid] = x[v]
            width = bbox[cid]
            _min = _x-max(1,width/2)-x_step
            _max = _x+max(1,width/2)+x_step

        weights = [bbox[rid] for rid in ramifs]

        def mean_ind(weights):
            left = bool(random()<0.5)
            mid= sum(weights)/2.
            total = 0
            n = 0
            for w in weights:
                if total+w <= mid:
                    total+= w
                else:
                    break
                n+=1

            if total-mid > 1 and left:
                n+=1
            if n == 0 and len(weights)>1:
                n+=1
            return n

        n = mean_ind(weights)
        for rid in reversed(ramifs[:n]):
            width = bbox[rid]
            x[rid] = _min - max(1,width/2)
            _min -= width
        for rid in ramifs[n:]:
            width = bbox[rid]
            x[rid] = _max + max(1,width/2)
            _max += width

	# TODO: The tree s not well proportionned because we impose a constraint that the
	# < is aligned to its parent

    position = dict((k, (x[k],y[k])) for k in y)
    g.properties()[property_name] = position

    return g


def simple_layout(g, vid=None, origin=(0,0), steps=(4,8), property_name='position', multiscale=True):
    """ Compute 2d coordinates for each vertex.

    This method compute a 2D layout of a tree or a MTG at a specific scale.
    This will allow to plot tree in matplotlib for instance.

    :Usage:

    .. code-block:: python

        >>> g = simple_layout(g)

    :Optional Parameters:

        - `origin` : a 2D point for the root of the tree.
        - `property` (str) : Name of the property storing the 2D coordinates.

    :Returns:

        - a MTG
    """

    def shuffle_post_order(tree, vtx_id):
        '''
        Traverse a tree in a postfix way.
        (from leaves to root)

        Same algorithm than post_order.
        The goal is to replace the post_order implementation.


        '''

        edge_type = tree.property('edge_type')

        def shuffle_children(vid):
            ''' Internal function to retrieve the children in a correct order:
                - Branch before successor.
            '''
            kids = tree.children(vid)
            plus = []
            successor = []
            for v in kids:
                if edge_type.get(v) == '<':
                    successor.append(v)
                else:
                    plus.append(v)
            n = len(plus)
            i = n/2
            if n%2!=0:
                left = int(random()<0.5)
                i += left
            child = plus[:i]+successor+plus[i:]

            return child

        visited = set([])

        queue = [vtx_id]

        # 1. select first '+' edges

        while queue:

            vtx_id = queue[-1]
            for vid in shuffle_children(vtx_id):
                if vid not in visited:
                    queue.append(vid)
                    break
            else: # no child or all have been visited
                yield vtx_id
                visited.add(vtx_id)
                queue.pop()

    if vid is None:
        vid = g.root
        if hasattr(g, 'max_scale'):
            vid = next(g.component_roots_at_scale_iter(g.root, g.max_scale()))

    # Algorithm
    # 1. the y is defined by the Height of a node
    # 2. The x is computed using non intersecting bounding box

    x_step, y_step = steps
    y= {}
    vtxs = traversal.pre_order2(g,vid)
    next(vtxs)
    y[vid] = origin[1]
    for v in vtxs:
        y[v] = y[g.parent(v)]+y_step

    def leaves(g, vid):
        for v in shuffle_post_order(g,vid):
            if g.is_leaf(v):
                yield v
    def successor(g, vid):
        for cid in g.children(vid):
            if g.edge_type(cid)=='<':
                return cid
        return

    x = {}
    x_pos = origin[0]

    for v in leaves(g,vid):
        x[v] = x_pos
        x_pos += x_step*10

    for v in shuffle_post_order(g,vid):
        if v in x:
            continue
        son_id = successor(g,v)
        if son_id:
            x[v] = x[son_id]
        else:
            children = g.children(v)
            x[v] = int(float(sum(x[cid] for cid in children)) / (len(children)))


    position = dict((k, (x[k],y[k])) for k in y)

    if multiscale:
        # get the position at the lower scales
        max_scale = g.scale(vid)

        for s in range(max_scale-1,0,-1):
            v_root = g.complex_at_scale(vid, scale=s)
            vtxs = traversal.pre_order2(g, v_root)
            for v in vtxs:
                comp_id = next(g.component_roots_at_scale_iter(v, scale=max_scale))
                position[v] = position[comp_id]

    g.properties()[property_name] = position

    return g


def fruchterman_reingold_layout(g,dim=2,k=None,
                                pos=None,
                                fixed=None,
                                iterations=50,
                                weight='weight',
                                scale=1.0):
    """Position nodes using Fruchterman-Reingold force-directed algorithm.

    Parameters
    ----------
    G : NetworkX graph

    dim : int
       Dimension of layout

    k : float (default=None)
       Optimal distance between nodes.  If None the distance is set to
       1/sqrt(n) where n is the number of nodes.  Increase this value
       to move nodes farther apart.


    pos : dict or None  optional (default=None)
       Initial positions for nodes as a dictionary with node as keys
       and values as a list or tuple.  If None, then nuse random initial
       positions.

    fixed : list or None  optional (default=None)
      Nodes to keep fixed at initial position.

    iterations : int  optional (default=50)
       Number of iterations of spring-force relaxation

    weight : string or None   optional (default='weight')
        The edge attribute that holds the numerical value used for
        the edge weight.  If None, then all edge weights are 1.

    scale : float (default=1.0)
        Scale factor for positions. The nodes are positioned
        in a box of size [0,scale] x [0,scale].


    Returns
    -------
    dict :
       A dictionary of positions keyed by node

    Examples
    --------
    >>> G=nx.path_graph(4)
    >>> pos=nx.spring_layout(G)

    # The same using longer function name
    >>> pos=nx.fruchterman_reingold_layout(G)
    """
    try:
        import numpy as np
    except ImportError:
        raise ImportError("fruchterman_reingold_layout() requires numpy: http://scipy.org/ ")

    max_scale = g.max_scale()
    vertexlist = g.vertices(scale=max_scale)
    if fixed is not None:
        nfixed=dict(list(zip(vertexlist,list(range(len(vertexlist))))))
        fixed=np.asarray([nfixed[v] for v in fixed])

    if pos is not None:
        pos_arr=np.asarray(np.random.random((len(vertexlist),dim)))
        for i,n in enumerate(vertexlist):
            if n in pos:
                pos_arr[i]=np.asarray(pos[n])
    else:
        pos_arr=None

    if len(vertexlist)==0:
        return {}
    if len(vertexlist)==1:
        return {vertexlist[0]:(1,)*dim}

    try:
        # Sparse matrix
        #if len(G) < 500:  # sparse solver for large graphs
        #    raise ValueError
        A=matrix.to_scipy_sparse_matrix(g,weight=weight,dtype='f')
        pos=_sparse_fruchterman_reingold(A,dim,k,pos_arr,fixed,iterations)
    except:
        A=matrix.to_numpy_matrix(G,weight=weight)
        pos=_fruchterman_reingold(A,dim,k,pos_arr,fixed,iterations)
    if fixed is None:
        pos=_rescale_layout(pos,scale=scale)
    return dict(list(zip(vertexlist,pos)))

spring_layout=fruchterman_reingold_layout

def _fruchterman_reingold(A, dim=2, k=None, pos=None, fixed=None,
                          iterations=50):
    # Position nodes in adjacency matrix A using Fruchterman-Reingold
    # Entry point for NetworkX graph is fruchterman_reingold_layout()
    try:
        import numpy as np
    except ImportError:
        raise ImportError("_fruchterman_reingold() requires numpy: http://scipy.org/ ")

    try:
        nnodes,_=A.shape
    except AttributeError:
        raise Exception(
            "fruchterman_reingold() takes an adjacency matrix as input")

    A=np.asarray(A) # make sure we have an array instead of a matrix

    if pos==None:
        # random initial positions
        pos=np.asarray(np.random.random((nnodes,dim)),dtype=A.dtype)
    else:
        # make sure positions are of same type as matrix
        pos=pos.astype(A.dtype)

    # optimal distance between nodes
    if k is None:
        k=np.sqrt(1.0/nnodes)
    # the initial "temperature"  is about .1 of domain area (=1x1)
    # this is the largest step allowed in the dynamics.
    t=0.1
    # simple cooling scheme.
    # linearly step down by dt on each iteration so last iteration is size dt.
    dt=t/float(iterations+1)
    delta = np.zeros((pos.shape[0],pos.shape[0],pos.shape[1]),dtype=A.dtype)
    # the inscrutable (but fast) version
    # this is still O(V^2)
    # could use multilevel methods to speed this up significantly
    for iteration in range(iterations):
        # matrix of difference between points
        for i in range(pos.shape[1]):
            delta[:,:,i]= pos[:,i,None]-pos[:,i]
        # distance between points
        distance=np.sqrt((delta**2).sum(axis=-1))
        # enforce minimum distance of 0.01
        distance=np.where(distance<0.01,0.01,distance)
        # displacement "force"
        displacement=np.transpose(np.transpose(delta)*\
                                  (k*k/distance**2-A*distance/k))\
                                  .sum(axis=1)
        # update positions
        length=np.sqrt((displacement**2).sum(axis=1))
        length=np.where(length<0.01,0.1,length)
        delta_pos=np.transpose(np.transpose(displacement)*t/length)
        if fixed is not None:
            # don't change positions of fixed nodes
            delta_pos[fixed]=0.0
        pos+=delta_pos
        # cool temperature
        t-=dt
        pos=_rescale_layout(pos)
    return pos


def _sparse_fruchterman_reingold(A, dim=2, k=None, pos=None, fixed=None,
                                 iterations=50):
    # Position nodes in adjacency matrix A using Fruchterman-Reingold
    # Entry point for NetworkX graph is fruchterman_reingold_layout()
    # Sparse version
    try:
        import numpy as np
    except ImportError:
        raise ImportError("_sparse_fruchterman_reingold() requires numpy: http://scipy.org/ ")
    try:
        nnodes,_=A.shape
    except AttributeError:
        raise Exception(
            "fruchterman_reingold() takes an adjacency matrix as input")
    try:
        from scipy.sparse import spdiags,coo_matrix
    except ImportError:
        raise ImportError("_sparse_fruchterman_reingold() scipy numpy: http://scipy.org/ ")
    # make sure we have a LIst of Lists representation
    try:
        A=A.tolil()
    except:
        A=(coo_matrix(A)).tolil()

    if pos==None:
        # random initial positions
        pos=np.asarray(np.random.random((nnodes,dim)),dtype=A.dtype)
    else:
        # make sure positions are of same type as matrix
        pos=pos.astype(A.dtype)

    # no fixed nodes
    if fixed==None:
        fixed=[]

    # optimal distance between nodes
    if k is None:
        k=np.sqrt(1.0/nnodes)
    # the initial "temperature"  is about .1 of domain area (=1x1)
    # this is the largest step allowed in the dynamics.
    t=0.1
    # simple cooling scheme.
    # linearly step down by dt on each iteration so last iteration is size dt.
    dt=t/float(iterations+1)

    displacement=np.zeros((dim,nnodes))
    for iteration in range(iterations):
        displacement*=0
        # loop over rows
        for i in range(A.shape[0]):
            if i in fixed:
                continue
            # difference between this row's node position and all others
            delta=(pos[i]-pos).T
            # distance between points
            distance=np.sqrt((delta**2).sum(axis=0))
            # enforce minimum distance of 0.01
            distance=np.where(distance<0.01,0.01,distance)
            # the adjacency matrix row
            Ai=np.asarray(A.getrowview(i).toarray())
            # displacement "force"
            displacement[:,i]+=\
                (delta*(k*k/distance**2-Ai*distance/k)).sum(axis=1)
        # update positions
        length=np.sqrt((displacement**2).sum(axis=0))
        length=np.where(length<0.01,0.1,length)
        pos+=(displacement*t/length).T
        # cool temperature
        t-=dt
        pos=_rescale_layout(pos)
    return pos

def _rescale_layout(pos,scale=1):
    # rescale to (0,pscale) in all axes

    # shift origin to (0,0)
    lim=0 # max coordinate for all axes
    for i in range(pos.shape[1]):
        pos[:,i]-=pos[:,i].min()
        lim=max(pos[:,i].max(),lim)
    # rescale to (0,scale) in all directions, preserves aspect
    for i in range(pos.shape[1]):
        pos[:,i]*=scale/lim
    return pos