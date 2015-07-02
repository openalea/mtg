from mtg import _ProxyNode, MTG

class Module(object):
    def __init__(self, name, scale, **parameters):
        self.name = name
        self.scale = scale
        self.parameters = parameters

def __apply_production__(mtg, current, production, edge_type):
    def add_module(current, module, edge_type):
        if module.scale == current.scale():
            cvid = mtg.add_child(current._vid, edge_type = edge_type, label = module.name, **module.parameters )
        elif module.scale < current.scale():
            ccomplex = current.complex()
            cvid = mtg.add_child(ccomplex._vid, edge_type = edge_type, label = module.name, _r_parent = current._vid, **module.parameters )

        elif module.scale > current.scale():
            assert (abs(module.scale - current.scale()) == 1 and edge_type != '+') and 'Should decompose at next scale only. No scale jump allowed'
            cvid = mtg.add_component(current._vid, label = module.name, **module.parameters )
            ## obliger de faire les liens a toutes les echelles
            if mtg.property('_r_parent').has_key(current._vid) :
                parent_at_scale = current._r_parent
                if mtg.scale(parent_at_scale) > module.scale:
                    parent_at_scale = mtg.complex(parent_at_scale, scale = module.scale)
                    mtg.property('_r_parent')[cvid] = current._r_parent
                mtg.replace_parent(cvid, current._r_parent)
                del mtg.property('_r_parent')[current._vid]
            else :
                complexparent = current.parent()
                if complexparent: 
                    comp = complexparent.component_roots_at_scale(module.scale)[0]
                    while True:
                        compchild = [c for c in comp.children() if c.edge_type() == '<' ]
                        if len(compchild) == 0: break
                        assert len(compchild) == 1
                        comp = compchild[0]
                    mtg.replace_parent(cvid, comp._vid)
        current = mtg.node(cvid)
        return current

    modstack = []

    for module in production:
        if type(module) == list:
            __apply_production__(mtg, current, module, '+')
        elif type(module) == str:
            if module == '[':
                edge_type = '+'
                modstack.append(current)
            elif module == ']':
                edge_type = '<'
                current = modstack.pop(-1)
            else:
                raise ValueError(module)
        elif isinstance(module,Module):
            if module.name == 'SB':
                edge_type = '+'
                modstack.append(current)
            elif module.name == 'EB':
                edge_type = '<'
                current = modstack.pop(-1)
            else:
                current = add_module(current, module, edge_type)
                edge_type = '<'
        elif isinstance(module, _ProxyNode):
            params = dict([(pname, mtg.property(pname)[vid]) for pname in mtg.property_names() if not pname in ['edge_type', 'label'] and mtg.property(pname).has_key(vid)])
            pmodule = Module(module.label, module.scale(), **params)
            current = add_module(current, pmodule, edge_type)
            edge_type = '<'

    return current

def __replace_and_produce__(mtg, vid, production):

    
    if mtg.parent(vid):
        current = mtg.node(mtg.parent(vid))

    current = __apply_production__(mtg, current, production, '<')

    # sewing
    for childvid in mtg.children(vid):
        mtg.replace_parent(childvid, current._vid)

    # removal of vid and its components
    def remove_components(mtg, vid):
        for compvid in mtg.components(vid):
            remove_components(mtg, compvid)
            mtg.remove_vertex(compvid)
    remove_components(mtg, vid)
    mtg.remove_vertex(vid)


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

    def match(self, moduletype):
        return self.label == moduletype().name





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

def produce(*modules):
    mtg = MTG()
    first = modules[0]
    fvid = mtg.add_component(mtg.root, label = first.name)
    __apply_production__(mtg, mtg.node(fvid), modules[1:],'<')
    return mtg


def forward_rewritting_traversal(self, scale):
    return [RewritableNode(self, vid) for vid in self.vertices(scale = scale)]


MTG.forward_rewritting_traversal = forward_rewritting_traversal

del forward_rewritting_traversal
