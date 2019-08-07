#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments

from setuptools import setup, find_packages


short_descr = "Multiscale Tree Graph datastructure and interfaces"
readme = open('README.rst').read()
history = open('HISTORY.rst').read()


# find version number in src/openalea/mtg/version.py
version = {}
with open("src/openalea/mtg/version.py") as fp:
    exec(fp.read(), version)


setup_kwds = dict(
    name='openalea.mtg',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="Christophe Pradal",
    author_email="christophe pradal __at__ cirad fr",
    url='http://github.com/openalea/mtg',
    license='cecill-c',
    zip_safe=False,

    packages=find_packages('src'),
    namespace_packages=['openalea'],
    package_dir={'': 'src'},
    setup_requires=[
        "pytest-runner",
        ],
    install_requires=[
        ],
    tests_require=[
        "coverage",
        "mock",
        "pytest",
        "pytest-cov",
        "sphinx",
        ],
    entry_points={},
    keywords='',
    )
# #}
# change setup_kwds below before the next pkglts tag

# setup_kwds['share_dirs'] = {'share': 'share'}

setup_kwds['entry_points']["wralea"] = ["mtg = openalea.mtg_wralea"]
setup_kwds['setup_requires'] = ['openalea.deploy']
setup_kwds['dependency_links'] = ['http://openalea.gforge.inria.fr/pi']
setup_kwds['pylint_packages'] = ['src/mtg', 'src/mtg/interface']

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
