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
Interface to use the new MTG implementation with the old AMAPmod interface.
'''
__docformat__ = "restructuredtext"

import openalea.mtg.mtg as mtg
from openalea.mtg.io import read_mtg_file

# Current graph which is a global variable.
_g = None

def MTG(filename):
    """
    MTG constructor.

    Builds a MTG from a coding file (text file) containing the description of one or several plants.

    Usage
    -----
    .. python ::
        MTG(filename)

    Parameters
    ----------
        - `filename` (str): name of the coding file describing the mtg

    Returns
    -------
        If the parsing process succeeds, returns an object of type `MTG`.
        Otherwise, an error is generated, and the formerly active `MTG` remains active.

    Side Effect
    -----------
        If the `MTG` is built, the new `MTG` becomes the active `MTG` (i.e. the `MTG` implicitly 
        used by other functions such as `Father()`, `Sons()`, `VtxList()`, ...).

    Details
    -------
        The parsing process is approximatively proportional to the number of components 
        defined in the coding file.

    Background
    ----------
        MTG is an acronyme for Multiscale Tree Graph.

    See also
    --------
        `Sons`, `Father`, ...
    """
    return read_mtg_file(filename)

def Activate(g):
    """
    Activate a MTG already loaded into memory

    All the functions of the MTG module use an implicit MTG argument 
    which is defined as the "active MTG". 

    This function activates a MTG already loaded into memory which thus becomes 
    the implicit argument of all functions of module MTG.

    Usage
    -----
    .. python ::
        Activate(g)

    Parameters
    ----------
        - `g`: MTG to be activated

    Details
    -------
        When several MTGs are loaded into memory, only one is active at a time. 
        By default, the active MTG is the last MTG loaded using function MTG(). 

        However, it is possible to activate an MTG already loaded using function Activate(). 
        The current active MTG can be identified using function Active().

    Background
    ----------
        MTGs

    See Also
    --------
        `MTG`, `Active()`.
    """
    global _g
    _g = g
    return _g

def Active():
    """
    Returns the active MTG.
    
    If no MTG is loaded into memory, None is returned.

    Usage
    -----
      - `Active()`

    Returns
    -------
      - `MTG`

    Details
    -------
        When several MTGs are loaded into memory, only one is active at a time. 
        By default, the active MTG is the last MTG loaded using function `MTG()`. 
        However, it is possible to activate an MTG already loaded using function `Activate()`. 
        The current active MTG can be identified using function `Active()`.

    See Also
    --------
        - `MTG`, `Activate()`.
    """
    global _g
    return _g

def MTGRoot():
    """
    Returns the root vertex of the MTG.

    It is the only vertex at scale 0 (the coarsest scale).

    Usage
    -----
    .. python ::
        MTGRoot()

    Returns
    -------
        vtx identifier

    Details
    -------
        This vertex is the complex of all vertices from scale 1. It is a mean to refer to the entire database.

    Background
    ----------
        MTGs
    See Also
    --------
        `MTG`, `Complex`, `Components`, `Scale`.
    """
    global _g
    return _g.root

def VtxList(Scale=0):
    """	
    Array of vertices contained in a MTG

    The set of all vertices in the MTG is returned as an array. 
    Vertices from all scales are returned if no option is used. 
    The order of the elements in this array is not significant. 

    Usage
    -----
    .. python ::
        VtxList()
        VtxList(Scale=2)

    Optional Parameters
    -------------------
        Scale (INT) : used to select components at a particular scale.

    Returns
    -------
        list of vid

    Background
    ----------
        MTGs

    See Also
    --------
        `MTG`, `Scale`, `Class`, `Index`.
    """
    global _g
    return list(_g.vertices(scale=Scale))

################################################################################
# Feature functions
################################################################################

def Class(vid):
    """
    Class of a vertex

    The `Class` of a vertex is a feature always defined and independent of time 
    (like the index). 
    It is represented by an alphabetic character in upper or lower case 
    (lower cases characters are considered different from upper cases). 
    The label of a vertex is the string defined by the concatenation 
    of its class and its index. 
    The label thus provides general information about a vertex and 
    enables us to encode the plant components.

    Usage
    -----
    .. python ::
        Class(v)

    Parameters
    ----------
        - v (vtx_id) : vertex of the active MTG

    Returns
    -------
        str

    See Also
    --------
        `MTG`, `Index`.
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

    The `Index` of a vertex is a feature always defined and independent of time 
    (like the index). 
    It is represented by an by a non negative integer. 
    The label of a vertex is the string defined by the concatenation 
    of its class and its index. 
    The label thus provides general information about a vertex and 
    enables us to encode the plant components.

    Usage
    -----
    .. python ::
        Index(v)

    Parameters 
    ----------
        - v (vtx_id) : vertex of the active MTG

    Returns
    -------
        int

    See Also
    --------	
	`MTG`, `Class`.
    """
    global _g
    labels = _g.property('label')
    label = labels.get(vid, '')
    try:
        return int(label[1:])
    except:
        return vid

def Scale(vid):
    """
    Scale of a vertex

    Returns the scale at which is defined the argument.

    Usage
    -----
    .. python ::
        Scale(vid)

    Parameters
    ----------
        - `vid` (vtx identifier) : vertex of the active MTG
        - `vid` (PLANTFRAME) : PlantFrame computed on the active MTG
        - `vid` (LINETREE) : LineTree computed on a PlantFrame representing the active MTG

    Returns
    -------
        int

    See Also
    --------
        `MTG`, `ClassScale`, `Class`, `Index`.

    """
    global _g
    return _g.scale(vid)

def Feature(vid, fname, date=None):
    """
    Extracts the attributes of a vertex.

    Returns the value of the attribute `fname` of a vertex in a `MTG`. 

    If the value of an attribute is not defined in the coding file, the value None is returned.

    Usage
    -----
    .. python ::
        Feature(vid, fname)
        Feature(vid, fname, date)

    Parameters 
    ----------
        - vid (vtx_id) : vertex of the active MTG.
        - fname (str) : name of the attribute (as specified in the coding file).
        - date (date) : (for a dynamic `MTG`) date at which the attribute of the vertex is considered.

    Returns
    -------
        int, str, date or float

    Details
    -------
        If for a given attribute, several values are available(corresponding to different dates), 
        the date of interest must be specified as a third attribute.

        This date must be a valid date appearing in the coding file for a considered vertex.
        Otherwise `None` is returned.

    Background
    ----------
        MTGs and Dynamic MTGs.

    See Also
    --------	
        `MTG`, `Class`, `Index`, `Scale`.

    """
    global _g
    return _g.property(fname).get(vid)

def ClassScale(c):
    """
    Scale at which appears a given class of vertex

    Every vertex is associated with a unique class. 
    Vertices from a given class only appear at a given scale 
    which can be retrieved using this function.

    Usage
    -----
    .. python ::
        ClassScale(c)

    Parameters
    ----------
        - `c` (str) : symbol of the considered class

    Returns
    -------
        int

    See Also
    --------
        `MTG`, `Class`, `Scale`, `Index`.

    """
    # TODO
    pass

def EdgeType(v1, v2):
    """
    Type of connection between two vertices.

    Returns the symbol of the type of connection between two vertices (either `<` or `+`). 
    If the vertices are not connected, None is returned.

    Usage
    -----
    .. python ::
        EdgeType(v1, v2)

    Parameters
    ----------
        - v1 (vid) : vertex of the active MTG
        - v2 (vid) : vertex of the active MTG

    Returns
    -------
        '<' (successor), '+' (branching) or `None`

    See Also
    --------
        `MTG`, `Sons`, `Father`.

    """
    global _g
    if _g.parent(v1) == v2:
        v1, v2 = v2, v1

    return _g.property('edge_type').get(v2)

def Defined(v):
    """
    Test whether a given vertex belongs to the active MTG.

    Usage
    -----
        Defined(v)

    Parameters
    ----------
        v (vtx_id) : vertex of the active MTG

    Returns
    -------
    BOOL

    See Also
    --------
        `MTG`.
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

    Usage
    -----
    .. python ::
        Order(v1)
        Order(v1, v2)

    Parameters
    ----------
        - v1 (vtx_id) : vertex of the active MTG
        - v2 (vtx_id) : vertex of the active MTG

    Returns
    -------
        int
    
    Note
    ----
        When the function takes two arguments, the order of the arguments is not important 
        provided that one is an ancestor of the other. 
        When the order is relevant, use function AlgOrder().

        Warning: the value returned by function Order is 0 for trunks, 1 for branches etc. 
        This might be different with some botanical conventions where 1 is the order of the 
        trunk, 2 the order of branches, etc.
    
    See Also
    --------
        `MTG`, `Rank`, `Height`, `EdgeType`, `AlgOrder`, `AlgRank`, `AlgHeight`.

    """
    # TODO
    global _g
    pass

def Rank(v1, v2=None):
    """
    Rank of one vertex with respect to another one.

    This function returns the number of consecutive '<'-type edges between two components, 
    at the same scale, and does not take into account the order of vertices v1 and v2. 
    The result is a non negative integer. 

    Usage
    -----
    .. python ::
        Rank(v1)
        Rank(v1, v2)

    Parameters
    ----------
        - v1 (vtx_id) : vertex of the active MTG
        - v2 (vtx_id) : vertex of the active MTG

    Returns
    -------
        `int`

        If v1 is not an ancestor of v2 (or vise versa) within the same botanical axis, 
        or if v1 and v2 are not defined at the same scale, an error value Undef id returned.

    See Also
    --------
        `MTG`, `Order`, `Height`, `EdgeType`, `AlgRank`, `AlgHeight`, `AlgOrder`.

    """
    # TODO
    global _g
    return 

def Height(v1, v2=None):
    """
    Number of components existing between two components in a tree graph.

    The height of a vertex (`v2`) with respect to another vertex (`v1`) 
    is the number of edges (of either type '+' or '<') that must be crossed 
    when going from `v1` to `v2` in the graph.

    This is a non-negative integer. When the function has only one argument `v1`, 
    the height of `v1` correspond to the height of `v1`with respect 
    to the root of the branching system containing `v1`.

    Usage
    -----
    .. python ::
        Height(v1)
        Height(v1, v2)

    Parameters
    ----------
        - v1 (vtx_id) : vertex of the active MTG
        - v2 (vtx_id) : vertex of the active MTG

    Returns
    -------
        int

    Note
    ----
        When the function takes two arguments, the order of the arguments is not important
        provided that one is an ancestor of the other. When the order is relevant, use
        function `AlgHeight`.

    See Also
    --------
        `MTG`, `Order`, `Rank`, `EdgeType`, `AlgHeight`, `AlgHeight`, `AlgOrder`.

    """
    # TODO
    global _g
    return 


def AlgOrder(v1, v2):
    """
    Algebraic value defining the relative order of one vertex with respect to another one.

    This function is similar to function `Order(v1, v2)` : it returns the number of `+`-type edges 
    between two components, at the same scale, but takes into account the order of vertices 
    `v1` and `v2`. 

    The result is positive if `v1` is an ancestor of `v2`, 
    and negative if `v2` is an ancestor of `v1`.

    Usage
    -----
    .. python ::
        AlgOrder(v1, v2)
    
    Parameters
    ----------
        - v1 (vtx_id) : vertex of the active MTG.
        - v2 (vtx_id) : vertex of the active MTG.

    Returns
    -------
        int

        If `v1` is not an ancestor of `v2` (or vise versa), or if `v1` and `v2` are not defined 
        at the same scale, an error value None is returned.


    See Also
    --------
        `MTG`, `Rank`, `Order`, `Height`, `EdgeType`, `AlgHeight`, `AlgRank`.
    """
    global _g
    return

def AlgRank(e1, e2):
    """
    Algebraic value defining the relative rank of one vertex with respect to another one.

    This function is similar to function `Rank(v1, v2)` : it returns the number of `<`-type edges 
    between two components, at the same scale, but takes into account the order of vertices 
    `v1` and `v2`. 

    The result is positive if `v1` is an ancestor of `v2`, 
    and negative if `v2` is an ancestor of `v1`.

    Usage
    -----
    .. python ::
        AlgRank(v1, v2)

    Parameters
    ----------
        - v1 (vtx_id) : vertex of the active MTG.
        - v2 (vtx_id) : vertex of the active MTG.

    Returns
    -------
        int

        If `v1` is not an ancestor of `v2` (or vise versa), or if `v1` and `v2` are not defined 
        at the same scale, an error value None is returned.

    See Also
    --------
        `MTG`, `Rank`, `Order`, `Height`, `EdgeType`, `AlgHeight`, `AlgOrder`.

    """
    global _g
    pass

def AlgHeight(e1, e2):
    """
    Algebraic value defining the number of components between two components.

    This function is similar to function `Height(v1, v2)` : it returns the number of components 
    between two components, at the same scale, but takes into account the order of vertices 
    `v1` and `v2`. 

    The result is positive if `v1` is an ancestor of `v2`, 
    and negative if `v2` is an ancestor of `v1`.

    Usage
    -----
    .. python ::
        AlgHeight(v1, v2)
    
    Parameters
    ----------
        - v1 (vtx_id) : vertex of the active MTG.
        - v2 (vtx_id) : vertex of the active MTG.

    Returns
    -------
        int

        If `v1` is not an ancestor of `v2` (or vise versa), or if `v1` and `v2` are not defined 
        at the same scale, an error value None is returned.

    See Also
    --------
        `MTG`, `Rank`, `Order`, `Height`, `EdgeType`, `AlgOrder`, `AlgRank`.

    """
    global _g
    pass


################################################################################
# Functions for moving in MTGs
################################################################################

def Father(v, EdgeType='*', RestrictedTo='NoRestriction', ContainedIn=None):
    """
    Topological father of a given vertex.
    
    Returns the topological father of a given vertex. And `None` if the father does not exist.
    If the argument is not a valid vertex, `None` is returned.

    Usage
    -----
    .. python ::
        Father(v)
        Father(v, EdgeType='<')
        Father(v, RestrictedTo='SameComplex')
        Father(v, ContainedIn=complex_id)
        Father(v, Scale=s)

    Parameters
    ----------
        v (vtx_id) : vertex of the active MTG

    Optional Parameters
    -------------------
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

          For instance, if `RestrictedTo` is set to 'SameComplex', `Father(v)` returns a
          defined vertex only if the father `f` of `v` existsin the MTG and if `v` and `f`
          have the same complex.

        - ContainedIn (vtx_id) : filter defining a subpart of the MTG where the father 
          must be considered. If the father is actuallyoutside this subpart, 
          the result is `None`. 
    
          In this case, the subpart of the MTG is made of the vertices 
          that composed `composite_id` (at any scale).

        - Scale (int) : the scale of the considered father. Returns the vertex from scale `s`
          which either bears and precedes the argument. 
            
          The scale `s` can be lower than the argument's (corresponding to a question such as 
          'which axis bears the internode?') or greater 
          (e.g. 'which internodes bears this annual shoot?').

    Returns
    -------
        vtx_id

    See Also
    --------
        `MTG`, `Defined`, `Sons`, `EdgeType`, `Complex`, `Components`.

    """
    global _g
    pass

def Successor(v, RestrictedTo='NoRestriction', ContainedIn=None):
    """
    Vertex that is connected to a given vertex by a '<' edge type (i.e. in the same botanical axis).
    
    This function is equivalent to Sons(v, EdgeType='<')[0]. 
    It returns the vertex that is connected to a given vertex by a `<' edge type 
    (i.e. in the same botanical axis). 
    If many such vertices exist, an arbitrary one is returned by the function. 
    If no such vertex exists, None is returned.

    Usage
    -----
    .. python ::
        Successor(v)

    Parameters
    ----------
        - v1 (vtx_id) : vertex of the active MTG

    Optional Parameters
    -------------------
        - RestrictedTo (str): cf. Father
        - ContainedIn (vtx_id): cf. Father

    Returns
    -------
        vtx_id

    See Also
    --------
        `MTG`, `Sons`, `Predecessor`.

    Examples
    --------
        >>> Sons(v) 
        [3,45,47,78,102]
        >>> Sons(v, EdgeType='+') # set of vertices borne by v
        [3,45,47,102]
        >>> Sons(v, EdgeType-> '<') # set of successors of v
        [78]
        >>> Successor(v)
        78
    """
    global _g
    pass

def Predecessor(e1):
    """
    """
    global _g
    pass

def Root(e1):
    """
    """
    global _g
    pass

def Complex(e1):
    """
    """
    global _g
    pass

def Location(e1):
    """
    """
    global _g
    pass

def Sons(e1):
    """
    """
    global _g
    pass

def Ancestors(e1):
    """
    """
    global _g
    pass

def Descendants(e1):
    """
    """
    global _g
    pass

def Extremities(e1):
    """
    """
    global _g
    pass

def Components(e1):
    """
    """
    global _g
    pass

def Componentroots(e1):
    """
    """
    global _g
    pass

def Path(e1, e2):
    """
    """
    global _g
    pass

def Axis(e1):
    """
    """
    global _g
    pass

def Trunk(e1):
    """
    """
    global _g
    pass

################################################################################
# Date functions
################################################################################

def DateSample(e1):
    """
    """
    global _g
    pass

def FirstDefinedFeature(e1, e2):
    """
    """
    global _g
    pass

def LastDefinedFeature(e1, e2):
    """
    """
    global _g
    pass

def NextDate(e1):
    """
    """
    global _g
    pass

def PreviousDate(e1):
    """
    """
    global _g
    pass




# Geometric interpretation
def PlantFrame(e1):
    """
    """
    global _g
    pass

def TopCoord(e1, e2):
    """
    """
    global _g
    pass

def RelTopCoord(e1, e2):
    """
    """
    global _g
    pass

def BottomCoord(e1, e2):
    """
    """
    global _g
    pass

def RelBottomCoord(e1, e2):
    """
    """
    global _g
    pass

def Coord(e1, e2):
    """
    """
    global _g
    pass

def DressingData(e1):
    """
    """
    global _g
    pass

def Plot(e1):
    """
    """
    global _g
    pass

def BottomDiameter(e1,e2):
    """
    """
    global _g
    pass

def TopDiameter(e1,e2):
    """
    """
    global _g
    pass

def Alpha(e1,e2):
    """
    """
    global _g
    pass

def Beta(e1,e2):
    """
    """
    global _g
    pass

def Length(e1,e2):
    """
    """
    global _g
    pass

def VirtualPattern(e1):
    """
    """
    global _g
    pass

def PDir(e1,e2):
    """
    """
    global _g
    pass

def SDir(e1,e2):
    """
    """
    global _g
    pass


