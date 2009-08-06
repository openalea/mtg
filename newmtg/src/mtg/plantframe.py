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
    Use topologic information and associated properties to reconstruct a 3D representation 
    of a plant. The 3D representation must satisfy all the intra and inter topological constraints
    and the properties defined by the user.

:Algorithm:


:Examples:

.. todo::
    - 
'''

import traversal


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
        # 3 Solve the different constraints by using a plug'in mechanism
        # 4. Design new algo and define new parameters.
        # 5. Use WeberPenn with MTG

        self._compute_global_data()



    def _extract_properties(self, name, kwds):
        ''' Extract the property from properties of the mtg 
        or from a user given function.
        '''
        d = {}

        func = kwds.get(name)
        if func:
            # Compute the value for all vertices
            all_values = ((vid,func(vid)) for vid in self.g.vertices())
            # Select only those which are defined
            values = ( (vid, fvid) for vid, fvid in all_values if fvid is not None)

            d = dict(values)
            
        name_property = self.g.property(name).copy()
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
            else:
                vid = self.g.complex(vid)
        self.origin = origin
        return self.origin

    def run(self, scale= -1):
        '''Compute the geometry of the plant.
        '''
        
        if scale == -1:
            scale = self.g.max_scale()

        root = list(self.g.roots(scale=scale))[0]

        # 1. compute the origin of the tree
        # Check if a complex has origin
        self.origin = self._get_origin(root)

        axes = compute_axes(self.g, root, self.points, self.origin)
        
        # Compute the points
        # 1. compute fixed points
        # 
        

def iter_order(g, v, edge_type = None):
    ''' Iter on a tree by considering first 
    all the vertices of the axe at the first order,
    then the vertices at the second order and so on.
    '''
    pass

def compute_axes(g, v, fixed_points, origin):
    marked = {}
    axes = {}
    for vid in traversal.post_order(g,v):
        if vid in marked:
            continue
        
        _axe = list(simple_axe(g,vid, marked, fixed_points))
        _axe.reverse()
        if g.order(vid) == 0: 
            new_points = compute_missing_points(g, _axe, fixed_points, origin=origin)
        else:
            new_points = compute_missing_points(g, _axe, fixed_points)
        fixed_points.update(new_points)
        
        _axe, other = zip(*_axe)
        axes.setdefault(g.order(_axe[0]),[]).append(list(_axe))
    return axes


def simple_axe(g, v, marked, fixed_points):
    edge_type = g.property('edge_type')
    
    while v is not None:
        if v in fixed_points:
            yield v, True
        else: 
            yield v, False
        
        assert v not in marked
        marked[v] = True
        
        if g.parent(v) is None or edge_type[v] == '+':
            break
        v = g.parent(v)

def compute_missing_points(g, axe, fixed_points, origin=None):
    """
    axe is a list of tuple containing both vid and a boolean indicated if
    a point is defined on a vertex.
    return a dict of {id:point}.
    """
    new_points = {} # list of points
    interval = [] # list of the different interval with missing values
    first = False
    last = False
    prev = -1 # previous id with a defined point value
    current = [] # list of points to define an interval

    begin = True 

    for vid, defined in axe:
        if begin:
            first = not defined
            begin = False

        if not defined:
            if (not current) and (prev != -1) :
                current.append(prev)
            current.append(vid)
        else:
            prev = vid
            if current:
                current.append(vid)
                interval.append(current)
                current = []
    if current:
        interval.append(current)
        last = True

    i0 = []
    i1 = []
    if first:
        i0 = interval[0]
        del interval[0]
    if last and interval:
        i1 = interval[-1]
        del interval[-1]

    for inter in interval:
        n = len(inter)-1
        v1, v2 = inter[0], inter[-1]
        p1, p2 = fixed_points[v1], fixed_points[v2]
        pt12 = Vector3(*p2) -Vector3(*p1)
        step = pt12 / n

        for i, v in enumerate(inter):
            if i == 0:
                pt = Vector3(*p1)
            elif i == n:
                continue
            else:
                pt = pt + step
                new_points[v] = pt
        
    # Management of first and last interval.
    # It is a silly algorithm.
    if i0:
        if origin and (i0[-1], True) in axe:
            inter = i0
            # The first point do not belong to the interval
            n = len(inter) 

            v2 = inter[-1]
            p1, p2 = Vector3(*origin), fixed_points[v2]
            pt12 = Vector3(*p2) -Vector3(*p1)
            step = pt12 / n
            pt = p1
            for i, v in enumerate(inter):
                if i+1 != n:
                    pt = pt + step
                    new_points[v] = pt

        else:

            v0 = i0[-1]
            if (v0, True) in axe:

                index0 = axe.index((v0,True))
                if index0+1 < len(axe):
                    v1, defined = axe[index0+1]
                    if defined:
                        p2 = Vector3(*fixed_points[v1])
                    else:
                        p2 = new_points.get(v1)
                
                    if p2:
                        p1 = Vector3(*fixed_points[v0])
                        pt21 = Vector3(*p1) -Vector3(*p2)
                        n = len(i0)-1
                        for i, v in enumerate(i0[:-1]):
                            index = n-i
                            pt = p1 + pt21*index
                            new_points[v] = pt

    if i1 and (i1 != i0):
        v1 = i1[0]
        v0 = g.parent(v1)
        p1 = fixed_points.get(v0,new_points.get(v0))
        if p1 :
            p1 = Vector3(*p1)
            p2 = fixed_points[v1]
            p2 = Vector3(*p2)
            pt12 = p2 -p1
            n = len(i1)-1
            for i, v in enumerate(i1[1:]):
                pt = p2 + pt12*(i+1)
                new_points[v] = pt
 
    return new_points

def compute_radius(g, v, last_radius):
    all_r2 = {}
    for vid in traversal.post_order(g, v):
        r2 = max(sum([all_r2[c] for c in g.children(vid)]), last_radius)
        all_r2[vid] = r2
    for k, v in all_r2.iteritems():
        all_r2[k] = sqrt(v)
    return all_r2

def compute_diameter(g, v, radius, default_value):

    all_r = {}
    unknow= []
    edge_type = g.property('edge_type')
    for vid in traversal.post_order(g, v):
        if vid in radius:
            if radius[vid] < default_value:
                all_r[vid] = default_value
            else:
                all_r[vid] = radius[vid]
        elif g.is_leaf(vid):
            v = g.complex(vid)
            while v:
                if v in radius:
                    all_r[vid] = radius[v]
                    break
                else:
                    v = g.complex(v)
            else:
                all_r[vid] = default_value
        else:
            # pipe model (r_parent **n = sum r_child**n with r ==2)
            all_r[vid] = sqrt(sum([all_r[c]**2 for c in g.children(vid)]))

    return all_r

def build_scene(g, origin, axes, points, rad, default_radius, option='axe'):


    scene = Scene()
    section = Polyline2D.Circle(0.5,10)

    polylines = []
    radius_law = []
    scale = g.max_scale()


    if option == 'cylinder':
        for vid in points :
            if g.scale(vid) != scale:
                continue
            parent = g.parent(vid)
            if parent is None:
                point_parent = origin
            elif parent in points:
                point_parent = points[parent]

            poly = [point_parent, points[vid]]
            curve = Polyline(poly)

            if vid not in rad or parent not in rad:
                rad_vid = rad.get(vid, default_radius)
                rad_parent = rad.get(parent, rad_vid)
                radius = [[rad_parent]*2, [rad_vid]*2]
                shape = Shape(Extrusion(curve, section, radius), Material(Color3(255,0,0)))
                shape.id = vid
                scene += shape
            else:
                rad_vid = rad.get(vid, 1)
                rad_parent = rad.get(parent, rad_vid)
                radius = [[rad_parent]*2, [rad_vid]*2]
                shape = Shape(Extrusion(curve, section, radius))
                shape.id = vid
                scene += shape

        return scene

    for order in axes:
        for axe in axes[order]:
            parent = g.parent(axe[0])
            if  order > 0 and parent and (parent in points):
                axe.insert(0,parent)
            elif order == 0:
                axe.insert(0, axe[0])
            poly = [points[vid] for vid in axe if vid in points]
            if order == 0:
                poly[0] = origin

            # Delete null segments
            eps = 1
            curve = Polyline(poly)

            radius = [[rad.get(vid, 1.)*2]*2 for vid in axe if vid in points]
            if len(radius)>1:
                radius[0] = radius[1]

                curve, radius = clean_curve(curve, radius)

                scene += Extrusion(curve, section, radius)

    return scene

def debug(g, scene, points, order, scale=3, color=(255,0,0)):
    c = Material(Color3(*color))
    sphere = Sphere(radius=30)
    for id, pt in points.iteritems():
        if g.order(id) == order and g.scale(id) == scale:
            scene+= Shape(Translated(pt,sphere), c)
    return scene
    

def clean_curve(poly, radius):
    """ Remove too small elements.
    """
    pts = poly.pointList
    n = len(pts)

    length = poly.getLength()
    mean = length / (n-1)

    eps = mean/100.
    eps2 = eps**2

    index = [True]*n

    new_poly = [pts[0]]
    new_radius = [radius[0]]

    for i in range(1,n):
         p12= pts[i] - pts[i-1]
         if p12.__normSquared__() > eps2:
            new_poly.append(pts[i])
            new_radius.append(radius[i])

    return Polyline(new_poly), new_radius

