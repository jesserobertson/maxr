""" file:   setup_extensions.py
    author: Jess Robertson, CSIRO Mineral Resources
    date:   August 2017

    description: Options for different compilers to make hyper cross-platform
"""

from os import path, listdir
from logging import getLogger
from multiprocessing import cpu_count

import numpy

# Here we try to import Cython - if it's here then we can generate new c sources
# directly from the pyx files using their build_ext class.
# If not then we just use the default setuptools version
try:
    from Cython.Distutils import build_ext
    HAVE_CYTHON = True
except ImportError:
    from setuptools.command.build_ext import build_ext
    HAVE_CYTHON = False
from setuptools import Extension
from setuptools.command.sdist import sdist

LOGGER = getLogger()

# Where are our extensions located?
EXTENSIONS_MODULE = ['hyper', 'ext']
PATH_TO_EXTENSIONS = path.join(*(
    [path.abspath(path.dirname(__file__))]
    + EXTENSIONS_MODULE
))

def update_thread_count():
    """ Update the thread count for OpenMP extensions

        Uses one thread per core, with the estimate of the number of cores from
        multiprocessing.cpu_count.
    """
    LOGGER.info('Updating thread count for cython code to %d', cpu_count())
    num_threads = cpu_count()  # We're just going for 1 thread/CPU here
    fname = path.join(PATH_TO_EXTENSIONS, 'common.pxd')
    with open(fname, 'r') as src:
        content = src.readlines()  # this is short, just slurp it
    with open(fname, 'w') as sink:
        for line in content:
            if line.startswith('cdef int NUM_THREADS'):
                sink.write('cdef int NUM_THREADS = {0}'.format(num_threads))
            else:
                sink.write(line)

def get_extensions():
    """ Find our extensions to build.

        Also updates the thread count for OpenMP extensions to the number of CPUs
        availble on the current machine.

        Returns:
            a list of Extension objects to pass to setup
    """
    update_thread_count()

    # Get the extensions
    if HAVE_CYTHON:
        files = [f for f in listdir(PATH_TO_EXTENSIONS) if f.endswith('.pyx')]
    else:
        files = [f for f in listdir(PATH_TO_EXTENSIONS) if f.endswith('.c')]

    # Construct keyword arguments for all extensions
    kwargs = dict(
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
        include_dirs=[numpy.get_include(), PATH_TO_EXTENSIONS]
    )

    # Construct all the extension objects and return them
    extensions = []
    for fname in files:
        module_name = path.splitext(path.split(fname)[1])[0]
        extension_name = '.'.join(EXTENSIONS_MODULE + [module_name])
        source = path.join(PATH_TO_EXTENSIONS, fname)
        extensions.append(Extension(extension_name, sources=[source], **kwargs))
    return extensions

# Update source distribution - we always require Cython for this...
class cython_sdist(sdist):

    def run(self):
        # Make sure the compiled Cython files in the distribution are up-to-date
        from Cython.Build import cythonize
        update_thread_count()
        cythonize([path.join(PATH_TO_EXTENSIONS, f)
                   for f in listdir(PATH_TO_EXTENSIONS)
                   if f.endswith('.pyx')])
        super().run()

def get_cmdclass():
    """ Return a command class which builds cython extensions automatically
    """
    cmdclass = {
        'build_ext': build_ext,
        'sdist': cython_sdist
    }
    return cmdclass
