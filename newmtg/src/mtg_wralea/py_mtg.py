###############################################################################
# -*- python -*-
#
#       amlPy function implementation
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__doc__="""
OpenAlea interface to the OpenAlea.MTG module.
"""

__license__= "Cecill-C"
__revision__=" $Id: $"

#//////////////////////////////////////////////////////////////////////////////

from openalea.core import *
from openalea.mtg.aml import *

"""
def max_mtg_scale(g):
    if not g:
        return 0
    
    g_str= str(g)
    scale= (g_str.split(',')[2]).strip()
    max_scale= int(scale.strip("levelnb="))
    return max_scale
"""

def set_mtg(g):
    old_g = Active()
    if not g:
        g= old_g
    elif g != old_g:
        Activate(g)

    return g

#//////////////////////////////////////////////////////////////////////////////

class py_MTG(Node):
    """
MTG( filename, ErrorNb= 10, VtxNumber= 10000 ) -> MTG

Input: filename
Ouput : MTG object if the parsing process succeeds.
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "filename", interface = IFileStr)
        #self.add_input( name = "ErrorNb", interface = IInt,value=None,hide=True)
        #self.add_input( name = "VtxNumber", interface = IInt, value=None,hide=True)
        #self.add_input( name = "AdjustSize", interface = IInt, value=None,hide=True)
        #self.add_input( name = "FeatureList", interface = ISequence, value=[],hide=True)
        #self.add_input( name = "FeatureMap", interface = ISequence, value=[],hide=True)
        #self.add_input( name = "OuputFile", interface = IFileStr, value=None,hide=True)
        #self.add_input( name = "HeaderFile", interface = IFileStr, value=None,hide=True)
        #self.add_input( name = "DiscardSymbols", interface = ISequence, value=None,hide=True)
            
        self.add_output( name = "MTG", interface = None) 

        

    def __call__(self, inputs):
        """ inputs is the list of input values """

	kwds = {}
	for desc in self.input_desc:
	    key = desc['name']
	    x = self.get_input(key)
	    if x is not None:  # selects the input arguments
		kwds[key] = x

	obj = kwds.get('filename',None)
	del kwds['filename']

        g = None
        if obj:
            try:
                g = MTG(obj, **kwds)
            except Exception, e:
                print e

	return g

#//////////////////////////////////////////////////////////////////////////////

class py_VtxList(Node):
    """\
VtxList( mtg, Scale= 2 ) -> [vtx]

Input:
  MTG (MTG)
Optional parameters:
  Scale: used to select components at a particular scale.
Output:
  VtxList: vertex array
    """

    def __init__(self):

        Node.__init__(self)

        self.add_input( name = "MTG", interface = None) 
        self.add_input( name = "Scale", interface = IInt, value= 0)
            
        self.add_output( name = "VtxList", interface = None) 

        

    def __call__(self, inputs):
        """ inputs is the list of input values """

        #from openalea.aml import VtxList as vertices
        #from openalea.aml import Active, Activate

        # We prefer here to get the value by key
        g= self.get_input("MTG")
        g = set_mtg(g)
        if not g:
            return ([],)
        
        scale = self.get_input("Scale")

#        max_scale= max_mtg_scale(g)

        vtxs= []
	if scale == 0: vtxs = VtxList()
	else : vtxs= VtxList(Scale=scale)
        
        return (vtxs,)

#//////////////////////////////////////////////////////////////////////////////

class py_Feature( Node ):

    def __init__(self):

	Node.__init__(self)

        self.add_input( name = "MTG", interface = None) 
        self.add_input(name= "Vtx", interface= IInt )
        self.add_input(name= "FeatureName", interface= IStr, value= "" )

        self.add_output(name= "FeatureData")


    def __call__(self, inputs):

        g= self.get_input("MTG")
        g = set_mtg(g)
        if not g:
            return None
 
        vtx = self.get_input("Vtx")
        name = self.get_input("FeatureName")

        if vtx is not None:
            return Feature(vtx,name)


#//////////////////////////////////////////////////////////////////////////////

class VtxFunction( Node ):
    """\
VtxFunction(string) -> func on vertex
Input:
  Name of the function.
Output:
  function that can be applied on a vertex.
    """
    
    vtx_func= { "Class" : Class,
                "Index" : Index,
                "Scale" : Scale,
                "Order" : Order,
                "Rank" : Rank,
                "Height" : Height }
    
    
    def __init__(self):
    
        Node.__init__(self)

        funs= self.vtx_func.keys()
        funs.sort()
        self.add_input( name = "Name", interface = IEnumStr(funs), value = funs[0]) 
        self.add_input( name = "Vtx" ) 
        self.add_output( name = "VtxFunction", interface = None)

    def __call__(self, inputs):
        func_name= self.get_input("Name")
        vtx = self.get_input("Vtx")
        f = self.vtx_func.get(func_name,None)
        self.set_caption(func_name)

        if not vtx:
            return f
        elif callable(vtx):
            return lambda x: f(vtx(x))
        else:
            return f(vtx)

#//////////////////////////////////////////////////////////////////////////////

class TopoFunction( Node ):
    """TopoFunction(string) -> func on vertex

    Input:
        Name of the function.
    Output:
        function that can be applied on a vertex.
    """
    
    vtx_func= { "Father" : Father,
                "Successor" : Successor,
                "Predecessor" : Predecessor,
                "Root" : Root,
                "Complex" : Complex,
                "Location" : Location,
                "Sons" : Sons,
                "Ancestors" : Ancestors, 
                "Descendants" : Descendants,
                "Extremities" : Extremities,
                "Components" : Components,
                "ComponentRoots" : ComponentRoots,
                "Axis" : Axis,
                "Trunk" :Trunk}
    
    
    def __init__(self):
    
        Node.__init__(self)

        funs= self.vtx_func.keys()
        funs.sort()
        self.add_input( name = "name", interface = IEnumStr(funs), value = funs[0]) 
        self.add_input( name = "Vtx" ) 
        self.add_output( name = "f", interface = None)

    def __call__(self, inputs):
        func_name= self.get_input("name")
        vtx = self.get_input("Vtx")
        f = self.vtx_func.get(func_name,None)
        self.set_caption(func_name)
        if not vtx:
            return f
        elif callable(vtx):
            return lambda x: f(vtx(x))
        else:
            return f(vtx)

#//////////////////////////////////////////////////////////////////////////////

class UnaryVtxFunc( Node ):
    
    def __init__(self,f):
    
        Node.__init__(self)
        self.f= f
        
        self.add_output( name = "f", interface = IFunction)

    def __call__(self, inputs):
        g= lambda x: self.f(x,*inputs)
        return (g,)

class py_Complex(UnaryVtxFunc):

    def __init__(self):
        UnaryVtxFunc.__init__(self,Complex)
        self.add_input(name= "Vtx", interface= IInt )
        self.add_input(name= "Scale", interface= IInt, value= 0 )

    def __call__(self, inputs):
        vtx = self.get_input("Vtx")
        scale= self.get_input("Scale")
        if vtx:
            return (self.f(vtx,Scale=scale),)
        else:
            g= lambda x: self.f(x,Scale= scale)
            return (g,)



class py_Components(UnaryVtxFunc):

    def __init__(self):
        UnaryVtxFunc.__init__(self,Components)
        self.add_input(name= "Vtx", interface= IInt )
        self.add_input(name= "Scale", interface= IInt, value= 0 )

    def __call__(self, inputs):
        vtx = self.get_input("Vtx")
        scale= self.get_input("Scale")
        if vtx:
            return (self.f(vtx,Scale=scale),)
        else:
            g= lambda x: self.f(x,Scale= scale)
            return (g,)

class py_Axis(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name= "Vtx", interface= IInt )
        self.add_input(name= "Scale", interface= IInt, value= 0 )

        self.add_output(name= "Axis", interface= ISequence)

    def __call__(self, inputs):
        vtx = self.get_input("Vtx")
        scale= self.get_input("Scale")

        if vtx is not None:
            return Axis(vtx,Scale=scale),
        else:
            g= lambda x: Axis(x,Scale= scale)
            return (g,)

def py_MTGRoot(graph):
    g = graph
    g = set_mtg(g)
    if not g:
        return None
    return MTGRoot(),


#//////////////////////////////////////////////////////////////////////////////

class py_PlantFrame( Node ):
    """\
Plot(aml object) -> Plot the object
Input:
  aml object
  
    """
    
    def __init__(self):
    
        Node.__init__(self)

        self.add_input( name = "MTG", interface = None) 
        self.add_input( name = "Vertex", interface = IInt, value= 0)
        self.add_input( name = "Scale", interface = IInt, value= 0,hide=True)
        self.add_input( name = "VoxelDist", interface = IFloat, value=None,hide=True)
        self.add_input( name = "TrunkDistance", interface = IFloat, value=None,hide=True)
        self.add_input( name = "Category", interface = IFunction,hide=True)
        self.add_input( name = "Length", interface = IFunction,hide=True)
        self.add_input( name = "LengthAlgo", interface = IStr, value=None,hide=True)
        self.add_input( name = "TopDiameter", interface = IFunction,hide=True)
        self.add_input( name = "BottomDiameter", interface = IFunction,hide=True)
        self.add_input( name = "Alpha", interface = IFunction,hide=True)
        self.add_input( name = "Azimuth", interface = IFunction,hide=True)
        self.add_input( name = "AA", interface = IFunction,hide=True)
        self.add_input( name = "BB", interface = IFunction,hide=True)
        self.add_input( name = "CC", interface = IFunction,hide=True)
        self.add_input( name = "XX", interface = IFunction,hide=True)
        self.add_input( name = "YY", interface = IFunction,hide=True)
        self.add_input( name = "ZZ", interface = IFunction,hide=True)
        self.add_input( name = "EulerAngles", interface = IFunction,hide=True)
        self.add_input( name = "DigitizedPoints", interface = IFunction,hide=True)
        self.add_input( name = "Mode", interface = IStr, value=None,hide=True)
        self.add_input( name = "Translate", interface = ISequence, value=None,hide=True)
        self.add_input( name = "Origin", interface = ISequence, value=None,hide=True)
        self.add_input( name = "DressingData",hide=True)
        self.add_output(name = "plantframe")

    def __call__(self, inputs):
        
        kwds={}

	# input_desc contains a list of dictionaries for 
	# each input port of the node
	for desc in self.input_desc:
	    key = desc['name']
	    x = self.get_input(key)
	    if x is not None:
		kwds[key] = x

	g = kwds.get('MTG',None)

        g = set_mtg(g)
        if not g:
            return (None,)

	scale = kwds.get('Scale',None)

	vtx = kwds.get('Vertex',None)
	del kwds['Vertex']
	if 'MTG' in kwds: del kwds['MTG']

	"""
        max_scale= max_mtg_scale(g)
        if scale > max_scale:
            scale = max_scale
        """

        try:
            pf = PlantFrame(vtx, **kwds)
        except Exception, e:
            print e
            pf=None

        return (pf,)

#//////////////////////////////////////////////////////////////////////////////

def py_dressingdata(g,filename):
    g =set_mtg(g)
    if not g:
        return

    if filename:
        try:
            d = DressingData(filename)
        except Exception, e:
            print e
            d = None
        return (d,)

#//////////////////////////////////////////////////////////////////////////////
        
class py_virtualpatterns( Node ):
    """\
Plot(aml object) -> Plot the object
Input:
  aml object
  
    """
    
    def __init__(self):
    
        Node.__init__(self)

        self.add_input( name = "patterntype", interface = IStr) 

        self.add_input( name = "Class", interface = IInt, value= 0,hide=True)
        self.add_input( name = "WhorlSize", interface = IInt, value= 0,hide=True)
        self.add_input( name = "PatternNumber", interface = IFloat, value=None)
        self.add_input( name = "Color", interface = IFloat, value=None,hide=True)
        self.add_input( name = "TopDiameter", interface = IFunction,hide=True)
        self.add_input( name = "Length", interface = IFunction,hide=True)
        self.add_input( name = "BottomDiameter", interface = IStr,hide=True)
        self.add_input( name = "Alpha", interface = IFunction,hide=True)
        self.add_input( name = "beta", interface = IFunction,hide=True)
        self.add_input( name = "gamma", interface = IFunction,hide=True)
        self.add_input( name = "Phyllotaxy", interface = IFunction,hide=True)
        self.add_input( name = "Azimuth", interface = IFunction,hide=True)
        self.add_input( name = "AA", interface = IFunction,hide=True)
        self.add_input( name = "BB", interface = IFunction,hide=True)
        self.add_input( name = "CC", interface = IFunction,hide=True)
        self.add_input( name = "XX", interface = IFunction,hide=True)
        self.add_input( name = "YY", interface = IFunction,hide=True)
        self.add_input( name = "ZZ", interface = IFunction,hide=True)

    def __call__(self, inputs):
        
        kwds={}

	# input_desc contains a list of dictionaries for 
	# each input port of the node
	for desc in self.input_desc:
	    key = desc['name']
	    x = self.get_input(key)
	    if x is not None:
		kwds[key] = x

	g = kwds.get('patterntype',None)

        g = set_mtg(g)
        if not g:
            return (None,)

	scale = kwds.get('Scale',None)

	vtx = kwds.get('Vertex',None)
	del kwds['Vertex']
	if 'MTG' in kwds: del kwds['MTG']

	"""
        max_scale= max_mtg_scale(g)
        if scale > max_scale:
            scale = max_scale
        """

        try:
            pf = PlantFrame(vtx, **kwds)
        except Exception, e:
            print e
            pf=None

        return (pf,)


#//////////////////////////////////////////////////////////////////////////////

class py_PlotPlantFrame( Node ):
    """\
Plot(aml object) -> Plot the object
Input:
  aml object
  
    """
    
    def __init__(self):
    
        Node.__init__(self)

        self.add_input( name = "obj", interface = None) 
        self.add_input( name = "Simplification", interface = IInt,value=None,hide=True) 
        self.add_input( name = "Show", interface = IFunction,hide=True) 
        self.add_input( name = "Display", interface = IEnumStr(['SHOW','HIDE']), value = 'SHOW',hide=True) 
        self.add_input( name = "Color", interface = IFunction,hide=True) 
        self.add_input( name = "ColorRGB", interface = IFunction,hide=True) 
        self.add_input( name = "Appearance", interface = IFunction,hide=True) 
        self.add_input( name = "Geometry", interface = IFunction,hide=True) 
        self.add_input( name = "DressindData",hide=True) 
        self.add_input( name = "Symbols", interface = IFunction,hide=True) 
        self.add_input( name = "VirtualFruits",hide=True) 
        self.add_input( name = "VirtualFlowers",hide=True) 
        self.add_input( name = "VirtualLeaves",hide=True) 
        self.add_input( name = "Interpol", interface = IFunction,hide=True) 
        self.add_input( name = "LineFile", interface = IFileStr,value=None,hide=True) 
        self.add_input( name = "MaxThreshold", interface = IFloat,value=None,hide=True) 
        self.add_input( name = "MinThreshold", interface = IFloat,value=None,hide=True) 
        self.add_input( name = "MediumThreshold", interface = IFloat,value=None,hide=True) 

        self.add_output( name = "Linetree") 

    def __call__(self, inputs):
        kwds={}
        # input_desc contains a list of dictionaries for 
        # each input port of the node
        for desc in self.input_desc:
            key = desc['name']
            x = self.get_input(key)
            if x is not None:  # selects the input arguments
                kwds[key] = x
        obj = kwds.get('obj',None)
        del kwds['obj']
        
        if obj:
            return Plot(obj, **kwds)

#//////////////////////////////////////////////////////////////////////////////
        
class py_PlotLineTree( Node ):
    """\
Plot(aml object) -> Plot the object
Input:
  aml object
  
    """
    
    def __init__(self):
    
        Node.__init__(self)

        self.add_input( name = "obj", interface = None) 
        self.add_input( name = "Color", interface = IFunction,hide=True) 
        self.add_input( name = "Geometry", interface = IFunction,hide=True) 
        self.add_input( name = "Symbol", interface = IFunction,hide=True) 
        self.add_input( name = "Appearance", interface = IFunction,hide=True) 
        self.add_input( name = "Show", interface = IFunction,hide=True) 
        self.add_input( name = "ShowMacro", interface = IFunction,hide=True) 
        self.add_input( name = "Display", interface = IEnumStr(['All','MicroOnly', 'MacroOnly','HIDE']), value = 'All') 
        self.add_output( name = "linetree") 

    def __call__(self, inputs):
        kwds={}
        
        # input_desc contains a list of dictionaries for 
        # each input port of the node
        for desc in self.input_desc:
            key = desc['name']
            x = self.get_input(key)
            if x is not None:  # selects the input arguments
                kwds[key] = x
        obj = kwds.get('obj',None)
        del kwds['obj']
        
        if obj:
            return Plot(obj, **kwds)

#//////////////////////////////////////////////////////////////////////////////

from openalea.plantgl.all import Scene

def py_Linetree2Scene(lt,scale = 'Micro'):
    id = Extract(lt,SceneId=scale)
    if id == 0:
        return None
    return Scene(Scene.pool().get(id))


#//////////////////////////////////////////////////////////////////////////////

def quotient_rep(lt,quotient,args):
    Plot(lt,Quotient=quotient,**args)
    ms_scene = py_Linetree2Scene(lt,'Macro')
    ms_graph = Extract(lt,Data='QuotientedGraph')
    return (ms_scene,ms_graph)    

class py_Quotient( Node ):
    """\
Quotient(linetree) -> Quotient the linetree
Input:
  linetree
  
    """
    
    def __init__(self):
    
        Node.__init__(self)

        self.add_input( name = "obj", interface = None) 
        self.add_input( name = "Quotient", interface = IFunction, value = None) 
        self.add_input( name = "Geometry", interface = IFunction, value = None ,hide = True) 
        self.add_input( name = "Appearance", interface = IFunction, value = None ,hide = True) 
        self.add_input( name = "Consider", interface = IFunction, value = None ,hide = True) 

        self.add_output( name = "Scene") 
        self.add_output( name = "Graph") 

    def __call__(self, inputs):
        obj = self.get_input("obj")
        quotient= self.get_input("Quotient")
        args = {'Display':'HIDE'}
        geometry= self.get_input("Geometry")
        if geometry:
            args['QuotientGeometry'] = geometry
        app= self.get_input("Appearance")
        if app:
            args['QuotientAppearance'] = app
        consider= self.get_input("Consider")
        if consider:
            args['QuotientConsider'] = consider
        if obj:
            if quotient:
                return quotient_rep(obj,quotient,args)
            else:
                return (lambda x : quotient_rep(obj,x,args),None)
        else:
            return (lambda x : quotient_rep(x,quotient,args),None)
    
#//////////////////////////////////////////////////////////////////////////////
class py_Compress( Node ):
    """\
Compress(linetree) -> Compress a linetree
Input:
  linetree
  
    """
    
    def __init__(self):
    
        Node.__init__(self)

        self.add_input( name = "obj", interface = None) 
        self.add_input( name = "rate", interface = IFloat, value = 0) 
        self.add_input( name = "sort", interface = IEnumStr(['DECREASINGSIZE','INCREASINGSIZE', 'DECREASINGORDER','INCREASINGORDER','NONE']),value='DECREASINGSIZE',hide=True) 
        self.add_output( name = "scene") 
    def __call__(self,inputs):
        obj = self.get_input("obj")
        rate = self.get_input("rate")
        sort = self.get_input("sort")
        Plot(obj,Compress=rate,Display='Hide',Sort=sort)
        return py_Linetree2Scene(obj,'Macro')
    

#//////////////////////////////////////////////////////////////////////////////

