""" file:   beta.pyx
    author: Jess Robertson, CSIRO Minerals
    date:   June 2018

    description: Cython implementation of second-order history integral terms
"""

from common cimport pow_3_2, pow_5_2, uint_t, real_t, SQRT_2, SQRT_3
from alpha cimport alpha

from libc.math import sqrt

cdef void beta(real_t *coeffs, uint_t n):
    "Second-order integration coefficients for history term"
    cdef uint_t i

    if n > 3:
        # Left boundary
        coeffs[0] = 4 / 5. * SQRT_2
        coeffs[1] = 14 / 5. * SQRT_3 - 12 / 5. * SQRT_2
        coeffs[2] = 176 / 15. - 42 / 5. * SQRT_3 + 12 / 5. * SQRT_2

        # Middle
        for i in range(3, n-1):
            coeffs[i] = 8/15. * (pow_5_2(i+2) - 3 * pow_5_2(i+1)
                                  + 3 * pow_5_2(i) - pow_5_2(i-1)) \
                          + 2/3. * (-pow_3_2(i+2) + 3 * pow_3_2(i+1)
                                   - 3 * pow_3_2(i) + pow_3_2(i-1))

        # Right boundary
        coeffs[n-1] = 8/15 * (-2 * pow_5_2(n) + 3 * pow_5_2(n-1) - pow_5_2(n-2)) \
                      + 2/3 * (4 * pow_3_2(n) - 3 * pow_3_2(n-1) + pow_3_2(n-2))
        coeffs[n] = 8/15. * (pow_5_2(n) - pow_5_2(n-1)) \
                    + 2/3. * (-3 * pow_3_2(n) + pow_3_2(n-1)) + 2 * sqrt(n)

    # First few have to be handled specially
    elif n == 1:
        alpha(coeffs, 1)

    elif n == 2:
        coeffs[0] = 12/15. * SQRT_2
        coeffs[1] = 16/15. * SQRT_2
        coeffs[2] = 2/15. * SQRT_2

    elif n == 3:
        coeffs[0] = 4/5. * SQRT_2
        coeffs[1] = 14/5. * SQRT_3 - 12/5. * SQRT_2
        coeffs[2] = -8/5. * SQRT_3 + 12/5. * SQRT_2
        coeffs[3] = 4/5. * SQRT_3  - 4/5. * SQRT_2
