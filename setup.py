# -*- coding: utf-8 -*-
__revision__ = "$Id$"

import os, sys
pj = os.path.join
from setuptools import setup, find_packages
from openalea.deploy.metainfo import read_metainfo


metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))


packages = [ namespace+"."+pkg for pkg in find_packages('src') if 'openalea' not in pkg]

setup(
    name=name,
    version=version,
    description=description,
    author=authors,
    author_email=authors_email,
    url=url,
    license=license,

    namespace_packages=['openalea'],
    create_namespaces = True,
    zip_safe = False,

    packages = packages,
    package_dir={ pkg_name : pj('src','mtg'), 
                  'openalea.mtg_wralea' : 'src/mtg_wralea', 
                  '' : 'src' },

    share_dirs = {'share':'share'},

    entry_points = {
        "wralea": ["mtg = openalea.mtg_wralea",
                  ]
            },

    # Dependencies
    setup_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
    pylint_packages = ['src/mtg', 'src/mtg/interface']
    )


