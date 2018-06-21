""" file:   alpha.pyx
    author: Jess Robertson, CSIRO Minerals
    date:   June 2018

    description: Cython implementation of first-order history integral terms
"""

from common cimport pow_3_2, uint_t, real_t
from libc.math import sqrt

cdef void alpha(real_t *coeffs, uint_t n):
    "First-order integration coefficients for history term"
    cdef uint_t i

    # Left, then middle, then right boundary
    coeffs[0] = 4/3.
    for i in range(1, n):
        coeffs[i] = 4/3. * (pow_3_2(i-1) + pow_3_2(i+1) - 2 * pow_3_2(i))
    coeffs[n] = 4/3. * (pow_3_2(n-1) - pow_3_2(n) + 6/4. * sqrt(n))