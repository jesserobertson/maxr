#!/usr/bin/env python
""" file: setup.py (maxr)
    author: Jess Robertson, CSIRO Earth Science and Resource Engineering
    date: Wednesday 1 May, 2013

    description: Setuptools installer script for maxr.
"""

# Check that our version of setuptools is new enough
# Resolving Cython and numpy dependencies via 'setup_requires' requires setuptools >= 18.0:
# https://github.com/pypa/setuptools/commit/a811c089a4362c0dc6c4a84b708953dde9ebdbf8
import sys
import textwrap
import pkg_resources
try:
    pkg_resources.require('setuptools >= 18.0')
except pkg_resources.ResolutionError:
    print(textwrap.dedent("""
        setuptools >= 18.0 is required, and the dependency cannot be
        automatically resolved with the version of setuptools that is
        currently installed (%s).

        You can upgrade setuptools:
        $ pip install -U setuptools
        """ % pkg_resources.get_distribution("setuptools").version),
        file=sys.stderr)
    sys.exit(1)

# Now we can do all our imports
from setuptools import setup, find_packages
from setup_extensions import get_extensions, get_cmdclass
import versioneer

## PACKAGE INFORMATION
# Get requirements from requirements.txt file
with open('requirements.txt', 'r') as src:
    REQUIREMENTS = [l.strip('\n') for l in src]

# Long description from readme
with open('README.md', 'r') as src:
    LONG_DESCRIPTION = src.read()

# Get extensions and update comandclass
VERSION = versioneer.get_version()
EXTENSIONS = get_extensions()
CMDCLASS = versioneer.get_cmdclass()
CMDCLASS.update(get_cmdclass())

# Actually configure setuptools
setup(
    name='maxr',
    version=VERSION,
    description='High-order integration for the Maxey-Riley equations',
    long_description=LONG_DESCRIPTION,
    author='Jess Robertson',
    author_email='jesse.robertson@csiro.au',
    url='ssh://git@bitbucket.csiro.au:7999/rose/hyper.git',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML'
    ],

    # Dependencies
    install_requires=REQUIREMENTS,
    setup_requires=[
        'pytest-runner',
        'Cython >= 0.20',
        'numpy'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],

    # Contents
    packages=find_packages(
        exclude=['tests', 'jupyter', 'resources']
    ),
    test_suite="tests",
    package_data={
        # 'hyper.scalars': ['*.json']
    },

    # Cython extensions & other stuff
    cmdclass=CMDCLASS,
    ext_modules=EXTENSIONS
)
