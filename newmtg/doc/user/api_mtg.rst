.. _MTG:

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


All
---

.. autoclass:: MTG
    :member-order: groupwise
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

Download the source file :download:`../../src/mtg/mtg.py`.

