# -*- python -*-
#
#       OpenAlea.mtg
#
#       Copyright 2008 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.pradal.at.cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

from openalea.mtg.mtg import *
import openalea.mtg.aml as wrap

def test1():
    fn='data/mtg1.mtg'
    g = wrap.MTG(fn)

    root = wrap.MTGRoot()
    assert root == 0
    
    g1 = wrap.Activate(g)
    assert g1 is g

    g1 = wrap.Active()
    assert g1 is g

    vtxs = wrap.VtxList(Scale=0)
    assert len(vtxs) == 1, "The root node 0"

    vtxs = wrap.VtxList(Scale=1)
    assert len(vtxs) == 6

    for vtx in vtxs:
        assert wrap.Class(vtx) == 'A'
        assert wrap.Index(vtx) == 1
        assert wrap.Scale(vtx) == 1

    props = ['diam', 'nbEl']
    for vid in vtxs:
        for p in props:
            wrap.Feature(vid,p)

    for i in range(len(vtxs)-1):
        assert wrap.EdgeType(vtxs[i],vtxs[i+1]) == '<'

    for vid in vtxs:
        assert wrap.Defined(vid)
        assert wrap.Order(vid) == 0
        assert wrap.AlgOrder(1,vid) == 0

    for i, vid in enumerate(vtxs):
        assert wrap.Rank(vid) == (wrap.Height(vid)-1) == i

    for i, vid in enumerate(vtxs):
        assert wrap.AlgRank(1,vid) == - wrap.AlgRank(vid,1) == i
    
