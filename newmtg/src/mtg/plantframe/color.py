import numpy as np
from pylab import cm, colorbar
import matplotlib
from matplotlib.colors import Normalize, LogNorm

def colormap(g, property_name, cmap='jet',lognorm=True):
    """ Compute a color property based on a given property and a colormap.

    """
    prop = g.property(property_name)
    keys = prop.keys()
    values = np.array(prop.values())
    #m, M = int(values.min()), int(values.max())
    if isinstance(cmap, str):
        _cmap = cm.get_cmap(cmap)
    else:
        _cmap = cmap
    norm = Normalize() if not lognorm else LogNorm() 
    values = norm(values)
    #my_colorbar(values, _cmap, norm)

    colors = (_cmap(values)[:,0:3])*255
    colors = np.array(colors,dtype=np.int).tolist()

    g.properties()['color'] = dict(zip(keys,colors))
    return g

def hex2color(s):
     return tuple([int(n, 16) for n in (s[1:3], s[3:5], s[5:7])])
def lut(g, property_name, colors=[], N=0):
    """ Compute a color property based on a given property and a colormap.

    """
    prop = g.property(property_name)
    keys = prop.keys()
    values = np.array(prop.values())
    #m, M = int(values.min()), int(values.max())

    if not colors:
        colors = [hex2color(c) for c in matplotlib.colors.cnames.values()]

    
    g.properties()['color'] = dict((keys[i], colors[values[i]]) for i in range(len(keys)))
    return g


