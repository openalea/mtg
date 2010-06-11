.. _newmtg_tutorial_mtg_aml:

The :mod:`openalea.mtg.aml` module: Long Tour
#############################################

Reading the file
================

This page illustrates the usage of all the functionalities available in :mod:`openalea.mtg.aml` module. All 
the examples uses the MTG file :download:`code_file2.mtg`. If you are interested in the syntax, we stronly recommend
you to look at Section :ref:`newmtg_intro`. 

First, let us read the MTG file with the function :func:`MTG`. Note that only one MTG object can be manipulated at a time. This MTG object is the **active** MTG.


.. figure:: fig3_4.png

    **Figure 1:** Graphical representation of the MTG file code_file2.mtg used as an input file to all examples contained in this page

.. doctest::

    >>> from openalea.mtg.aml import *
    >>> g = MTG('user/code_file2.mtg')
    >>> Active() == g
    True

The :func:`Active` function checks that `g` is currently the active MTG.


If a new MTG file is read, it becomes the new active MTG object. However, the function :func:`Activate` can be use to switch between MTG objects as follows:

.. doctest::
    :options: +SKIP

    >>> h = MTG('user/agraf.mtg')
    >>> Active() == h
    True
    >>> Activate(g)

.. doctest::

    >>> MTGRoot()
    0

Feature functions
=================


Order, Rank and Height
----------------------


:func:`Order` (:func:`AlgOrder`) look at the number of + sign that need to be crossed before reaching the vertex considered

.. doctest::

    >>> Order(3)
    0
    >>> Order(14)
    1
    >>> AlgOrder(3,14)
    1

:func:`Height` (:func:`AlgHeight`) look at the number of components between the root of the vertex's branch and the vertex's position.

.. doctest::

    >>> Height(3)
    0
    >>> Height(14)
    10
    >>> AlgHeight(3, 14)
    10

:func:`Rank` (:func:`AlgRank`) returns the number  < sign that need to be crosssed before reaching the vertex considered.

.. doctest::

    >>> Rank(3)
    0
    >>> Rank(14)
    4
    >>> AlgRank(3, 14)
    5

:func:`Class`, :func:`Index`, :func:`Label`, :func:`Feature`
--------------------------------------------------------------

:func:`Class` gives the type of vertex usually defined by a letter

.. doctest::

    >>> Class(3)
    'I'

and :func:`Index` gives the other part of the label

.. doctest::

    >>> Index(3)
    1

When speaking about multiscale tree graph, we also want to access the :func:`Scale`:

.. doctest::

    >>> Scale(3)
    3

A new function called :func:`Label` combines the `Class` and `Index`:

.. doctest::

    >>> Label(3)
    'I1'


Finally, :func:`Feature` returns value of a given feature coded in the MTG file.

.. doctest:: 

    >>> Feature(2, "Len")
    10.0

:func:`ClassScale`, :func:`EdgeType`, :func:`Defined`
------------------------------------------------------

:func:`ClassScale` returns the Scale at which appears a given class of vertex:

.. doctest::

    >>> ClassScale('U')
    3

:func:`EdgeType` returns the type of connection between two vertices (e.g., +, <)

.. doctest::

    >>> i=8; Class(i), Index(i)
    ('I', 6)
    >>> i=9; Class(i), Index(i)
    ('U', 1)
    >>> EdgeType(8,9)
    '+'

:func:`Defined` tests whether a vertex's id is present in the active MTG

.. doctest:: 

    >>> Defined(1)
    True
    >>> Defined(100000)
    False


Date functions
==============

The following function requires MTG files to contain Date information.

.. todo:: not yet implemented

==============================  =========================
Function
==============================  =========================
DateSample(e1)
FirstDefinedFeature(e1, e2)
LastDefinedFeature(e1, e2)
NextDate(e1)
PreviousDate(e1)
==============================  =========================


Functions for moving in MTGs
============================

:func:`Trunk`
---------------
:func:`Trunk` returns the list of vertices constituting the bearing botanical axis of a branching system

.. doctest::

    >>> Trunk(2)    # vertex 2  is U1 therefore the Trunk should return index related to U1, U2, U3
    [2, 24, 31]
    >>> Class(24), Index(24)
    ('U', 2)


    >>> Trunk(3)    # vertex 3 is an internode, so we get all internode of the axis containing vertex 3
    [3, 4, 5, 6, 7, 8, 21, 22, 23, 25, 26, 27, 28, 29, 30, 32, 33, 34, 35]
    >>> Class(35), Index(35)
    ('I', 19)

:func:`Father`
----------------
Topological father of a given vertex.

.. doctest::

    >>> Label(8)
    'I6'
    >>> Father(8)
    7
    >>> Label(9)      # Let us look at vertex 9 (with the U1 label)
    'U1'
    >>> Father(9)               # and look for its father's index
    2
    >>> Label(2)      # and its father's label that appear to also be equal to 1
    'U1'


:func:`Axis`
-----------------
:func:`Axis` returns the vertices of the axis to which belongs a given vertex.

.. doctest::

    >>> [Label(x) for x in Axis(9)]
    ['U1', 'U2']

The scale may be specified

.. doctest::

    >>> [Label(x) for x in Axis(9, Scale=3)]
    ['I20', 'I21', 'I22', 'I23', 'I24', 'I25', 'I26', 'I27', 'I28', 'I29']


:func:`Ancestors`
-----------------

:func:`Ancestors` returns a list of ancestors of a given vertex

.. doctest::

    >>> Ancestors(20)   # of I29
    [20, 19, 18, 17, 16, 14, 13, 12, 11, 10, 8, 7, 6, 5, 4, 3]
    >>> [Class(x)+str(Index(x)) for x in Ancestors(20)]
    ['I29', 'I28', 'I27', 'I26', 'I25', 'I24', 'I23', 'I22', 'I21', 'I20', 'I6', 'I5', 'I4', 'I3', 'I2', 'I1']

:func:`Path`
-------------

The :func:`Path` returns a list of vertices defining the path between two vertices

.. doctest::

    >>> [Class(x)+str(Index(x)) for x in Path(8, 20)]
    ['I20', 'I21', 'I22', 'I23', 'I24', 'I25', 'I26', 'I27', 'I28', 'I29']


:func:`Sons`
------------------

In order to illustrate the :func:`Sons` function, let us consider the vertex 8

.. doctest::

    >>> Class(8), Index(8)
    ('I', 6)
    >>> [Class(x)+str(Index(x)) for x in Sons(8)]
    ['I20', 'I7']

:func:`Descendants` and :func:`Ancestors`
------------------------------------------

:func:`Descendants` an array with  all the vertices, at the same scale as v, that belong to the branching system starting at v::

    >>> [Class(x)+str(Index(x)) for x in Descendants(8)]

:func:`Ancestors` contains the vertices on the path from v back to the root (in this order) and finishes by the tree root.::

    >>> [Class(x)+str(Index(x)) for x in Ancestors(8)]

:func:`Predecessor` and :func:`Successor`
----------------------------------------------------------------

:func:`Predecessor` returns the Father of a vertex connected to it by a ‘<’ edge, and is therefore equivalent to::

    Father(v, EdgeType-> ‘<’). 


Similarly, :func:`Successor` is equivalent to ::

    Sons(v, EdgeType=’<’)[0]

:func:`Root`
--------------

:func:`Root` returns root of the branching systenme containing a given vertex and therefore is equivalent to::

    Ancestors(v, EdgeType=’<’)[-1]

    >>> [Class(x)+str(Index(x)) for x in Ancestors(8)]
    ['I6', 'I5', 'I4', 'I3', 'I2', 'I1']
    >>> Root(8)
    3
    >>> Class(3)+str(Index(3))
    'I1'

.. todo:: Complex returns Scale(v)-1 why what is it for?

.. doctest::

    >>> Complex(8)
    2

:func:`Components`
--------------------

Returns a list of vertices that are included in the upper scale of the vertex's id considered. The array is empty if the vertex has no components. 

    >>> Components(1, Scale=2)
    [2, 9, 15, 24, 31]
    >>> Components(1, Scale=3)
    [3, 4, 5, 6, 7, 8, 21, 22, 23, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 25, 26, 27, 28, 29, 30, 32, 33, 34, 35]

:func:`ComponentRoots`
----------------------

.. todo:: to be done. find example


:func:`Location`
-----------------

Vertex defining the father of a vertex with maximum scale.

.. doctest::

    >>> Label(9)            # starting from a Component U1 at vertex's id 9
    'U1'
    >>> Father(9)           # what is its Father ?
    2
    >>> Label(Father(9))    # answer: another U1 of vertex's id 2
    'U1'
    >>> Location(9)         # what is the location of vertex 9
    8
    >>> Label(Location(9))  # the internode I6
    'I6'

:func:`Extremities`
--------------------

.. doctest::

    >>> Label(8)
    'I6'
    >>> Label(Extremities(8))
    ['I29', 'I19']


Geometric interpretation
========================

Most of the following functions are not yet implemented. See :ref:`newmtg_quick_start` to see the usage of :func:`PlantFrame` with dressing data. 

You may also use the former AML code using `openalea.aml` package


:func:`PlantFrame` and :func:`Plot`
-----------------------------------------

One can use openalea.aml for now:

.. doctest::
    :options: +SKIP

    >>> import openalea.aml as aml
    >>> aml.MTG('code_file2.txt')
    >>> pf = aml.PlantFrame(2)
    >>> aml.Plot()

Shows the MTG file at scale 2. This is possible because Diameter and Lenmgth features are provided at that scale. 

========================= ======================
========================= ======================
:func:`DressingData`
:func:`Plot`
:func:`TopCoord`
RelTopCoord(e1, e2)
BottomCoord(e1, e2)
RelBottomCoord(e1, e2)
Coord(e1, e2)
BottomDiameter(e1,e2)
TopDiameter(e1,e2)
Alpha(e1,e2)
Beta(e1,e2)
Length(e1,e2)
VirtualPattern(e1)
PDir(e1,e2)
SDir(e1,e2)
========================= ======================


Comparison Functions
====================
.. todo:: not yet implemented

TreeMatching(e1)
MatchingExtract(e1)


.. topic:: documentation status: 

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@inria.fr>, Dec 2009

    Documentation adapted from the AMAPmod user manual version 1.8 Dec 2009.
    
    Documentation to be revised
