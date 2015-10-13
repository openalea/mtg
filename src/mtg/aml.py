# -*- python -*-
# -*- coding: utf-8 -*-
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
Interface to use the new MTG implementation with the old AMAPmod interface.

.. testsetup:: *

    from openalea.mtg.aml import *
    from openalea.mtg  import MTG

"""
__docformat__ = "restructuredtext"

import openalea.mtg.mtg as mtg
from openalea.mtg.io import read_mtg_file
import openalea.mtg.algo as algo

# Current graph which is a global variable.
_g = None

def MTG(filename):
    """
    MTG constructor.

    Builds a MTG from a coding file (text file) containing the description of one or several plants.

    :Usage:

    ::

        MTG(filename)

    :Parameters:

        - `filename` (str): name of the coding file describing the mtg

    :Returns:

        If the parsing process succeeds, returns an object of type :func:`MTG`.
        Otherwise, an error is generated, and the formerly active `MTG` remains active.

    :Side Effect:

        If the :func:`MTG` is built, the new :func:`MTG` becomes the active :func:`MTG` (i.e. the :func:`MTG` implicitly
        used by other functions such as :func:`Father()`, :func:`Sons()`, :func:`VtxList()`, ...).

    :Details:

        The parsing process is approximatively proportional to the number of components
        defined in the coding file.

    :Background:

        MTG is an acronyme for Multiscale Tree Graph.

    .. seealso:: :func:`Activate` and all :mod:`openalea.mtg.aml` functions.
    """
    global _g
    _g = read_mtg_file(filename)
    return _g

def Activate(g):
    """
    Activate a MTG already loaded into memory

    All the functions of the MTG module use an implicit MTG argument
    which is defined as the active MTG.

    This function activates a MTG already loaded into memory which thus becomes
    the implicit argument of all functions of module MTG.

    :Usage:

    .. code-block:: python

        >>> Activate(g)

    :Parameters:

        - `g`: MTG to be activated

    :Details:

        When several MTGs are loaded into memory, only one is active at a time.
        By default, the active MTG is the last MTG loaded using function :func:`MTG`.

        However, it is possible to activate an MTG already loaded using function :func:`Activate`
        The current active MTG can be identified using function :func:`Active()`.

    :Background:

        :func:`MTG`

    .. seealso:: :func:`MTG`

    """
    global _g
    _g = g
    return _g


def Active():
    """Returns the active MTG.

    If no MTG is loaded into memory, None is returned.

    :Usage:

    .. code-block:: python

        >>> Active()

    :Returns:

        - :func:`MTG`

    :Details:

        When several MTGs are loaded into memory, only one is active at a time.
        By default, the active MTG is the last MTG loaded using function :func:`MTG`.
        However, it is possible to activate an MTG already loaded using function :func:`Activate`.
        The current active MTG can be identified using function :func:`Active`.

    .. seealso:: :func:`MTG`, :func:`Activate`.
    """
    global _g
    return _g


def MTGRoot():
    """Returns the root vertex of the MTG.

    It is the only vertex at scale 0 (the coarsest scale).

    :Usage:

    .. code-block:: python

        >>> MTGRoot()

    :Returns:

        - vtx identifier

    :Details:

        This vertex is the complex of all vertices from scale 1. It is a mean to refer to the entire database.


    .. seealso:: :func:`MTG`, :func:`Complex`, :func:`Components`, :func:`Scale`.
    """
    global _g
    return _g.root


def VtxList(Scale=-1):
    """	
    Array of vertices contained in a MTG

    The set of all vertices in the :func:`MTG` is returned as an array.
    Vertices from all scales are returned if no option is used.
    The order of the elements in this array is not significant.

    :Usage:

    .. code-block:: python

        >>> VtxList()
        >>> VtxList(Scale=2)

    :Optional Parameters:

        - `Scale` (int): used to select components at a particular scale.

    :Returns:

        - list of vid

    :Background:

        :func:`MTGs`

    .. seealso:: :func:`MTG`, :func:`Scale`, :func:`Class`, :func:`Index`.
    """
    global _g
    return _g.vertices(scale=Scale)

################################################################################
# Feature functions
################################################################################
def Label(v):
    """Label of a vertex

    :Usage:

        >>> Label(v) #doctest: +SKIP

    :Parameters:

        - `vid` (int) : vertex of the active MTG

    :Returns:

        The class and Index of the vertex (str).

    .. seealso:: :func:`MTG`, :func:`Index`, :func:`Class`
    """
    if isinstance(v, list):
        return [ (Class(x)+str(Index(x))) for x in v]
    else:
        return Class(v)+str(Index(v))


def Class(vid):
    """
    Class of a vertex

    The :func:`Class` of a vertex is a feature always defined and independent of time
    (like the index).
    It is represented by an alphabetic character in upper or lower case
    (lower cases characters are considered different from upper cases).
    The label of a vertex is the string defined by the concatenation
    of its class and its index.
    The label thus provides general information about a vertex and
    enables us to encode the plant components.

    :Usage:

        >>> Class(v)

    :Parameters:

        - `vid` (int) : vertex of the active MTG

    :Returns:

        The class of the vertex.

    .. seealso:: :func:`MTG`, :func:`Index`, :func:`Scale`.
    """
    global _g
    labels = _g.property('label')
    label = labels.get(vid, '')
    if label:
        return label[0]
    else:
        return ''


def Index(vid):
    """
    Index of a vertex

    The :func:`Index` of a vertex is a feature always defined and independent of time
    (like the index).
    It is represented by a non negative integer.
    The label of a vertex is the string defined by the concatenation
    of its class and its index.
    The label thus provides general information about a vertex and
    enables us to encode the plant components.

    :Usage:

        >>> Index(v)

    :Parameters:

        - `vid` (int) : vertex of the active MTG

    :Returns:

        int

    .. seealso:: :func:`MTG`, :func:`Class`, :func:`Scale`
    """
    global _g
    indices = _g.property('index')
    return indices.get(vid, vid)

def Scale(vid):
    """
    Scale of a vertex

    Returns the scale at which is defined the argument.

    :Usage:

        >>> Scale(vid)

    :Parameters:

        - `vid` (int) : vertex of the active MTG
        - `vid` (PlantFrame) : a PlantFrame object computed on the active MTG
        - `vid` (LineTree) : a LineTree computed on a PlantFrame representing the active MTG

    :Returns:

        int

    .. seealso:: :func:`MTG`, :func:`ClassScale`, :func:`Class`, :func:`Index`.

    """
    global _g
    return _g.scale(vid)

def Feature(vid, fname, date=None):
    """
    Extracts the attributes of a vertex.

    Returns the value of the attribute `fname` of a vertex in a `MTG`.

    If the value of an attribute is not defined in the coding file, the value None is returned.

    :Usage:

    .. code-block:: python

        Feature(vid, fname)
        Feature(vid, fname, date)

    :Parameters:

        - vid (int) : vertex of the active MTG.
        - fname (str) : name of the attribute (as specified in the coding file).
        - date (date) : (for a dynamic `MTG`) date at which the attribute of the vertex is considered.

    :Returns:

        int, str, date or float

    :Details:

        If for a given attribute, several values are available(corresponding to different dates),
        the date of interest must be specified as a third attribute.

        This date must be a valid date appearing in the coding file for a considered vertex.
        Otherwise `None` is returned.

    :Background:

        MTGs and Dynamic MTGs.

    .. todo:: specify the format of `date`

    .. seealso:: :func:`MTG`, :func:`Class`, :func:`Index`, :func:`Scale`.

    """
    global _g
    return _g.property(fname).get(vid)

def ClassScale(c):
    """
    Scale at which appears a given class of vertex

    Every vertex is associated with a unique class.
    Vertices from a given class only appear at a given scale
    which can be retrieved using this function.

    :Usage: 

    .. code-block:: python

        ClassScale(c)

    :Parameters:

        - `c` (str) : symbol of the considered class

    :Returns:

        int

    .. seealso:: :func:`MTG`, :func:`Class`, :func:`Scale`, :func:`Index`.

    """
    # non optimal way of writing  ClassScale function (loop is surely useless)
    global _g
    for x in _g.vertices():
        if Class(x) == c:
            return Scale(x)

def EdgeType(v1, v2):
    """
    Type of connection between two vertices.

    Returns the symbol of the type of connection between two vertices (either `<` or `+`).
    If the vertices are not connected, None is returned.

    :Usage:

    .. code-block:: python

        EdgeType(v1, v2)

    :Parameters:

        - v1 (int) : vertex of the active MTG
        - v2 (int) : vertex of the active MTG

    :Returns:

        '<' (successor), '+' (branching) or `None`

    .. image:: ../user/mtg_edgetype.png

    .. seealso:: :func:`MTG`, :func:`Sons`, :func:`Father`.

    """
    global _g
    if _g.parent(v1) == v2:
        v1, v2 = v2, v1

    return _g.property('edge_type').get(v2)

def Defined(vid):
    """
    Test whether a given vertex belongs to the active MTG.

    :Usage:

    .. code-block:: python

        Defined(v)

    :Parameters:

        - v (int) : vertex of the active MTG

    :Returns:

        True or False

    .. seealso:: :func:`MTG`.
    """
    global _g
    return vid in _g


def Order(v1, v2=None):
    """
    Order of a vertex in a graph.

    The order of a vertex (`v2`) with respect to another vertex (`v1`)
    is the number of edges of either type '+' that must be crossed
    when going from `v1` to `v2` in the graph. This is thus a non negative integer
    which corresponds to the "botanical order".

    When the function only has one argument `v1`, the order of `v1` correspond
    to the order of `v1` with respect to the root of the branching system containing `v1`.

    :Usage:

    .. code-block:: python

        Order(v1)
        Order(v1, v2)

    :Parameters:

        - v1 (int) : vertex of the active MTG
        - v2 (int) : vertex of the active MTG

    :Returns:

        int

    .. note::

        When the function takes two arguments, the order of the arguments is not important
        provided that one is an ancestor of the other.
        When the order is relevant, use function AlgOrder().

    .. warning:: 

        The value returned by function Order is 0 for trunks, 1 for branches etc.
        This might be different with some botanical conventions where 1 is the order of the
        trunk, 2 the order of branches, etc.

    .. seealso:: :func:`MTG`, :func:`Rank`, :func:`Height`, :func:`EdgeType`, :func:`AlgOrder`, :func:`AlgRank`, :func:`AlgHeight`.

    """
    global _g
    return algo.order(_g,v1,v2)

def Rank(v1, v2=None):
    """
    Rank of one vertex with respect to another one.

    This function returns the number of consecutive '<'-type edges between two components,
    at the same scale, and does not take into account the order of vertices v1 and v2.
    The result is a non negative integer.

    :Usage:

    .. code-block:: python

        Rank(v1)
        Rank(v1, v2)

    :Parameters:

        - v1 (int) : vertex of the active MTG
        - v2 (int) : vertex of the active MTG

    :Returns:

        `int`

        If v1 is not an ancestor of v2 (or vise versa) within the same botanical axis,
        or if v1 and v2 are not defined at the same scale, an error value Undef id returned.

    .. seealso:: :func:`MTG`, :func:`Order`, :func:`Height`, :func:`EdgeType`, :func:`AlgRank`, :func:`AlgHeight`, :func:`AlgOrder`.

    """
    global _g
    return algo.rank(_g,v1,v2)

def Height(v1, v2=None):
    """
    Number of components existing between two components in a tree graph.

    The height of a vertex (`v2`) with respect to another vertex (`v1`)
    is the number of edges (of either type '+' or '<') that must be crossed
    when going from `v1` to `v2` in the graph.

    This is a non-negative integer. When the function has only one argument `v1`,
    the height of `v1` correspond to the height of `v1`with respect
    to the root of the branching system containing `v1`.

    :Usage:

    .. code-block:: python

        Height(v1)
        Height(v1, v2)

    :Parameters:

        - v1 (int) : vertex of the active MTG
        - v2 (int) : vertex of the active MTG

    :Returns:

        int

    .. note::

        When the function takes two arguments, the order of the arguments is not important
        provided that one is an ancestor of the other. When the order is relevant, use
        function `AlgHeight`.

    .. seealso:: :func:`MTG`, :func:`Order`, :func:`Rank`, :func:`EdgeType`, :func:`AlgHeight`, :func:`AlgHeight`, :func:`AlgOrder`.

    """
    global _g
    return algo.height(_g, v1, v2)


def AlgOrder(v1, v2):
    """
    Algebraic value defining the relative order of one vertex with respect to another one.

    This function is similar to function `Order(v1, v2)` : it returns the number of `+`-type edges
    between two components, at the same scale, but takes into account the order of vertices
    `v1` and `v2`.

    The result is positive if `v1` is an ancestor of `v2`,
    and negative if `v2` is an ancestor of `v1`.

    :Usage:

    .. code-block:: python

        AlgOrder(v1, v2)

    :Parameters:

        - v1 (int) : vertex of the active MTG.
        - v2 (int) : vertex of the active MTG.

    :Returns:

        int

        If `v1` is not an ancestor of `v2` (or vise versa), or if `v1` and `v2` are not defined
        at the same scale, an error value None is returned.


    .. seealso:: :func:`MTG`, :func:`Rank`, :func:`Order`, :func:`Height`, :func:`EdgeType`, :func:`AlgHeight`, :func:`AlgRank`.
    """
    global _g
    return algo.alg_order(_g, v1, v2)

def AlgRank(v1, v2):
    """
    Algebraic value defining the relative rank of one vertex with respect to another one.

    This function is similar to function `Rank(v1, v2)` : it returns the number of `<`-type edges
    between two components, at the same scale, but takes into account the order of vertices
    `v1` and `v2`.

    The result is positive if `v1` is an ancestor of `v2`,
    and negative if `v2` is an ancestor of `v1`.

    :Usage:

    .. code-block:: python

        AlgRank(v1, v2)

    :Parameters:

        - v1 (int) : vertex of the active MTG.
        - v2 (int) : vertex of the active MTG.

    :Returns:

        int

        If `v1` is not an ancestor of `v2` (or vise versa), or if `v1` and `v2` are not defined
        at the same scale, an error value None is returned.

    .. seealso:: :func:`MTG`, :func:`Rank`, :func:`Order`, :func:`Height`, :func:`EdgeType`, :func:`AlgHeight`, :func:`AlgOrder`.

    """
    global _g
    return algo.alg_rank(_g, v1, v2)

def AlgHeight(v1, v2):
    """
    Algebraic value defining the number of components between two components.

    This function is similar to function `Height(v1, v2)` : it returns the number of components
    between two components, at the same scale, but takes into account the order of vertices
    `v1` and `v2`.

    The result is positive if `v1` is an ancestor of `v2`,
    and negative if `v2` is an ancestor of `v1`.

    :Usage:

    .. code-block:: python

        AlgHeight(v1, v2)

    :Parameters:

        - v1 (int) : vertex of the active MTG.
        - v2 (int) : vertex of the active MTG.

    :Returns:

        int

        If `v1` is not an ancestor of `v2` (or vise versa), or if `v1` and `v2` are not defined
        at the same scale, an error value None is returned.

    .. seealso:: :func:`MTG`, :func:`Rank`, :func:`Order`, :func:`Height`, :func:`EdgeType`, :func:`AlgOrder`, :func:`AlgRank`.

    """
    global _g
    return algo.alg_height(_g, v1, v2)


################################################################################
# Functions for moving in MTGs
################################################################################

def Father(v, EdgeType='*', RestrictedTo='NoRestriction', ContainedIn=None, Scale = -1):
    """
    Topological father of a given vertex.

    Returns the topological father of a given vertex. And `None` if the father does not exist.
    If the argument is not a valid vertex, `None` is returned.

    :Usage:

    .. code-block:: python

        Father(v)
        Father(v, EdgeType='<')
        Father(v, RestrictedTo='SameComplex')
        Father(v, ContainedIn=complex_id)
        Father(v, Scale=s)

    :Parameters:

        v (int) : vertex of the active MTG

    :Optional Parameters:

        If no optional argument is specified,  the function returns the topological father
        of the argument (vertex that bears or precedes to the vertex passed as an argument).

        It may be usefull in some cases to consider that the function only applies to a
        subpart of the MTG (e.g. an axis).

        The following options enables us to specify such restrictions:

        - EdgeType (str) : filter on the type of edge that connect the vertex to its father.

          Values can be '<', '+', and '*'. Values '*' means both '<' and '+'.
          Only the vertex connected with the specified type of edge will be considered.

        - RestrictedTo (str) : filter defining a subpart of the MTG where the father
          must be considered. If the father is actually outside this subpart,
          the result is `None`. Possible subparts are defined using keywords in
          ['SameComplex', 'SameAxis', 'NoRestriction'].

          For instance, if `RestrictedTo` is set to 'SameComplex', :func:`Father(v)` returns a
          defined vertex only if the father `f` of `v` existsin the MTG and if `v` and `f`
          have the same complex.

        - ContainedIn (int) : filter defining a subpart of the MTG where the father
          must be considered. If the father is actually outside this subpart,
          the result is `None`.

          In this case, the subpart of the MTG is made of the vertices
          that composed `composite_id` (at any scale).

        - Scale (int) : the scale of the considered father. Returns the vertex from scale `s`
          which either bears and precedes the argument.

          The scale `s` can be lower than the argument's (corresponding to a question such as
          'which axis bears the internode?') or greater
          (e.g. 'which internodes bears this annual shoot?').

    :Returns:

        the vertex id of the Father (int)

    .. seealso:: :func:`MTG`, :func:`Defined`, :func:`Sons`, :func:`EdgeType`, :func:`Complex`, :func:`Components`.

    """

    global _g

    if EdgeType not in ['+', '<', '*']:
        raise Exception('Invalid argument %s. Value of EdgeType is "<", "+" or "*".'%EdgeType)

    if RestrictedTo not in ['SameComplex', 'SameAxis', 'NoRestriction']:
        raise Exception('Invalid argument %s. Value of RestrictedTo is SameComplex, SameAxis, NoRestriction .'%RestrictedTo)

    return algo.father(_g, v, scale=Scale, EdgeType=EdgeType, RestrictedTo=RestrictedTo, ContainedIn=ContainedIn)

def Successor(v, RestrictedTo='NoRestriction', ContainedIn=None):
    """
    Vertex that is connected to a given vertex by a '<' edge type (i.e. in the same botanical axis).

    This function is equivalent to Sons(v, EdgeType='<')[0].
    It returns the vertex that is connected to a given vertex by a '<' edge type
    (i.e. in the same botanical axis).
    If many such vertices exist, an arbitrary one is returned by the function.
    If no such vertex exists, None is returned.

    :Usage:

    .. code-block:: python

        Successor(v)

    :Parameters:

        - v1 (int) : vertex of the active MTG

    :Optional Parameters:

        - RestrictedTo (str): cf. Father
        - ContainedIn (int): cf. Father

    :Returns:

        Returns vertex's id (int)


    :Examples:

    .. code-block:: python

        >>> Sons(v)
        [3, 45, 47, 78, 102]
        >>> Sons(v, EdgeType='+') # set of vertices borne by v
        [3, 45, 47, 102]
        >>> Sons(v, EdgeType-> '<') # set of successors of v
        [78]
        >>> Successor(v)
        78

    .. seealso:: :func:`MTG`, :func:`Sons`, :func:`Predecessor`.
    """
    global _g
    return algo.successor(_g, v, RestrictedTo=RestrictedTo, ContainedIn=ContainedIn)


def Predecessor(v, **kwds):
    """
    Father of a vertex connected to it by a '<' edge

    This function is equivalent to Father(v, EdgeType-> '<').
    It thus returns the father (at the same scale) of the argument
    if it is located in the same botanical.
    If it does not exist, None is returned.

    :Usage:

    .. code-block:: python

        Predecessor(v)

    :Parameters:

        - v (int) : vertex of the active MTG

    :Optional Parameters:

        - RestrictedTo (str): cf. `Father`
        - ContainedIn (int): cf. `Father`

    :Returns:

        return the vertex id (int)


    :Examples:

    .. code-block:: python

        >>> Predecessor(v)
        7
        >>> Father(v, EdgeType='+')
        >>> Father(v, EdgeType-> '<')
        7

    .. seealso:: :func:`MTG`, :func:`Father`, :func:`Successor`.
    """
    return Father(v, EdgeType='<', **kwds)

def Root(v, RestrictedTo='*', ContainedIn=None):
    """
    Root of the branching system containing a vertex

    This function is equivalent to Ancestors(v, EdgeType='<')[-1].
    It thus returns the root of the branching system containing the argument.
    This function never returns None.

    :Usage:

    .. code-block:: python

        Root(v)

    :Parameters:

        - v (int) : vertex of the active MTG

    :Optional Parameters:

        - RestrictedTo (str): cf. Father
        - ContainedIn (int): cf. Father

    :Returns:

       return vertex's id (int)


    :Examples:

    .. code-block:: python

        >>> Ancestors(v) # set of ancestors of v
        [102,78,35,33,24,12]
        >>> Root(v) # root of the branching system containing v
        12

    .. image:: ../user/mtg_root.png

    .. seealso:: :func:`MTG`, :func:`Extremities`.
    """
    global _g
    return algo.root(_g, v, RestrictedTo=RestrictedTo, ContainedIn=ContainedIn)

def Complex(v, Scale=-1):
    """
    Complex of a vertex.

    Returns the complex of `v`. The complex of a vertex `v` has a scale lower than `v` :
    `Scale(v)` - 1. In a MTG, every vertex except for the MTG root (cf. `MTGRoot`),
    has a uniq complex. None is returned if the argument is the MTG Root
    or if the vertex is undefined.

    :Usage:

    .. code-block:: python

        Complex(v)
        Complex(v, Scale=2)

    :Parameters:

        - `v` (int) : vertex of the active MTG

    :Optional Parameters:

        - `Scale` (int) : scale of the complex

    :Returns:

        Returns vertex's id (int)

    :Details:

        When a scale different form Scale(v)-1 is specified using the optional parameter
        `Scale`, this scale must be lower than that of the vertex argument.

    .. todo:: Complex(v, Scale=10) returns v why ? is this expected

    .. seealso:: :func:`MTG`, :func:`Components`.
    """
    global _g
    if Scale == -1 or Scale == _g.scale(v)-1:
        return _g.complex(v)
    else:
        return _g.complex_at_scale(v, scale=Scale)

def Location(v, Scale=-1, ContainedIn=None):
    """
    Vertex defining the father of a vertex with maximum scale.

    If no options are supplied, this function returns the vertex defining the father of a vertex
    with maximum scale (cf. :func:`Father`). If it does not exist, None is returned.
    If a scale is specified, the function is equivalent to `Father(v, Scale=s)`.

    :Usage:

    .. code-block:: python

        Location(v)
        Location(v, Scale=s)
        Location(v, ContainedIn=complex_id)

    :Parameters:

        - v (int) : vertex of the active MTG.

    :Optional Parameters:

        - Scale (int) : scale at which the location is required.
        - ContainedIn (int) : cf. :func:`Father`

    :Returns:
        Returns vertex's id (int)


    :Examples:

    .. code-block:: python

        >>> Father(v, EdgeType='+')
        7
        >>> Complex(v)
        4
        >>> Components(7)
        [9,19,23, 34, 77, 89]
        >>> Location(v)
        23
        >>> Location(v, Scale= Scale(v)+1)
        23
        >>> Location(v, Scale= Scale(v))
        7
        >>> Location(v, Scale= Scale(v)-1)
        4

    .. seealso::        :func:`MTG`, :func:`Father`.
    """
    global _g
    return algo.location(_g, v, Scale=Scale, ContainedIn=ContainedIn)

def Sons(v, RestrictedTo='NoRestriction', EdgeType='*', Scale=-1, ContainedIn= None):
    """
    Set of vertices born or preceded by a vertex

    The set of sons of a given vertex is returned as an array of vertices.
    The order of the vertices in the array is not significant.
    The array can be empty if there are no son vertices.

    :Usage:

    .. code-block:: python

        from openalea.mtg.aml import Sons
        Sons(v)
        Sons(v, EdgeType= '+')
        Sons(v, Scale= 3)

    :Parameters:

        - v (int) : vertex of the active MTG

    :Optional Parameters:

        - RestrictedTo (str) : cf. `Father`
        - ContainedIn (int) : cf. `Father`
        - EdgeType (str) : filter on the type of sons.
        - Scale (int) : set the scale at which sons are considered.

    :Returns:

        list(vid)

    :Details:

        When the option EdgeType is applied, the function returns the set of sons
        that are connected to the argument with the specified type of relation.
        
    .. note:: `Sons(v, EdgeType= '<')` is not equivalent to `Successor(v)`.
        The first function returns an array of vertices while the second function
        returns a vertex.

        The returned vertices have the same scale as the argument.
        However, coarser or finer vertices can be obtained by specifying
        the optional argument `Scale` at which the sons are considered.


    :Examples:

    .. code-block:: python

        >>> Sons(v)
        [3,45,47,78,102]
        >>>  Sons(v, EdgeType= '+') # set of vertices borne by v
        [3,45,47,102]
        >>>  Sons(v, EdgeType= '<') # set of successors of v on the same axis
        [78]

    .. seealso:: :func:`MTG`, :func:`Father`, :func:`Successor`, :func:`Descendants`.
    """
    global _g
    return algo.sons(_g, v, EdgeType=EdgeType, RestrictedTo=RestrictedTo, Scale=Scale, ContainedIn=ContainedIn)

def Ancestors(v, EdgeType='*', RestrictedTo='NoRestriction', ContainedIn=None):
    """
    Array of all vertices which are ancestors of a given vertex

    This function returns the array of vertices which are located
    before the vertex passed as an argument.
    These vertices are defined at the same scale as `v`. The array starts by `v`,
    then contains the vertices on the path from `v` back to the root (in this order)
    and finishes by the tree root.

    .. note:: The anscestor array always contains at least the argument vertex `v`.

    :Usage:

    .. code-block:: python

        Ancestors(v)

    :Parameters:

        - v (int) : vertex of the active MTG

    :Optional Parameters:

        - RestrictedTo (str): cf. `Father`
        - ContainedIn (int): cf. `Father`
        - EdgeType (str): cf. `Father`

    :Returns:

        list of vertices's id (int)


    :Examples:

    .. code-block:: python

        >>> v # prints vertex v
        78
        >>> Ancestors(v) # set of ancestors of v at the same scale
        [78,45,32,10,4]
        >>> list(reversed(Ancestors(v))) # To get the vertices in the order from the root to the vertex v
        [4,10,32,45,78]


    .. seealso:: :func:`MTG`, :func:`Descendants`.
    """
    global _g
    return list(algo.full_ancestors(_g, v, RestrictedTo=RestrictedTo,
                                          EdgeType=EdgeType,
                                          ContainedIn=ContainedIn))

def Descendants(v, EdgeType='*', RestrictedTo='NoRestriction', ContainedIn=None):
    """
    Set of vertices in the branching system borne by a vertex.

    This function returns the set of descendants of its argument as an array of vertices.
    The array thus consists of all the vertices, at the same scale as `v`,
    that belong to the branching system starting at `v`.
    The order of the vertices in the array is not significant.

    .. note:: The argument always belongs to the set of its descendants.

    :Usage:

    .. code-block:: python

        Descendants(v)

    :Parameters:

        - v (int) : vertex of the active MTG

    :Optional Parameters:

        - RestrictedTo (str): cf. `Father`
        - ContainedIn (int): cf. `Father`
        - EdgeType (str): cf. `Father`

    :Returns:

        list of int.


    :Examples:

    .. code-block:: python

        >>> v
        78
        >>> Sons(v) # set of sons of v
        [78,99,101]
        >>> Descendants(v) # set of descendants of v
        [78,99,101,121,133,135,156,171,190]

    .. image:: ../user/mtg_descendants.png

    .. seealso:: :func:`MTG`, :func:`Ancestors`.
    """
    global _g
    return list(algo.descendants(_g, v,
                                 RestrictedTo=RestrictedTo,
                                 ContainedIn=ContainedIn))

def Extremities(v, RestrictedTo='NoRestriction', ContainedIn=None):
    """
    Set of vertices that are the extremities of the branching system
    born by a given vertex.

    This function returns the extremities of the branching system defined by the argument
    as a list of vertices. These vertices have the same scale as `v` and their order in
    the list is not signifiant. The result is always a non empty array.

    :Usage:

    .. code-block:: python

        Extremities(v)

    :Properties:

        -  v (int) : vertex of the active MTG

    :Optional Parameters:

        - RestrictedTo (str): cf. :func:`Father`
        - ContainedIn (int): cf. :func:`Father`

    :Returns:

        list of vertices's id (int)


    :Examples:

    .. code-block:: python

        >>> Descendants(v)
        [3, 45, 47, 78, 102]
        >>> Extremities(v)
        [47, 102]

    .. seealso:: :func:`MTG`, :func:`Descendants`, :func:`Root`, :func:`MTGRoot`.
    """
    global _g
    return list(algo.extremities(_g, v, RestrictedTo=RestrictedTo, ContainedIn=ContainedIn))

def Components(v, Scale=-1):
    """
    Set of components of a vertex.

    The set of components of a vertex is returned as a list of vertices.
    If **s** defines the scale of **v**, components are defined at scale **s** + 1.
    The array is empty if the vertex has no components.
    The order of the components in the array is not significant.

    When a scale is specified using optional argument :arg:Scale,
    it must be necessarily greater than the scale of the argument.

    :Usage:

    .. code-block:: python

        Components(v)
        Components(v, Scale=2)

    :Parameters:

        - v (int) : vertex of the active MTG

    :Optional Parameters:

        - Scale (int) : scale of the components.

    :Returns:

        list of int

    .. image:: ../user/mtg_components.png

    .. seealso:: :func:`MTG`, :func:`Complex`.
    """
    global _g
    scale = _g.scale(v)
    components = []
    if Scale == -1 or scale == Scale:
        components = _g.components(v)
    elif scale < Scale:
        components = _g.components_at_scale(v, scale=Scale)
    return components

def ComponentRoots(v, Scale=-1):
    """
    Set of roots of the tree graphs that compose a vertex

    In a MTG, a vertex may have be decomposed into components.
    Some of these components are connected to each other, while other are not.
    In the most general case, the components of a vertex are organized into several tree-graphs.
    This is for example the case of a MTG containing the description of several plants:
    the MTG root vertex can be decomposed into tree graphs (not connected)
    that represent the different plants.
    This function returns the set of roots of these tree graphs at scale *Scale(v)+1*.
    The order of these roots is not significant.

    When a scale different from *Scale(v)+1* is specified using the optional argument :func:`Scale`,
    this scale must be greater than that of the vertex argument.

    :Usage:

    .. code-block:: python

        ComponentRoots(v)
        ComponentRoots(v, Scale=s)

    :Parameters:

        - v (int) : vertex of the active MTG

    :Optional Parameters:

        - Scale (str): scale of the component roots.

    :Returns:

        list of vertices's id (int)


    :Examples:

    .. code-block:: python

        >>> v=MTGRoot() # global MTG root
        0
        >>> ComponentRoots(v) # set of first vertices at scale 1
        [1,34,76,100,199,255]
        >>> ComponentRoots(v, Scale=2) # set of first vertices at scale 2
        [2,35,77,101,200,256]

    .. image:: ../user/mtg_componentroots.png

    .. seealso:: :func:`MTG`, :func:`Components`, :func:`Trunk`.
    """
    global _g
    return _g.component_roots_at_scale(v, scale=Scale)

def Path(v1, v2):
    """
    List of vertices defining the path between two vertices

    This function returns the list of vertices defining the path
    between two vertices that are in an ancestor relationship.
    The vertex `v1` must be an ancestor of vertex `v2`.
    Otherwise, if both vertices are valid, then the empty array is returned
    and if at least one vertex is undefined, None is returned.


    :Usage:

    .. code-block:: python

        Path(v1, v2)

    :Parameters:

        - `v1` (int) : vertex of the active MTG
        - `v2` (int) : vertex of the active MTG

    :Returns:

        list of vertices's id (int)


    :Examples:

    .. code-block:: python

        >>> v # print the value of v
        78
        >>> Ancestors(v)
        [78,45,32,10,4]
        >>> Path(10,v)
        [10,32,45,78]
        >>> Path(9,v) # 9 is not an ancestor of 78
        []

    .. note:: `v1` can be equal to `v2`.

    .. image:: ../user/mtg_path.png

    .. seealso:: :func:`MTG`, :func:`Axis`, :func:`Ancestors`.
    """
    global _g
    return list(algo.path(_g, v1, v2)[0])

def Axis(v, Scale=-1):
    """
    Array of vertices constituting a botanical axis

    An axis is a maximal sequence of vertices connected by '<'-type edges.
    Axis return the array of vertices representing the botanical axis which the argument v belongs to.
    The optional argument enables the user to choose the scale at which the axis decomposition is required.

    :Usage:

    .. code-block:: python

        Axis(v)
        Axis(v, Scale=s)

    :Parameters:

        - v (int) : Vertex of the active MTG

    :Optional Parameters:

        - Scale (str): scale at which the axis components are required.

    :Returns:

        list of vertices ids

    .. image:: ../user/mtg_axis.png

    .. seealso:: :func:`MTG`, :func:`Path`, :func:`Ancestors`.
    """
    global _g
    return list(algo.axis(_g, v, scale=Scale))

def Trunk(v, Scale=-1):
    """
    List of vertices constituting the bearing botanical axis of a branching system.

    Trunk returns the list of vertices representing the botanical axis defined as
    the bearing axis of the whole branching system defined by `v`.
    The optional argument enables the user to choose the scale at which the trunk should be detailed.

    :Usage:

    .. code-block:: python

        Trunk(v)
        Trunk(v, Scale= s)

    :Parameters:

        - `v` (int) : Vertex of the active MTG.

    :Optional Parameters:

        - `Scale` (str): scale at which the axis components are required.

    :Returns:

        list of vertices ids

    .. todo:: check the usage of the optional argument Scale

    .. seealso:: :func:`MTG`, :func:`Path`, :func:`Ancestors`, :func:`Axis`.
    """
    global _g
    return list(algo.trunk(_g, v, scale=Scale))
################################################################################
# Date functions
################################################################################

def DateSample(e1):
    """
    Array of observation dates of a vertex.

    Returns the set of dates at which a given vertex (passed as an argument)
    has been observed as an array of ordered dates.
    Options can be specified to define a temporal window and the total
    list of observation dates will be truncated according to the corresponding temporal window.

    :Usage:

    .. code-block:: python

        DateSample(v)
        DateSample(v, MinDate=d1, MaxDate=d2)

    :Parameters:

        - v (VTX) : vertex of the active MTG.

    :Optional Parameters:

        - MinDate (date) : defines a minimum date of interest.
        - MaxDate (date) : defines a maximum date of interest.

    :Returns:

        list of date

    .. seealso:: :func:`MTG`, :func:`FirstDefinedFeature`, :func:`LastDefinedFeature`, :func:`PreviousDate`, :func:`NextDate`.

    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def FirstDefinedFeature(e1, e2):
    """
    Date of first observation of a vertex.

    Returns the date `d` for which the attribute `fname` is defined for the first time
    on the vertex `v` passed as an argument. This date must be greater than
    the option `MinDate` and/or less than the maximum `MaxData` when specified.
    Otherwise the returned date is None.

    :Usage:

    .. code-block:: python

        FirstDefinedFeature(v, fname)
        FirstDefinedFeature(v, fname, MinDate=d1, MaxDate=d2)

    :Properties:

        - v (int) : vertex of the active MTG
        - fname (str) : name of the considered property

    :Optional Properties:

        - MinDate (date) : minimum date of interest.
        - MaxData (date) : maximum date of interest.

    :Returns:

        date

    .. seealso:: :func:`MTG`, :func:`DateSample`, :func:`LastDefinedFeature`, :func:`PreviousDate`, :func:`NextDate`.

    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def LastDefinedFeature(e1, e2):
    """
    Date of last observation of a given attribute of a vertex.

    Returns the date `d` for which the attribute `fname` is defined for the last time
    on the vertex `v` passed as an argument. This date must be greater than
    the option `MinDate` and/or less than the maximum `MaxData` when specified.
    Otherwise the returned date is None.

    :Usage:

    .. code-block:: python

        FirstDefinedFeature(v, fname)
        FirstDefinedFeature(v, fname, MinDate=d1, MaxDate=d2)

    :Properties:

        - v (int) : vertex of the active MTG
        - fname (str) : name of the considered property

    :Optional Properties:

        - MinDate (date) : minimum date of interest.
        - MaxData (date) : maximum date of interest.

    :Returns:

        date

    .. seealso:: :func:`MTG`, :func:`DateSample`, :func:`FirstDefinedFeature`, :func:`PreviousDate`, :func:`NextDate`.
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def NextDate(e1):
    """
    Next date at which a vertex has been observed after a specified date

    Returns the first observation date at which the vertex has been observed
    starting at date d and proceeding forward in time.
    None is returned if it does not exists.

    :Usage:

    .. code-block:: python

        NextDate(v, d)

    :Parameters:

        - v (int) : vertex of the active MTG.
        - d (date) : departure date.

    :Returns:

       date

    .. seealso:: :func:`MTG`, :func:`DateSample`, :func:`FirstDefinedFeature`, :func:`LastDefinedFeature`, :func:`PreviousDate`.
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def PreviousDate(e1):
    """
    Previous date at which a vertex has been observed after a specified date.

    Returns the first observation date at which the vertex has been observed
    starting at date d and proceeding backward in time.
    None is returned if it does not exists.

    :Usage:

    .. code-block:: python

        PreviousDate(v, d)

    :Parameters:

        - v (int) : vertex of the active MTG.
        - d (date) : departure date.

    :Returns:

       date

    .. seealso:: :func:`MTG`, :func:`DateSample`, :func:`FirstDefinedFeature`, :func:`LastDefinedFeature`, :func:`NextDate`.
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass




# Geometric interpretation
def PlantFrame(e1):
    """Use openalea.mtg.plantframe.PlantFrame insteead of this function"""
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def TopCoord(e1, e2):
    """
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def RelTopCoord(e1, e2):
    """
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def BottomCoord(e1, e2):
    """
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def RelBottomCoord(e1, e2):
    """
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def Coord(e1, e2):
    """
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def DressingData(e1):
    """Use openalea.mtg.dresser.DressingData instead of this function"""
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def Plot(e1):
    """
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def BottomDiameter(e1,e2):
    """
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def TopDiameter(e1,e2):
    """
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def Alpha(e1,e2):
    """
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def Beta(e1,e2):
    """
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def Length(e1,e2):
    """
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def VirtualPattern(e1):
    """
    """
    raise NotImplementedError("Function not yet implemented")
    global _g
    pass

def PDir(e1,e2):
    """
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass

def SDir(e1,e2):
    """
    """
    global _g
    raise NotImplementedError("Function not yet implemented")
    pass


