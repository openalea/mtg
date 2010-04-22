from openalea.mtg.turtle import *

def test1():
    fn = r'data/mtg1.mtg'
    g = read_mtg_file(fn)
    return TurtleFrame(g)

def test2():
    fn = r'data/monopodial_plant.mtg'
    g = read_mtg_file(fn)
    return TurtleFrame(g)

def test3():
    fn = r'data/monopodial_plant.mtg'
    g = read_mtg_file(fn)
    
    def visitor(g, v, turtle):
        if g.edge_type(v) == '+':
            turtle.down(90)
        turtle.F()
        turtle.rollL()

    return TurtleFrame(g, visitor)

