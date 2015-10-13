
import openalea.mtg.io as io
dreload(io)

io.debug = 1
fn = r'data/test5.mtg'

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

