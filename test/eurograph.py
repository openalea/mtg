
import os, sys

from openalea.mtg import *
import openalea.mtg.io as io

reload(io)

#io.debug = 1
fn = r'data/agraf.mtg'
fn2 = r'data/rapple.mtg'

#fn = r'data/mtg5.mtg'
"""
f = open(fn)
s = f.read()
f.close()

r = io.Reader(s)
# skip the header
r.header()

# read the MTG header
r._nb_feature=2
r._feature_head = ['nbEl', 'diam']
r._feature_slice=slice(5,7)

#debug
r.preprocess_code()
print r._new_code
"""
g = io.read_mtg_file(fn)


