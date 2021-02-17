# {# pkglts, base

from . import version

__version__ = version.__version__

# #}
from .mtg import *

try:
    from .plantframe import turtle, frame, plantframe, dresser

    DressingData = dresser.DressingData
    PlantFrame = plantframe.PlantFrame
except ImportError:
    DressingData = None
    PlantFrame = None
