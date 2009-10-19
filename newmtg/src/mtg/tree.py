# -*- coding: utf-8 -*-
# -*- python -*-
#
#       OpenAlea.Container
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
This is a copy of the file in openalea.container.
This copy is used only for dependencies management
before moving MTG in openalea.container.

This module provides an implementation of a rooted tree graph.
For interface definition, see :mod:`openalea.container.interface.tree`.
'''

__docformat__ = "restructuredtext"
__license__ = "Cecill-C"
__revision__ = " $Id: $ "

#from interface.tree import ITree, IMutableTree, IEditableTree
#from interface.graph import IRootedGraph, InvalidVertex, InvalidEdge
#from traversal.tree import pre_order, post_order

class GraphError(Exception):
    """
    base class of all graph exceptions
    """

class InvalidVertex (GraphError, KeyError) :
    """
    exception raised when a wrong vertex id is provided
    """

class Tree(object):
    '''
    Implementation of a rooted :class:`Tree`, 
    with methods to add and remove vertex.
    '''

    def __init__(self, tree= None):
        '''
        Tree constructor.
        '''
        self._root = 0
        self._id = 0
        # Tree structure
        # Parent is a dict for DAG implementation
        self._parent = {self._root : None}
        self._children = {}


    #########################################################################
    # Some Vertex List Graph Concept methods.
    #########################################################################

    def __len__(self):
        return self.nb_vertices()

    def nb_vertices(self):
        '''
        returns the number of vertices.

        :returns: int
        '''
        return len(self._parent)

    def vertices(self):
        '''
        :returns: iter of vertex_id
        '''
        return self._parent.iterkeys()

    def __iter__(self):
        return self.vertices()

    #########################################################################
    # GraphConcept methods.
    #########################################################################

    def has_vertex(self, vid):
        """
        Test wether a vertex belong to the graph

        :param vid: vertex id to test
        :type vid: vid
        :rtype: bool
        """
        return vid in self._parent

    def __contains__(self, vid):
        return self.has_vertex(vid)

    def is_valid(self):
        """
        test the validity of the graph

        :rtype: bool
        """
        # TODO
        return True

    def iteredges(self):
        """
        Iter on the edges of the tree.
        """
        return ((parent, child) for child, parent in self._parent.iteritems())

    #########################################################################
    # MutableVertexGraphConcept methods.
    #########################################################################

    def remove_vertex(self, vid):
        """
        remove a specified vertex of the graph
        remove all the edges attached to it

        :param vid: the id of the vertex to remove
        :type vid: vid
        """
        if vid == self.root:
            raise InvalidVertex('Removing the root node %d is forbidden.'% vid)

        elif self.nb_children(vid) == 0:
            p = self._parent[vid]
            self._children[p].remove(vid)
            del self._parent[vid]
            if vid in self._children:
                del self._children[vid]
        else:
            raise InvalidVertex('Can not remove vertex %d  with children. Use remove_tree instead.'% vid)

    def clear(self):
        """
        remove all vertices and edges
        don't change references to objects
        """
        self._root = 0
        self._id = 0

        # Tree structure
        # Parent is a dict for DAG implementation
        self._parent.clear()
        self._children.clear()
        self._parent[self._root] = None


    #########################################################################
    # RootedTreeConcept methods.
    #########################################################################

    def set_root(self, vtx_id):
        '''
        Set the tree root.

        :param vtx_id: The vertex identifier.
         '''
        self._root = vtx_id
        if self._root not in self._parent:
            self._parent[self._root] = None

    def get_root(self):
        '''
        Return the tree root.

        :return: vertex identifier
        '''
        return self._root

    root= property( get_root, set_root )

    def parent(self, vtx_id):
        '''
        Return the parent of `vtx_id`.

        :Parameters:
         - `vtx_id`: The vertex identifier.

        :returns: vertex identifier
        '''
        return self._parent.get(vtx_id)

    def children(self, vtx_id):
        '''
        returns a vertex iterator

        :param vtx_id: The vertex identifier.

        :returns: iter of vertex identifier
        '''
        return iter(self._children.get(vtx_id,[]))

    def nb_children(self, vtx_id):
        '''
        returns the number of children

        :Parameters:
         - `vtx_id`: The vertex identifier.

        :returns: int
        '''
        return len(self._children.get(vtx_id,[]))

    def siblings(self, vtx_id):
        '''
        returns an iterator of vtx_id siblings.
        vtx_id is not include in siblings.

        :Parameters:
         - `vtx_id`: The vertex identifier.

        :returns: iter of vertex identifier
        '''
        parent = self.parent(vtx_id)
        return (vid for vid in self._children[parent] if vid != vtx_id)


    def nb_siblings(self, vtx_id):
        '''
        returns the number of siblings

        :returns: int
        '''
        parent = self.parent(vtx_id)
        return self.nb_children(parent)-1


    def is_leaf(self, vtx_id):
        '''
        Test if `vtx_id` is a leaf.

        :returns: bool
        '''
        return self.nb_children(vtx_id) == 0

    #########################################################################
    # MutableTreeConcept methods.
    #########################################################################
    
    def add_child(self, parent, child=None, **properties):
        '''
        Add a child at the end of children

        :param parent: The parent identifier.
        :param child: The child identifier.

        :returns: vertex id
        '''


        if child is None:
            self._id += 1
            child = self._id

        self._children.setdefault(parent,[]).append(child)
        self._parent[child] = parent

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

        parent = self.parent(vtx_id1)
        siblings = self._children[parent]
        index = siblings.index(vtx_id1)
        siblings.insert(index,vtx_id2)

        self._parent[vtx_id2] = parent

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

        old_parent = self.parent(vtx_id)
        children = self._children[old_parent]

        self.add_child(parent_id, vtx_id)
        # replace vtx_id by parent_id in children of old_parent
        index = children.index(vtx_id)
        children[index] = parent_id
        return parent_id


    def __str__(self):
        l = ["Tree : nb_vertices=%d"%(self.nb_vertices())]
        v  = self.root

        edge_type = self.property('edge_type')
        label = self.property('label')
        l.extend(display_tree(self,v, edge_type=edge_type, labels=label))
        return '\n'.join(l)

    #########################################################################
    # Editable Tree Interface.
    #########################################################################

    def sub_tree(self, vtx_id, copy=True):
        """Return the subtree rooted on `vtx_id`.

        The induced subtree of the tree has the vertices in the ancestors of vtx_id.

        :Parameters:
          - `vtx_id`: A vertex of the original tree.
          - `copy`:  
            If True, return a new tree holding the subtree. If False, the subtree is
            created using the original tree by deleting all vertices not in the subtree.

        :returns: A sub tree of the tree. If copy=True, a new Tree is returned. 
            Else the subtree is created inplace by modifying the original tree. 
        """

        if not copy:
            # remove all vertices not in the sub_tree
            bunch = set(pre_order(self, vtx_id))
            for vid in self:
                if vid not in bunch:
                    self.remove_vertex(vid)

            self._root = vtx_id
            self._parent[self._root] = None
            return self
        else:
            treeid_id = {}
            tree = Tree()
            tree.root = 0
            treeid_id[vtx_id] = tree.root
            subtree = pre_order(self, vtx_id)
            
            subtree.next()
            for vid in subtree:
                parent = treeid_id[self.parent(vid)]
                v = tree.add_child(parent)
                treeid_id[vid] = v

            return tree

    def insert_sibling_tree(self, vid, tree ): 
        """
        Insert a tree before the vid.
        vid and the root of the tree are siblings.
        Complexity have to be O(1) if tree comes from the actual tree
        ( tree= self.sub_tree() )

        :param vid: vertex identifier
        :param tree: a rooted tree
        """
        treeid_id = {}
        root = tree.root
        root_id = self.insert_sibling(vid)
        treeid_id[root]=root_id

        # pre_order traversal from root and renumbering
        for vtx_id in pre_order(tree, vid):
            parent = treeid_id[tree.parent(vtx_id)]
            v = self.add_child(parent)
            treeid_id[vtx_id] = v

        return treeid_id
        

    def add_child_tree(self, parent, tree): 
        """
        Add a tree after the children of the parent vertex.
        Complexity have to be O(1) if tree == sub_tree()

        :param parent: vertex identifier
        :param tree: a rooted tree
        """
        treeid_id = {}
        root = tree.root
        root_id = self.add_child(parent)
        treeid_id[root]=root_id

        # pre_order traversal from root and renumbering
        for vtx_id in pre_order(tree, root):
            parent = treeid_id[tree.parent(vtx_id)]
            vid = self.add_child(parent)
            treeid_id[vtx_id] = vid

        return treeid_id

    def remove_tree(self, vtx_id):
        """
        Remove the sub tree rooted on `vtx_id`.

        :returns: bool
        """
        vid = vtx_id

        vertices = []

        for vtx_id in post_order(self, vid):
            self.remove_vertex(vtx_id)
            vertices.append(vtx_id)

        return vertices
            


    def copy(self):
        """ Deep copy of the tree.
        """
        return deepcopy(self)


class PropertyTree(Tree):

    def __init__(self, *args, **kwds):
        '''
        Tree with proeprties.
        '''
        super(PropertyTree, self).__init__(*args, **kwds)
        self._properties = {}

    def remove_vertex(self, vid):
        """
        remove a specified vertex of the graph
        remove all the edges attached to it

        :param vid: the id of the vertex to remove
        :type vid: vid
        """
        vid = super(PropertyTree, self).remove_vertex(vid)
        self._remove_vertex_properties(vid)

    def add_child(self, parent, child=None, **properties):
        '''
        Add a child at the end of children

        :param parent: The parent identifier.
        :param child: The child identifier.

        :returns: vertex id
        '''

        child = super(PropertyTree, self).add_child(parent, child)

        # Update the properties
        self._add_vertex_properties(child, properties)

        return child

    def insert_sibling(self, vtx_id1, vtx_id2=None, **properties):
        '''
        Insert vtx_id2 before vtx_id1.

        :Parameters:
         - `vtx_id1`: a vertex identifier
         - `vtx_id2`: the vertex to insert
        '''

        vtx_id2 = super(PropertyTree, self).insert_sibling(vtx_id1, vtx_id2)

        # Update the properties
        self._add_vertex_properties(vtx_id2, properties)
 
        return vtx_id2

    def insert_parent(self, vtx_id, parent_id=None, **properties):
        '''
        Insert parent_id between vtx_id and its actual parent.
        Inherit of the complex of the parent of vtx_id.

        :Parameters:
         - `vtx_id`: a vertex identifier
         - `parent_id`: a vertex identifier
        '''

        parent_id = super(PropertyTree, self).insert_parent(vtx_id, parent_id)
        self._add_vertex_properties(parent_id, properties)

        return parent_id

    #########################################################################
    # Editable Tree Interface.
    #########################################################################

    def sub_tree(self, vtx_id, copy=True):
        """Return the subtree rooted on `vtx_id`.

        The induced subtree of the tree has the vertices in the ancestors of vtx_id.

        :Parameters:
          - `vtx_id`: A vertex of the original tree.
          - `copy`:  
            If True, return a new tree holding the subtree. If False, the subtree is
            created using the original tree by deleting all vertices not in the subtree.

        :returns: A sub tree of the tree. If copy=True, a new Tree is returned. 
            Else the subtree is created inplace by modifying the original tree. 
        """
        if not copy:
            # remove all vertices not in the sub_tree
            bunch = set(pre_order(self, vtx_id))
            for vid in self:
                if vid not in bunch:
                    self.remove_vertex(vid)
                    self._remove_vertex_properties(vid)

            self.root = vtx_id
            return self
        else:
            treeid_id = {}
            tree = self.__class__()
            tree.root = 0
            treeid_id[vtx_id] = tree.root
            subtree = pre_order(tree, vtx_id)
            subtree.next()
            for vid in subtree:
                parent = treeid_id[self.parent(vid)]
                v = tree.add_child(parent)
                treeid_id[vid] = v

            for tid, vid in treeid_id.iteritems():
                for name in self.properties():
                    v = self.property(name).get(tid)
                    if v is not None:
                        tree._properties[name][vid] = v

            return tree

    def insert_sibling_tree(self, vid, tree ): 
        """
        Insert a tree before the vid.
        vid and the root of the tree are siblings.
        Complexity have to be O(1) if tree comes from the actual tree
        ( tree= self.sub_tree() )

        :param vid: vertex identifier
        :param tree: a rooted tree
        """
        treeid_id = super(PropertyTree, self).insert_sibling_tree(vid, tree)
        for tid, vid in treeid_id.iteritems():
            for name in tree.properties():
                v = tree.property(name).get(tid)
                if v is not None:
                    self._properties[name][vid] = v

        return treeid_id
        

    def add_child_tree(self, parent, tree): 
        """
        Add a tree after the children of the parent vertex.
        Complexity have to be O(1) if tree == sub_tree()

        :param parent: vertex identifier
        :param tree: a rooted tree
        """
        treeid_id = super(PropertyTree, self).add_child_tree(parent, tree)
        for tid, vid in treeid_id.iteritems():
            for name in tree.properties():
                v = tree.property(name).get(tid)
                if v is not None:
                    self._properties[name][vid] = v

        return treeid_id

    def remove_tree(self, vtx_id):
        """
        Remove the sub tree rooted on `vtx_id`.

        :returns: bool
        """
        vids = super(PropertyTree, self).remove_tree(vids)
        for vid in vids:
            self._remove_vertex_properties(vid)
        return vids

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
        :returns:  dict of {vid:data}
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

    def _remove_vertex_properties(self, vid):
        """
        Add a set of properties for a vertex identifier.
        """
        for name in self.properties():
            p = self.property(name)
            if vid in p:
                del p[vid]


def pre_order(tree, vtx_id, edge_type_property = None):
    ''' 
    Traverse a tree in a prefix way.
    (root then children)
    Return an iterator on vertices.
    If an edge_type_property is given, visit first branches rather than successor.

    This is a non recursive implementation.
    '''

    if edge_type_property is None:
        yield vtx_id
        for vid in tree.children(vtx_id):
            for node in pre_order(tree, vid):
                yield node
    else:

        # 1. select first '+' edges
        successor = []
        yield vtx_id
        for vid in tree.children(vtx_id):
            if edge_type.get(vid) == '<':
                successor.append(vid)
                continue

            for node in pre_order(tree, vid):
                yield node

        # 2. select then '<' edges
        for vid in successor:
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

def level_order(tree, vtx_id):
    ''' Traverse the vertices in a level order.

    Traverse the root node, then its children and so on.
    '''
    queue = deque()
    queue.append(vtx_id)

    while queue:
        vid = queue.popleft()
        yield vid
        queue.extend(tree.children(vid))


def depth_order(tree, vtx_id):
    '''Traverse all the leaves first.
    Then their parent until the root.

    .. todo:: To implement

    '''
    raise NotImplementedError


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

