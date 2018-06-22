""" file: common.pxd (maxr.ext)
    author: Jess Robertson, CSIRO Mineral Resources
    date:   March 2016

    description: Common inclusions for cython extensions
"""

from libc.math cimport sqrt

# Custom types
ctypedef double real_t
ctypedef unsigned int uint_t

# Define some compile-time constants
cdef real_t SQRT_2 = 1.4142135623730950488
cdef real_t SQRT_3 = 1.7320508075688772936
cdef real_t SQRT_5 = 2.2360679774997896964
cdef real_t SQRT_6 = 2.4494897427831780982

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