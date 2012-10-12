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
################################################################################
''' This module implement a solver to build 3D representation of a plant mockup 
based on various infomation.

:Principles:
    

:Algorithm:


:Examples:

.. todo::
    - See the turtle frame. What is missing in both?
    - 
'''




class Frame(object):
    """ Frame representing geometric variables of each topologic elements.
    
    A frame is used to have a common representation of the geometric information 
    for each topological elements.

    Variables contain:
        * origin: 3D point
        * transformation: 3 euler angles
        * bounding box: length, top and bottom radius.
    """

    def __init__(self, **kwds):
        """ Build a default frame.

        By default there is no default value.
        :Parameters:
            - origin : the origin of the frame
            - angles : euler angles representing the transormation between absolute and local frame.
            - length : length of the element
            - bottom_radius : bottom radius of the bounding box
            - top_radius: top radius of the bounding box.

        Defining only top and bottom radius rather than width and height imply 
        an axial or radial symmetry 
        which is often the case for plant (leaves, branches, fruit).
        """
        self._top = kwds.get('top')
        self._bottom = kwds.get('bottom')
        self._angles = kwds.get('angles')
        self._length = kwds.get('length')
        self._bottom_radius = kwds.get('bottom_radius')
        self._top_radius = kwds.get('top_radius')

        # Are the variables hard or soft constraints?
        # Is it a user input or the result of a solver, or an algorithm?
        self._has_bottom= bool(self.bottom)
        self._has_top= bool(self.top)
        self._has_angles = bool(self.angles)
        self._has_length = bool(self.length)
        self._has_bottom_radius = bool(self.bottom_radius)
        self._has_top_radius = bool(self.top_radius)

    def set_origin(self, origin, hard=False):
        """ Set the origin of the frame.
        """
        self._origin = origin
        self_has_origin = hard

    def get_origin(self):
        return self._origin

    origin = property(get_origin, set_origin, 'Origin of the Frame')
        
    def set_angles(self, angles, hard=False):
        """ Set the angles of the frame.
        hard indicates if it is a hard (user defines) or soft (computed value) constraints.
        """
        self._angles = angles
        self_has_angles = hard

    def get_angles(self):
        return self._angles

    angles = property(get_angles, set_angles, 'angles of the Frame')

    def set_length(self, length, hard=False):
        """ Set the length of the frame.
        hard indicates if it is a hard (user defines) or soft (computed value) constraints.
        """
        self._length = length
        self_has_length = hard

    def get_length(self):
        return self._length

    length = property(get_length, set_length, 'length of the Frame')

    def set_bottom_radius(self, bottom_radius, hard=False):
        """ Set the bottom_radius of the frame.
        hard indicates if it is a hard (user defines) or soft (computed value) constraints.
        """
        self._bottom_radius = bottom_radius
        self_has_bottom_radius = hard

    def get_bottom_radius(self):
        return self._bottom_radius

    bottom_radius = property(get_bottom_radius, set_bottom_radius, 'bottom_radius of the Frame')

    def set_top_radius(self, top_radius, hard=False):
        """ Set the top_radius of the frame.
        hard indicates if it is a hard (user defines) or soft (computed value) constraints.
        """
        self._top_radius = top_radius
        self_has_top_radius = hard

    def get_top_radius(self):
        return self._top_radius

    top_radius = property(get_top_radius, set_top_radius, 'top_radius of the Frame')


class AxialFrames(object):
    ''' Solve continuity constraints on an axis, i.e. a set of frames.

    '''
    pass



class PlantFrame(object):
    ''' Engine to compute the geometry of a plant based on 
    its topological description and parameters.
    '''

    def __init__(self, g, *args, **kwds):
        ''' Compute a geometric representation of a plant.

        Compute the skeleton of the MTG with a Frame linked to each elements.
        
        :Parameters:
            - g: MTG representing the plant architecture at different scales.
        '''
        self.g = g

        # Global parameters
        self.origin = kwds.get('origin', (0,0,0))

        # properties defined for each vertex.
        # length define the length of a vertex
        self.length = self._extract_properties('Length', kwds)
        self.top_diameter = self._extract_properties('TopDiameter', kwds)
        self.bottom_diameter = self._extract_properties('BottomDiameter', kwds)

        # Absolute coordinate of the components
        self.xx= self._extract_properties('XX', kwds)
        self.yy = self._extract_properties('YY', kwds)
        self.zz = self._extract_properties('ZZ', kwds)

        # Absolute euler angles in degree
        self.aa= self._extract_properties('AA', kwds)
        self.bb = self._extract_properties('BB', kwds)
        self.cc = self._extract_properties('CC', kwds)

        # Relative angles: TO BE DEFINED: alpha, beta, rolll
        # Default values: Dressing data as a dictionnary or an object.
        # Curves associated to an element
        # Geometry associated to an element with mtg parameters
        
        # Express everything in degrees or radians. 
        # Do not mix both.

        # Define the inference algorithms to compute missing parameters.
        # Add new algorithms as:
        #   - Visitors 
        #   - plug'in.
        #   - derivation


        # 1. Get the different parameters
        # 2. Build for each element at a given scale the frames.
        # 3 Solve the different constranits by using a plug'in mechanism
        # 4. Design new algo and define new parameters.
        # 5. Use WeberPenn with MTG

    def _extract_properties(self, name, kwds):
        ''' Extract the property from properties of the mtg 
        or from a user given function.
        '''
        d = {}

        func = kwds.get(name)
        if func:
            # Compute the value for all vertices
            all_values = ((vid,func(vid)) for vid in g.vertices_iter())
            # Select only those which are defined
            values = ( (vid, fvid) for vid, fvid in all_values if fvid is not None)

            d = dict(values)
            
        name_property = g.property(name).copy()
        name_property.update(d)

        return name_property
        
        

    def _compute_global_data(self, factor=1):
        self.points = {}
        points = self.points
        for vid in self.xx:
            try:
                points[vid] = xx[vid]*factor, yy[vid]*factor, zz[vid]*factor
            except:
                continue

        self.euler_angles = {}
        angles = self.euler_angles
        for vid in self.aa:
            try:
                angles[vid] = self.aa[vid], self.bb[vid], self.cc[vid]
            except:
                continue

    def _get_origin(self, vid):
        ''' Compute the origin for the vertex `vid`.
        '''
        # 1. compute the origin of the tree
        # Check if a complex has origin
        origin = self.origin
        vid = self.g.complex(vid)
        while vid:
            if vid in self.points:
                origin = self.points[vid]
                break
        self.origin = origin
        return self.origin

    def run(self, scale= -1):
        '''Compute the geometry of the plant.
        '''
        
        if scale == -1:
            scale = g.max_scale()

        root = g.roots(scale=scale)[0]

        # 1. compute the origin of the tree
        # Check if a complex has origin
        self.origin = self._get_origin(root)

        axes = compute_axes(g, root, self.points)
        
        # Compute the points
        # 1. compute fixed points
        # 
        

def iter_order(g, v, edge_type = None):
    ''' Iter on a tree by considering first 
    all the vertices of the axe at the first order,
    then the vertices at the second order and so on.
    '''
    pass

def compute_axes(g, v, fixed_points):
    marked = {}
    axes = {}
    for vid in post_order(g,v):
        if vid in marked:
            continue
        _axe = list(simple_axe(g,vid, marked, fixed_points))
        _axe.reverse()
        axes.setdefault(g.order(_axe[0]),[]).append(_axe)
    return axes

def simple_axe(g, v, marked, fixed_points):
    edge_type = g.property('edge_type')
    
    while v is not None:
        if v in fixed_points:
            yield v
        
        assert v not in marked
        marked[v] = True
        
        if g.parent(v) is None or edge_type[v] == '+':
            break
        v = g.parent(v)

def compute_radius(g, v, last_radius):
    all_r2 = {}
    for vid in post_order(g, v):
        r2 = max(sum([all_r2[c] for c in g.children_iter(vid)]), last_radius)
        all_r2[vid] = r2
    for k, v in all_r2.iteritems():
        all_r2[k] = sqrt(v)
    return all_r2


#def PlantFrame(g, Vertex=0, **kwds):
#    pass    

 
#self.add_input( name = "MTG", interface = None) 
#        self.add_input( name = "Vertex", interface = IInt, value= 0)
#        self.add_input( name = "Scale", interface = IInt, value= 0,hide=True)
#        self.add_input( name = "VoxelDist", interface = IFloat, value=None,hide=True)
#        self.add_input( name = "TrunkDistance", interface = IFloat, value=None,hide=True)
#        self.add_input( name = "Category", interface = IFunction,hide=True)
#        self.add_input( name = "Length", interface = IFunction,hide=True)
#        self.add_input( name = "LengthAlgo", interface = IStr, value=None,hide=True)
#        self.add_input( name = "TopDiameter", interface = IFunction,hide=True)
#        self.add_input( name = "BottomDiameter", interface = IFunction,hide=True)
#        self.add_input( name = "Alpha", interface = IFunction,hide=True)
#        self.add_input( name = "Azimuth", interface = IFunction,hide=True)
#        self.add_input( name = "AA", interface = IFunction,hide=True)
#        self.add_input( name = "BB", interface = IFunction,hide=True)
#        self.add_input( name = "CC", interface = IFunction,hide=True)
#        self.add_input( name = "XX", interface = IFunction,hide=True)
#        self.add_input( name = "YY", interface = IFunction,hide=True)
#        self.add_input( name = "ZZ", interface = IFunction,hide=True)
#        self.add_input( name = "EulerAngles", interface = IFunction,hide=True)
#        self.add_input( name = "DigitizedPoints", interface = IFunction,hide=True)
#        self.add_input( name = "Mode", interface = IStr, value=None,hide=True)
#        self.add_input( name = "Translate", interface = ISequence, value=None,hide=True)
#        self.add_input( name = "Origin", interface = ISequence, value=None,hide=True)
#        self.add_input( name = "DressingData",hide=True)


