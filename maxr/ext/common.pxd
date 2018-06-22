""" file: common.pxd (maxr.ext)
    author: Jess Robertson, CSIRO Mineral Resources
    date:   March 2016

    description: Common inclusions for cython extensions
"""

from libc.math cimport sqrt

# Custom types
ctypedef double real_t
ctypedef unsigned int uint_t

# Power functions
cdef inline real_t pow_3_2(int n):
    "Evaulate n ** 3/2"
    return sqrt(n * n * n)

cdef inline real_t pow_5_2(int n):
    "Evaulate n ** 5/2"
    return sqrt(n * n * n * n * n)

cdef inline real_t pow_7_2(int n):
    "Evaulate n ** 7/2"
    return sqrt(n * n * n * n * n * n * n)

# This gets updated automatically by setup.py...
cdef int NUM_THREADS = 8