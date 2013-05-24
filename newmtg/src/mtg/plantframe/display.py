from math import pi

import numpy as np
from matplotlib import pyplot, mpl
from pylab import cm, colorbar
from pylab import plot as pylab_plot
from matplotlib.colors import Normalize, LogNorm

from openalea.mtg import turtle as turt
import openalea.plantgl.all as pgl


#X def root_visitor(g, v, turtle):
#X     angles = [90,45]+[30]*5
#X     n = g.node(v)
#X     radius = n.radius*1.e4
#X     order = n.order
#X     length = n.length*1.e4
#X 
#X     if g.edge_type(v) == '+':
#X         angle = angles[order]
#X         turtle.down(angle)
#X 
#X 
#X     turtle.setId(v)
#X     turtle.setWidth(radius)
#X     for c in n.children():
#X         if c.edge_type() == '+':
#X             turtle.rollL(130)
#X     #turtle.setColor(order+1)
#X     turtle.F(length)
#X 
#X     # define the color property
#X     #n.color = random.random()
#X 

def plot(pf, length=1.e-4, has_radius=False, r_base=1., r_tip=0.25, visitor=root_visitor, prop_cmap=None):
    """
    Exemple:

        >>> from openalea.plantgl.all import *
        >>> s = plot()
        >>> shapes = dict( (x.getId(), x.geometry) for x in s)
        >>> Viewer.display(s)
    """

    turtle = turt.PglTurtle()
    turtle.down(180)
    scene = turt.TurtleFrame(g, visitor=root_visitor, turtle=turtle, gc=False)

    # Compute color from radius
    if prop_cmap:
        my_colormap(g,prop_cmap)

    shapes = dict( (sh.getId(),sh) for sh in scene)

    colors = g.property('color')
    for vid in colors:
        shapes[vid].appearance = pgl.Material(colors[vid])
    scene = pgl.Scene(shapes.values())
    return scene

def my_colormap(g, property_name, cmap='jet',lognorm=True):
    prop = g.property(property_name)
    keys = prop.keys()
    values = np.array(prop.values())
    #m, M = int(values.min()), int(values.max())
    _cmap = cm.get_cmap(cmap)
    norm = Normalize() if not lognorm else LogNorm() 
    values = norm(values)
    #my_colorbar(values, _cmap, norm)

    colors = (_cmap(values)[:,0:3])*255
    colors = np.array(colors,dtype=np.int).tolist()

    g.properties()['color'] = dict(zip(keys,colors))
    
def my_colorbar(values, cmap, norm):
    fig = pyplot.figure(figsize=(8,3))
    ax = fig.add_axes([0.05, 0.65, 0.9, 0.15])
    cb = mpl.colorbar.ColorbarBase(ax,cmap=cmap, norm=norm, values=values)
    

