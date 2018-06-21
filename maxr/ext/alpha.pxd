""" file:   alpha.pyd
    author: Jess Robertson, CSIRO Minerals
    date:   June 2018

    description: Cython description of first-order history integral terms
"""

from common cimport real_t, uint_t

cdef void alpha(real_t *coeffs, uint_t n)