.. testsetup::

    from openalea.mtg.aml import *

.. _newmtg_quick_start:

Quick Start to manipulate MTGs
###################################


Reading an MTG file and activate it
===================================


A plant architecture described in a coding file can be loaded in :mod:`openalea.mtg.aml` as follows:

.. doctest::

    >>> from openalea.mtg.aml import MTG
    >>> g1 = MTG('user/agraf.mtg')          # some errors may occur while loading the MTG
    ERROR: Missing component for vertex 2532


.. note:: In order to reproduce the example, download  :download:`agraf MTG file <agraf.mtg>` and the :download:`agraf DRF file <agraf.drf>`.
        Other files that may be required are also available in the same directory (`*smb` files) but are not compulsary.

The MTG function attempts to read a valid MTG description and parses the coding file. If errors are detected during the parsing, they are displayed on the screen and the parsing fails. In this case, no MTG is built and the user should make corrections to the coding file. If the parsing succeeds, this function creates an internal representation of the plant (or a set of plants) encoded as a MTG. In this example, the MTG object is stored in variable `g1` for further use. Note that a MTG should always be stored in a variable otherwise it is destroyed immediately after its building. The last built MTG is considered as the "active" MTG. It is used as an implicit argument by all the functions of the MTG module.

It is possible to change the active MTG using :func:`Activate` ::

    g1 = MTG("filename1") # g1 is the current MTG
    g2 = MTG("filename2") # g2 becomes the current MTG
    Activate(g1)          # g1 is now again the current MTG

.. warning:: the notion of activation is very important. Each call to a function in the package MTG will look at the active MTG.

Plotting
==========

.. warning:: PlantFrame is still in development and not all MTG files can be plotted with the current code, 
   especially the files that have no information about positions

The following examples shows how to plot the contents of a MTG given that a dressing data file (DRF) is available. See the :ref:`newmtg_syntax` section for more 
information about the MTG and DRF syntax. Note that the following code should be simplified in the future.

.. code-block:: python
    :linenos:

    from openalea.mtg.aml import MTG
    from openalea.mtg.dresser import dressing_data_from_file
    from openalea.mtg.plantframe import PlantFrame, compute_axes, build_scene
    g = MTG('agraf.mtg')
    dressing_data = dressing_data_from_file('agraf.drf')
    topdia = lambda x:  g.property('TopDia').get(x)
    pf = PlantFrame(g, TopDiameter=topdia,    DressingData = dressing_data)
    axes = compute_axes(g, 3, pf.points, pf.origin)
    diameters = pf.algo_diameter()
    scene = build_scene(pf.g, pf.origin, axes, pf.points, diameters, 10000)
    from  vplants.plantgl.all import Viewer
    Viewer.display(scene)

.. figure:: fig3_5_bis.png
    :align: center
    :width: 50%
    :height: 300px

    **Figure 3.5** An apple tree plotted with the python script shown above


Functions related to MTGs
==================================

There exists a comprehensive set of functions related to MTGs. These functions may be directly used on the active MTG or they may be combined with each other in order to define new functions on MTGs. Here are some of them. Full details may be found elsewhere either in the tutorials (e.g., :ref:`newmtg_tutorial_mtg_aml`)  or in the :ref:`newmtg_reference` section.

    * **MTG constructor**.
      We've already seen how to read a MTG file by using :func:`~openalea.mtg.aml.MTG`, which takes one mandatory argument, namely the MTG's filename.

    * **Extraction of vertex sets: e.g. VtxList().**
      Different types of lists of vertices can be extracted from a MTG through the function :func:`~openalea.mtg.aml.VtxList`. Notably, the set of functions at a given scale is obtained with the optional argument **Scale**:

      .. code-block:: python
          :linenos:

          from openalea.mtg.aml import VtxList
          VtxList()
          vtx1 = VtxList(Scale=1) # vtx 1 returns a list e.g., [1]
          vtx2 = VtxList(Scale=2)
          vtx3 = VtxList(Scale=3)

      On line 2, we extract the vertices that have scale set to 1. The returned list contains only 1 element that have the index 1. Conversely, we could use the :func:`~openalea.mtg.aml.Scale` function to figure out what is the Scale of the vertex that have the index 1:

      .. doctest::

          >>> from openalea.mtg.aml import Scale
          >>> Scale(1)
          1

    * **Functions returning vertex attributes: e.g. Class(vtx), Index(vtx), Feature(vtx, feature_name).**
      The different attributes attached to a given vertex can be retrieved by these functions. The class and the index of a vertex are respectively returned by functions :func:`~openalea.mtg.aml.Class()` and :func:`~openalea.mtg.aml.Index()`.
      The value of any other attribute may be obtained by specifying its name:

      .. doctest::

          >>> from openalea.mtg.aml import Feature, Class, Index
          >>> vtxList = VtxList(Scale=2)  # get a list of vertices according to a scale
          >>> v1 = vtxList[0]             # look at the first vertex
          >>> # Feature(vertex_id, name)  
          >>> Feature(v1, "XX")
          0.0
          >>> Class(v1)
          'U'
          >>> Index(v1)
          94

      Returns the attribute "XX" (if any) of a vertex v1. These functions return scalar (INTEGER, STRING, REAL), i.e. elementary types different from VTX.

    * **Functions for moving in MTGs: e.g. Father(vtx), Complex(vtx), Successor(vtx), Predecessor(vtx).**
      Some functions take a VTX as an argument and return a VTX. These functions allow topological moves in the MTG, i.e. they allow to select new vertices with topological reference to given vertices. See :func:`~openalea.mtg.aml.Father`, :func:`~openalea.mtg.aml.Predecessor`  , :func:`~openalea.mtg.aml.Successor`, and :func:`~openalea.mtg.aml.Complex`
 
        .. doctest::

          >>> from openalea.mtg.aml import Father, Successor, Predecessor
          >>> Father(v1)
          >>> Predecessor(v1)

        .. note::  The predecessor is a special case of Father; predecessor function is 
           equivalent to Father(v, EdgeType-> '<'). It thus returns the father 
           (at the same scale) of the argument 


    * **Functions for creating collections of vertices: e.g. Sons(vtx), Components(vtx), Axix(vtx).**
      These functions return sets of vertices associated with a certain vertex. Components() returns all the vertices that compose at the scale immediately superior a given vertex. Axis() returns the ordered set of vertices which compose the axis which the argument belongs to.

    * **Functions for creating graphical representations of MTGs: PlantFrame(), Plot(), DressingData**
      PlantFrame() enables the user to compute 3D-geometrical representations of MTGs.

The above functions can be combined together using the Python language to extract from plant databases various types of information.


.. topic:: documentation status: 

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@inria.fr>, Dec 2009

    Documentation adapted from the AMAPmod user manual version 1.8 Dec 2009.

    Documentation to be revised

