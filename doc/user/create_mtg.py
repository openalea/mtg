from openalea.mtg.mtg import *
from openalea.mtg.aml import *


g = mtg.MTG()
plant_id = g.add_component(g.root, label='P1')

#first u1
u1 = g.add_component(plant_id, label='U1', Length=10, Diameter=5.9)
i = g.add_component(u1,label='I1' )
i = g.add_child(i,label='I2', edge_type='<' )
i = g.add_child(i,label='I3', edge_type='<' )
i = g.add_child(i,label='I4', edge_type='<' )
i = g.add_child(i,label='I5', edge_type='<' )
i6 = i = g.add_child(i,label='I6', edge_type='<' )

#u2 branch
i,u2 = g.add_child_and_complex(i6,label='I20', edge_type='+', Length=7, Diameter=3.5 )
g.node(u2).label='U2'
g.node(u2).edge_type='+'
i = g.add_child(i,label='I21', edge_type='<' )
i = g.add_child(i,label='I22', edge_type='<' )
i = g.add_child(i,label='I23', edge_type='<' )
i = g.add_child(i,label='I24', edge_type='<' )

#u3 branch
i,u3 = g.add_child_and_complex(i,label='I25', edge_type='<', Length=4, Diameter=2.1)
g.node(u3).label='U3'
g.node(u3).edge_type='<'
i = g.add_child(i,label='I25', edge_type='<' )
i = g.add_child(i,label='I26', edge_type='<' )
i = g.add_child(i,label='I27', edge_type='<' )
i = g.add_child(i,label='I28', edge_type='<' )
i = g.add_child(i,label='I29', edge_type='<' )

#continue u1
i = g.add_child(i6,label='I7', edge_type='<' )
i = g.add_child(i,label='I8', edge_type='<' )
i = g.add_child(i,label='I9', edge_type='<' )

# u2 main axe
i,c = g.add_child_and_complex(i,label='I10', edge_type='<' , Length=8, Diameter=4.3)
g.node(c).label='U2'
g.node(c).edge_type='<'
i = g.add_child(i,label='I11', edge_type='<' )
i = g.add_child(i,label='I12', edge_type='<' )
i = g.add_child(i,label='I13', edge_type='<' )
i = g.add_child(i,label='I14', edge_type='<' )
i = g.add_child(i,label='I15', edge_type='<' )


# u3 main axe
i,c = g.add_child_and_complex(i,label='I16', edge_type='<', Length=7.5, diameter=3.9 )
g.node(c).label='U3'
g.node(c).edge_type='<'
i = g.add_child(i,label='I17', edge_type='<' )
i = g.add_child(i,label='I18', edge_type='<' )
i = g.add_child(i,label='I19', edge_type='<' )


#fat_mtg(g)

print g.is_valid()
print g

for id in g.vertices():
    print g[id]
from openalea.mtg.io import *

print list(g.property_names())
properties = [(p, 'REAL') for p in g.property_names() if p not in ['edge_type', 'index', 'label']]
print properties
mtg_lines = write_mtg(g, properties)
f = open('test.mtg', 'w')
f.write(mtg_lines)
f.close()

