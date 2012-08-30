from openalea.mtg.io import axialtree2mtg, mtg2mss , lpy2mtg, mtg2lpy
from openalea.lpy import AxialTree, generateScene, Lsystem
from openalea.plantgl.all import Scene, Viewer
from openalea.core.path import path

def str2mtg(s):
    #s = s.replace('N', 'F')
    tree = AxialTree(s) 
    l = Lsystem()
    l.addInterpretationRule('N --> F', 0)
    geom_tree = l.homomorphism(tree)
    scene = l.sceneInterpretation(geom_tree)
    scale = dict(zip(('P','A','N', 'L', 'F'),(1,2,3,3,3)))
    mtg = axialtree2mtg(tree, scale, scene)
    return tree, mtg, scene



def str2mss(s, envelop):
    tree, mtg, scene = str2mtg(s)
    return mtg2mss('test', mtg, scene, envelop), mtg, tree, s

def check(tree, mtg, scene):
    s = str(tree)
    n1, n2 = [s.count(char) for char in ['P', 'A']]
    n3 = s.count('N') + s.count('L') + s.count('F')
    assert mtg.nb_vertices(scale=1) == n1, '%d, %d'%(mtg.nb_vertices(scale=1), n1 )
    assert mtg.nb_vertices(scale=2) == n2, '%d, %d'%(mtg.nb_vertices(scale=2), n2 )
    assert mtg.nb_vertices(scale=3) == n3, '%d, %d'%(mtg.nb_vertices(scale=3), n3)
    v3 = set(mtg.vertices(scale=3))
    geom3 = set((sh.id for sh in scene))
    assert v3 == geom3, str(v3)+'!='+str(geom3)
        
def check_mss(mss, mtg, tree, s=None):
    if not mss: print tree
    assert mss.depth == mtg.max_scale()
    for scale in range(1,mss.depth+1):
        assert len(set(mss.get1Scale(scale))) == len(set(mtg.vertices(scale=scale))), (str(set(mss.get1Scale(scale)))+' !='+ str(set(mtg.vertices(scale=scale))),s)
    

def test0():
    # simple set of two successives axes
    trees = '''
PANNN[+ANNN][-ANNN]AN
PANNN[+ANNN][-ANNN]NNNANAN
PANNN[+ANNN][-ANNN]AN[+ANNN][-ANNN]ANNN[+ANNN][-ANNN]AN
PANNN[+ANNN][-ANNN]AN[+ANNN][-ANNN]ANNN[+ANNN][-ANNN]ANPANNN[+ANNN][-ANNN]AN[+ANNN][-ANNN]ANNN[+ANNN][-ANNN]ANPANNN[+ANNN][-ANNN]AN[+ANNN][-ANNN]ANNN[+ANNN][-ANNN]AN
PANNN[+ANNN[+ANNN[+ANNN][-ANNN]NNNANAN]][-ANNN[+ANNN[-ANNN]]NN]NANAN
'''
    for s in trees.split():
        check( *str2mtg(s) )

def test1():
    # simple set of two successives axes
    trees = '''
PANNN[+(+30)ANNN][-ANNN]AN
PANNN[+(-30)ANNN][-(2)ANNN]AN
'''
    for s in trees.split():
        check( *str2mtg(s) )

def test2():
    # simple set of two successives axes
    trees = '''
PA(9)N
'''
    for s in trees.split():
        check( *str2mtg(s) )

def _test_mss():
    trees = '''
PANNN[+ANNN][-ANNN]AN
PANNN[+ANNN][-ANNN]NNNANAN
PANNN[+ANNN][-ANNN]AN[+ANNN][-ANNN]ANNN[+ANNN][-ANNN]AN
PANNN[+ANNN][-ANNN]AN[+ANNN][-ANNN]ANNN[+ANNN][-ANNN]ANPANNN[+ANNN][-ANNN]AN[+ANNN][-ANNN]ANNN[+ANNN][-ANNN]ANPANNN[+ANNN][-ANNN]AN[+ANNN][-ANNN]ANNN[+ANNN][-ANNN]AN
PANNN[+ANNN[+ANNN[+ANNN][-ANNN]NNNANAN]][-ANNN[+ANNN[-ANNN]]NN]NANAN
'''
    envelop = ['CvxHull', 'Box', 'Sphere']
    for s in trees.split():
        print s
        for env in envelop:
            print env
            check_mss( *str2mss(s, env) )

def test_mtglpy():
    fn = path('ex_luz4.lpy')
    if not fn.exists():
        return

    l = Lsystem('ex_luz4.lpy')

    tree = l.iterate()

    scene = l.sceneInterpretation(tree)

    mtg = lpy2mtg(tree, l, scene)
    print len(mtg)
    axial_tree = AxialTree()
    axial_tree = mtg2lpy(mtg, l, axial_tree)
    print len(axial_tree)
    #axial_tree = mtg2axialtree(mtg, scale, parameters, axial_tree)
    
    # Check
    assert True
    return mtg, tree

def test_mtglpy_topvine():
    fn = path('vinemtg_n.lpy')
    if not fn.exists():
        return

    l = Lsystem(fn)
    parameters = {}
    parameters['carto_file'] = 'geom_n.dat'
    parameters['picle_file'] = 'vine_n.dat'
    parameters['TTfin'] = None

    #l.context().updateNamespace(parameters)

    c_iter = l.getLastIterationNb()
    nbstep = l.derivationLength - c_iter
    tree = l.iterate(l.axiom,c_iter,nbstep)

    scene = l.sceneInterpretation(tree)

    mtg = lpy2mtg(tree, l, scene)

    print len(mtg)
    axial_tree = AxialTree()
    axial_tree = mtg2lpy(mtg, l, axial_tree)

    g = lpy2mtg(axial_tree, l, scene)

    assert len(g) == len(mtg)
    #axial_tree = mtg2axialtree(mtg, scale, parameters, axial_tree)
    
    # Check
    assert True
    return mtg, tree, axial_tree

