The openalea.mtg.aml module: how to start
#########################################


.. note:: This tutorial is adapted from the AMAPmod user manual, ref 1.8

Reading an MTG file and activate it
===================================

A plant architecture described in a coding file can be loaded in :mod:`openalea.mtg` using primitive MTG:

.. doctest::
    :options: +SKIP

    >>> from openalea.mtg.aml import MTG
    >>> g1 = MTG('reconstructed_appletree.mtg')

The MTG primitive attempts to read a valid MTG description and parses the coding file. If errors are detected during the parsing, they are displayed on the screen and the parsing fails. In this case, no MTG is built and the user should make corrections to the coding file. If the parsing succeeds, this function creates an internal representation of the plant (or a set of plants) encoded as a MTG. In this example, the MTG object is stored in variable `g1` for further use. Note that a MTG should always be stored in a variable otherwise it is destroyed immediately after its building. The last built MTG is considered as the "active" MTG. It is used as an implicit argument by all the functions of the MTG module.

It is possible to change the active MTG using primitive Activate ::

    g1 = MTG("filename1") # g1 is the current MTG
    g2 = MTG("filename2") # g2 becomes the current MTG
    Activate(g1)          # g1 is now again the current MTG

.. warning:: the notion of activation is very important. Each call to a function in the package MTG will look at the active MTG.

AML primitives related to MTGs
==================================

There exists a comprehensive set of primitives related to MTGs. These primitives may be directly used on the active MTG or they may be combined with each other in order to define new functions on MTGs. Let us give a few examples of these specific primitives.

    * **MTG constructor**.
      A MTG can be built from its code file by using the primitive :class:`~openalea.mtg.aml.MTG` which takes one mandatory argument, i.e. the name of the MTG code file.

    * **Extraction of vertex sets: e.g. VtxList().**
      Different types of lists of vertices can be extracted from a MTG through the primitive :func:`~openalea.mtg.aml.VtxList`. Notably, the set of primitives at a given scale is obtained with the optional argument **Scale**:

      .. code-block:: python
          :linenos:

          from openalea.mtg.aml import VtxList
          VtxList()
          vtx1 = VtxList(Scale=1) # vtx 1 returns a list e.g., [1]
          vtx2 = VtxList(Scale=2)
          vtx3 = VtxList(Scale=3)

      On line 2, we extract the vertices that have scale 1. The list that is returned contains only 1 element that have the index 1. conversely, we could use the :func:`~openalea.mtg.aml.Scale` function to figure out what is the scale if the vertex that have the index 1:

      .. doctest::

          >>> from openalea.mtg.aml import Scale
          >>> aml.Scale(1)
          1

    * **Primitives returning vertex attributes: e.g. Class(vtx), Index(vtx), Feature(vtx, feature_name).**
      The different attributes attached to a given vertex can be retrieved by these functions. The class and the index of a vertex are respectively returned by primitives :func:`~openalea.mtg.aml.Class()` and :func:`~openalea.mtg.aml.Index()`.
      The value of any other attribute may be obtained by specifying its name:

      .. doctest::

          >>> from openalea.mtg.aml import Feature, Class, Index
          >>> vtxList = VtxList(Scale=2)  # get a list of vertices according to a scale
          >>> v1 = vtxList[0]             # look at the first vertex
          >>> # Feature(vertex_id, name)  
          >>> Feature(v1,"XX")
          >>> Class(v1)
          >>> Index(v1)

      Returns the attribute "XX" (if any) of a vertex v1. These primitives return scalar (INTEGER, STRING, REAL), i.e. elementary types different from VTX.

    * **Primitives for moving in MTGs: e.g. Father(vtx), Complex(vtx), Successor(vtx), Predecessor(vtx).**
      Some primitives take a VTX as an argument and return a VTX. These primitives allow topological moves in the MTG, i.e. they allow to select new vertices with topological reference to given vertices. See :func:`~openalea.mtg.aml.Father`, :func:`~openalea.mtg.aml.Predecessor`  , :func:`~openalea.mtg.aml.Successor`, and :func:`~openalea.mtg.aml.Complex`
 
        .. doctest::

          >>> from openalea.mtg.aml import Father, complex, Successor, Predecessor
          >>> Father(v1)
          >>> Predecessor(v1)

        .. note::  The predecessor is a special case of Father; predecessor function is 
           equivalent to Father(v, EdgeType-> '<'). It thus returns the father 
           (at the same scale) of the argument 

        .. todo:: What is a complex 


    * Primitives for creating collections of vertices: e.g. Sons(vtx), Components(vtx), Axis(vtx).
      These primitives return sets of vertices associated with a certain vertex. Components() returns all the vertices that compose at the scale immediately superior a given vertex. Axis() returns the ordered set of vertices which compose the axis which the argument belongs to.

    * Primitives for creating graphical representations of MTGs: PlantFrame(vtx) Plot(PlantFrame), DressingData(filename), VirtualPattern().
      PlantFrame() enables the user to compute 3D-geometrical representations of MTGs.

The above primitives can be combined together using the AML language to extract from plant databases various types of information.


.. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@inria.fr>, Dec 2009
.. topic:: documentation status

    Documentation adapted from the AMAPmod user manual.
