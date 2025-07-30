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
from itertools import repeat
from glob import glob
import pytest

from openalea.mtg import *
from openalea.mtg.io import *

def files_to_check():
    files = glob('data/*.mtg')
    exclude = set('''
    reconstructed_appletree.mtg
    test6_apricot2.mtg
    mtg_dynamic.mtg
    '''.split())
    files = [f for f in files if os.path.basename(f) not in exclude]

    #files = list(glob('data/test13*.mtg'))
    print(files)
    return files


def build_mtg_and_check(fn):
    g = read_mtg_file(fn)

    props = (p for p in g.property_names() if p not in ['edge_type', 'index', 'label'])
    props = list(zip(props, repeat('REAL')))

    # Write it on a string
    #try:
    s = write_mtg(g, props)
    """
    except Exception, e:
        print(e)
        #assert False, 'MTG %s can not be written'%fn
    """
    return g, s

def check(g, s, fn):
    from openalea.mtg import MTG
    f = open('tmp.mtg', 'w')
    f.write(s)
    f.close()
    try:
        g1 = MTG('tmp.mtg')
    except Exception as e:
        os.remove('tmp.mtg')
        assert False, fn
    
    os.remove('tmp.mtg')

@pytest.mark.parametrize('fn', files_to_check())
def test_files(fn):
        g, s = build_mtg_and_check(fn)
        check(g, s, fn)

