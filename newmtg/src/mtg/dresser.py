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
    >>> g=MTG('a_MTG')
    >>> d = DressingData('file')
    >>> pf = PlantFrame(1, Scale=3, DressingData=d)
    >>> Plot(pf)

'''

from math import pi


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
        
        # TODO: finish all the possible args.
        # Refactor on smaller elements build separetly:
            # - geometric properties by organs (leaves, flower, fruits.
            # - geometric parameters for the plant
            # - phyllotaxy, position between plants, ...


def dressing_data(f):
    """ Parse a dressing data file and return a Dressing Data object.
    """
    pass
