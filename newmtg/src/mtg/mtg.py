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
For interface definition, see openalea.core.graph.interface
'''

__docformat__ = "restructuredtext"

import itertools
import traversal
import random

try: 
    from openalea.container.tree import PropertyTree, InvalidVertex
except ImportError:
    from tree import PropertyTree, InvalidVertex


class MTG(PropertyTree):

    def __init__(self):
        '''
        MTG constructor.
        '''

        super(MTG, self).__init__()

        self._scale = {0:0}

        # Multiscale structure
        self._complex = {}
        self._components = {}

        # add default properties
        self.add_property('edge_type')
        self.add_property('label')

    def scale(self, vid):
        '''
        Returns the scale of a vertex_scale identifier.

        :param vid: vertex identifier
        :rtype: int
        '''
        return self._scale[vid]

    def nb_scales(self):
        '''
        :returns: the number of scales.
        '''
        return len(set(self._scale.itervalues()))

    def scales(self):
        '''
        :returns: iter of scale_id
        '''
        return iter(set(self._scale.itervalues()))

    def max_scale(self):
        '''
        :returns: the max scale identifier.
        '''
        return max(self._scale.itervalues())

    #########################################################################
    # Some Vertex List Graph Concept methods.
    #########################################################################

    def nb_vertices(self, scale = -1):
        '''
        returns the number of vertices.

        :returns: int
        '''
        if scale < 0:
            return len(self._scale)
        else:
            return len(set(self.vertices(scale=scale)))

    def vertices(self, scale = -1):
        '''
        :returns: iter of vertex_id
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

        if self.nb_components(vid) == 0:
            super(MTG, self).remove_vertex(vid)
            if vid in self._scale:
                del self._scale[vid]
            if vid in self._complex:
                del self._complex[vid]
        else:
            raise InvalidVertex('Can not remove vertex %d with components.'
            'Use remove_tree instead.'%vid)

    def clear(self):
        """
        remove all vertices and edges
        don't change references to objects
        """
        super(MTG, self).clear()

        self._scale.clear()
        self._scale = {0:0}

        self._complex.clear()
        self._components.clear()

    def roots(self, scale=0):
        '''
        returns an iterator of the vtx_id roots at a given `scale`.

        :returns: iter of vertex identifier
        '''
        return (vid for vid in self.vertices(scale=scale) if self.parent(vid) is None)


    #########################################################################
    # MutableTreeConcept methods.
    # TODO: Add methods from MutableVertexGraph concept.
    #########################################################################
    
    def add_child(self, parent, child=None, **properties):
        '''
        Add a child at the end of children

        :param parent: The parent identifier.
        :param child: The child identifier.

        :returns: vertex id
        '''

        child = super(MTG, self).add_child(parent, child, **properties)
        self._scale[child] = self._scale[parent]
        return child

    def insert_sibling(self, vtx_id1, vtx_id2=None, **properties):
        '''
        Insert vtx_id2 before vtx_id1.

        :Parameters:
         - `vtx_id1`: a vertex identifier
         - `vtx_id2`: the vertex to insert
        '''

        vtx_id2 = super(MTG, self).insert_sibling(vtx_id1, vtx_id2, **properties)
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

        self._scale[parent_id] = self.scale(vtx_id)

        parent_id = super(MTG, self).insert_parent(vtx_id, parent_id, **properties)

        return parent_id

    #########################################################################
    # Mutable Multiscale Tree Concept methods.
    #########################################################################

    def complex(self, vtx_id):
        '''
        returns the complex of `vtx_id`.

        :Parameters:
         - `vtx_id`: The vertex identifier.

        :returns: vertex identifier
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
        returns the complex of `vtx_id` at scale `scale`.

        :Parameters:
         - `vtx_id`: The vertex identifier.
         - `scale`: The scale identifier.

        :returns: vertex identifier
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
        # oops: search in the tree all the nodes which have not another
        # explicit complex.

        if vid in self._components:
            v = self._components[vid][0]
            for vtx in traversal.pre_order(self, v, complex=vid):
                yield vtx

    def components_at_scale(self, vid, scale):
        '''
        returns a vertex iterator

        :Parameters:
         - `vid`: The vertex identifier.

        :returns: iter of vertex identifier
        '''
        # oops: search in the tree all the nodes which have not another
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
            for i in range(cur_scale+1, scale):
                gen = (vid for vtx in gen for vid in self.component_roots(vtx)) 
            return gen
        
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
        :returns: (vid, vid)
        '''

        if complex is None:
            self._id += 1
            complex = self._id

        child = super(MTG, self).add_child(parent, child, **properties)
        self._scale[child] = self._scale[parent]


        parent_complex = self.complex(parent)

        super(MTG, self).add_child(parent_complex, complex)
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
    for vtx in traversal.iter_mtg(mtg, vid):
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



