
.. highlight:: python
   :linenothreshold: 5

.. _newmtg_tutorial:

#######################################
Tutorial: Create MTG file from scratch
#######################################


This tutorial briefly introduces the main features of the package
and should show you the contents and potential of the **openalea.mtg** library.

All the examples can be tested in a Python interpreter.

MTG creation
================

    Let us consider the following example:


.. code-block:: python
    :linenos:

    import openalea.mtg as mtg

    g = mtg.MTG()

    print len(g)
    print g.nb_vertices()
    print g.nb_scales()

    root = g.root
    print g.scale(root)


* First, the package is imported (**line 1**). 
* Then, a mtg is instantiated without parameters (**line 3**).
* However, as for a :class:`~openalea.container.tree.Tree`, the mtg is not empty (**line 5-7**).
* There is always a root node at scale 0 (**line 9-10**).


Simple edition
================

We add a component `root1` to the root node, which will be the root node of the tree 
at the scale 1.

.. code-block:: python
    :linenos:

    root1 = g.add_component(root)

    # Edit the tree at scale 1 by adding three children
    # to the vertex `root1`.
    v1 = g.add_child(root1)
    v2 = g.add_child(root1)
    v3 = g.add_child(root1)

    g.parent(v1) == root1
    g.complex(v1) == root
    v3 in g.siblings(v1)

Traversing the mtg at one scale
=================================


The mtg can be traversed at any scales like a regular tree.
Their are three traversal algorithms working on Tree data structures (:ref:`container_algo_traversal`):

    * :class:`pre_order`
    * :class:`post_order`
    * :class:`level_order`

These methods take as parameters a tree like data structure, and a vertex.
They will traverse the subtree rooted on this vertex in a specific order.
They will return an iterator on the traversed vertices.

.. code-block:: python
    :linenos:

    from openalea.container.traversal.tree import *

    print list(g.components(root))

    print list(pre_order(g, root1))
    print list(post_order(g, root1))
    print list(level_order(g, root1))

.. warning::

    On **MTG** data structure, methods that return collection of vertices 
    always return an iterator rather than :class:`list`, :class:`array`, or :class:`set`. 
    
    You have to convert the iterator into a :class:`list` if you want to display it,
    or compute its length.


        >>> print len(g.components(root)) #doctest: +SKIP
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        TypeError: object of type 'generator' has no len()

    Use rather:

        >>> components = list(g.components(root)) #doctest: +SKIP
        >>> print components #doctest: +SKIP
        [1, 2, 3, 4]


Full example: how to create an MTG
======================================

.. figure:: fig3_4.png
    :width: 50%

    **Figure 1:** Graphical representation of the MTG file code_file2.mtg used as an input file to all examples contained in this page


.. literalinclude:: create_mtg.py
    :linenos:
    :language: python






:Authors: Christophe Pradal <christophe pradal __at__ cirad fr>, Thomas Cokelaer <thomas cokelaer __at__ sophia inria fr>
