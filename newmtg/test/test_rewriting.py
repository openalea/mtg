import openalea.mtg.rewriting as rw; reload(rw) 
from openalea.mtg.rewriting import *


module('Plant',       1, globals())
module('BS',          2, globals())
module('Internode',   3, globals())
module('GrowthPoint', 4, globals())
module('Segment',     4, globals())

def axiom():
    return produce(Plant(), BS(), Internode(), Segment(), [Internode(), Segment()], GrowthPoint(), [Internode(), Segment()] , Internode(), Segment() )

def printresult(mtg):
    print
    print 'Result:'
    mtg.display(display_scale=True)

def runsimu(simu, display=True):
    simu.init()
    mtg = simu.currentmtg

    print 'Axiom:'
    mtg.display(display_scale=True)

    mtg = simu.run()

    if display: printresult(mtg)

    return mtg

def test1():
    class MySimu(MTGLsystem):
        def __init__(self):
            MTGLsystem.__init__(self)


        def axiom(self):
            return axiom()

        @production
        def GrowthPoint(self, node): 
            node.produce( BS(), Internode(), Segment())


    return runsimu(MySimu())


def test2():
    mtg = axiom()
    mtg.display(display_scale=True)

    for vid in [6,8,10]:
        print vid,'->',mtg.parent(vid)
    mtg.replace_parent(8,3)
    mtg.replace_parent(10,3)
    for vid in [6,8,10]:
        print vid,'->',mtg.parent(vid)

def test3():
    class MySimu(MTGLsystem):
        """ This test look when a macro node is deleted, if its components are linked with previous macro nodes. """
        def __init__(self):  MTGLsystem.__init__(self)


        def axiom(self):
            return produce(Plant(), BS(bid = 1), Internode(), Segment(), [Internode(), Segment()], BS(bid=2), Internode, Segment, [Internode(), Segment()] , Internode(), Segment() )

        @production
        def BS(self, node): 
            if node.bid == 2:
                node.produce( )


    return runsimu(MySimu())

def test4():
    class MySimu(MTGLsystem):
        """ This test look at the seewing with the children at the macro scale """
        def __init__(self):   MTGLsystem.__init__(self)

        def axiom(self):
            return produce(Plant(), BS(), Internode(), Segment(), [Internode(), Segment()], GrowthPoint(), [Internode(), Segment()] , Segment(), Internode(), Segment() )

        @production
        def GrowthPoint(self, node): 
            node.produce( BS,  Internode(), Segment())


    mtg = runsimu(MySimu(), False)

    printresult(mtg)

    return mtg

def test5():
    class MySimu(MTGLsystem):
        def __init__(self):
            MTGLsystem.__init__(self)


        def axiom(self):
            return axiom()

        @production
        def GrowthPoint(self, node): 
            node.produce( )


    return runsimu(MySimu())




if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        mtg = globals()['test'+sys.argv[1]]()
    else:
        mtg = test4()