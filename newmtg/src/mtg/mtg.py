# -*- python -*-
#
#       OpenAlea.mtg
#
#       Copyright 2008 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.pradal.at.cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

'''
This module provides an implementation of Multiscale Tree Graph.
For interface definition, see openalea.core.graph.interface
'''

import itertools

class MTG(object):

    def __init__(self):
        '''
        MTG constructor.
        TODO: add properties
        '''
        self._root = 0
        self._id = 0
        self._scale = {0:0}

        # Tree structure
        # Parent is a dict for DAG implementation
        self._parent = {}
        self._children = {}

        # Multiscale structure
        self._complex = {}
        self._components = {}

        # Properties: name vs property map
        self._properties = {}

        # add default properties
        self.add_property('edge_type')
        self.add_property('label')
        
    def scale(self, vsid):
        '''
        Return the scale of a vertex_scale identifier.
        '''
        return self._scale[vsid]

    def nb_scales(self):
        '''
        Return the number of scales.
        '''
        return len(set(self._scale.itervalues()))

    def scales(self):
        '''
        :Return: iter of scale_id
        '''
        return iter(set(self._scale.itervalues()))

    def max_scale(self):
        '''
        Return the max scale identifier.
        '''
        return max(self._scale.itervalues())

    #########################################################################
    # Some Vertex List Graph Concept methods.
    #########################################################################
    def __len__(self): 
        return self.nb_vertices()

    def nb_vertices(self, scale = -1):
        '''
        Return the number of vertices.

        :Return: int
        '''
        if scale < 0:
            return len(self._scale)
        else:
            return len(set(self.vertices(scale=scale)))

    def vertices(self, scale = -1):
        '''
        :Return: iter of vertex_id
        '''
        if scale < 0:
            return self._scale.iterkeys()
        else:
            return (vid for vid, sid in self._scale.iteritems() if sid == scale)

    def __iter__(self):
        return self.vertices()

    #########################################################################
    # GraphConcept methods.
    #########################################################################

    def has_vertex(self, vid):
        """
        test wether a vertex belong to the graph

        :param vid: vertex id to test
        :type vid: vid
        :rtype: bool
        """
        return vid in self._scale

    def __contains__(self, vid):
        return self.has_vertex(vid)

    def is_valid(self):
        """
        test the validity of the graph

        :rtype: bool
        """
        # TODO
        return True

    def iteredges(self, scale=-1):
        """
        iter on the edges of the mtg at a given scale.
        """
        if scale < 0:
            return self._parent.iteritems()
        else:
            return ((parent, child) for child, parent in self._parent.iteritems() if self.scale(parent) == scale)

    #########################################################################
    # MutableVertexGraphConcept methods.
    #########################################################################
    def add_element(self, parent_id, edge_type = '/', scale_id=None):
        """
        add an element to the graph, if vid is not provided create a new vid

        :param vid: the id of the vertex to add, default=None
        :type vid: vid
        :return: the id of the created vertex
        :rtype: vid
        """
        raise NotImplementedError

    def remove_vertex(self, vid):
        """
        remove a specified vertex of the graph
        remove all the edges attached to it

        :param vid: the id of the vertex to remove
        :type vid: vid
        """
        # TODO: remove recursively the sub_trees intra and inter scale.
        raise NotImplementedError

        if vid == self._root:
            raise 'Unable to delete the root of the MTG.'
        if vid in self._parent:
            del self._parent[vid]
        if vid in self._children:
            del self._children[vid]
        if vid in self._scale:
            del self._scale[vid]

    def clear(self):
        """
        remove all vertices and edges
        don't change references to objects
        """
        self._scale.clear()
        self._root = 0
        self._id = 0
        self._scale = {0:0}

        # Tree structure
        # Parent is a dict for DAG implementation
        self._parent.clear()
        self._children.clear()

        self._complex.clear()
        self._components.clear()

    #########################################################################
    # RootedTreeConcept methods.
    # TODO: Add methods from VertexListGraph concept
    #########################################################################

    def set_root(self, vtx_id):
        '''
        Set the tree root.
        
        :Parameters:
         - `vtx_id`: The vertex identifier.
         '''
        self._root = vtx_id

    def get_root(self): 
        '''
        Return the tree root.

        :Return: vertex identifier
        '''
        return self._root

    root= property( get_root, set_root )

    def parent(self, vtx_id):
        '''
        Return the parent of `vtx_id`.

        :Parameters:
        - `vtx_id`: The vertex identifier.

        :Return: vertex identifier
        '''
        #assert vtx_id in self._children[self._parent[vtx_id]]
        return self._parent.get(vtx_id)

    def children(self, vtx_id):
        '''
        Return a vertex iterator

        :Parameters:
        - `vtx_id`: The vertex identifier.

        :Return: iter of vertex identifier
        '''
        return iter(self._children.get(vtx_id,[]))

    def nb_children(self, vtx_id):
        '''
        Return the number of children

        :Parameters:
        - `vtx_id`: The vertex identifier.

        :Return: int
        '''
        return len(self._children.get(vtx_id,[]))

    def siblings(self, vtx_id):
        '''
        Return an iterator of vtx_id siblings.
        vtx_id is not include in siblings.

        :Parameters:
        - `vtx_id`: The vertex identifier.

        :Return: iter of vertex identifier
        '''
        parent = self.parent(vtx_id)
        return (vid for vid in self._children[parent] if vid != vtx_id)


    def nb_siblings(self, vtx_id):
        '''
        Return the number of siblings

        :Return: int
        '''
        parent = self.parent(vtx_id)
        return self.nb_children(parent)-1


    def is_leaf(self, vtx_id):
        '''
        Test if `vtx_id` is a leaf.

        :Return: bool
        '''
        return self.nb_children(vtx_id) == 0

    def roots(self, scale=0):
        '''
        Return an iterator of the vtx_id roots at a given `scale`.

        :Return: iter of vertex identifier
        '''
        return (vid for vid in self.vertices(scale=scale) if self.parent(vid) is None)


    #########################################################################
    # MutableTreeConcept methods.
    # TODO: Add methods from MutableVertexGraph concept.
    #########################################################################
    
    def add_child(self, parent, child=None, **properties):
        '''
        Add a child at the end of children

        :Parameters:
         - `parent`: The parent identifier.
         - `child`: The child identifier.

        :Return: vertex id
        '''


        if child is None:
            self._id += 1
            child = self._id

        self._add_vertex_properties(child, properties)

        self._children.setdefault(parent,[]).append(child)
        self._parent[child] = parent
        self._scale[child] = self._scale[parent]
        return child

    def insert_sibling(self, vtx_id1, vtx_id2=None, **properties):
        '''
        Insert vtx_id2 before vtx_id1.

        :Parameters:
         - `vtx_id1`: a vertex identifier
         - `vtx_id2`: the vertex to insert
        '''

        if vtx_id2 is None:
            self._id += 1
            vtx_id2 = self._id

        self._add_vertex_properties(vtx_id2, properties)

        parent = self.parent(vtx_id1)
        siblings = self._children[parent]
        index = siblings.index(vtx_id1)
        siblings.insert(index,vtx_id2)

        self._parent[vtx_id2] = parent
        self._scale[vtx_id2] = self._scale[vtx_id1]
        return vtx_id2

    def insert_parent(self, vtx_id, parent_id=None, **properties): 
        '''
        Insert parent_id between vtx_id and its actual parent.
        Inherit of the complex of the parent of vtx_id.

        :Parameters:
        - `vtx_id`: a vertex identifier
        - `parent_id`: a vertex identifier
        '''

        if parent_id is None:
            self._id += 1
            parent_id = self._id

        self._add_vertex_properties(parent_id, properties)

        old_parent = self.parent(vtx_id)
        children = self._children[old_parent]

        self.add_child(parent_id, vtx_id)
        # replace vtx_id by parent_id in children of old_parent
        index = children.index(vtx_id)
        children[index] = parent_id
        return parent_id

    #########################################################################
    # Mutable Multiscale Tree Concept methods.
    #########################################################################

    def complex(self, vtx_id):
        '''
        Return the complex of `vtx_id`.

        :Parameters:
        - `vtx_id`: The vertex identifier.

        :Return: vertex identifier
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
        Return the complex of `vtx_id` at scale `scale`.

        :Parameters:
        - `vtx_id`: The vertex identifier.
        - `scale`: The scale identifier.

        :Return: vertex identifier
        '''
        complex_id = vtx_id
        current_scale = self.scale(complex_id)
        for i in range(scale, current_scale):
            complex_id = self.complex(complex_id)
        return complex_id

    def components(self, vid):
        '''
        Return a vertex iterator

        :Parameters:
        - `vid`: The vertex identifier.

        :Return: iter of vertex identifier
        '''
        # oops: search in the tree all the nodes which have not another
        # explicit complex.

        # Be sure to copy the list beforez modifying it...
        l = list(self._components.get(vid,[]))

        while len(l) > 0:
            vid = l.pop(0)
            yield vid
            for id in self.children(vid):
                if id in self._complex:
                    continue
                l.insert(0,id)

    def nb_components(self, vid):
        '''
        Return the number of components

        :Parameters:
        - `vid`: The vertex identifier.

        :Return: int
        '''
        return len(list(self.components(vid)))

    # mutable
    def add_component(self, complex_id, component_id=None, **properties):
        '''
        Add a component at the end of the components

        :Parameters:
         - `complex_id`: The complex identifier.
         - `component_id`: Set the component identifier to this value if defined.
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
        :Return: (vid, vid)
        '''

        if child is None:
            self._id += 1
            child = self._id

        self._add_vertex_properties(child, properties)

        self._children.setdefault(parent,[]).append(child)
        self._parent[child] = parent
        self._scale[child] = self._scale[parent]

        if complex is None:
            self._id += 1
            complex = self._id

        parent_complex = self.complex(parent)

        self._children.setdefault(parent_complex,[]).append(complex)
        self._parent[complex] = parent_complex
        self._scale[complex] = self._scale[parent_complex]


        self._components.setdefault(complex,[]).append(child)
        self._complex[child] = complex

        return child, complex

    def __str__(self):
        l = ["MTG : nb_vertices=%d, nb_scales=%d"%(self.nb_vertices(), self.nb_scales())]
        v  = self.root

        edge_type = self.property('edge_type')
        label = self.property('label')
        while v is not None:
            l.append("\nScale %d"%self.scale(v))
            l.extend(display_tree(self,v, edge_type=edge_type, labels=label))
            compo = self._components.get(v,[None])
            v= compo[0]
        return '\n'.join(l)

    #########################################################################
    # Property Interface for Tree Graph and Mutable property concept.
    #########################################################################

    def property_names(self):
        '''
        iter on names of all property maps.
        Properties are defined only on vertices, even edge properties.
        return iter of names
        '''
        return self._properties.iterkeys()

    def property(self, name):
        '''
        Returns the property map between the vid and the data.
        :Return:  dict of {vid:data}
        '''
        return self._properties.get(name, {})

    def add_property(self, property_name):
        """
        Add a new map between vid and a data
        Do not fill this property for any vertex
        """
        self._properties[property_name] = {}

    def remove_property(self, property_name):
        """
        Remove the property map called property_name from the graph.
        """
        del self._properties[property_name]

    def properties(self):
        """
        Returns all the property maps contain in the graph.
        """
        return self._properties

    def _add_vertex_properties(self, vid, properties):
        """
        Add a set of properties for a vertex identifier.
        """
        for name in properties:
            if name in self._properties:
                self._properties[name][vid] = properties[name]

################################################################################
# Tree Traversals
################################################################################

def pre_order(tree, vtx_id):
    ''' 
    Traverse a tree in a prefix way.
    (root then children)

    This is a non recursive implementation.
    '''
    yield vtx_id
    for vid in tree.children(vtx_id):
        for node in pre_order(tree, vid):
            yield node
    
def post_order(tree, vtx_id):
    ''' 
    Traverse a tree in a postfix way.
    (from leaves to root)
    '''
    for vid in tree.children(vtx_id):
        for node in post_order(tree, vid):
            yield node
    yield vtx_id

def traverse_tree(tree, vtx_id, visitor):
  ''' 
  Traverse a tree in a prefix or postfix way.
  
  We call a visitor for each vertex.
  This is usefull for printing, cmputing or storing vertices 
  in a specific order. 
  
  See boost.graph.
  '''

  yield visitor.pre_order(vtx_id)

  for v in tree.children(vtx_id):
     for res in traverse_tree(tree, v, visitor):
        yield res

  yield visitor.post_order(vtx_id)


class Visitor(object):
  ''' Used during a tree traversal. '''

  def pre_order(self, vtx_id): 
     pass

  def post_order(self, vtx_id): 
     pass

def iter_mtg(mtg, vtx_id):
    
    for vid in pre_order(mtg, vtx_id): 
        for node in iter_scale(mtg, vid):
            yield node

def iter_scale( mtg, vtx_id):
    yield vtx_id
    for vid in mtg.components(vtx_id):
        for node in iter_scale(mtg, vid):
            yield node
    
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
    for vtx in iter_mtg(mtg, vid):
        yield mtg.scale(vtx) * '  ' + edge_type.get(vtx, '/') + label.get(vtx, str(vtx))

def fat_mtg(slim_mtg):
    """
    Compute missing edges at each scales based on the explicit edges
    defines at finer scales and decomposition relationship.
    """ 
    max_scale = max(slim_mtg.scales())
    roots = slim_mtg.roots(scale=max_scale)
    assert len(list(roots)) == 1
    
    for scale in range(max_scale-1,0,-1):
        compute_missing_edges(slim_mtg, scale)
    return slim_mtg

def compute_missing_edges(mtg, scale):
    roots = mtg.roots(scale=scale)

    for vid in roots:
        components = mtg._components[vid]
        #assert len(components) == 1
        cid = components[0]
        if mtg.parent(cid) is None:
            continue
        edge_type = mtg.property('edge_type')[cid]
        parent_id = mtg.complex(mtg.parent(cid))
        mtg.add_child(parent_id, child=vid, edge_type=edge_type)
        
    return True


