# -*- python -*-
#
#       OpenAlea.mtg
#
#       Copyright 2008-2009 INRIA - CIRAD - INRA  
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
''' Data and default geometric parameters used to compute 
the geometric interpretation of a MTG (i.e. PlantFrame)

:Description:
    The dressing data contains the default data that are used to define 
    the geometry of an MTG vertices (i.e. of a plant entities) 
    and to compute their geometric parameters when inference algorithms 
    cannot be applied. These data are basically constant values and may be 
    redefined in the dressing file. 
    If no dressing file is defined, default (hard-coded) values are used 
    (see `Dressing files`). The dressing file .drf , if it exists in the 
    current directory, is always used as a default dressing file.

    Objects of type DRESSING_DATA is used by primitive Plantframe. 
    It may also be used by primitive Plot when VIRTUAL_PATTERNs are plotted. 
    

:Examples:

    >>> g = MTG('a_MTG') #doctest: +SKIP
    >>> d = DressingData('file') #doctest: +SKIP
    >>> pf = PlantFrame(1, Scale=3, DressingData=d) #doctest: +SKIP
    >>> Plot(pf) #doctest: +SKIP

'''

from math import pi
import os
from openalea.plantgl.scenegraph import AmapSymbol

class DressingData(object):
    """ Data and default geometric parameters.

    The dressing data are the default data that are used to define 
    the geometric models associated with geometric entities 
    and to compute their geometric parameters when inference algorithms 
    cannot be applied. 
    These data are basically constant values and may be redefined by the user.

    """

    def __init__(self, **kwds):
        """ Build an object containing default parameters and geometric models
        associated to category.

        :Parameters:
            - Classes : dict between a Class name (key) and a 3D shape (value).
            - BranchPatterns: dict between a category and a 3D curve.
            
            - LeafClass : symbol name associated to the leaf component.
            - FlowerClass : symbol name associated to the flower component.
            - FruitClass : symbol name associated to the fruit component.
            
            - LengthUnit : Unit used to divide all the length data (default : 1)
            - DiameterUnit : Unit used to divide all the length data (default : 1)
            - AlphaUnit : Unit used to divide all the insertion angle (180/pi)
            - AzimuthUnit : Unit used to divide all the azimuth angle (180/pi)

            - DefaultEdge : Type of edge used to reconstruct a connected MTG (PLUS or LESS)

            - DefaultAlpha : Default insertion angle (value in degrees with respect to the horizontal plane).
            - DefaultTeta : Default first Euler angle
            - DefaultPhi : Default second Euler angle
            - DefaultPsi : Default third Euler angle

            - DefaultTrunkCategory : Default category for elements of the plant trunk. 
            - DefaultCategory : The default category of the other axes than the trunk is their (botanical) order starting at 0 on the trunk.

            - Alpha : Nature of the insertion angle (Absolute or Relative)
            - Phyllotaxy : Phyllotaxic angle (given in degrees) or in number of turns over number of leaves for this number of turns (default : 180)

            - MinLength: dict betwwen Class and default value for element of class `Class`.
            - MinTopDiameter: dict betwwen Class and default value for element of class `Class`.
            - MinBottomDiameter: dict betwwen Class and default value for element of class `Class`.

            - LeafLength = 1
            - LeafTopDiameter = 2
            - LeafBottomDiameter = 2
            - LeafAlpha = 0
            - LeafBeta = 0

            - FruitLength = 1
            - FruitTopDiameter = 1
            - FruitBottomDiameter = 1
            - FruitAlpha = 0
            - FruitBeta = 0

            - FlowerLength = 10
            - FlowerTopDiameter = 5
            - FlowerBottomDiameter = 5
            - FlowerAlpha = 180
            - FlowerBeta = 0

            - DefaultTrunkCategory = 0
            - DefaultDistance = 1000
            - NbPlantsPerLine = 6

            # Colors for interpolation

            - MediumThreshold
            - MinThreshold
            - MaxThreshold

        Defining only top and bottom radius rather than width and height imply 
        an axial or radial symmetry 
        which is often the case for plant (leaves, branches, fruit).
        """
 
        self.classes = kwds.get('Classes', {})
        self.branch_patterns = kwds.get('BranchPatterns', {})
        self.leaf_class = kwds.get('LeafClass')
        self.flower_class = kwds.get('FlowerClass')
        self.fruit_class = kwds.get('FruitClass')
        self.length_unit = kwds.get('LengthUnit',1)
        self.diameter_unit = kwds.get('DiameterUnit',1)
        self.azimuth_unit = kwds.get('AzimuthUnit', 180/pi)
        self.alpha_unit = kwds.get('AlphaUnit', 180/pi)

        self.default_edge = kwds.get('DefaultEdge')

        self.default_alpha= kwds.get('DefaultAlpha', 30)
        self.default_teta= kwds.get('DefaultTeta', 0)
        self.default_phi= kwds.get('DefaultPhi', 0)
        self.default_psi= kwds.get('DefaultPsi', 0)
        
        self.min_length = kwds.get('MinLength', {})
        self.min_topdia = kwds.get('MinTopDiameter', {})
        self.min_botdia = kwds.get('MinBottomDiameter', {})

        self.leaf_class= kwds.get('LeafClass', 'L')
        self.leaf_length = kwds.get('LeafLength', 50)
        self.leaf_topdia = kwds.get('LeafTopDiameter', 5)
        self.leaf_botdia = kwds.get('LeafBottomDiameter', 5)
        self.leaf_alpha = kwds.get('LeafAlpha', 30)
        self.leaf_beta= kwds.get('LeafBeta', 180)

        self.fruit_class= kwds.get('FruitClass', 'F')
        self.fruit_length = kwds.get('FruitLength', 50)
        self.fruit_topdia = kwds.get('FruitTopDiameter', 5)
        self.fruit_botdia = kwds.get('FruitBottomDiameter', 5)
        self.fruit_alpha = kwds.get('FruitAlpha', 30)
        self.fruit_beta= kwds.get('FruitBeta', 180)

        self.flower_class= kwds.get('FlowerClass', 'W')
        self.flower_length = kwds.get('FlowerLength', 50)
        self.flower_topdia = kwds.get('FlowerTopDiameter', 5)
        self.flower_botdia = kwds.get('FlowerBottomDiameter', 5)
        self.flower_alpha = kwds.get('FlowerAlpha', 30)
        self.flower_beta= kwds.get('FlowerBeta', 180)

        self.min_threshold = kwds.get('MinThreshold',(0,255,0))
        self.medium_threshold = kwds.get('MediumThreshold',(18,13,2))
        self.max_threshold = kwds.get('MinThreshold',(0,255,255))

        self.nb_whorl = kwds.get('Whorl', 2)
        
        # Symbols is a dict between a name and a geom object
        self.symbols = {}
        # TODO: finish all the possible args.
        # Refactor on smaller elements build separetly:
            # - geometric properties by organs (leaves, flower, fruits).
            # - geometric parameters for the plant
            # - phyllotaxy, position between plants, ...


def dressing_data_from_file(fn):
    f=open(fn)
    dresser = dressing_data(f)
    f.close()
    return dresser

def dressing_data(file):
    """ Parse a dressing data file and return a Dressing Data object.
    """
    dresser = DressingData()
    grammar = Reader(dresser)

    words = []
    line = 0

    for l in file:
        line+=1
        l = l.strip()
        if l.startswith('#') or not l:
            continue
        else: 
            status = grammar.parse(l, line)
    print '\n'.join(grammar.errors)
    return dresser

###############################################################
## Define the parser which is just a dict from keyword to a function 
class Reader(object):
    def __init__(self, dresser):
        self.dresser = dresser
        
        self.build_grammar()

        self.init()

    def init(self):
        self.errors = []
        self.smbpath = None

    def parse(self, l, line):
        """ Parse a line and update the dresser.

        Parse a line of a dressing file by calling the appropriate function
        and update the dresser object with the new values.

        TODO: Error management
        """
        self.line = line
        words = l.split()
        if words[0] in self.grammar:
            key = words[0]
            # process the line
            f = self.grammar[key]
            f(words)
        else:
            self._add_error(l, 'Unable to parse this line')

        return True

    def build_grammar(self):
        self.grammar = {}
        grammar = self.grammar

        grammar['SMBPath'] = self.smb_path
        grammar['SMBModel'] = self.smb_model

        grammar['Class'] = self.klass 
        grammar['BranchPattern'] = self.branch_pattern 
        grammar['LeafClass'] = self.leaf_klass 
        grammar['FlowerClass'] = self.flower_klass 
        grammar['FruitClass'] = self.fruit_klass 


        grammar['LengthUnit'] = self.length_unit
        grammar['DiameterUnit'] = self.diameter_unit
        grammar['AlphaUnit'] = self.alpha_unit
        grammar['AzimuthUnit'] = self.azimuth_unit

        grammar['DefaultEdge'] = self.default_edge

        grammar['DefaultAlpha'] = self.default_alpha
        grammar['DefaultTeta'] =  self.default_teta
        grammar['DefaultPhi'] =  self.default_phi
        grammar['DefaultPsi'] = self.default_psi 

        grammar['DefaultTrunkCategory'] =self.default_trunk_category
        grammar['DefaultCategory'] = self.default_category

        grammar['Alpha'] =self.alpha
        grammar['Phyllotaxy'] = self.phyllotaxy

        grammar['MinLength'] = self.min_length
        grammar['MinTopDiameter'] = self.min_top_diameter
        grammar['MinBottomDiameter'] = self.min_bottom_diameter


        grammar['LeafLength'] = self.leaf_length
        grammar['LeafTopDiameter'] = self.leaf_topdia
        grammar['LeafBottomDiameter'] = self.leaf_botdia
        grammar['LeafAlpha'] = self.leaf_alpha
        grammar['LeafBeta'] = self.leaf_beta

        grammar['FruitLength'] = self.fruit_length
        grammar['FruitTopDiameter'] = self.fruit_topdia
        grammar['FruitBottomDiameter'] = self.fruit_botdia
        grammar['FruitAlpha'] = self.fruit_alpha
        grammar['FruitBeta'] = self.fruit_beta

        grammar['FlowerLength'] = self.flower_length
        grammar['FlowerTopDiameter'] = self.flower_topdia
        grammar['FlowerBottomDiameter'] = self.flower_botdia
        grammar['FlowerAlpha'] = self.flower_alpha
        grammar['FlowerBeta'] = self.flower_beta

        grammar['DefaultTrunkCategory'] = self.def_trunk_cat
        grammar['DefaultDistance'] = self.def_dist
        grammar['NbPlantsPerLine'] = self.nbplants_line

        grammar['MediumThreshold'] = self.med_thres
        grammar['MinThreshold'] = self.min_thres
        grammar['MaxThreshold'] = self.max_thres

    def _add_error(self, l, note=''):
        msg = 'ERROR (%d): %s'%(self.line, ' '.join(l))
        if note:
            msg = '\n'.join([msg, ' --> %s'%note])
        self.errors.append(msg)

    def smb_path(self, l):
        "SMBPath = path"
        p = l[2]
        if os.path.exists(p):
            self.smbpath = p
        else:
            self._add_error(l, 'Invalid path')

    def smb_model(self, l):
        "SMBModel node = nentn105"
        if not self.smbpath:
            return
        name = l[1]
        file = l[3]+'.smb'
        absfile = os.path.join(self.smbpath, file)
        if os.path.exists(os.path.join(self.smbpath, file)):
            geom = AmapSymbol(absfile)
            if geom.isValid():
                self.dresser.symbols[name] = geom
        else:
            self._add_error(l, 'Impossible to locate symbol file')

        
    def klass (self, l):
        "Class B = node"
        class_name = l[1]
        smb_name = l[3]
        d = self.dresser
        if smb_name in d.symbols:
            d.classes[class_name] = smb_name
        else:
            self._add_error(l, '%s is not defined'%smb_name)

    def branch_pattern (self, l):
        "BranchPattern apple_forms = file.crv"
        self._add_error(l, 'BranchPattern is not yet implemented')

    def leaf_klass (self, l):
        "LeafClass = Z"
        name = l[2]
        d = self.dresser
        if name in d.symbols:
            d.leaf_class = name
        else:
            self._add_error(l, '%s is not defined'%name)
        
    def flower_klass(self, l):
        "FlowerClass = Z"
        name = l[2]
        d = self.dresser
        if name in d.symbols:
            d.flower_class = name
        else:
            self._add_error(l, '%s is not defined'%name)

    def fruit_klass (self, l):
        "FruitClass = Z"
        name = l[2]
        d = self.dresser
        if name in d.symbols:
            d.fruit_class = name
        else:
            self._add_error(l, '%s is not defined'%name)

    def length_unit(self, l):
        "LengthUnit = 1"
        unit = l[2]
        try:
            self.dresser.length_unit = float(unit)
        except:
            self._add_error(l, 'Bad unit format')
        

    def diameter_unit(self, l):
        "DiameterUnit = 1"
        unit = l[2]
        try:
            self.dresser.diameter_unit = float(unit)
        except:
            self._add_error(l, 'Bad unit format')

    def alpha_unit(self, l):
        "AlphaUnit = 1"
        unit = l[2]
        try:
            self.dresser.alpha_unit = float(unit)
        except:
            self._add_error(l, 'Bad unit format')

    def azimuth_unit(self, l):
        "AzimuthUnit = 1"
        unit = l[2]
        try:
            self.dresser.azimuth_unit = float(unit)
        except:
            self._add_error(l, 'Bad unit format')


    def default_edge(self, l):
        "DefaultEdge = PLUS | LESS"
        edge_type = l[2]
        if edge_type in ['PLUS', 'LESS']:
            self.default_edge = edge_type
        else:
            self._add_error(l, 'Bad edge format')

    def default_alpha(self, l):
        angle = l[2]
        try:
            self.dresser.default_alpha = float(angle)
        except:
            self._add_error(l, 'Bad angle format')

    def default_teta(self, l):
        angle = l[2]
        try:
            self.dresser.default_teta= float(angle)
        except:
            self._add_error(l, 'Bad angle format')

    def default_phi(self, l):
        angle = l[2]
        try:
            self.dresser.default_phi= float(angle)
        except:
            self._add_error(l, 'Bad angle format')

    def default_psi (self, l):
        angle = l[2]
        try:
            self.dresser.default_psi= float(angle)
        except:
            self._add_error(l, 'Bad angle format')


    def default_trunk_category(self, l):
        pass

    def default_category(self, l):
        pass


    def alpha(self, l):
        "Alpha = Absolute | Relative" 
        _alpha = l[2]
        if _alpha in ['Absolute', 'Relative']:
            self.dresser.alpha = _alpha
        else:
            self._add_error(l, 'Should be Absolute or Relative ')
        

    def phyllotaxy(self, l):
        angle = l[2]
        try:
            self.dresser.phyllotaxy= float(angle)
        except:
            self._add_error(l)
        

    def min_length(self, l):
        "MinLenght A = 10"
        name = l[1]
        value = l[3]
        self.dresser.min_length[name] = float(value)

    def min_top_diameter(self, l):
        "MinTopDiameter A = 10"
        name = l[1]
        value = l[3]
        self.dresser.min_topdia[name] = float(value)

    def min_bottom_diameter(self, l):
        "MinBottomDiameter A = 10"
        name = l[1]
        value = l[3]
        self.dresser.min_botdia[name] = float(value)

    def leaf_length(self, l):
        "LeafLength = 100"
        value = l[2]
        try:
            self.dresser.leaf_length= float(value)
        except:
            self._add_error(l, 'Bad format')

    def leaf_topdia(self, l):
        value = l[2]
        try:
            self.dresser.leaf_topdia= float(value)
        except:
            self._add_error(l, 'Bad format')

    def leaf_botdia(self, l):
        value = l[2]
        try:
            self.dresser.leaf_botdia= float(value)
        except:
            self._add_error(l, 'Bad format')

    def leaf_alpha(self, l):
        value = l[2]
        try:
            self.dresser.leaf_alpha= float(value)
        except:
            self._add_error(l, 'Bad format')

    def leaf_beta(self, l):
        value = l[2]
        try:
            self.dresser.leaf_beta= float(value)
        except:
            self._add_error(l, 'Bad format')

    def fruit_length(self, l):
        "LeafLength = 100"
        value = l[2]
        try:
            self.dresser.fruit_length= float(value)
        except:
            self._add_error(l, 'Bad format')

    def fruit_topdia(self, l):
        value = l[2]
        try:
            self.dresser.fruit_topdia= float(value)
        except:
            self._add_error(l, 'Bad format')

    def fruit_botdia(self, l):
        value = l[2]
        try:
            self.dresser.fruit_botdia= float(value)
        except:
            self._add_error(l, 'Bad format')

    def fruit_alpha(self, l):
        value = l[2]
        try:
            self.dresser.fruit_alpha= float(value)
        except:
            self._add_error(l, 'Bad format')

    def fruit_beta(self, l):
        value = l[2]
        try:
            self.dresser.fruit_beta= float(value)
        except:
            self._add_error(l, 'Bad format')

    def flower_length(self, l):
        "LeafLength = 100"
        value = l[2]
        try:
            self.dresser.flower_length= float(value)
        except:
            self._add_error(l, 'Bad format')

    def flower_topdia(self, l):
        value = l[2]
        try:
            self.dresser.flower_topdia= float(value)
        except:
            self._add_error(l, 'Bad format')

    def flower_botdia(self, l):
        value = l[2]
        try:
            self.dresser.flower_botdia= float(value)
        except:
            self._add_error(l, 'Bad format')

    def flower_alpha(self, l):
        value = l[2]
        try:
            self.dresser.flower_alpha= float(value)
        except:
            self._add_error(l, 'Bad format')

    def flower_beta(self, l):
        value = l[2]
        try:
            self.dresser.flower_beta= float(value)
        except:
            self._add_error(l, 'Bad format')

    def def_trunk_cat(self, l):
        pass

    def def_dist(self, l):
        pass

    def nbplants_line(self, l):
        pass


    def med_thres(self, l):
        pass

    def min_thres(self, l):
        pass

    def max_thres(self, l):
        pass



