# import openalea.mtg.rewriting as rw; reload(rw)
from openalea.mtg.rewriting import *

display = False

module('Plant',     1, globals())
module('Internode', 2, globals())
module('Leaf',      2, globals())
module('LeafBud',   3, globals())
module('AxisBud',   3, globals())
module('ISegment',  3, globals())
module('LSegment',  3, globals())


def example1(display = False):
    from openalea.plantgl.all import PglTurtle, Viewer

    axiom = produce(Plant(), Internode(), ISegment(), [Internode(), ISegment()], LeafBud(size=3))

    print('Axiom:')
    axiom.display(display_scale=True)

    mtg = axiom
    # Rewritting
    for node in mtg.forward_rewritting_traversal():

        if node.match(LeafBud):

            length = 1.5 * node.size
            #node.nproduce(node)

            node.nproduce('[',Internode(),ISegment())
            node.nproduce('[',Leaf(length=length))
            for i in range(5):
                node.nproduce(LSegment(radius = 3))
            node.nproduce(']')
            node.produce(']')

    # display
    if display:
        t = PglTurtle()
        for node in mtg.forward_rewritting_traversal(2):
            if node.label == 'Internode':
                t.F()
            elif node.label == 'Leaf':
                t.down(60).setColor(2).quad()

        Viewer.display(t.getScene())

    return mtg

#mtg = example1()


class MySimu(MTGLsystem):
    def __init__(self):
        MTGLsystem.__init__(self)


    def axiom(self):
        mtg = produce(Plant(), Internode(), ISegment(length=3), [ LeafBud()], AxisBud(age=0))
        
        print('Axiom:')
        mtg.display(display_scale=True)

        return mtg

    @production
    def LeafBud(self, node): 
        from math import sin, pi
        if node.parent().match(ISegment):      
            #node.nproduce(node)

            node.nproduce('[',Internode(), ISegment(length=2), Leaf())
            for i in range(5):
                node.nproduce(LSegment(radius = sin((i+1)*pi/6.5)))
            node.produce(']')

    @production
    def AxisBud(self, node): 
        if node.parent().match(ISegment):      
            #node.nproduce(node)

            node.nproduce( Internode(),ISegment(length=3))
            node.nproduce( [LeafBud()])
            node.age += 1
            node.produce( node )

    @interpretation
    def ISegment(self, node, turtle):
        #print '***', 'ISegment', node.edge_type(), node._vid
        turtle.rollL(137)
        if node.edge_type() == '+': turtle.down(60)
        turtle.F(node.length)

    @interpretation
    def Leaf(self, node, turtle):
        turtle.setColor(2).rollToVert()

    @interpretation
    def LSegment(self, node, turtle):
        try:
            n = node.children()[0]
            topradius = n.radius
        except:
            topradius = 0
        turtle.down(10).setWidth(node.radius).quad(2, topradius)


simu = MySimu()
mtg = simu.animate(30)




print()
print('Result:')
mtg.display(display_scale=True)

print()
#for vid in mtg:
#    print mtg.edge_type(vid), vid, mtg.label(vid), mtg.scale(vid) #, mtg[vid]