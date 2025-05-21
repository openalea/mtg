from openalea.mtg.io import *
import openalea.mtg.aml as aml
from openalea.mtg.data import data_dir


def check(fn):
    g = read_mtg_file(fn)
    g1 = aml.MTG(fn)

    assert list(g.vertices()) == aml.VtxList()
    for scale in range(1, g.nb_scales()):
        assert list(g.vertices(scale=scale)) == aml.VtxList(Scale=scale), set(g.vertices(scale=scale)).difference(
            aml.VtxList(Scale=scale))

    l = aml.VtxList(Scale=g.max_scale())
    for vid in l:
        assert g.parent(vid) == aml.Father(vid), 'vertex %d has not the same parent at scale %d' % (vid, g.max_scale())

    return g


def test1():
    fn = data_dir/'mtg1.mtg'
    g = check(fn)
    assert len(g) == 7
    assert g.nb_vertices(scale=1) == 6
