import importlib.metadata

__version__ =  importlib.metadata.version("openalea.mtg")

major, minor, post = __version__.split(".")
