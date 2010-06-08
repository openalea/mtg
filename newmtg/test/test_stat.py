from openalea.mtg import *
from openalea.mtg.io import *
from openalea.mtg.stat import *
import openalea.mtg.algo as algo
from vplants.sequence_analysis import *
from numpy.random import random_integers
from numpy import *

#l = [random_integers(0,10,20).tolist() for i in range(10)]
#seq = Sequences(l)

def build_vector(nb_vectors=10, nb_variables=5):
    return [random_integers(0,10,nb_variables).tolist() for i in range(nb_vectors)]

def build_sequence(nb_seqs=10, nb_vectors=5, nb_variables=3):
    return [[random_integers(0,10,nb_variables).tolist() for i in range(nb_vectors)] for j in range(nb_seqs)]

def test_vector_ctor():
    vectors = Vectors(build_vector(10,5))

    assert vectors.nb_vector == 10
    assert vectors.nb_variable == 5
    return vectors

def test_sequence_ctor():
    seqs = Sequences(build_sequence(10,5,3))
    assert seqs.nb_sequence == 10
    assert seqs.nb_variable == 3
    assert max(seqs.get_length(i) for i in range(seqs.nb_sequence)) == 5
    return seqs

def test_mtg_vector():
    fn = r'data/test8_boutdenoylum2.mtg'
    g = read_mtg_file(fn)

    topdia = g.property('TopDia')
    nfe = g.property('NFe')

    vids = [vid for vid in g.vertices(scale=3) if vid in topdia and vid in nfe]
    vectors = extract_vectors(g, vids, ['TopDia', 'NFe'])
    assert vectors.nb_vector == len(vids)
    assert vectors.nb_variable == 2
    # Plot(vectors)
    return vectors


def test_mtg_sequences():
    fn = r'data/test8_boutdenoylum2.mtg'
    g = read_mtg_file(fn)

    topdia = g.property('TopDia')
    nfe = g.property('NFe')

    leaves = (vid for vid in g.vertices(scale=3) if g.is_leaf(vid))
    seqs = [list(reversed([vid for vid in algo.ancestors(g, lid) if vid in topdia and vid in nfe])) for lid in leaves]

    sequences = build_sequences(g,seqs,['TopDia', 'NFe'])
    return sequences

