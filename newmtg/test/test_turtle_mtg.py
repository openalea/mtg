from openalea.mtg.mtg import *
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from vplants.plantgl.all import *

def traverse_with_turtle1(g, vid):
    turtle = PglTurtle()

    def push_turtle(v):
        if g.edge_type(v) == '+':
            turtle.push()
        return True

    def pop_turtle(v):
        if g.edge_type(v) == '+':
            turtle.pop()

    for v in pre_order2_with_filter(g, vid, None, push_turtle, pop_turtle):
        if g.edge_type(v) == '+':
            turtle.down()
        turtle.F()
        turtle.rollL()

    return turtle.getScene()

def visitor(g, v, turtle):
        if g.edge_type(v) == '+':
            turtle.down()
        turtle.F()
        turtle.rollL()

def traverse_with_turtle(g, vid, visitor):
    turtle = PglTurtle()

    def push_turtle(v):
        if g.edge_type(v) == '+':
            turtle.push()
        return True

    def pop_turtle(v):
        if g.edge_type(v) == '+':
            turtle.pop()

    for v in pre_order2_with_filter(g, vid, None, push_turtle, pop_turtle):
        visitor(g,v,turtle)

    return turtle.getScene()

def run(fn):
    g = read_mtg_file(fn)
    n = g.max_scale()
    v = g.component_roots_at_scale(g.root, scale=n).next()
    #return traverse_with_turtle1(g,v)
    return traverse_with_turtle(g,v, visitor)

def test1():
    fn = r'data/mtg1.mtg'
    return run(fn)

