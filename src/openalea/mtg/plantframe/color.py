import numpy as np
from pylab import cm
import matplotlib
from matplotlib.colors import Normalize, LogNorm
import matplotlib as mpl
from matplotlib import pyplot
import openalea.plantgl.all as pgl

def get_cmap(cmap):
    _cmap = cmap
    if isinstance(cmap, str):
        _cmap = cm.get_cmap(cmap)
    return _cmap

def colormap(g, property_name, cmap='jet',lognorm=True):
    """ Compute a color property based on a given property and a colormap.

    """
    prop = g.property(property_name)
    keys = list(prop.keys())
    values = np.array(list(prop.values()))
    #m, M = int(values.min()), int(values.max())

    _cmap = get_cmap(cmap)
    norm = Normalize() if not lognorm else LogNorm()
    values = norm(values)
    #my_colorbar(values, _cmap, norm)

    colors = (_cmap(values)[:,0:3])*255
    colors = np.array(colors,dtype=np.int).tolist()

    g.properties()['color'] = dict(list(zip(keys,colors)))
    return g

def hex2color(s):
     return tuple([int(n, 16) for n in (s[1:3], s[3:5], s[5:7])])
def lut(g, property_name, colors=[], N=0):
    """ Compute a color property based on a given property and a colormap.

    """
    prop = g.property(property_name)
    keys = list(prop.keys())
    values = list(prop.values())
    #m, M = int(values.min()), int(values.max())

    if not colors:
        colors = [hex2color(c) for c in list(matplotlib.colors.cnames.values())]

    n = len(colors)
    if n < max(values):
        print('values max ', max(values), '  when nb colors is ', n)
    g.properties()['color'] = dict((keys[i], colors[values[i]%n]) for i in range(len(keys)))
    return g, colors


def colorbar(g, property_name, cmap='jet',lognorm=True, N=5, fmt='%.1e'):
    fig = pyplot.figure(figsize=(8,3))
    ax = fig.add_axes([0.05, 0.65, 0.9, 0.15])

    prop = g.property(property_name)
    keys = list(prop.keys())
    values = np.array(list(prop.values()))
    m, M = values.min(), values.max()

    ticks = np.linspace(m,M,N)

    _cmap = get_cmap(cmap)
    norm = Normalize() if not lognorm else LogNorm()
    values = norm(values)


    cb = mpl.colorbar.ColorbarBase(ax, cmap=_cmap,
                                   norm=norm,
                                   ticks=ticks,
                                   orientation='horizontal')
    cb.ax.set_xticklabels([fmt%x for x in ticks])# horizontal colorbar
    cb.set_label(property_name)

    #cb = fig.colorbar(cax, ticks=[_min, (_min+_max)/2., _max], orientation='horizontal')

    pyplot.show()
    return g, cb

def colorbar_lut(g, property_name, colors=[], N=5, fmt='%d'):
    fig = pyplot.figure(figsize=(8,3))
    ax = fig.add_axes([0.05, 0.65, 0.9, 0.15])

    if not colors:
        colors = [hex2color(c) for c in list(matplotlib.colors.cnames.values())]

    prop = g.property(property_name)
    keys = list(prop.keys())
    values = list(prop.values())
    m, M = min(values), max(values)

    n = len(colors)

    m , M = 0, min(n,M)
    values = list(range(M))

    ticks = np.linspace(m,M,M+1)

    array_colors = np.array(colors,dtype=np.float)
    if array_colors.max() > 1.:
        array_colors /= 255.

    cmap = mpl.colors.ListedColormap(array_colors)

    cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                   ticks=ticks,
                                   boundaries=ticks,
                                   orientation='horizontal')
    #cb.ax.set_xticklabels([fmt%x for x in ticks])# horizontal colorbar
    cb.set_label(property_name)

    #cb = fig.colorbar(cax, ticks=[_min, (_min+_max)/2., _max], orientation='horizontal')

    pyplot.show()
    return g, cb

def plot3d(g):
    """
    Create a PlantGL scene from a MTG. Then, plot the created scene and return it.
    """
    Material = pgl.Material
    Color3 = pgl.Color3
    Shape = pgl.Shape
    Scene = pgl.Scene

    colors = g.property('color')
    geometries = g.property('geometry')

    scene = Scene()

    def geom2shape(vid, mesh, scene):
        shape = None
        if isinstance(mesh, list):
            for m in mesh:
                geom2shape(vid, m, scene)
            return
        if mesh is None:
            return
        if isinstance(mesh, Shape):
            shape = mesh
            mesh = mesh.geometry

        if colors:
            shape = Shape(mesh, Material(Color3(* colors.get(vid, [0,0,0]) )))

        shape.id = vid
        scene.add(shape)

    for vid, mesh in geometries.items():
        geom2shape(vid, mesh, scene)
    pgl.Viewer.display(scene)
    return scene
