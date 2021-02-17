# Header

import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize, LogNorm

def colormap(g, property_name, cmap='jet',lognorm=True):
    """ Apply a colormap on a given MTG property to compute the 'color' property

    The colormap are thus defined in matplotlib.
    If lognorm is set to True, then the values are normalised on a log scale.
    """
    prop = g.property(property_name)

    keys = list(prop.keys())
    v = np.array(list(prop.values()))

    _cmap = cm.get_cmap(cmap)
    norm = Normalize() if not lognorm else LogNorm() 
    values = norm(v)

    colors = (_cmap(values)[:,0:3])*255
    colors = np.array(colors,dtype=np.int).tolist()

    g.properties()['color'] = dict(list(zip(keys,colors)))
    return g
    
