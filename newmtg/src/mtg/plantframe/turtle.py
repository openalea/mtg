from openalea.mtg.mtg import *
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from vplants.plantgl.all import *


def visitor(g, v, turtle):
        if g.edge_type(v) == '+':
            turtle.down()
        turtle.setId(v)
        turtle.F()
        turtle.rollL()

def traverse_with_turtle(g, vid, visitor=visitor, turtle=None, gc=True):
    if turtle is None:
        turtle = PglTurtle()

    def push_turtle(v):
        if g.edge_type(v) == '+':
            turtle.push()
            if gc:
                turtle.startGC()
            turtle.setId(v)
        return True

    def pop_turtle(v):
        if g.edge_type(v) == '+':
            if gc:
                turtle.stopGC()
            turtle.pop()

    turtle.push()
    if gc: turtle.startGC()
    visitor(g,vid,turtle)
    for v in pre_order2_with_filter(g, vid, None, push_turtle, pop_turtle):
        if v == vid: continue
        visitor(g,v,turtle)
    if gc: turtle.stopGC()
    return turtle.getScene()

def TurtleFrame(g, visitor=visitor, turtle=None, gc=True, all_roots = False):
    n = g.max_scale()
    if not all_roots:
        v = g.component_roots_at_scale_iter(g.root, scale=n).next()
        s = traverse_with_turtle(g,v, visitor, turtle=turtle, gc=gc)
    else:
        for v in g.component_roots_at_scale_iter(g.root, scale=n):
            s = traverse_with_turtle(g,v, visitor, turtle=turtle, gc=gc)
    return s

def Plot(scene):
    Viewer.display(scene)

def test1():
    fn = r'data/mtg1.mtg'
    g = read_mtg_file(fn)
    return TurtleFrame(g)

def test2():
    fn = r'/home/pradal/devlp/studies/plantframe/examples/PlantFrame/monopodial_plant.mtg'
    g = read_mtg_file(fn)
    return TurtleFrame(g)

def test3():
    fn = r'/home/pradal/devlp/studies/plantframe/examples/PlantFrame/monopodial_plant.mtg'
    g = read_mtg_file(fn)
    
    def visitor(g, v, turtle):
        if g.edge_type(v) == '+':
            turtle.down(90)
        turtle.F()
        turtle.rollL()
    return TurtleFrame(g, visitor)

