# -*- python -*-
#
#       aml package: AMAPmod package interface for the amlPy module
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


"""
Wralea for OpenAlea.Mtg package.
"""

from openalea.core import *

__license__= "Cecill"
__revision__=" $Id: $"

__name__ = "openalea.mtg"
__version__ = '0.7.2'
__license__ = 'CECILL-C'
__authors__ = 'Christophe Pradal, Christophe Godin'
__institutes__ = 'CIRAD / INRIA'
__description__ = 'Multiscale Tree Graph data structure'
__url__ = 'http://openalea.gforge.inria.fr/doc/vplants/mtg/doc/html/contents.html'


__all__ = []

mtg = Factory( name= "MTG", 
              description= "MTG file creation", 
              category = "scene.MTG", 
              nodemodule = "py_mtg",
              nodeclass = "py_MTG",
              )

__all__.append('mtg')

vtxlist = Factory( name= "VtxList", 
              description= "Array of vertices contained in a MTG", 
              category = "scene.MTG", 
              nodemodule = "py_mtg",
              nodeclass = "py_VtxList",
              )

__all__.append('vtxlist')

feature = Factory( name= "Feature", 
              description= "Feature data stored on MTG vertices", 
              category = "scene.MTG", 
              nodemodule = "py_mtg",
              nodeclass = "py_Feature",
              )
__all__.append('feature')


vtxfunction = Factory( name= "VtxFunction", 
              description= "Common function on  MTG", 
              category = "scene.MTG", 
              nodemodule = "py_mtg",
              nodeclass = "VtxFunction",
              )
__all__.append('vtxfunction')


topofunction = Factory( name= "TopoFunction", 
              description= "Common function on  MTG", 
              category = "scene.MTG", 
              nodemodule = "py_mtg",
              nodeclass = "TopoFunction",
              )
__all__.append('topofunction')


complex = Factory( name= "Complex", 
              description= "Complex of a vertex.", 
              category = "scene.MTG", 
              nodemodule = "py_mtg",
              nodeclass = "py_Complex",
              )

__all__.append('complex')

components = Factory( name= "Components", 
              description= "Set of components of a vertex.", 
              category = "scene.MTG", 
              nodemodule = "py_mtg",
              nodeclass = "py_Components",
              )

__all__.append('components')

mtgroot = Factory( name= "MTGRoot", 
              description= "Returns the global root of a MTG.", 
              category = "scene.MTG", 
              nodemodule = "py_mtg",
              nodeclass = "py_MTGRoot",
              inputs=(dict(name='graph'),),
              outputs=(dict(name='Vtx',interface=IInt),),
              )

__all__.append('mtgroot')

axis = Factory( name= "Axis", 
              description= "Returns the sequence of vertices defining the axis of a given vertex.", 
              category = "scene.MTG", 
              nodemodule = "py_mtg",
              nodeclass = "py_Axis",
              )

__all__.append('axis')

#pf = Factory( name= "PlantFrame", 
#              description= "Constructs a geometric interpretation of a MTG.", 
#              category = "scene.MTG", 
#              nodemodule = "py_mtg",
#              nodeclass = "py_PlantFrame",
#              )
#__all__.append('pf')

#dressingdata = Factory( name= "DressingData", 
#             description= "Data and default geometric parameters used to compute the geometric interpretation of a MTG.", 
#             category = "scene.MTG", 
#             nodemodule = "py_mtg",
#             nodeclass = "py_dressingdata",
#             inputs=(dict(name="MTG"),dict(name="filename", interface=IFileStr)),
#             outputs=(dict(name="DressingData"),),
#             )
#__all__.append('dressingdata')
# 
# plot_pf = Factory( name= "PlotPlantFrame", 
#               description= "Plot PlantFrame objects.", 
#               category = "scene.MTG", 
#               nodemodule = "py_mtg",
#               nodeclass = "py_PlotPlantFrame",
#               )
# __all__.append('plot_pf')
# 
# plot_linetree = Factory( name= "PlotLineTree", 
#               description= "Plot Linetree objects.", 
#               category = "scene.MTG", 
#               nodemodule = "py_mtg",
#               nodeclass = "py_PlotLineTree",
#               )
# __all__.append('plot_linetree')
# 
# linetree2scene = Factory( name= "Linetree2Scene", 
#               description= "Extract scene from Linetree.", 
#               category = "scene.MTG", 
#               nodemodule = "py_mtg",
#               nodeclass = "py_Linetree2Scene",
#               inputs= ( dict( name = "linetree", interface=None ),
#                         dict( name = "scale", interface=IEnumStr(['Micro', 'Macro']), value = 'Micro'),
#                       ),
#               outputs=(dict(name="Scene", interface = None),
#                       ),
#               )
# __all__.append('linetree2scene')
# 
# quotient= Factory( name= "Quotient", 
#               description= "Quotient Linetree objects.", 
#               category = "scene.MTG", 
#               nodemodule = "py_mtg",
#               nodeclass = "py_Quotient",
#               )
# __all__.append('quotient')
# 
# compress = Factory( name= "Compress", 
#               description= "Create a compressed representation of Linetree objects.", 
#               category = "scene.MTG", 
#               nodemodule = "py_mtg",
#               nodeclass = "py_Compress",
#               )
# __all__.append('compress')
# 


