# -*- python -*-
#
#       OpenAlea.mtg
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.pradal.at.cirad.fr>
#
#
#    Copyright (C) 2006-2011 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
###############################################################################
"""
This module provides functions to convert 
MTG to and from other matrix formats.

The code comes from NetworkX.


"""

def to_scipy_sparse_matrix(g, vertexlist=None, dtype=None, 
                           weight='weight', format='csr'):
    """Return the graph adjacency matrix as a SciPy sparse matrix.

    Parameters
    ----------
    g : graph
        The MTG used to construct the NumPy matrix.

    vertexlist : list, optional
       The rows and columns are ordered according to the nodes in `vertexlist`.
       If `vertexlist` is None, then the ordering is produced by g.vertices().

    dtype : NumPy data-type, optional
        A valid NumPy dtype used to initialize the array. If None, then the
        NumPy default is used.

    weight : string or None   optional (default='weight')
        The edge attribute that holds the numerical value used for 
        the edge weight.  If None then all edge weights are 1.

    format : str in {'bsr', 'csr', 'csc', 'coo', 'lil', 'dia', 'dok'} 
        The type of the matrix to be returned (default 'csr').  For
        some algorithms different implementations of sparse matrices
        can perform better.  See [1]_ for details.

    Returns
    -------
    M : SciPy sparse matrix
       Graph adjacency matrix.

    Notes
    -----
    The matrix entries are populated using the edge attribute held in
    parameter weight. When an edge does not have that attribute, the
    value of the entry is 1.

    For multiple edges the matrix values are the sums of the edge weights.

    When `vertexlist` does not contain every node in `G`, the matrix is built
    from the subgraph of `G` that is induced by the nodes in `vertexlist`.

    Uses coo_matrix format. To convert to other formats specify the
    format= keyword.

    Examples
    --------
    >>> G = nx.MultiDiGraph()
    >>> G.add_edge(0,1,weight=2)
    >>> G.add_edge(1,0)
    >>> G.add_edge(2,2,weight=3)
    >>> G.add_edge(2,2)
    >>> S = nx.to_scipy_sparse_matrix(G, vertexlist=[0,1,2])
    >>> print(S.todense())
    [[0 2 0]
     [1 0 0]
     [0 0 4]]

    References
    ----------
    .. [1] Scipy Dev. References, "Sparse Matrices",
       http://docs.scipy.org/doc/scipy/reference/sparse.html
    """
    try:
        from scipy import sparse
    except ImportError:
        raise ImportError(\
          "to_scipy_sparse_matrix() requires scipy: http://scipy.org/ ")

    if vertexlist is None:
        vertexlist = g.vertices(scale=g.max_scale())
    nlen = len(vertexlist)
    if nlen == 0:
        raise Exception("Graph has no nodes or edges")

    if len(vertexlist) != len(set(vertexlist)):
        msg = "Ambiguous ordering: `vertexlist` contained duplicates."
        raise Exception(msg)

    index = dict(list(zip(vertexlist,list(range(nlen)))))
    if len(vertexlist) < 2:
        row,col,data=[],[],[]
    else:
        row,col,data=list(zip(*((index[g.parent(vid)],index[vid],1)
                           for vid in vertexlist
                           if g.parent(vid) in index and vid in index)))
    M = sparse.coo_matrix((data,(row,col)),shape=(nlen,nlen), dtype=dtype)

    try:
        return M.asformat(format)
    except AttributeError:
        raise Exception("Unknown sparse matrix format: %s"%format)

