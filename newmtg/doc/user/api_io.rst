.. currentmodule:: openalea.mtg.io

Reading and writing MTG
==================================

MTG
----

The MTG data structure can be read/write from/to a MTG file format.
The functions :func:`read_mtg` , :func:`write_mtg` , :func:`read_mtg_file`.

.. autofunction:: read_mtg

.. autofunction:: read_mtg_file

.. autofunction:: write_mtg


LPy 
------------------------------------

The two functions :func:`lpy2mtg` and :func:`mtg2lpy` allow to convert the MTG
data-structure into lpy and vise-versa. It ease the communication between the two modules.
Each structure are traversed and the properties are copied. Properties can be any pyton object.

.. autofunction:: lpy2mtg

.. autofunction:: mtg2lpy

AxialTree
-----------------

.. autofunction:: axialtree2mtg

.. autofunction:: mtg2axialtree

Cpfg
---------------------------

.. autofunction:: read_lsystem_string

Mss
----

.. autofunction:: mtg2mss

Download the source file :download:`../../src/mtg/io.py`.

