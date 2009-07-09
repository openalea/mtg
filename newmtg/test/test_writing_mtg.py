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

import os
from itertools import izip, repeat
from glob import glob

from openalea.mtg import *
from openalea.mtg.io import *

from openalea import aml

def test():
    files = glob('data/*.mtg')
    exclude = '''
    reconstructed_appletree.mtg
    '''.split()
    files = [f for f in files for e in exclude if e not in f]

    files = glob('data/test13*.mtg')
    exclude = []
    for fn in files:

        g, s = build_mtg_and_check(fn)
        yield check, g, s, fn

def build_mtg_and_check(fn):
    g = read_mtg_file(fn)

    props = (p for p in g.property_names() if p not in ['edge_type', 'index', 'label'])
    props = list(izip(props, repeat('REAL')))

    # Write it on a string
    #try:
    s = write_mtg(g, props)
    """
    except Exception, e:
        print e
        #assert False, 'MTG %s can not be written'%fn
    """
    return g, s

def check(g, s, fn):
    res = True
    f = open('tmp.mtg', 'w')
    f.write(s)
    f.close()
    try:
        g1 = aml.MTG('tmp.mtg')
    except Exception, e:
        os.remove('tmp.mtg')
        assert False, fn
    
    os.remove('tmp.mtg')

    return res

