""" Dataframe implementation

"""

import pandas as pd
from .algo import orders

def to_dataframe(g):
	d=g.properties()
	parents = g._parent
	complexes = {vid: g.complex(vid) for vid in g if g.complex(vid)}
	scales = g._scale

	d['parent']=parents
	d['complex'] = complexes
	d['scale']=scales
	d['order']=orders(g)
	dataframe = pd.DataFrame.from_dict(d)
	return dataframe

