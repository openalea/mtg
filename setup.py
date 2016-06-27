#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments

from setuptools import setup, find_packages


short_descr = "Multiscale Tree Graph datastructure and interfaces"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def parse_requirements(fname):
    with open(fname, 'r') as f:
        txt = f.read()

    reqs = []
    for line in txt.splitlines():
        line = line.strip()
        if len(line) > 0 and not line.startswith("#"):
            reqs.append(line)

    return reqs

# find version number in src/openalea/mtg/version.py
version = {}
with open("src/openalea/mtg/version.py") as fp:
    exec(fp.read(), version)


setup_kwds = dict(
    name='openalea.mtg',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="Christophe Pradal, Thomas Cokelaer, ",
    author_email="christophe pradal __at__ cirad fr, thomas cokelaer __at__ inria fr, ",
    url='http://openalea.gforge.inria.fr',
    license='cecill-c',
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=parse_requirements("requirements.txt"),
    tests_require=parse_requirements("dvlpt_requirements.txt"),
    entry_points={},
    keywords='',
    test_suite='nose.collector',
)
# #}
# change setup_kwds below before the next pkglts tag

setup_kwds['share_dirs'] = {'share': 'share'},

setup_kwds['entry_points']["wralea"] = ["mtg = openalea.mtg_wralea"]
# setup_kwds['setup_requires'] = ['openalea.deploy']
setup_kwds['dependency_links'] = ['http://openalea.gforge.inria.fr/pi']
setup_kwds['pylint_packages'] = ['src/mtg', 'src/mtg/interface']

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
