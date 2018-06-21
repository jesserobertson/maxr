""" file:   gamma.pxd
    author: Jess Robertson, CSIRO Minerals
    date:   June 2018

    description: Cython description of third-order history integral terms
"""

from common cimport real_t
from common cimport uint_t

cdef void gamma(real_t *coeffs, uint_t n)