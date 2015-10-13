.. _MTG_datastruct:

MTG - Mutlti-scale Tree Graph
================================

Overview
--------
.. currentmodule:: openalea.mtg.mtg
.. autofunction:: MTG


Iterating over vertices
-----------------------

.. autosummary::

    MTG.root
    MTG.vertices
    MTG.nb_vertices
    MTG.parent
    MTG.children
    MTG.nb_children
    MTG.siblings
    MTG.nb_siblings
    MTG.roots
    MTG.complex
    MTG.components
    MTG.nb_components
    MTG.complex_at_scale
    MTG.components_at_scale


Adding and removing vertices
----------------------------

.. autosummary::

    MTG.__init__
    MTG.add_child
    MTG.insert_parent
    MTG.insert_sibling
    MTG.add_component
    MTG.add_child_and_complex
    MTG.add_child_tree
    MTG.clear

Some usefull functions
-----------------------

.. autosummary::

    simple_tree
    random_tree
    random_mtg
    colored_tree
    display_tree
    display_mtg

All
---

.. autoclass:: MTG
    :member-order: groupwise
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

.. autofunction:: simple_tree
.. autofunction:: random_tree
.. autofunction:: random_mtg
.. autofunction:: colored_tree
.. autofunction:: display_tree
.. autofunction:: display_mtg

Download the source file :download:`../../src/mtg/mtg.py`.

