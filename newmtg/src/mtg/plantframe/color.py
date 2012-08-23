import numpy as np
from pylab import cm, colorbar
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

