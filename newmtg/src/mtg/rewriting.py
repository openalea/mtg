# -*- coding: utf-8 -*-
# -*- python -*-
#
#       openAlea.mtg.rewriting
#
#       Copyright 2015 INRIA - CIRAD - INRA  
#
#       File author(s): Frederic Boudon <frederic.boudon.at.cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
""" MTG rewriting facilities """

from mtg import _ProxyNode, MTG

#### Module declaration #######

class Module(object):
    def __init__(self, name, scale, **parameters):
        self.name = name
        self.scale = scale
        self.parameters = parameters


class SB(Module):
    def __init__(self):
        Module.__init__(self, 'SB', 0)

class EB(Module):
    def __init__(self):
        Module.__init__(self, 'EB', 0)


def module(name, scale, namespace):
    """ declare a module in the namespace """

    def __init_custom_module__(self, **args):
        Module.__init__(self, name, scale, **args)

    from new import classobj
    namespace[name] = classobj(name,(Module,),{'__init__':__init_custom_module__})

def retrieve_modules(mtg, namespace):
    labels = mtg.property('label')
    uniquelabels = set(labels.values())
    modules = dict()
    for l in uniquelabels:
        for vid, label in labels.items():
            if l == label:
                modules[l] = mtg.scale(vid)
                break
    for name, scale in modules.items():
        module(name, scale, namespace) 


#### Production application

def __apply_production__(mtg, current, production, edge_type, lasts = None):
    if lasts is None : lasts = dict()
    def add_module(current, module, edge_type, lasts):
        if module.scale == current.scale():
            cvid = mtg.add_child(current._vid, edge_type = edge_type, label = module.name, **module.parameters )
        elif module.scale < current.scale():
            ccomplex = current.complex_at_scale(module.scale)
            cvid = mtg.add_child(ccomplex._vid, edge_type = edge_type, label = module.name, _r_parent = current._vid, **module.parameters )

        elif module.scale > current.scale():
            assert (abs(module.scale - current.scale()) == 1 and edge_type != '+') and 'Should decompose at next scale only. No scale jump allowed'
            cvid = mtg.add_component(current._vid, label = module.name, **module.parameters )
            ## obliger de faire les liens a toutes les echelles
            if mtg.property('_r_parent').has_key(current._vid) :
                parent_at_scale = current._r_parent
                if mtg.scale(parent_at_scale) > module.scale:
                    parent_at_scale = mtg.complex_at_scale(parent_at_scale, scale = module.scale)
                    mtg.property('_r_parent')[cvid] = current._r_parent
                mtg.replace_parent(cvid, parent_at_scale)
                del mtg.property('_r_parent')[current._vid]
                # need to propagate the edge type throw scale
                edge_types = mtg.property('edge_type')
                edge_types[cvid] = edge_types[current._vid]
            else :
                ## fuzy case: we do not know what are the element at the smallest scale which should be the parent.
                ## we choose the last apical one.
                complexparent = current.parent()
                if complexparent: 
                    apicalcomponent = complexparent.component_roots_at_scale(module.scale)[0]
                    while True:
                        compchild = [c for c in comp.children() if c.edge_type() == '<' ]
                        if len(compchild) == 0: break
                        assert len(compchild) == 1
                        apicalcomponent = compchild[0]
                    mtg.replace_parent(cvid, apicalcomponent._vid)

                    # need to propagate the edge type throw scale
                    edge_types = mtg.property('edge_type')
                    edge_types[cvid] = edge_types[current._vid]
        current = mtg.node(cvid)
        lasts[module.scale] = cvid
        return current

    modstack = []

    for module in production:
        if type(module) == list:
            __apply_production__(mtg, current, module, '+', lasts)
        elif type(module) == str:
            if module == '[':
                edge_type = '+'
                modstack.append(current)
            elif module == ']':
                edge_type = '<'
                current = modstack.pop(-1)
            else:
                raise ValueError(module)
        elif isinstance(module,Module) or (type(module) == type and issubclass(module,Module)):
            if (type(module) == type and issubclass(module,Module)): module = module()
            if module.name == 'SB':
                edge_type = '+'
                modstack.append(current)
            elif module.name == 'EB':
                edge_type = '<'
                current = modstack.pop(-1)
            else:
                current = add_module(current, module, edge_type, lasts)
                edge_type = '<'
        elif isinstance(module, _ProxyNode):
            vid = module._vid
            params = dict([(pname, mtg.property(pname)[vid]) for pname in mtg.property_names() if not pname in ['edge_type', 'label'] and mtg.property(pname).has_key(vid)])
            pmodule = Module(module.label, module.scale(), **params)
            current = add_module(current, pmodule, edge_type, lasts)
            edge_type = '<'


def macro_children_at_maxscale(mtg, vid, macroscale):
    result = []
    children = list(mtg.children(vid))

    vidcomplexes = dict()
    for s in xrange(mtg.scale(vid)-1,macroscale-1,-1):
        vidcomplexes[s] = mtg.complex_at_scale(vid, s)

    while len(children) > 0:
        nchildren = []
        for child in children:
            upscale = mtg.scale(child)-1
            cchild = mtg.complex(child)
            if cchild != vidcomplexes[upscale]:
                result.append(cchild)
                if upscale < macroscale:
                    nchildren.append(cchild)
            else:
                nchildren += list(mtg.children(child))
        children = nchildren

    return result

def __replace_and_produce__(mtg, vid, production):

    if mtg.parent(vid):
        pcurrent = mtg.node(mtg.parent(vid))
        edge_type = '<'
    else:
        pcurrent = mtg.node(mtg.complex(vid))
        edge_type = '/'

    lasts = dict([(pcurrent.scale(), pcurrent._vid)])
    __apply_production__(mtg, pcurrent, production, edge_type, lasts)

    # sewing

    scalevid = mtg.scale(vid)
    newparent = lasts[scalevid] 
    del lasts[scalevid]

    mchildren = macro_children_at_maxscale(mtg, vid, min(lasts.keys())) if len(lasts) > 0 else []

    for childvid in list(mtg.children(vid)):
        mtg.replace_parent(childvid, newparent)

    for mchild in mchildren:
        mscale = mtg.scale(mchild)
        if mtg.parent(mchild) != lasts[mscale]:
            mtg.replace_parent(mchild, lasts[mscale])

    # removal of vid and its components
    # def remove_components(mtg, vid):
    #     for compvid in mtg.components(vid):
    #         remove_components(mtg, compvid)
    #         mtg.remove_vertex(compvid)
    #remove_components(mtg, vid)

    # removal of vid
    mtg.remove_vertex(vid)

    # removal of properties of vid
    for property in mtg.properties().values():
        if property.has_key(vid) : del property[vid]


############   The rewritable node and production structures ######

def match(self, moduletype):
    return self.label == moduletype().name

_ProxyNode.match = match
del match


class RewritableNode(_ProxyNode):
    def __init__(self, mtg, vid):
        self.__dict__['_production'] = []
        _ProxyNode.__init__(self, mtg, vid)

    def is_valid(self):
        return not (self._vid is None or self._g is None)

    def nproduce(self, *modules):
        assert self.is_valid() and "Production already occured"
        self.__dict__['_production'] += modules

    def produce(self, *modules):
        assert self.is_valid() and "Production already occured"
        self.nproduce(*modules)
        __replace_and_produce__(self._g, self._vid, self._production)
        self.__dict__['_vid'] = None


def produce(*modules):
    """ Function that produce an MTG from a serie of modules """
    mtg = MTG()
    first = modules[0]
    fvid = mtg.add_component(mtg.root, label = first.name)
    __apply_production__(mtg, mtg.node(fvid), modules[1:],'<')
    return mtg

class MTGProducer(object):
    """ To produce an MTG in several steps """
    def __init__(self):
        self._production = []
    

    def nproduce(self, *modules):
        self._production += modules

    def produce(self, *modules):
        self.nproduce(*modules)
        return produce(*self._production)


#### Traversal of the MTG for the rewriting

def forward_rewriting_traversal(mtg):
    from traversal import iter_mtg2
    return [RewritableNode(mtg, vid) for vid in list(iter_mtg2(mtg, mtg.root))]

def backward_rewriting_traversal(mgt):
    from traversal import iter_mtg2
    return [RewritableNode(mtg, vid) for vid in reversed(iter_mtg2(mtg, mtg.root))]

def nodes_forward_traversal(mtg, pre_order, post_order):
    from traversal import iter_mtg2_with_filter

    def pre_order_filter(vid):
        pre_order(mtg.node(vid))
        return True

    def post_order_visitor(vid):
        post_order(mtg.node(vid))

    for vid in iter_mtg2_with_filter(mtg, mtg.root, pre_order_filter, post_order_visitor) :
        pass

MTG.forward_rewriting_traversal = forward_rewriting_traversal
del forward_rewriting_traversal

MTG.backward_rewriting_traversal = backward_rewriting_traversal
del backward_rewriting_traversal



#######  The decorators

def production(f):
    f.__isproduction__ = True
    return f


def interpretation(f):
    f.__isinterpretation__ = True
    return f


####### The MTG Lsystem kernel

eForward, eBackward = 1,0

class MTGLsystem(object):
    rules = dict()

    def __init__(self):
        self.currentmtg = None
        self.direction = eForward

    def axiom(self):
        raise NotImplemented()

    def init(self):
        self.currentmtg = self.axiom()
        if self.__dict__.has_key('start') : self.start(self.currentmtg)

    def __get_rules(self, tag = '__isproduction__'):
        import inspect
        rules = dict()
        for attname in dir(self):
            attvalue = getattr(self, attname)
            if hasattr(attvalue,tag) :
                if inspect.isclass(attvalue):
                    for sattname in dir(attvalue):
                        sattvalue = getattr(self, sattname)
                        if  type(sattvalue) == function:
                            rules[sattname] = sattvalue
                else:
                    rules[attname] = attvalue

        return rules

    def iterate(self, inputmtg = None):
        if inputmtg is None:
            if self.currentmtg is None: self.init() 
            mtg = self.currentmtg
        else : mtg = inputmtg 

        if self.__dict__.has_key('startEach') : self.startEach(mtg)

        rules = self.__get_rules()
        if self.direction == eForward:
            for node in mtg.forward_rewriting_traversal():
                if rules.has_key(node.label):
                    rules[node.label](node)
        elif self.direction == eBackward:
            for node in mtg.backward_rewriting_traversal():
                if rules.has_key(node.label):
                    rules[node.label](node)

        if self.__dict__.has_key('endEach') : self.endEach(mtg)

        if inputmtg is None:
            self.currentmtg = mtg

        return mtg

    def run(self, nbiter = 1):
        self.init()
        for i in xrange(nbiter):
            self.iterate()
        if self.__dict__.has_key('end') : self.end(self.currentmtg)
        return self.currentmtg


    def interpret(self, inputmtg = None, turtle = None):
        if inputmtg is None:
            if self.currentmtg is None: self.init() 
            mtg = self.currentmtg
        else : mtg = inputmtg 

        if turtle is None:
            from openalea.plantgl.all import PglTurtle
            turtle = PglTurtle()

        turtle.start()

        rules = self.__get_rules('__isinterpretation__')

        def preorder(node):
            if node.edge_type() == '+': turtle.push()
            turtle.setId(node._vid)
            if rules.has_key(node.label):
                rules[node.label](node, turtle)

        def postorder(node):
            if node.edge_type() == '+': turtle.pop()

        nodes_forward_traversal(mtg, preorder, postorder)

        turtle.stop()

        return turtle

    def sceneInterpretation(self, inputmtg = None):
        scene  =  self.interpret(inputmtg).getScene()

        if inputmtg is None: mtg = self.currentmtg
        else : mtg = inputmtg

        mtg.properties()['geometry'] = scene.todict() 

        return scene

    def plot(self, inputmtg = None):
        from openalea.plantgl.all import Viewer
        Viewer.display(self.sceneInterpretation(inputmtg))

    def animate(self, nbiter = 1, dt = 0.1):
        from openalea.plantgl.all import Sequencer
        s = Sequencer(dt)
        self.init()
        self.plot()
        s.touch()
        for i in xrange(nbiter):
            self.iterate()
            self.plot()
            s.touch()
        if self.__dict__.has_key('end') : self.end(self.currentmtg)
        return self.currentmtg

