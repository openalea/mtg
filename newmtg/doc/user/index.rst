.. _newmtg_user:

MTG User Guide
####################

:Version: |version|
:Release: |release|
:Date: |today|


:Provides: **MTG** or *Multiscale Tree Graph* data structure.

The :mod:`openalea.mtg` package defines a *multiscale tree graph* data 
structure. which consists of a set of layered *trees* (:ref:`container_tree`). 

A vertex is a node of a tree at a given scale, i.e. given level of representation. It has a unique parent and may have several children. It is also connected to the two trees at the upper and lower scales. It has a unique complex and may have several components.
A MTG integrates - within a unique data structure - the different tree graph representations that correspond to the different scales of description of a structure (e.g. a plant architecture).


This manual details functions, modules, and objects included in 
**OpenAlea.MTG**, describing what they are and what they do. 
For learning how to use OpenAlea.MTG see :ref:`newmtg_reference`.

.. seealso::

    :ref:`container_user`
        Data structures such as graph, tree, and topological mesh.

.. toctree::
    :maxdepth: 2
    :numbered:
    
    intro.rst
    tutorial.rst
    data_structure.rst
    algorithm.rst


