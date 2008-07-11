from openalea.mtg.io import *
from openalea.plantgl.all import *

symbols = {'newPlant' : 1, 'newAxe' : 2, 'newMetamer' :3, 'StemElement':4, 'LeafElement':4}
functions = {}


def StemElement(optical_species, length, diameter_base, diameter_top ):
    mesh = None
    if length > 0 and diameter_base > 0:
        cylinder = Cylinder(height = length, radius = diameter_base/2.)
        tess = Tesselator()
        cylinder.apply(tess) 
        mesh = tess.triangulation
    return {'geometry':mesh}

def LeafElement(optical_species, final_length, radius_max, s_base, s_top, leaf_rank, seed ):
    mesh = None
    length = final_length * (s_top - s_base)
    if length > 0 and radius_max > 0:
        cylinder = Cylinder(height = length, radius = radius_max)
        tess = Tesselator()
        cylinder.apply(tess) 
        mesh = tess.triangulation
    return {'geometry':mesh}

functions['StemElement'] = StemElement
functions['LeafElement'] = LeafElement


def check_connectivity(g):
    for scale in g.scales():
        assert len(list(g.roots(scale=scale))) == 1, 'g.roots(scale=%d) != %d'%(scale, len(list(g.roots(scale=scale))))

def test1():
    # simple set of two successives axes
    s = """
newPlant
[+(45)newAxe
]
"""
    g = read_lsystem_string(s, symbols)
    assert len(g) == 3
    assert g.nb_vertices(scale=1)==1
    assert g.nb_vertices(scale=2)==1
    check_connectivity(g)

def test1():
    s = """
newPlant
[+(45)newAxe
newMetamer
StemElement(1,0.000000,0.04,0.04)
 [+(45)newAxe
 ]
StemElement(1,0.436111,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,7.665278,0.346528,0.000000,1,10,0.5)]
newMetamer
StemElement(1,0.000000,0.04,0.04)
 [+(45)newAxe
 ]
StemElement(1,0.000000,0.04,0.04)[/(0.000000)+(0.631719)LeafElement(1,10.050000,0.383524,0.368281,1,9,0.5)]
newMetamer
StemElement(1,0.000000,0.04,0.04)
 [+(45)newAxe
 ]
StemElement(1,0.000000,0.04,0.04)[/(180.000000)+(0.000000)LeafElement(1,7.900000,0.455263,1.000000,1,8,0.5)]
]
"""
    g = read_lsystem_string(s, symbols)
    assert len(g) == 18
    assert g.nb_scales() == 5
    assert g.max_scale() == 4
    assert g.nb_vertices(scale=1)==1
    assert g.nb_vertices(scale=2)==4
    assert g.nb_vertices(scale=3)==3
    assert g.nb_vertices(scale=4)==9
    check_connectivity(g)
    
def test2():
    s = """
newPlant
[+(45)newAxe
newMetamer
StemElement(1,0.000000,0.04,0.04)
 [+(45)newAxe
 ]
StemElement(1,0.436111,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,7.665278,0.346528,0.000000,1,10,0.5)]
"""
    g = read_lsystem_string(s, symbols)
    assert len(g) == 8
    assert g.nb_scales() == 5
    assert g.max_scale() == 4
    assert g.nb_vertices(scale=1)==1
    assert g.nb_vertices(scale=2)==2
    assert g.nb_vertices(scale=3)==1
    assert g.nb_vertices(scale=4)==3
    check_connectivity(g)

def test3():
    s = """
newPlant
[+(45)newAxe
newMetamer
StemElement(1,0.000000,0.04,0.04)
 [+(45)newAxe
 ]
StemElement(1,0.436111,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,7.665278,0.346528,0.000000,1,10,0.5)]
newMetamer

"""
    g = read_lsystem_string(s, symbols)
    assert len(g) == 9
    assert g.nb_scales() == 5
    assert g.max_scale() == 4
    assert g.nb_vertices(scale=1)==1
    assert g.nb_vertices(scale=2)==2
    assert g.nb_vertices(scale=3)==2
    assert g.nb_vertices(scale=4)==3
    check_connectivity(g)

def test4():
    s = """
newPlant
[+(45)newAxe
newMetamer
StemElement(1,0.000000,0.04,0.04)
 [+(45)newAxe
 ]
StemElement(1,0.436111,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,7.665278,0.346528,0.000000,1,10,0.5)]
newMetamer
StemElement(1,0.000000,0.04,0.04)
 [+(45)newAxe
 ]
StemElement(1,0.000000,0.04,0.04)[/(0.000000)+(0.631719)LeafElement(1,10.050000,0.383524,0.368281,1,9,0.5)]
"""
    g = read_lsystem_string(s, symbols)
    assert len(g) ==13 
    assert g.nb_scales() == 5
    assert g.max_scale() == 4
    assert g.nb_vertices(scale=1)==1
    assert g.nb_vertices(scale=2)==3
    assert g.nb_vertices(scale=3)==2
    assert g.nb_vertices(scale=4)==6
    check_connectivity(g)

def test5():
    s="""
newPlant
[+(45)newAxe
newMetamer
StemElement(1,0.000000,0.04,0.04)
 [+(45)newAxe
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,0.540000,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,5.095000,0.308000,0.000000,1,7,0.5)]]]
"""
    g = read_lsystem_string(s, symbols)
    assert len(g) ==10 
    assert g.nb_scales() == 5
    assert g.max_scale() == 4
    assert g.nb_vertices(scale=1)==1
    assert g.nb_vertices(scale=2)==2
    assert g.nb_vertices(scale=3)==2
    assert g.nb_vertices(scale=4)==4
    check_connectivity(g)

def test6():
    s="""
newPlant
[+(45)newAxe
newMetamer
StemElement(1,0.000000,0.04,0.04)
 [+(45)newAxe
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,0.540000,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,5.095000,0.308000,0.000000,1,7,0.5)]]]
"""
    s = s+s+s
    g = read_lsystem_string(s, symbols)

    #assert len(g) ==10 
    assert g.nb_scales() == 5
    assert g.max_scale() == 4
    assert g.nb_vertices(scale=1)==1*3
    assert g.nb_vertices(scale=2)==2*3
    assert g.nb_vertices(scale=3)==2*3
    assert g.nb_vertices(scale=4)==4*3
    assert g.nb_vertices(scale=1) == len(list(g.roots(scale=4)))


def test_full():
    s="""
newPlant
[newAxe
newMetamer
StemElement(1,0.000000,0.04,0.04)
 [+(45)newAxe
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,0.540000,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,5.095000,0.308000,0.000000,1,7,0.5)]
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,0.559999,0.04,0.04)[/(0.000000)+(45.000000)LeafElement(1,7.075000,0.401579,0.000000,1,6,0.5)]
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,1.361539,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,9.000000,0.522500,0.000000,1,5,0.5)]
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,3.838462,0.04,0.04)[/(0.000000)+(45.000000)LeafElement(1,11.800000,0.766154,0.000000,1,4,0.5)]
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,6.982353,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,17.000000,1.015882,0.000000,1,3,0.5)]
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,6.417647,0.04,0.04)[/(0.000000)+(45.000000)LeafElement(1,18.900000,1.062400,0.000000,1,2,0.5)]
 newMetamer
 StemElement(1,1.300000,0.04,0.04)StemElement(1,12.999998,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,20.647058,1.135625,0.000000,1,1,0.5)]
 newMetamer
 StemElement(1,4.700003,0.04,0.04)StemElement(1,14.000000,0.04,0.04)[/(0.000000)+(45.000000)LeafElement(1,20.799999,1.235000,0.000000,1,0,0.5)]
 ]
StemElement(1,0.436111,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,7.665278,0.346528,0.000000,1,10,0.5)]
newMetamer
StemElement(1,0.000000,0.04,0.04)
 [+(-45)newAxe
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,0.398890,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,5.525000,0.312500,0.000000,1,7,0.5)]
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,0.588077,0.04,0.04)[/(0.000000)+(45.000000)LeafElement(1,7.850000,0.424400,0.000000,1,6,0.5)]
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,3.448352,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,9.750000,0.640714,0.000000,1,5,0.5)]
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,3.323809,0.04,0.04)[/(0.000000)+(45.000000)LeafElement(1,14.100000,0.900952,0.000000,1,4,0.5)]
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,3.104762,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,17.500000,1.037917,0.000000,1,3,0.5)]
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,10.650002,0.04,0.04)[/(0.000000)+(45.000000)LeafElement(1,19.900000,1.116250,0.000000,1,2,0.5)]
 newMetamer
 StemElement(1,0.000000,0.04,0.04)StemElement(1,13.549996,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,22.100000,1.195714,0.000000,1,1,0.5)]
 newMetamer
 StemElement(1,3.200003,0.04,0.04)StemElement(1,16.500000,0.04,0.04)[/(0.000000)+(45.000000)LeafElement(1,16.500000,1.325714,0.000000,1,0,0.5)]
 ]
StemElement(1,0.000000,0.04,0.04)[/(0.000000)+(0.993730)LeafElement(1,10.050000,0.383524,0.006270,1,9,0.5)]
newMetamer
StemElement(1,0.000000,0.04,0.04)StemElement(1,0.000000,0.04,0.04)[/(180.000000)+(0.999426)LeafElement(1,7.900000,0.455263,0.000574,1,8,0.5)]
newMetamer
StemElement(1,0.000000,0.04,0.04)StemElement(1,0.743889,0.04,0.04)[/(0.000000)+(45.000000)LeafElement(1,7.800000,0.358000,0.000000,1,7,0.5)]
newMetamer
StemElement(1,0.000000,0.04,0.04)StemElement(1,0.679999,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,8.550000,0.523333,0.000000,1,6,0.5)]
newMetamer
StemElement(1,0.000000,0.04,0.04)StemElement(1,2.518572,0.04,0.04)[/(0.000000)+(45.000000)LeafElement(1,9.700000,0.714286,0.000000,1,5,0.5)]
newMetamer
StemElement(1,0.000000,0.04,0.04)StemElement(1,3.344506,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,13.100000,1.014286,0.000000,1,4,0.5)]
newMetamer
StemElement(1,0.000000,0.04,0.04)StemElement(1,3.076922,0.04,0.04)[/(0.000000)+(45.000000)LeafElement(1,17.400000,1.104286,0.000000,1,3,0.5)]
newMetamer
StemElement(1,0.000000,0.04,0.04)StemElement(1,10.900000,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,20.200001,1.196552,0.000000,1,2,0.5)]
newMetamer
StemElement(1,0.000000,0.04,0.04)StemElement(1,13.800000,0.04,0.04)[/(0.000000)+(45.000000)LeafElement(1,23.216667,1.302667,0.000000,1,1,0.5)]
newMetamer
StemElement(1,3.200001,0.04,0.04)StemElement(1,16.250000,0.04,0.04)[/(180.000000)+(45.000000)LeafElement(1,19.549999,1.438667,0.000000,1,0,0.5)]
]
"""
    g = read_lsystem_string(s, symbols, functions)
    assert len(g) ==113 
    assert g.nb_scales() == 5
    assert g.max_scale() == 4
    assert g.nb_vertices(scale=1)==1
    assert g.nb_vertices(scale=2)==3
    assert g.nb_vertices(scale=3)==27
    assert g.nb_vertices(scale=4)==81
    check_connectivity(g)

