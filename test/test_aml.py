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

from glob import glob
from os.path import basename

from openalea.mtg.mtg import *
import openalea.mtg.aml as wrap
import openalea.aml as aml


excludes = """
mtg51.mtg:Descendants
mtg51.mtg:Extremities
mtg51.mtg:Sons
mtg51.mtg:Height
mtg51.mtg:Order
mtg51.mtg:Father
mtg51.mtg:Ancestors
mtg51.mtg:Root
test11_wij10.mtg:Sons
test11_wij10.mtg:Descendants
test11_wij10.mtg:Extremities
test11_wij10.mtg:Height
test11_wij10.mtg:Order
test11_wij10.mtg:Father
test11_wij10.mtg:Ancestors
test11_wij10.mtg:Root
test11_wij10.mtg:Axis
test11_wij10.mtg:Successor
test11_wij10.mtg:Rank
test11_wij10.mtg:Predecessor

""".split()
excludes = [l.split(':') for l in excludes]
excludes = []

def compare(func_name, *args, **kwds):
    """Apply the same function to the two modules with the same args. 
    TODO: Add customizable comment, and a cmp function.
    """
    rnew = wrap.__dict__[func_name](*args, **kwds)
    raml = aml.__dict__[func_name](*args, **kwds)

    params = []
    if args: 
        params.extend((str(x) for x in args))
    if kwds: 
        params.extend(('%s=%s'%(k,v) for k, v in kwds.iteritems()))

    f = func_name+'('+','.join(params)+')'
    try:
        assert (rnew == raml) or set(rnew) == set(raml) , 'Method %s -> %s != %s'%(f,rnew,raml)
    except:
        assert (rnew == raml), 'Method %s -> %s != %s'%(f,rnew,raml)

def check(fn):
    " Compare result with the AML library. "

    g = wrap.MTG(fn)
    g1 = aml.MTG(fn)

    # Test root
    compare('MTGRoot')

    nb_scales = g.nb_scales()

    # Test VtxList at each scale
    for scale in range(1,nb_scales):
        compare('VtxList', Scale=scale)

    # Test VtxList at all scales
    compare('VtxList')

    vtxs = aml.VtxList()

    methods = """
    Class
    Index
    Scale

    Rank
    Height
    Order

    Defined
    Father
    Successor
    Predecessor
    Complex
    Sons
    Ancestors
    ComponentRoots
    Descendants
    Extremities
    Root
    Axis
    Components
    """.split()

    methods = [ m for m in methods if [basename(fn), m] not in excludes]

    """
    Trunk
    Location
    Path # require 2 arguments
    """
    i= vtxs.index(g.root)
    del vtxs[i]
    for v in vtxs:
        for m in methods:
            compare(m,v)
    return g

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
        assert wrap.Rank(vid) == wrap.Height(vid) == i

    for i, vid in enumerate(vtxs):
        assert wrap.AlgRank(1,vid) == - wrap.AlgRank(vid,1) == i

def test():
    files = glob('data/*.mtg')
    exclude = '''
    reconstructed_appletree.mtg
    '''.split()
    files = [f for f in files for e in exclude if e not in f]
    for fn in files:
        yield check, fn

