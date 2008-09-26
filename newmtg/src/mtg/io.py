# -*- python -*-
#
#       OpenAlea.mtg
#
#       Copyright 2008 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.pradal.at.cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

'''
This module provides functions to read / write mtg data structure.
'''

import re
from string import Template
from warnings import warn

import openalea.plantgl.all as pgl

from mtg import *
from traversal import iter_mtg

debug = 0
def log(*args):
    if debug:
        print '  '.join(map(str, args))

################## UTILS
def get_expr(s, expr):
    res = re.search(expr, s)
    _str = ''
    if res:
        _str = s[res.start():res.end()]
    return _str

def get_label(s):
    name = r'[a-zA-Z0-9]+'
    return get_expr(s, name)

def get_name(s):
    name = r'[a-zA-Z]+'
    return get_expr(s, name)

def get_index(s):
    name = r'[0-9]+'
    return get_expr(s, name)

def get_args(s):
    args = r'\([0-9,-\.\+]+\)'
    return get_expr(s, args)

def get_float(s):
    args = r'[0-9-\+]+'
    num = get_expr(s, args)
    return float(num)

def multiscale_edit(s, symbol_at_scale = {}, class_type={}):

    def get_properties(name):
        _type = dict([('INT', int), ('REAL', float), ('ALPHA', str)])
        args = {}
        l = name.strip().split('(')
        label = l[0]
        index = get_index(label)
        if index.isdigit():
            args['index'] = int(index)
        args['label'] = label
        if len(l) > 1:
            s = l[1][:-1]
            if s:
                l = s.split(',')
                for arg in l:
                    k, v = arg.split('=')
                    klass = _type[class_type[k]]
                    args[k] = klass(v)
        return args

    implicit_scale = bool(symbol_at_scale)

    mtg = MTG()

    vid = mtg.root # vid of the support tree, i.e. at the finest scale
    current_vertex = mtg.root
    branching_stack = []

    if not implicit_scale:
        symbols = ['/', '\\', '[', ']', '+', '<', '<<']
    else:
        symbols = ['/', '[', ']', '+', '<', '<<']

    pending_edge = '' # edge type for the next edge to be created
    scale = 0

    # 2. add some properties to the MTG
    mtg.add_property('index')
    for k in class_type.keys():
        mtg.add_property(k)

    for edge_type in symbols:
        s = s.replace(edge_type, '\n%s'%edge_type)
    s = s.replace('<\n<', '<<')
    l = filter( None, s.split('\n'))

    for node in l:
        if node.startswith('<<'):
            tag = '<<'
            name = node[2:]
        else:
            tag = node[0]
            name = node[1:]
            assert tag in symbols, tag
        
        if tag == '[':
            branching_stack.append(vid)
        elif tag == ']':
            vid = branching_stack.pop()
            current_vertex = vid
        else:
            if class_type:
                args = get_properties(name)
            else:
                label = get_label(name)
                index = get_index(name)
                args = {'label':label}
                if index.isdigit():
                    args['index'] = int(index)

            if implicit_scale:
                symbol_class = get_name(name)
                new_scale = symbol_at_scale[symbol_class]
                while new_scale < scale:
                    scale -= 1
                    current_vertex = mtg.complex(current_vertex)

            if tag in ['+', '<']:
                if mtg.scale(vid) == scale:
                    vid = mtg.add_child(vid, edge_type=tag, **args)
                    current_vertex = vid
                    pending_edge = ''
                else:
                    complex = mtg.complex(current_vertex)
                    current_vertex = mtg.add_component(complex, **args)
                    pending_edge = tag
            elif tag == '<<':
                index = args['index']
                label = args['label']
                previous_index = mtg.property('index')[current_vertex]
                pending_edge = ''
                for i in range(previous_index+1, index+1):
                    args['index'] = i
                    args['label'] = label.replace(str(index), str(i))
                    vid = mtg.add_child(vid, edge_type='<', **args)
                    current_vertex = vid
            elif tag == '/':
                if mtg.scale(vid) == scale:
                    vid = mtg.add_component(vid, **args)
                    current_vertex = vid
                    scale += 1
                else:
                    scale += 1
                    component = mtg.add_component(current_vertex, **args)
                    if mtg.scale(vid) == scale:
                        vid = mtg.add_child(vid, 
                                            child=component, 
                                            edge_type=pending_edge, 
                                            label=name)
                        assert vid == component
                        current_vertex = vid
                    else:
                        current_vertex = component
            elif tag == '\\':
                scale -= 1
                current_vertex = mtg.complex(current_vertex)
        
    
    mtg = fat_mtg(mtg)
    return mtg

def read_lsystem_string( string, 
                         symbol_at_scale, 
                         functional_symbol={}, 
                         mtg=None ):
    '''
     Read a string generated by a lsystem.
    
     :Parameters:
      - `string`: The lsystem string representing the axial tree.
      - `symbol_at_scale`: A dict containing the scale for each symbol name.
      _ `functional_symbol`: A dict containing a function for specific symbols.
    
    The args of the function have to be coherent with those in the string.
    The return type of the functions have to be a dictionary of properties: dict(name, value)

    :Retturn: mtg
    '''
    
    s = string

    def transform(turtle, mesh):
        x = turtle.getUp()
        z = turtle.getHeading()

        bo = pgl.BaseOrientation(x, z^x)
        matrix = pgl.Transform4(bo.getMatrix())
        matrix.translate(turtle.getPosition())
        mesh = mesh.transform(matrix)
        return mesh
        

    # 1. Create the mtg structure.
    if mtg is None:
        mtg = MTG()

    # 2. add some properties to the MTG
    mtg.add_property('index')
    mtg.add_property('can_label')
    mtg.add_property('geometry')


    vid = mtg.root # vid of the support tree, i.e. at the finest scale
    current_vertex = mtg.root
    branching_stack = []

    pending_edge = '' # edge type for the next edge to be created
    scale = 0

    lsys_symbols = ['[', ']', '/', '+', 'f']
    modules = symbol_at_scale.keys()
    symbols = lsys_symbols + modules

    index = dict(zip(symbol_at_scale.keys(), [0]*len(symbol_at_scale)))

    is_ramif = False 

    # 2. Create a PlantGL Turtle...
    turtle = pgl.Turtle()

    max_scale = max(symbol_at_scale.values())

    for edge_type in symbols:
        if edge_type != 'f':
            s = s.replace(edge_type, '\n%s'%edge_type)
        else:
            s = s.replace('f(', '\nf(')
    l = s.split()

    plant_name = [s for s in symbol_at_scale.keys() if 'plant' in s.lower()][0]

    for node in l:
        # Check if node is a module

        tag = node[0]
        
        if tag == '[':
            branching_stack.append(vid)
            turtle.push()
            is_ramif = True
        elif tag == ']':
            vid = branching_stack.pop()
            current_vertex = vid
            scale = mtg.scale(vid)
            turtle.pop()
            is_ramif = False
        elif tag == '/':
            args = get_args(node[1:])
            if args:
                angle = get_float(args[1:-1])
                turtle.rollR(angle)
            else:
                turtle.rollR()
        elif tag == '+':
            args = get_args(node[1:])
            if args:
                angle = get_float(args[1:-1])
                turtle.left(angle)
            else:
                turtle.left()
        elif tag == 'f' and node[1] == '(':
            args = get_args(node[1:])
            if args:
                length = get_float(args[1:-1])
                if length > 0:
                    turtle.f(length)
            else:
                turtle.f()
        else:
            # add new modules to the mtg (i.e. add nodes)
            name = get_name(node)
            if name not in modules:
                print 'Unknow element %s'% name
                continue
            
            module_scale = symbol_at_scale[name]
            if is_ramif:
                edge_type = '+'
            else:
                edge_type = '<'

            log(node, module_scale, edge_type )
            
            if module_scale == scale:
                if mtg.scale(vid) == scale:
                    vid = mtg.add_child(vid, edge_type=edge_type, label=name)
                    current_vertex = vid
                    pending_edge = ''

                    log('','Cas 1.1', scale, 
                        'mtg.scale(vid)', mtg.scale(vid), 
                        'generated vertex', vid)

                    assert mtg.scale(vid) == module_scale
                else:
                    # add the edge to the current vertex
                    current_vertex = mtg.add_child(current_vertex, 
                                                   edge_type=edge_type, 
                                                   label=name)
                    log('', 'Cas 1.2', scale, 
                        'mtg.scale(vid)', mtg.scale(vid), 
                        'generated vertex', current_vertex)
                    assert mtg.scale(current_vertex) == module_scale
                is_ramif = False
            elif module_scale > scale:
                log('', 'Cas 2', scale, 'mtg.scale(vid)', mtg.scale(vid))

                old_current_vertex = current_vertex
                while module_scale > scale:
                    if mtg.scale(vid) == scale:
                        assert vid == current_vertex
                        vid = mtg.add_component(vid)
                        current_vertex = vid
                        log('', '', 'Cas 2.1', scale, 'generate new component', current_vertex)
                        scale += 1
                        if module_scale == scale:
                            assert mtg.scale(current_vertex) == module_scale
                            mtg.property('label')[current_vertex] = name
                            break
                    else:
                        scale += 1
                        current_vertex = mtg.add_component(current_vertex)
                else:
                    log(node, 'add_child(%d, child=%d)'%(old_current_vertex, current_vertex))
                    mtg.property('label')[current_vertex] = name
                    if mtg.scale(vid) == scale:
                        vid = mtg.add_child(vid, child=current_vertex, edge_type=edge_type)
                        is_ramif = False
            else:
                assert module_scale < scale
                while module_scale < scale:
                    scale -= 1
                    current_vertex = mtg.complex(current_vertex)
                else:
                    current_vertex = mtg.add_child(current_vertex, edge_type=edge_type, label=name)
                    assert mtg.scale(current_vertex) == module_scale
        
            # MANAGE the properties, the geometry and the indices!!!
            index[name] += 1
            if name == plant_name:
                for k in index.keys():
                    if k != name:
                        index[k] = 0

            mtg.property('index')[current_vertex] = index[name]
            if name in functional_symbol:
                features = eval(node, functional_symbol)
                geom = features.get('geometry')
                canlabel = features.get('label')
                if geom:
                    # get the transformation from the turtle
                    geom = transform(turtle, geom)
                    mtg.property('geometry')[current_vertex] = geom

                    if name == 'StemElement':
                        # parse args to know how the turtle has to move .
                        args = get_args(node)[1:-1]
                        list_args= args.split(',')
                        length = float(list_args[1]) # 2nd arg
                        if length > 0:
                            turtle.f(length)

                if canlabel:
                    canlabel.elt_id = index[name]
                    plant_id = mtg.complex_at_scale(current_vertex, scale=1)
                    canlabel.plant_id = mtg.property('index')[plant_id]
                    mtg.property('can_label')[current_vertex] = canlabel
        
    mtg = fat_mtg(mtg)
    return mtg

def axialtree2mtg(tree, scale, scene):
    """
    Create a MTG from an AxialTree with scales.
    :Parameters:
      - `tree`: The axial tree generated by the L-system
      - `scale`: A dict containing the scale for each symbol name.
    
    :Retturn: mtg
    """
    def scene_id(scene):
        d = {}
        if scene:
            for sh in scene:
                d.setdefault(sh.id,[]).append(sh)
        return d

    def change_id(axial_id, mtg_id):
        """
        Change the id of the shape in the scene by the id of the mtg element.
        """
        if geoms:
            for shape in geoms[axial_id]:
                shape.id = mtg_id
            mtg.property('geometry')[mtg_id]=geoms[axial_id]

    # The string represented by the axial tree...

    geoms = scene_id(scene)

    mtg = MTG()
    if scene:
        mtg.add_property('geometry')

    vid = mtg.root
    current_vertex = vid
    branching_stack = []

    pending_edge = '' # edge type for the next edge to be created

    max_scale = max(scale.itervalues())
    for aid, label in enumerate(tree):
        label = label.name
        if label == '[':
            branching_stack.append(vid)
            pending_edge = '+'
        elif label == ']':
            vid = branching_stack.pop()
            current_vertex = vid
            pending_edge = ''
        elif label not in scale:
            continue
        else:
            _scale = scale[label]
            if mtg.scale(vid) == mtg.scale(current_vertex) == _scale:
                # Add a vertex at the finer scale
                if pending_edge == '+':
                    edge_type = '+'
                else:
                    edge_type = '<'

                vid = mtg.add_child(vid, edge_type=edge_type, label=label)
                current_vertex = vid
                pending_edge = ''
            elif mtg.scale(vid) < max_scale:
                assert mtg.scale(vid) == mtg.scale(current_vertex)
                # Descend in scale for the first time
                vid = mtg.add_component(vid, label=label)
                current_vertex = vid
            elif mtg.scale(current_vertex) < _scale:
                assert mtg.scale(current_vertex) == _scale - 1
                current_vertex = mtg.add_component(current_vertex, label=label)
                if mtg.scale(vid) == _scale:
                    if pending_edge == '+':
                        edge_type = '+'
                    else:
                        edge_type = '<'
                    vid = mtg.add_child(vid, 
                                        child=current_vertex, 
                                        label=label, 
                                        edge_type=edge_type)
                    assert vid == current_vertex
                    pending_edge = ''
            else:
                while mtg.scale(current_vertex) >= _scale:
                    current_vertex = mtg.complex(current_vertex)
                assert mtg.scale(current_vertex) == _scale - 1
                current_vertex = mtg.add_component(current_vertex, label=label)

            assert mtg.scale(current_vertex) == _scale

            if max_scale == _scale:
                change_id(aid,current_vertex)

    mtg = fat_mtg(mtg)
    return mtg

def mtg2mss(name, mtg, scene, envelop_type = 'CvxHull'):

    from openalea.fractalysis.light import ssFromDict

    l = []
    for scale in range(1, mtg.nb_scales()-1):
        d = {}
        for vid in mtg.vertices(scale=scale):
            d[vid] = list(mtg.components(vid))
        l.append(d)
    return ssFromDict(name, scene, l, envelop_type)
    

###############################################################################
# Class and methods to read the famous MTG file format.
###############################################################################

class Reader(object):
    """
    Parse a MTG string from a classic MTG file format.

    The mtg format is composed of a header and the mtg code.
    The header is used to construct and validate the mtg.
    The code contains topology relations and properties.
    """

    def __init__(self, string):
        self.mtg = None

        # First implementation.
        # Do not store 3 time the structure (mtg, txt and lines)
        self.txt = string
        self.lines = string.split('\n')

        # header information
        self._code = ""
        self._symbols = {}
        self._description = None
        self._features = {}

        # debug
        self._no_line = 0
        self.warnings = []

    def parse(self):
        """
        """
        self.header()
        self.code()
        
        self.errors()
        return self.mtg
        
    def header(self):
        """
        Parse an MTG header and create the mtg datastructure.

        An mtg header contains different parts:
            - code:  definition
            - classes: symbol name and scale 
            - description: allowed relationship between symbols
            - features: property name and type
        """

        # 1. Read the file from the begining
        self._no_line = -1 
        self.code_form()
        self.classes()
        self.description()
        self.features()


    def check(self):
        """
        Check the validity of the MTG without building it.
        """
        return True

    #### internal methods ####
    def code_form(self):
        """
        CODE: FORM-A / FORM-B
        """
        l = self._next_line()
        code = l.split(':')
        if len(code) == 2 and 'CODE' in code[0] and 'FORM-' in code[1]:
            self._code = code[1] 
        else:
            # error
            self.warnings.append((self._no_line, "Code form error"))

    def classes(self):
        """
        CLASSES:
        SYMBOL  SCALE   DECOMPOSITION   INDEXATION  DEFINITION
        ...
        """
        decomp = ['NONE', 'FREE', 'CONNECTED', 'LINEAR', 'PURELINEAR', '<-LINEAR', '+-LINEAR']
        l = self._next_line()
        if not l.startswith('CLASSES'):
            self.warnings.append((self._no_line, "CLASSES section not found."))
            
        l = self._next_line()
        class_header = l.split()
        if class_header != ['SYMBOL', 'SCALE', 'DECOMPOSITION', 'INDEXATION', 'DEFINITION']:
            self.warnings.append((self._no_line, "CLASS header error."))
        
        while l:
            l = self._next_line()
            if l.startswith('DESCRIPTION'):
                break
            line = l.split()
            if len(line) != 5:
                self.warnings.append((self._no_line, "CLASS error."))
                break
            else:
                symbol, scale, decomposition, indexation, definition = line
                # validation
                if not symbol.isalpha() and symbol != '$':
                    self.warnings.append((self._no_line, "Bad symbol %s."%symbol))
                if not scale.isdigit():
                    self.warnings.append((self._no_line, "Bad scale %s."%scale))
                if decomposition not in decomp: 
                    self.warnings.append((self._no_line, "Bad decomposition id %s."%decomposition))
                # TODO: validate indexation
                if definition not in ['IMPLICIT', 'EXPLICIT']:
                    self.warnings.append((self._no_line, "Bad definition %s."%definition))

                if symbol != '$':
                    self._symbols[symbol] = int(scale)

        if l.startswith('DESCRIPTION'):
            self._no_line -= 1

    def description(self):
        """
        DESCRIPTION:
        LEFT RIGHT RELTYPE MAX
        U U,I + ?
        ...
        """
        l = self._next_line()
        if not l.startswith('DESCRIPTION'):
            self.warnings.append((self._no_line, "DESCRIPTION section not found."))
            
        l = self._next_line()
        desc_header = l.split()
        if desc_header != ['LEFT', 'RIGHT', 'RELTYPE', 'MAX']:
            self.warnings.append((self._no_line, "DESCRIPTION header error."))

        while l :
            l = self._next_line()
            if l.startswith('FEATURES'):
                break
            line = l.split()
            if len(line) < 2:
                self.warnings.append((self._no_line, "Class description error."))
                continue

            left = line[0]
            if left not in self._symbols:
                self.warnings.append((self._no_line, "Unknown left symbol %s."%left))
            right = ''.join(line[1:-2])
            rights = [symbol.strip() for symbol in right.split(',')]
            bad_right= filter(lambda x: x not in self._symbols, rights)
            if bad_right:
                self.warnings.append((self._no_line, "Unknown right symbols %s."%bad_right))
                
            reltype, _max = line[-2:]
            if reltype not in ['+', '<']:
                self.warnings.append((self._no_line, "Unknown relation type %s."%reltype))
                
            if _max != '?' and not _max.isdigit():
                msg = "Error in the maximum number of relationships (%s)."%_max
                msg += "Give a number or ?"
                self.warnings.append((self._no_line, msg))

        if l.startswith('FEATURES'):
            self._no_line -= 1

    def features(self):
        """
        FEATURES:
        NAME TYPE
        nb_plant INT
        """
        l = self._next_line()
        if not l.startswith('FEATURES'):
            self.warnings.append((self._no_line, "FEATURES section not found."))
            
        l = self._next_line()
        f_header = l.split()
        if f_header != ['NAME', 'TYPE']:
            self.warnings.append((self._no_line, "FEATURES header error."))

        while l:
            l = self._next_line()
            if not l or l.startswith('MTG'):
                break
            line = l.split()
            if len(line) != 2:
                self.warnings.append((self._no_line, "FEATURE description error."))
                continue
            name, _type = line
            self._features[name] = _type

        if l.startswith('MTG'):
            self._no_line -= 1

    def _next_line(self):
        self._no_line += 1
        if self._no_line == len(self.lines):
            self._no_line -= 1
            return ""
        
        l = self.lines[self._no_line]
        l = l.strip()
        if not l or l[0] == '#':
            return self._next_line()
        else:
            return l

    def errors(self):
        nb_lines = len(self.lines)
        for id, warn in self.warnings:
            if id < nb_lines:
                print "== Line %d: %s"%(id, self.lines[id])
                print warn
            else:
                print id, " ", warn
    ############################################################################
    ### Parsing of the MTG code
    ### That's the real stuff...
    ############################################################################

    def code(self):
        """
        Parse the code and populate the MTG.
        """
        l = self._next_line()
        
        if not l.startswith('MTG'):
            self.warnings.append((self._no_line, "MTG section not found."))

        l = self._next_line()
        if not l.startswith('ENTITY-CODE'):
            self.warnings.append((self._no_line, "ENTITY-CODE not found."))
        
        features = l.split()[1:]
        self._nb_features = len(features)
        self._feature_head = []
        for feature in features:
            if feature not in self._features:
                self.warnings.append((self._no_line, "Error in ENTITY-CODE: Feature %s is unknown."%feature))
            else:
                self._feature_head.append(feature)

        code_topo = l[:l.find(features[0])]
        nb_cols = len(code_topo.split('\t'))
        self._feature_slice = slice(nb_cols-1, nb_cols-1+self._nb_features)

        self.preprocess_code()
        self.build_mtg()

    def preprocess_code(self):
        code = [l for l in self.lines[self._no_line+1:] if l.strip() and not l.strip().startswith('#')]

        indent = [0]
        edge_type = []
        tab = 0
        new_code = []
        for l in code:
            #l = l.expandtabs(4)
            s = l.strip()
            s= s.split()[0]
            # args
            args = l.split('\t')[self._feature_slice]
            n = len(args)
            params = [ "%s=%s"%(k,v) for k, v in zip(self._feature_head, args) if v.strip()]

            if params:
                s = s + "("+','.join(params)+")"
            
            # build 
            nb_spaces = len(l) - len(l.lstrip('\t'))

            diff_space = nb_spaces - indent[-1]
            
            # DEBUG
            if debug:
                print 'line :%s, nb_spaces: %d, diff_space: %d, edge_type:%s, %s'%(l[:10], 
                                                                                   nb_spaces, 
                                                                                   diff_space, 
                                                                                   str(edge_type), 
                                                                                   str(indent)) 
            if diff_space == 0:
                if s.startswith('^'):
                    s = s[1:]
                    if s.startswith('+'):
                        s = '[' + s
                        edge_type.append('+')
                elif s.startswith('+'):
                    if edge_type[-1] == '+':
                        s = '][' + s
                    else:
                        #error
                        print "ERROR ", edge_type[-1], s

            elif diff_space > 0:
                # indent
                indent.append(nb_spaces)
                edge_type.append(s[0])
                if s[0] == '^':
                    print 'ERROR'
                    print 'diff_space ', diff_space
                    print 's ', s
                    print nb_spaces, indent[:-1]
                #assert s[0] != '^'
                if s.startswith('+'):
                    s = "[" + s
            else:
                # unindent
                brackets = []
                while nb_spaces - indent[-1] < 0:
                    indent.pop()
                    edge = edge_type.pop()
                    if edge == '+':
                        brackets.append(']')

                if nb_spaces - indent[-1] == 0:
                    #if edge_type and edge_type[-1] == '+':
                    #   print 'REMOVE edge_type and add ]'
                    #   brackets.append(']')
                    #   edge_type.pop()

                    if s.startswith('^'):
                        s = s[1:]
                        if s.startswith('+'):
                            brackets.append('[')
                            edge_type.append('+')
                    elif s.startswith('+'):
                        brackets.append('][')
                        print 'REPLACE %s by +'%(edge_type[-1])
                        edge_type[-1] = '+'
                        
                
                s = ''.join(brackets+[s])
            new_code.append(s)
            
        while edge_type:
            edge = edge_type.pop()
            if edge == '+':
                new_code.append(']')

        self._new_code = ''.join(new_code)
        #print self._new_code

    def build_mtg(self):
        """
        """
        self.mtg = multiscale_edit(self._new_code, self._symbols, self._features)

def read_mtg(s):
    reader = Reader(s)
    g = reader.parse()
    return g

def read_mtg_file(fn):
    f = open(fn)
    txt = f.read()
    f.close()
    return read_mtg(txt)


def mtg_display(g, vtx_id, tab='  ', edge_type=None, label=None):
    """
    Test the traversal of an mtg.
    A first step before writing it.
    """
    import traversal
    if not edge_type:
        edge_type = g.properties().get('edge_type', {})
    if not label:
        label= g.properties().get('label', {})

    prev = vtx_id
    prev_order = 0
    prev_scale = g.scale(vtx_id)
    for  vid in traversal.iter_mtg(g, vtx_id):
        if prev == vid:
            continue

        name = label.get(vid, vid)

        if vid in edge_type:
            et = edge_type[vid]
        elif prev == g.parent(vid):
            et = '<'
        else:
            et = '?'

        space = ''

        scale = g.scale(vid)
        order = g.order(vid)

        if prev == g.complex(vid):
            et = '/'
            # add one blank line
            space = '^'
        elif prev_scale == scale and et == '<':
            space = '^'
        
        if scale < prev_scale:
            yield ''

        order = g.order(vid)

        prev = vid
        prev_scale = scale
        prev_order = order
        if order != prev_order:
            indent = 0

        yield (order*tab) +space+et+ name
        

###############################################################################
# Class and methods to write in the famous MTG file format.
###############################################################################

class Writer(object):
    """
     Write a MTG string from a mtg object.

    The mtg format is composed of a header and the mtg code.
    The header is used to construct and validate the mtg.
    The code contains topology relations and properties.
    """

    def __init__(self, g, header = '' ):

        self.g = g
        self._header = header

    def header(self):
        """
        Build the MTG header from the datastructure.

        An mtg header contains different parts:
            - code:  definition
            - classes: symbol name and scale 
            - description: allowed relationship between symbols
            - features: property name and type
        """

        code = self._code()
        classes = self.classes()
        desc = self.description()
        features = self.features()

    def code(self, property_names, nb_tab=8):
        """
        Traverse the MTG and write the code.
        """
        head = ['MTG :']

        entity = ['ENTITY-CODE'] 
        entity.extend((nb_tab-1)*[''])
        entity.extend(property_names)
        head.append('\t'.join(entity))

        # Create for each line a string with code and propertie values.
        # TODO : duplication of code from display_mtg and mtg_display.
        labels = self.g.property('label')
        edge_type = self.g.property('edge_type')

        properties = self.g.properties()
        current_vertex = self.g.root
        tab = 0
        prev_scale = 0

        for vtx in traversal.iter_mtg(self.g, self.g.root):
            
            cur_scale = self.g.scale(vtx)
            if vtx == current_vertex:
                current_vertex = vtx
                prev_scale = cur_scale
                continue

            # The previous vertex was not a complex of the current one.
            if prev_scale >= cur_scale:
                et = edge_type[vtx]
                if prev_scale == cur_scale:
                    et = '^'+et
                    if self.g.parent(vtx) != current_vertex:
                        tab -= 1
                        if tab <0:
                            tab = 0
                            et = et[1:]
                elif prev_scale > cur_scale:
                    v = current_vertex
                    for i in range(prev_scale-cur_scale):
                        v = self.g.complex(v)
                    et = '^'+et
                    if self.g.parent(vtx) != v:
                        tab -= 1
                        if tab < 0:
                            tab = 0
                            et = et[1:]

            else:
                et = '/'
                if current_vertex != self.g.root:
                    if tab+1 < nb_tab: 
                        tab += 1
                    else:
                        et = '^'+et

            # Create a valid line with properties.
            label = labels.get(vtx, str(vtx))
            name = '%s%s'%(et,get_label(label))
            line = ['']*nb_tab
            line[tab] = name

            for pname in property_names:
                p = properties[pname].get(vtx,'') 
                line.append(str(p))

            head.append('\t'.join(line))

            current_vertex = vtx
            prev_scale = cur_scale

        return head


    @staticmethod
    def _code(code='A'):
        """
        Define the MTG code format.
        """
        if code not in ['A', 'B']:
            code = 'A'

        return "CODE :  \tFORM-%s" % code

    @staticmethod
    def _classes(symbols):
        """
        Define the different symbols with their scale.
        symbols is a list of dictionary with specific keys:
            - symbol is the class name
            - scale is an positive integer 
            - decomposition (optional) is in [FREE, LINEAR, CONNECTED, +-LINEAR, <-LINEAR, NOTCONNECTED, NONE]
            - indexation (optional) is FREE or CONSECUTIVE
            - definition (optional) is EXPLICIT or IMPLICIT
        """
        
        klass = ['CLASSES :']
    
        head = ['SYMBOL', 'SCALE', 'DECOMPOSITION', 'INDEXATION', 'DEFINITION']
        klass.append('\t'.join(head))
    
        default = dict(decomposition='FREE', indexation='FREE', definition='EXPLICIT')
        template = Template('\t'.join(['$symbol', '$scale', '$decomposition', '$indexation', '$definition']))
        
        d = default.copy()
        d.update(dict(symbol='$', scale='0', definition='IMPLICIT'))
    
        s = template.substitute(d) 
        klass.append(s)
    
        for sdict in symbols:
            d = default.copy()
            d.update(sdict)
            s = template.substitute(d) 
            klass.append(s)
        
        return '\n'.join(klass)

    @staticmethod
    def _description(scale_symbol):
        """
        Generate the description header file for a MTG.
        scale_symbol is a dict that associate a scale integer with the different symbols at this scale.
        """
    
        desc = ['DESCRIPTION :']
        head = ['LEFT', 'RIGHT', 'RELTYPE', 'MAX']
        desc.append('\t'.join(head))
    
        template = Template('\t'.join(['$left', '$right', '$reltype', '$max']))
    
        d = {}
        d['max'] = '?'
        scales = sorted(scale_symbol.keys())
        for scale in scales:
            symbols = scale_symbol[scale]
            d['right'] = ','.join(symbols)
            for s in symbols:
                d['left'] = s
                for edge_type in ['<', '+']:
                    d['reltype'] = edge_type
                    l = template.substitute(d)
                    desc.append(l)
    
        return '\n'.join(desc)

    @staticmethod
    def _features(name_type):
        """
        Generate the Feature header.
        name_type is a list of tuple containing the property name and the associated property type.
        type is INT, REAL, ALPHA or DATE (DD/MM, DD/MM/YY, DD/MM-TIME, DD/MM/YY-TIME).
        """
        predefined_types = ['INT', 'REAL', 'ALPHA', 'DD/MM', 'DD/MM/YY', 'DD/MM-TIME', 'DD/MM/YY-TIME']
        features = ['FEATURES :']
        features.append('\t'.join(['NAME', 'TYPE']))
        for name, type_ in name_type:
            if type_ not in predefined_types:
                warn('The type %s for the feature %s is not allow'%(type_, name), SyntaxWarning) 
                continue
            features.append('\t'.join([name, type_]))

        return '\n'.join(features)


    @staticmethod
    def _scale2symbol(scales):
        """
        scale is a dict mapping scale to a list of symbols.
        Returns a list of dict with two keys symbol and scale.
        """
        symbols = []
        for s, classes in scales.iteritems():
            for class_ in classes:
                symbols.append(dict(scale=str(s), symbol=class_))
    
        return symbols 

def write_mtg(g, properties=[], class_at_scale=None):
    """
    Returns a list of strings.
    g is a MTG.
    class_at_scale is a dict : scale -> [symbol])
    properties is a list of the property names wth their associated type to be written.
    """

    w = Writer(g)

    header = [w._code()]
    header.append('')

    if not class_at_scale:
        label = g.property('label')
        class_at_scale = dict(((get_name(lab),g.scale(id)) for id, lab in label.iteritems()))

    scales = {}
    for class_, scale in class_at_scale.iteritems():
        scales.setdefault(scale, []).append(class_)

    symbols = w._scale2symbol(scales)
    class_str = w._classes(symbols)
    header.append(class_str)
    header.append('')

    header.append(w._description(scales))
    header.append('')

    prop = dict(properties)
    features = w._features(properties)
    header.append(features)
    header.append('')

    property_name = [p[0] for p in properties]
    code = w.code(property_name)

    header.extend(code)
    header.append('')

    return '\n'.join(header)
