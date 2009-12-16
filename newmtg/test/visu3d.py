
import os, sys

from openalea.mtg import *
from openalea.mtg.io import *
from openalea.mtg.traversal import *
import openalea.mtg.util as util
from openalea.plantgl.all import *
from math import sqrt

reload(util)

#io.debug = 1
fn = r'data/mtg5.mtg'
fn = r'data/reconstructed_appletree.mtg'
fn = r'data/test9_noylum2.mtg'

g = read_mtg_file(fn)

# 1. Read all the points and draw it
xx = g.property('XX')
yy = g.property('YY')
zz = g.property('ZZ')

scale = 3
points = {}

factor = 100
factor = 1
for vid in g.vertices(scale=scale):
    try:
        points[vid] = xx[vid]*factor, yy[vid]*factor, zz[vid]*factor
    except:
        continue

scene = Scene()

# Create all the edges with only tree info
#segments = [(points[g.parent(vid)], points[vid]) for vid in pre_order(g,3) if vid in points and g.parent(vid)]
#[scene.add(Polyline(s)) for s in segments]
#Viewer.display(scene)

# Build all the axes at a given order

def compute_axes(g, v):
    marked = {}
    axes = {}
    for vid in post_order(g,v):
        if vid in marked:
            continue
        _axe = list(simple_axe(g,vid, marked))
        _axe.reverse()
        axes.setdefault(g.order(_axe[0]),[]).append(_axe)
    return axes

def simple_axe(g, v, marked):
    edge_type = g.property('edge_type')
    
    while v is not None:
        if v in points:
            yield v
        
        assert v not in marked
        marked[v] = True
        
        if g.parent(v) is None or edge_type[v] == '+':
            break
        v = g.parent(v)

def compute_radius(g, v, last_radius):
    all_r2 = {}
    for vid in post_order(g, v):
        r2 = max(sum([all_r2[c] for c in g.children(vid)]), last_radius)
        all_r2[vid] = r2
    for k, v in all_r2.iteritems():
        all_r2[k] = sqrt(v)
    return all_r2

def compute_diameter(g, v, diameter_property):
    radius = {}
    #for vid in 

axes = compute_axes(g,3)
rad = compute_radius(g,3, 0.07)

scene.clear()
polylines = []
radius_law = []
for order in axes:
    for axe in axes[order]:
        parent = g.parent(axe[0])
        if  order > 0 and parent and parent in points:
            axe.insert(0,parent)
        polylines.append((Polyline([points[vid] for vid in axe]), [[rad[vid]]*2 for vid in axe]))

sf = 0.01
p= [Vector2(0.5,0), Vector2( 0,0.5), Vector2(-0.05,0), Vector2(0,-0.5), Vector2(0.5,0)]
#p= map(lambda x: x*sf, p)
section= Polyline2D(p)
section = Polyline2D.Circle(0.5,10)
scene.clear()
for axe, radius in polylines:
    radius[0] = radius[1]
    scene+= Extrusion(axe,section,radius)

"""
Algo:
  - compute all the axes
  - compute the points for each element of the axes
  - compute the radius
  - compute a section
  - display it

Proposal:
  1. remove noise from measured points on axes:
    * given points do not represent the skeleton but are exterior points.
    * some points may be aligned (guideline)
      but branching points are on a spiral.
      -> these points may provide usefull info on radius.
         RMF may be used to found a better axis for the skeleton.
  2. Create factories for curves
"""
