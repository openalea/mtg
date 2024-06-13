
"""
TULIP = True
try:
    import tulip
except ImportError:
    TULIP = False

if not TULIP:
    import sys
    sys.exit(1)

from openalea.mtg.io import *
from openalea.mtg import iox
from tulip import *

fn = r'data/test9_noylum2.mtg'
fn = r'data/test8_boutdenoylum2.mtg'

g = read_mtg_file(fn)
def layout(g, vid):
    n = g.node(vid)
    x, y, z = n.XX, n.YY, n.ZZ
    if x and y and z:
        return tlp.Coord(n.XX, n.YY, n.ZZ)

def size(g, vid):
    n = g.node(vid)
    dia = n.TopDia
    return tlp.Size(dia, dia) if dia else None

props={}
props['viewLayout'] = layout
props['viewSize'] = size
props={}
iox.save_tulip(g, 'tulip_files/tulip_test8_2.tlp.gz', properties=props)
"""
def test_tulip():
    pass
