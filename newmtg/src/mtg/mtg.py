# -*- python -*-
#
#       OpenAlea.mtg
#
#       Copyright 2008-2009 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.pradal.at.cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

'''
This module provides an implementation of Multiscale Tree Graph.
For interface definition, see openalea.container.interface package.

:todo: MTG definition and usage.
'''

__docformat__ = "restructuredtext"

import re
import itertools
import warnings

import traversal
import random

try:
    from openalea.container.tree import PropertyTree, InvalidVertex
except ImportError:
    from tree import PropertyTree, InvalidVertex
    
    
class MTG(PropertyTree):
    ''' A Multiscale Tree Graph (MTG) class.

    MTGs describe tree structures at different levels
    of details, named scales.
    For example, a botanist can described plants at different scales :

        - at scale 0, the whole scene.
        - at scale 1, the individual plants.
        - at scale 2, the axes of each plants.
        - at scale 3, the growth units of each axis, and so on.

    Each scale can have a label, e.g. :

     - scale 1 : P(lant)
     - scale 2 : A(xis)
     - sclae 3 : U(nit of growth)

    Compared to a classical tree, :func:`complex` can be seen as :func:`parent`
    and :func:`components` as :func:`children`.
    An element at :func:`scale` N belongs to a :func:`complex` at :func:`scale` N-1 and has :func:`components` at scale N+1:

     - /P/A/U (decomposition is noted using "/")

    Each scale is itself described as a tree or a forest (i.e. set of trees), e.g.:

     - /P1/P2/P3
     - A1+A2<A3
     - ...

    '''

    def __init__(self):
        ''' Create a new MTG object.

        :Usage:

            >>> g = MTG()
        '''

        super(MTG, self).__init__()

        # Map a vid to its scale
        self._scale = {0:0}

        # Multiscale tree:
        # complex <=> parent : vid -> vid
        # components <=> children : vid -> [vid]
        self._complex = {}
        self._components = {}

        # add default properties
        self.add_property('edge_type')
        self.add_property('label')

    def __getitem__(self, vtx_id):
        """A simple getitem to extract relevant information on a vertex

        """
        return {"vid":vtx_id,
                "label":self.label(vtx_id),
                "index":self.index(vtx_id),
                "complex":self.complex(vtx_id),
                "scale":self._scale.get(vtx_id)}




    #########################################################################
    # Querying scale infos
    #########################################################################

    def scale(self, vid):
        ''' Returns the scale of a vertex.

        All vertices should belong to a given scale.

        :Usage:

        .. code-block:: python

            g.scale(vid)

        :Parameters:

            - `vid` (int) - vertex identifier.

        :Returns:
            The scale of the vertex. 
            It is a positive int in [0,g.max_scale()].
        '''
        try:
            return self._scale[vid]
        except:
            pass

    def nb_scales(self):
        '''
        :Returns:
            The number of scales defined in the mtg..
        :Returns Type:
            int

        .. note:: The complexity is :math:`O(n)`.
        '''
        return len(set(self._scale.itervalues()))

    def scales(self):
        '''Return the different scales of the mtg.

        :Returns:
            Iterator on scale identifiers (ints).

        .. note:: The complexity is :math:`O(n)`.
        '''
        return iter(set(self._scale.itervalues()))

    def max_scale(self):
        '''Return the max scale identifier.

        By convention, the mtg contains scales in :math:`[0,max\_scale]`.

        :Usage:
            >>> print g.max_scale()

        :Returns: 
            S, the maximum scale identifier.

        .. note:: The complexity is :math:`O(n)`.
        .. seealso:: :func:`scale`, :func:`scales`
        '''
        return max(self._scale.itervalues())


    #########################################################################
    # Some Vertex List Graph Concept methods.
    #########################################################################
    def nb_vertices(self, scale = -1):
        '''
        Returns the number of vertices.

        :Usage:
            >>> g.nb_vertices()
            100
            >>> g.nb_vertices(scale=3)
            68

        :Parameters:
         - `scale` (int) - Id of scale for which to count
           vertices.

        :Returns:
            Number of vertices at `scale` or total
            number of vertices if scale < 0.
        '''
        if scale < 0:
            return len(self._scale)
        else:
            return len(set(self.vertices(scale=scale)))

    def vertices(self, scale = -1):
        '''
        Return an iterator of the vertices contained in an MTG.

        The set of all vertices in the MTG is returned.
        Vertices from all scales are returned if no scale is given.
        Otherwise, it returns only the vertices of the given scale.
        The order of the elements in this array is not significant.

        :Usage:

        .. code-block:: python

            g = MTG()
            len(g) == len(list(g.vertices()))
            for vid in g.vertices(scale=2):
                print g.class_name(vid)

        :Optional Parameters:
            - `scale` (int): used to select vertices at a given scale.

        :Returns:
            Iterator on vertices at "scale" or on all
            vertices if scale < 0.

        :Returns Type:
            iter of vid

        :Background:

        .. seealso:: :meth:`children`, :meth:`components`.
        '''
        if scale < 0:
            return self._scale.iterkeys()
        else:
            return (vid for vid, sid in self._scale.iteritems() if sid == scale)

    #########################################################################
    # Python Iterator and Container interfaces
    #########################################################################
    def __iter__(self):
        '''
        Iterable interface.

        :Usage:

        .. code-block:: python

            for v in g:
                print g.class_name(v)

        '''
        return self.vertices()

    def __contains__(self, vid):
        '''
        Container interface

        :Usage:

        .. code-block:: python

            if v in g:
                print v, " is in the mtg."
        '''
        return self.has_vertex(vid)


    #########################################################################
    # GraphConcept methods.
    #########################################################################
    def has_vertex(self, vid):
        """
        Tests whether a vertex belongs to the graph.

        :Parameters:
         - `vid` (int) - vertex id to test
        :Returns Type:
            bool
        """
        return vid in self._scale


    def is_valid(self):
        """
        Tests the validity of the graph. Currently
        always returns True.

        :Returns Type:
            bool
        :todo: Implement this function.
        """
        return True

    def iteredges(self, scale=-1):
        warnings.warn("Deprecated, use iter_edges instead", DeprecationWarning)
        return self.iter_edges(scale)

    def iter_edges(self, scale=-1):
        """
        :Parameters:
         - `scale` (int) - Scale at which to iterate.
        :Returns:
            Iterator on the edges of the MTG at a given scale
            or on all edges if scale < 0.
        :Returns Type:
            iter
        """
        if scale < 0:
            return ((v,k) for k,v in self._parent.iteritems())
        else:
            return ((parent, child) for child, parent in self._parent.iteritems() if self.scale(parent) == scale)


    #########################################################################
    # MutableVertexGraphConcept methods.
    # TODO: Add methods from MutableVertexGraph concept.
    #########################################################################

    def add_element(self, parent_id, edge_type = '/', scale_id=None):
        """
        Add an element to the graph, if vid is not provided create a new vid ???
        .. warning: Not Implemented.

        :Parameters:
        - `parent_id` (int) - The id of the parent vertex
        - `edge_type` (str) - The type of relation:

            - "/" : component (default)
            - "+" : branch
            - "<" : successor.
        - `scale_id` (int)  - The id of the scale in which to
            add the vertex.

        :Returns:
            The vid of the created vertex

        """
        raise NotImplementedError

    def remove_vertex(self, vid):
        """
        Remove a specified vertex of the graph and
        remove all the edges attached to it.

        :Parameters:
            - `vid` (int) : the id of the vertex to remove
        :Returns: None
        """

        if self.nb_components(vid) == 0:
            super(MTG, self).remove_vertex(vid)
            if vid in self._components:
                del self._components[vid]
            if vid in self._scale:
                del self._scale[vid]
            if vid in self._complex:
                cid = self._complex[vid]
                l = self._components[cid]
                try:
                    i = l.index(vid)
                    del l[i]
                except ValueError, e:
                    pass 
                del self._complex[vid]
        else:
            raise InvalidVertex('Can not remove vertex %d with components.'
            'Use remove_tree instead.'%vid)

    def clear(self):
        """Remove all vertices and edges from the MTG.

        This also removes all vertex properties.
        Don't change references to object such as internal dictionaries.

        :Example: ::

            >>> g.clear()
            >>> g.nb_vertices()
            0
            >>> len(g)
            0


        """
        super(MTG, self).clear()

        self._scale.clear()
        self._scale[0] = 0

        self._complex.clear()
        self._components.clear()

    def copy(self):
        """ Return a copy of the graph.

        :Returns:
            - `g` (MTG) - A copy of the MTG

        """
        return g.sub_mtg(g.root)

    def roots(self, scale=0):
        '''
        :Returns:
            iterator on vertex identifiers of root vertices at a given `scale`.
        :Returns Type:
            iter
        '''
        return (vid for vid in self.vertices(scale=scale) if self.parent(vid) is None)


    #########################################################################
    # MutableTreeConcept methods.
    #########################################################################
    def add_child(self, parent, child=None, **properties):
        ''' Add a child to a parent. Child is appended to the parent's child list.

        :Parameters:
         - `parent` (int) - The parent identifier.
         - `child`  (int or None) - The child identifier. If None,
                    an ID is generated.

        :Returns:
            Identifier of the inserted vertex (child)
        :Returns Type:
            int
        '''

        child = super(MTG, self).add_child(parent, child, **properties)
        self._scale[child] = self._scale[parent]
        return child

    def insert_sibling(self, vtx_id1, vtx_id2=None, **properties):
        '''
        Insert a sibling of vtk_id1. The vertex in inserted before vtx_id1.

        :Parameters:
         - `vtx_id1` (int) : a vertex identifier
         - `vtx_id2` (int) : the vertex to insert

        :Returns:
            Identifier of the inserted vertex (vtx_id2)
        :Returns Type:
            int
        '''
        vtx_id2 = super(MTG, self).insert_sibling(vtx_id1, vtx_id2, **properties)
        self._scale[vtx_id2] = self._scale[vtx_id1]
        return vtx_id2

    def insert_parent(self, vtx_id, parent_id=None, **properties):
        '''
        Insert parent_id between vtx_id and its actual parent.
        Inherit of the complex of the parent of vtx_id.

        :Parameters:
         - `vtx_id` (int): a vertex identifier
         - `parent_id` (int): a vertex identifier

        :Returns:
            Identifier of the inserted vertex (parent_id).
        :Returns Type:
            int
        '''
        if parent_id is None:
            self._id += 1
            parent_id = self._id

        self._scale[parent_id] = self.scale(vtx_id)

        parent_id = super(MTG, self).insert_parent(vtx_id, parent_id, **properties)

        return parent_id

    def replace_parent(self, vtx_id, new_parent_id, **properties):
        '''
        Change the parent of vtx_id to new_parent_id.
        The new parent of vtx_id is new_parent_id.
        vtx_id and new_parent_id must have the same scale.

        This function do not change the edge_type between vtx_id and its parent.
        
        Inherit of the complex of the parent of vtx_id.

        :Parameters:
         - `vtx_id` (int): a vertex identifier
         - `new_parent_id` (int): a vertex identifier

        :Returns:
            Identifier of the inserted vertex (parent_id).
        :Returns Type:
            int
        '''
        if new_parent_id not in self:
            raise ""
        if self.scale(vtx_id) != self.scale(new_parent_id):
            raise ""

        old_parent = self.parent(vtx_id)
        old_complex = self._complex.get(vtx_id)
        old_components = self._components.get(vtx_id)

        if old_components is not None:
            raise "Unable to replace the parent for a vertex with components"
        self.add_child(new_parent_id, vtx_id)
        if old_parent is not None:
            children = self._children[old_parent]
            index = children.index(vtx_id)
            del children[index]

        if old_complex is not None:
            self.replace_parent(old_complex, self.complex(new_parent_id))
        
    #########################################################################
    # Mutable Multiscale Tree Concept methods.
    #########################################################################

    def complex(self, vtx_id):
        '''
        Returns the complex of `vtx_id`.

        :Parameters:
         - `vtx_id` (int) - The vertex identifier.

        :Returns:
            complex identifier or None if vtx_id has no parent.
        :Return Type:
            int
        '''
        complex_id = self._complex.get(vtx_id)
        while complex_id is None:
            vtx_id = self.parent(vtx_id)
            if vtx_id is None:
                break
            complex_id = self._complex.get(vtx_id)
        return complex_id

    def complex_at_scale(self, vtx_id, scale):
        '''
        Returns the complex of `vtx_id` at scale `scale`.

        :Parameters:
         - `vtx_id`: The vertex identifier.
         - `scale`: The scale identifier.

        :returns:
            vertex identifier
        :Returns Type:
            int
        '''
        complex_id = vtx_id
        current_scale = self.scale(complex_id)
        for i in range(scale, current_scale):
            complex_id = self.complex(complex_id)
        return complex_id

    def components(self, vid):
        '''
        returns a vertex iterator

        :param vid: The vertex identifier.

        :returns: iter of vertex identifier
        '''

        if vid in self._components:
            for v in self.component_roots(vid):
                for vtx in traversal.pre_order(self, v, complex=vid):
                    yield vtx

    def components_at_scale(self, vid, scale):
        '''
        returns a vertex iterator

        :Parameters:
         - `vid`: The vertex identifier.

        :returns: iter of vertex identifier
        '''
        # oops: search in the tree all the nodes which do not have another
        # explicit complex.

        cur_scale = self.scale(vid)

        gen = (vid, )
        for i in range(cur_scale, scale):
            gen = (vid for vtx in gen for vid in self.components(vtx) )

        return gen

    def component_roots(self, vtx_id):
        '''Return the set of roots of the tree graphs that compose a vertex.
        '''
        components = self._components.get(vtx_id,[])

        for ci in components:
            p = self.parent(ci)
            if p is None or self.complex(p) != vtx_id: 
                yield ci

    def component_roots_at_scale(self, vtx_id, scale):
        '''Return the set of roots of the tree graphs that compose a vertex.
        '''
        cur_scale = self.scale(vtx_id)
        if scale == -1 or scale == cur_scale+1:
           return self.component_roots(vtx_id)
        elif scale > cur_scale+1:
            gen = (vtx_id,)
            for i in range(cur_scale, scale):
                gen = (vid for vtx in gen for vid in self.component_roots(vtx))
            return gen
        else:
            return iter([])

    def nb_components(self, vid):
        '''
        returns the number of components

        :Parameters:
         - `vid`: The vertex identifier.

        :returns: int
        '''
        return len(list(self.components(vid)))

    # mutable
    def add_component(self, complex_id, component_id=None, **properties):
        '''
        Add a component at the end of the components

        :Parameters:
         - `complex_id`: The complex identifier.
         - `component_id`: Set the component identifier to this value if defined.

	:Returns: The id of the new component or the component_id if given.
        '''
        if component_id is None:
            self._id += 1
            component_id = self._id

        self._add_vertex_properties(component_id, properties)

        self._components.setdefault(complex_id,[]).append(component_id)
        self._complex[component_id] = complex_id
        self._scale[component_id] = self._scale[complex_id]+1

        return component_id

    def add_child_and_complex(self, parent, child=None, complex=None, **properties):
        '''
        Add a child at the end of children that belong to an other complex.

        :Parameters:
         - `parent`: The parent identifier.
         - `child`: Set the child identifier to this value if defined.
         - `complex`: Set the complex identifier to this value if defined.
        :returns: (vid, vid): child and complex ids.
        '''

        if complex is None:
            self._id += 1
            complex = self._id

        if child in self._children.get(parent, []):
            # add only the properties
            self._add_vertex_properties(child, properties)
        else:
            child = self.add_child(parent, child, **properties)
        self._scale[child] = self._scale[parent]


        parent_complex = self.complex(parent)

        if complex not in self._children.get(parent_complex, []):
            self.add_child(parent_complex, complex)
        self._scale[complex] = self._scale[parent_complex]

        self._components.setdefault(complex,[]).append(child)
        self._complex[child] = complex

        return child, complex

    def __str__(self):
        l = ["MTG : nb_vertices=%d, nb_scales=%d"%(self.nb_vertices(), self.nb_scales())]
        v  = self.root

        edge_type = self.property('edge_type')
        label = self.property('label')
        while v is not None and self.scale(v) is not None:
            l.append("\nScale %d"%self.scale(v))
            l.extend(display_tree(self,v, edge_type=edge_type, labels=label))
            compo = self._components.get(v,[None])
            v= compo[0]
        return '\n'.join(l)

    #########################################################################
    # Algorithms to copy extract and extend sub_mtg
    #########################################################################
    def sub_mtg(self, vtx_id, copy=True):
        """Return the submtg rooted on `vtx_id`.

        The induced sub mtg of the mtg are all the vertices which have vtx_id
        has a complex plus vtx_id.

        :Parameters:
          - `vtx_id`: A vertex of the original tree.
          - `copy`:
            If True, return a new tree holding the subtree. If False, the subtree is
            created using the original tree by deleting all vertices not in the subtree.

        :returns: A sub mtg of the mtg. If copy=True, a new MTG is returned.
            Else the sub mtg is created inplace by modifying the original tree.
        """

        if not copy:
            # remove all vertices not in the sub_tree

            bunch = set(traversal.pre_order_in_scale(self, vtx_id))
            remove_bunch = set(self) - bunch

            self.root = vtx_id

            # remove vertices by removing the element and deleting all the deges.
            # We do not use standard methods because the graph will not be functional
            # until the removal of all vertices.

            # force remove
            for vid in remove_bunch:

                # TODO: Build specific methods (_force_remove) to edit a MTG without
                # any verification. The MTG/Tree/whatever will be temporary invalid.

                # remove properties
                self._remove_vertex_properties(vid)
                del self._scale[vid]

                # remove parent edge
                pid = self.parent(vid)
                if pid is not None:
                    self._children[pid].remove(vid)
                    del self._parent[vid]
                # remove children edges
                for cid in self.children(vid):
                    self._parent[cid] = None
                if vid in self._children:
                    del self._children[vid]

                # remove complex edges
                complex_id = self._complex.get(vid)
                if complex_id is not None:
                    self._components[complex_id].remove(vid)
                    del self._complex[vid]
                # remove components edges
                for cid in self.components(vid):
                    del self._complex[cid]
                if vid in self._components:
                    del self._components[vid]

            # Update the scale of the nodes
            scale = self._scale
            root_scale = self.scale(vtx_id)
            for vid in scale:
                scale[vid] = scale[vid]-root_scale

            self._scale[self.root] = 0

            return self
        else:
            treeid_id = {}
            g = MTG()
            g.root = 0

            for name in self.properties():
                g.add_property(name)

            treeid_id[vtx_id] = g.root
            subtree = traversal.iter_mtg2(self, vtx_id)


            # Skip the first vertex vtx_id
            subtree.next()
            # Traverse all the sub_mtg.
            # Every vertex has a complex in this sub_mtg.
            # Complex vertices are traversed before there components and
            # parent before the children.

            for vid in subtree:
                complex_id = treeid_id[self.complex(vid)]
                v = g.add_component(complex_id)
                treeid_id[vid] = v

                pid = self.parent(vid)
                if pid is not None:
                    parent = treeid_id[pid]
                    v = g.add_child(parent, child=v)

                # Copy the properties
                g._add_vertex_properties(v, self.get_vertex_property(vid))

            return g


    #########################################################################
    # Specialised algorithms for aml compatibility.
    #########################################################################
    def order(self, v1):
        """
        Order of a vertex in a graph.

        The order of a vertex in a graph is the number of '+' edges crossed
        when going from `v1`to `v2`.

        If v2 is None, the order of v1 correspond to the order of v1 with
        respect to the root.
        """
        _order = 0
        edge_type = self.property('edge_type')
        if not edge_type:
            return 0

        vid = v1
        while vid is not None:
            if edge_type.get(vid) == '+':
                _order += 1
            vid = self.parent(vid)

        return _order

    def edge_type(self, vid):
        """
        Type of the edge between a vertex and its parent.

        The different values are '<' for successor, and '+' for ramification.
        """
        return self.property('edge_type').get(vid,'')

    def label(self, vid):
        """Label of a vertex.

        :Usage:

            >>> g.label(v)

        :Parameters:
            - `vid` (int) : vertex of the MTG

        :Returns:
            The class and Index of the vertex (str).

        .. seealso:: :func:`MTG`, :func:`index`, :func:`class_name`
        """
        return self.property('label').get(vid, '')

    def class_name(self, vid):
        """Class of a vertex.

        The Class of a vertex are the first characters of the label.
        The label of a vertex is the string defined by the concatenation
        of the class and its index.

        The label thus provides general information about a vertex and
        enable to encode the plant components.

        The class_name may be not defined. Then, an empty string is returned.

        :Usage:

            >>> g.class_name(1)

        :Parameters:

            - `vid` (int)

        :Returns:
            The class name of the vertex (str).

        .. seealso:: :func:`MTG`, :func:`openalea.mtg.aml.Index`, :func:`openalea.mtg.aml.Class`
        """
        pattern = r'[a-zA-Z]+'
        label = self.property('label').get(vid)
        if not label:
            return ''
        else:
            m=re.match(pattern, label)
            if m:
                return m.group(0)
            else:
                return ''

    def index(self, vid):
        """
        Index of a vertex

        The Index of a vertex is a feature always defined and independent of time
        (like the index).
        It is represented by a non negative integer.
        The label of a vertex is the string defined by the concatenation
        of its class and its index.
        The label thus provides general information about a vertex and
        enables us to encode the plant components.
        """
        pattern = r'[0-9]+$'
        label = self.property('label').get(vid)
        if not label:
            return vid
        else:
            m=re.search(pattern, label)
            if m:
                return m.group(0)
            else:
                return vid

    #########################################################################
    # Proxy node interface
    #########################################################################
    def node(self, vid, klass=None):
        """
        Return a node associated to the vertex `vid`.

        It allows to access to the properties with an object oriented interface.

        :Example:
        
        .. code-block:: python

            node = g.node(1)
            print node.edge_type
            print node.label
            node.label = 'B'
            print g.label(1)

            print node.parent
            print list(node.children)
        """
        if klass is None:
            klass = _ProxyNode
        if vid in self:
            return klass(self,vid)
        else:
            # TODO: retunr an error
            return None


################################################################################
# Graph generators
################################################################################

def fat_mtg(slim_mtg):
    """
    Compute missing edges at each scales based on the explicit edges
    defines at finer scales and decomposition relationship.
    """
    max_scale = slim_mtg.max_scale()
    #print 'max_scale %d'%max_scale
    #roots = slim_mtg.roots(scale=max_scale)
    #assert len(list(roots)) == 1
    edge_type_property = slim_mtg.property('edge_type')

    for scale in range(max_scale-1,0,-1):
        _compute_missing_edges(slim_mtg, scale, edge_type_property)
    return slim_mtg


def _compute_missing_edges(mtg, scale, edge_type_property=None):
    """ Compute missing edges on an incomplete MTG at a given scale.

    This is often usefull to create a minimal MTG with missing edges.
    The missing edges can be computing by using the tree at the finer scale,
    and by adding edges between the complexes of these nodes.

    For all the non connected nodes (root nodes)
        - extract the components
        - compute parent's components and the edge type between

    """
    roots = list(mtg.roots(scale=scale))
    #print 'roots: ', list(roots), scale
    for vid in roots:
        components = mtg._components.get(vid)
        if components is None:
            print 'ERROR: Missing component for vertex %d'%vid
            continue
        #assert len(components) == 1
        cid = components[0]
        if mtg.parent(cid) is None:
            continue
        parent_id = mtg.complex(mtg.parent(cid))
        if parent_id is None:
            #roots.append(vid)
            print 'ERROR: Missing complex for vertex %d'%parent_id
            continue
        if edge_type_property:
            edge_type = edge_type_property.get(cid)
            mtg.add_child(parent_id, child=vid, edge_type=edge_type)
        else:
            mtg.add_child(parent_id, child=vid)

    return True



################################################################################
# Graph generators
################################################################################

def simple_tree(tree, vtx_id, nb_children=3, nb_vertices=20):
    vid = vtx_id
    l=[vid]
    while nb_vertices > 0:
        n = min(nb_children, nb_vertices)
        vid = l.pop(0)
        for i in range(n):
            v = tree.add_child(vid)
            nb_vertices -= 1
            l.append(v)
    return tree

def random_tree(mtg, root, nb_children=3, nb_vertices=20):
    from random import randint
    vid = root
    l=[vid]
    while nb_vertices > 0:
        n = min(randint(1,nb_children), nb_vertices)
        vid = l.pop()
        for i in range(n):
            edge_type = '+'
            if i == n/2:
                edge_type='<'

            v=mtg.add_child(vid, edge_type=edge_type)
            nb_vertices -= 1
            l.append(v)
    return l[-1]

def random_mtg(tree, nb_scales):
    n = len(tree)
    # colors contained the colored vertices at each scale
    # based on the vertex of the initial tree
    colors = {}
    colors[nb_scales-1] = list(tree.vertices())
    for s in range(nb_scales-2, 0, -1):
        n = random.randint(1, n)
        l = random.sample(colors[s+1], n)
        l.sort()
        if tree.root not in l:
            l.insert(0, tree.root)
        colors[s] = l


    return colored_tree(tree, colors)[0]


def colored_tree(tree, colors):
    """
    Compute a mtg from a tree and the list of vertices to be quotiented.
    """

    nb_scales = max(colors.keys())+1

    map_index = {}
    g = MTG()
    # scale 0: 1 vertex
    count = 1

    for scale in range(1, nb_scales):
        map_index[scale] = {}
        for id in colors[scale]:
            map_index[scale][id] = count
            count += 1

    # build the mtg
    # 1. Add multiscale info
    index_scale = map_index[1]
    for id in colors[1]:
        g.add_component(g.root,index_scale[id])
    # Edit the graph with multiscale info
    for scale in range(2, nb_scales):
        prev_index_scale = index_scale
        index_scale = map_index[scale]
        for id in colors[scale]:
            complex_id = prev_index_scale.get(id)
            component_id = index_scale.get(id)

            if complex_id:
                g.add_component(complex_id, index_scale[id])
            elif component_id:
                g._scale[component_id] = scale

    # copy the tree information in the MTG
    if isinstance(tree, MTG):
        max_scale = tree.max_scale()
        g._parent.update(dict(((index_scale[k], index_scale[v])
                                for k, v in tree._parent.iteritems() if v and tree.scale(v) == max_scale)))
        for parent, children in tree._children.iteritems():

            if tree.scale(parent) == max_scale:
                g._children[index_scale[parent]] = [index_scale[id] for id in children]
    else:
        g._parent.update(dict(((index_scale[k], index_scale[v])
                                for k, v in tree._parent.iteritems() )))
        for parent, children in tree._children.iteritems():
            g._children[index_scale[parent]] = [index_scale[id] for id in children]

    # Copy the properties of the tree
    for pname, prop in tree.properties().iteritems():
        property = g._properties.setdefault(pname, {})
        for id, v in prop.iteritems():
            if tree.scale(id) == max_scale:
                property[index_scale[id]] = v

    return fat_mtg(g), dict(zip(index_scale.values(),index_scale.keys()))



################################################################################
# Utilities
################################################################################

def display_tree(tree, vid, tab = "", labels = {}, edge_type = {}):
    '''
    Display a tree structure.
    '''
    if not labels:
        labels = tree.property('label')
    if not edge_type:
        edge_type = tree.property('edge_type')

    et = '%s'%(edge_type.get(vid,'/'))
    assert vid in tree
    label = labels.get(vid, str(vid))
    yield tab+et+label
    for v in tree.children(vid):
        if edge_type.get(v) == '+':
            tab +='\t'
        for s in display_tree(tree, v, tab, edge_type=edge_type, labels=labels):
            yield s
        if edge_type.get(v) == '+':
            tab=tab[:-1]

def display_mtg(mtg, vid):
    label = mtg.property('label')
    edge_type = mtg.property('edge_type')
    current_vertex = vid
    tab = 0
    for vtx in traversal.iter_mtg2(mtg, vid):
        et = '/'
        if vtx != current_vertex:
            scale1 = mtg.scale(current_vertex)
            scale2 = mtg.scale(vtx)
            if scale1 >= scale2:
                et = edge_type[vtx]
                if scale1 == scale2:
                    if mtg.parent(vtx) != current_vertex:
                        tab = -1
                        et = '^'+et
                    else:
                        et = '^'+et
                elif scale1 > scale2:
                    v = current_vertex
                    for i in range(scale1-scale2):
                        v = mtg.complex(v)
                    if mtg.parent(vtx) == v:
                        et = '^'+et
                    else:
                        tab -= 1
                        et = '^'+et

            else:
                assert scale2 - scale1 == 1
                tab += 1

            yield tab* '\t' + et + label.get(vtx, str(vtx))
        current_vertex = vtx



def return_proxy(f):
    mtg_f = getattr(MTG, f.func_name)

    def new_f(self, *args, **kwds):
        id = mtg_f(self._g,self._vid,*args,**kwds)
        if id is not None:
            return self.__class__(self._g, id)
        else:
            return
    new_f.func_name = f.func_name
    new_f.__doc__ = mtg_f.__doc__
    return new_f

def proxy(f):
    mtg_f = getattr(MTG, f.func_name)
    def new_f(self, *args, **kwds):
        return mtg_f(self._g,self._vid,*args,**kwds)
    new_f.func_name = f.func_name
    new_f.__doc__ = mtg_f.__doc__
    return new_f

def return_iter_proxy(f):
    mtg_f = getattr(MTG, f.func_name)
    def new_f(self, *args, **kwds):
        return iter(self.__class__(self._g, id) for id in mtg_f(self._g,self._vid,*args,**kwds))
    new_f.func_name = f.func_name
    new_f.__doc__ = mtg_f.__doc__
    return new_f

def return_tuple_proxy(f):
    mtg_f = getattr(MTG, f.func_name)
    def new_f(self, *args, **kwds):
        return tuple(self.__class__(self._g, id) for id in mtg_f(self._g,self._vid,*args,**kwds))
    new_f.func_name = f.func_name
    new_f.__doc__ = mtg_f.__doc__
    return new_f

class _ProxyNode(object):
    def __init__(self, g, vid):
        self.__dict__['_g'] = g
        self.__dict__['_vid'] = vid

    def __setattr__(self,name, value):
        g = self._g; vid = self._vid
        if name not in g.property_names():
            g.add_property(name)
        g.property(name)[vid] = value

    def __getattr__(self, name):
        g = self._g; vid = self._vid

        if name in g.property_names():
            return g.property(name).get(vid)
        else:
            raise AttributeError(name) 

    def __eq__(self, other):
        return self._vid == other._vid
    def __hash__(self):
        return hash(self._vid)

    def __str__(self):
        return '_ProxyNode(%d)'%self._vid
    def __repr__(self):
        return '_ProxyNode(%d)'%self._vid

    # Wrappers for MTG methods.
    @proxy
    def scale(): pass
    @proxy
    def edge_type(): pass
    @proxy
    def index(): pass
    @return_proxy
    def parent(): pass
    @return_iter_proxy
    def children(): pass
    @proxy
    def nb_children(): pass
    @return_iter_proxy
    def siblings(): pass
    @proxy
    def nb_siblings(): pass
    @return_proxy
    def complex(): pass
    @return_iter_proxy
    def components(): pass
    @proxy
    def nb_components(): pass
    @return_proxy
    def complex_at_scale(): pass
    @return_iter_proxy
    def components_at_scale(): pass
    @return_iter_proxy
    def component_roots(): pass
    @return_iter_proxy
    def component_roots_at_scale(): pass
    @return_proxy
    def add_child(): pass
    @return_tuple_proxy
    def add_child_and_complex(): pass
    @return_proxy
    def insert_parent(): pass
    @return_proxy
    def insert_sibling(): pass
    @return_proxy
    def add_component(): pass
    @proxy
    def remove_vertex(): pass
    @return_iter_proxy
    def remove_tree(): pass
    

