.. _newmtg_intro:

############################
Introduction
############################

.. include:: overview.txt


Plants are formally represented in AMAPmod by multiscale tree graphs (MTGs), [20].
A MTG basically consists of a set of layered tree graphs, 
representing plant topology at different scales (internodes, growth units, axes, etc.). 
To build up MTGs from plants, plants are first broken down into plant components, 
organised in different scales Figure 3-2a and 2b). 
Components are given labels that specify their type 
(Figure 3-2b, U = growth unit, F = flowering site, S = short shoot, I = internode). 
These labels are then used to encode the plant architecture into a textual form. 
The resulting coding file (Figure 3-2c) can then be analysed by AMAPmod to build 
the corresponding MTG (Figure 3-2d). 
Basically, in an MTG, the organisation of plant components at a given scale of detail is represented by a tree graph, where each component is represented by a vertex in the graph and edges represent the physical connections between them. At any given scale, the plant components are linked by two types of relation, corresponding to the two basic mechanisms of plant growth, namely the apical growth and the branching processes. Apical growth is responsible for the creation of axes, by producing new components (corresponding to new portions of stem and leaves) on top of previous components. The connection between two components resulting from the apical growth is a ''precedes'' relation and is denoted by a '<'. 
On the other hand, the branching process is responsible for the creation of axillary buds
(these buds can then create axillary axes with their own apical growth). 
The connection between two components resulting from the branching process 
is a ''bears'' relation and is denoted by a '+'.
A MTG integrates - within a unique model - the different tree graph representations 
that correspond to the different scales at which the plant is described.

Various types of attribute can be attached to the plant components represented in the MTG,
at any scale. Attributes may be geometrical 
(e.g. diameter of a stem, surface area of a leaf or 3D positioning of a plant component) 
or morphological (e.g. number of flowers, nature of the associated leaf, 
type of axillary production - latent bud, short shoot or long shoot -).

MTGs can be constructed from field observations using textual encoding of the plant 
architecture as described in [22] (Figure 3-2). 
Alternatively, code files representing plant architectures can also be constructed 
from simulation programs that generate artificial plants, 
or directly from any Python program, as we will illustrate it in the :ref:`mtg_tutorial`.

The code files usually have a spreadsheet format and contain the description of 
plant topology in the first few columns and the description of attributes attached 
to plant components on subsequent columns. 

