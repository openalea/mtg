# copied from core
# 'distribution(distribution_name).version' cause 'No package metadata was found for openalea.mtg'
# import importlib.metadata
#
# __version__ =  importlib.metadata.version("openalea.mtg")
#
# numbers = __version__.split(".")
#
# try:
#     major, minor, post = numbers[0], numbers[1], numbers[2]
#     patch = '.'.join(numbers[3:])
# except IndexError:
#     major, minor, post = '2', '4', '0'
#     patch = '0'

major, minor, post = '2', '4', '0'
patch = 'a1'
__version__ = '.'.join([major, minor, post, patch])