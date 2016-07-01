import warnings
warnings.warn("Call to deprecated module %s. Use openalea.mtg.plantframe.turtle instead." % __name__, category=DeprecationWarning)
from .plantframe.turtle import *
