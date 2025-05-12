import importlib.metadata

__version__ =  importlib.metadata.version("openalea.mtg")

numbers = __version__.split(".")

try:
    major, minor, post = numbers[0], numbers[1], numbers[2]
    patch = '.'.join(numbers[3:])
except IndexError:
    major, minor, post = '2', '4', '0'
    patch = '0'
