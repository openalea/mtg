import os,sys

# read sphinx conf.py file
try:
    from openalea.misc.sphinx_configuration import *
except:
    raise IOError('openalea.misc.sphinx_configuration file not found. You must install OpenAlea to generate the doc or create your own conf.py using sphinx_quickstart.')
from openalea.misc.sphinx_tools import sphinx_check_version, read_metainfo
sphinx_check_version()
# must update some fields with the package information
version, authors, release, project = read_metainfo('../metainfo.ini')
# and extra by-product fields
latex_documents = [('contents', 'main.tex', project + ' documentation', authors, 'manual')]


html_static_path = ['_static', os.path.join(os.environ['OPENALEA'], 'doc', '_static')]
html_style = 'openalea.css'


