""" file:   beta.pxd
    author: Jess Robertson, CSIRO Minerals
    date:   June 2018

    description: Cython description of first-order history integral terms
"""

from common cimport real_t, uint_t

cdef void beta(real_t *coeffs, uint_t n)