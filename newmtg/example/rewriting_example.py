from openalea.mtg.rewriting import *
from openalea.plantgl.all import *
from openalea.mtg import *

display = False

module('Plant',     1, globals())
module('Internode', 2, globals())
module('Leaf',      2, globals())
module('LeafBud',   3, globals())
module('ISegment',  3, globals())
module('LSegment',  3, globals())

axiom = produce(Plant(), Internode(), ISegment(), [Internode(), ISegment()], LeafBud(size=3))

print 'Axiom:'
axiom.display(display_scale=True)

mtg = axiom
# Rewritting
for node in mtg.forward_rewritting_traversal(scale = 3):

    if node.match(LeafBud):

        length = 1.5 * node.size
        #node.nproduce(node)

        node.nproduce('[',Internode(),ISegment())
        node.nproduce('[',Leaf(length=length))
        for i in xrange(5):
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


print
print 'Result:'
mtg.display(display_scale=True)

print
#for vid in mtg:
#    print mtg.edge_type(vid), vid, mtg.label(vid), mtg.scale(vid) #, mtg[vid]