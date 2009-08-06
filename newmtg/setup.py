import os, sys
pj = os.path.join

from setuptools import setup, find_packages


# Package name
name = 'OpenAlea.Mtg'
namespace = 'openalea'
pkg_name = 'openalea.mtg'
version = '0.7.3' 
description = 'Multiscale Tree Graph datastructure and interfaces.' 

author = 'Christophe Pradal'
author_email = 'christophe pradal at cirad fr, christophe godin at sophia inria fr'

url = 'http://openalea.gforge.inria.fr'
license = 'Cecill-C' 

packages = [ namespace+"."+pkg for pkg in find_packages('src') if 'openalea' not in pkg]

setup(
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,

    namespace_packages=['openalea'],
    create_namespaces = True,
    zip_safe = False,

    packages = packages,
    package_dir={ pkg_name : pj('src','mtg'), 
                  'openalea.mtg_wralea' : 'src/mtg_wralea', 
                  '' : 'src' },

    entry_points = {
        "wralea": ["mtg = openalea.mtg_wralea",
                  ]
            },

    # Dependencies
    install_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
                     
    )


