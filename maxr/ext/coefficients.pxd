""" file:   coefficients.pxd
    author: Jess Robertson, CSIRO Minerals
    date:   June 2018

    description: Cython definition of history integral terms
"""

cimport common
from common cimport uint_t, real_t

cdef class IntegratorCoeffs:

    cdef:
        public uint_t n, order
        real_t *_coeffs