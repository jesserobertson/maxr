""" file:   gamma.pyx
    author: Jess Robertson, CSIRO Minerals
    date:   June 2018

    description: Cython implementation of third-order history integral terms
"""

from common cimport pow_3_2, pow_5_2, pow_7_2, uint_t, real_t
from alpha cimport alpha
from beta cimport beta

from libc.math cimport sqrt

# Define some compile-time constants
cdef real_t SQRT_2 = 1.4142135623730950488
cdef real_t SQRT_3 = 1.7320508075688772936
cdef real_t SQRT_5 = 2.2360679774997896964
cdef real_t SQRT_6 = 2.4494897427831780982

cdef void gamma(real_t *coeffs, uint_t n):
    "Third-order integration coefficients for history term"
    cdef uint_t i

    if n > 6:
        # Left boundary
        coeffs[0] = 244/315. * SQRT_2
        coeffs[1] = 362/105. * SQRT_3 - 976/315. * SQRT_2
        coeffs[2] = 5584/315. - 1448/105. * SQRT_3 + 488/105. * SQRT_2
        coeffs[3] = 1130/63. * SQRT_5 - 22336/315. + 724/35. * SQRT_3 \
                   - 976/315. * SQRT_2

        # Middle
        for i in range(4, n-3):
            coeffs[i] = (
                16/105. * (pow_7_2(i+2) + pow_7_2(i-2) - 4 * pow_7_2(i+1)
                    - 4 * pow_7_2(i-1) + 6 * pow_7_2(i))
                + 2/9. * (4 * pow_3_2(i+1) + 4 * pow_3_2(i-1) - pow_3_2(i+2)
                    - pow_3_2(i-2) - 6 * pow_3_2(i))
            )

        # Right boundary
        coeffs[n-3] = (
            16/105. * (pow_7_2(n) - 4 * pow_7_2(n-2) + 6 * pow_7_2(n-3)
                - 4 * pow_7_2(n-4) + pow_7_2(n-5)) - 8/15. * pow_5_2(n)
            + 4/9. * pow_3_2(n) + 8/9. * pow_3_2(n-2) - 4/3. * pow_3_2(n-3)
            + 8/9. * pow_3_2(n-4) - 2/9. * pow_3_2(n-5)
        )
        coeffs[n-2] = (
            16/105. * (pow_7_2(n-4) - 4 * pow_7_2(n-3) + 6 * pow_7_2(n-2)
                - 3 * pow_7_2(n)) + 32/15. * pow_5_2(n) - 2 * pow_3_2(n)
            - 4/3. * pow_3_2(n-2) + 8/9. * pow_3_2(n-3) - 2/9. * pow_3_2(n-4)
        )
        coeffs[n-1] = (
            16/105. * (3 * pow_7_2(n) - 4 * pow_7_2(n-2) + pow_7_2(n-3))
            - 8/3. * pow_5_2(n) + 4 * pow_3_2(n) + 8/9. * pow_3_2(n-2)
            - 2/9. * pow_3_2(n-3)
        )
        coeffs[n] = (
            16/105. * (pow_7_2(n-2) - pow_7_2(n)) + 16/15. * pow_5_2(n)
            - 22/9. * pow_3_2(n) - 2/9. * pow_3_2(n-2) + 2 * sqrt(n)
        )

    # First few have to be handled specially
    elif n == 1:
        alpha(coeffs, 1)

    elif n == 2:
        beta(coeffs, 2)

    elif n == 3:
        coeffs[0] = 68/105. * SQRT_3
        coeffs[1] = 6/7. * SQRT_3
        coeffs[2] = 12/35. * SQRT_3
        coeffs[3] = 16/105. * SQRT_3

    elif n == 4:
        coeffs[0] = 244/315. * SQRT_2
        coeffs[1] = 1888/315. - 976/315. * SQRT_2
        coeffs[2] = -656/105. + 488/105. * SQRT_2
        coeffs[3] = 544/105. - 976/315. * SQRT_2
        coeffs[4] = -292/315. + 244/315. * SQRT_2

    elif n == 5:
        coeffs[0] = 244/315. * SQRT_2
        coeffs[1] = 362/105. * SQRT_3 - 976/315. * SQRT_2
        coeffs[2] = 500/63. * SQRT_5 - 1448/105. * SQRT_3 + 488/105. * SQRT_2
        coeffs[3] = -290/21. * SQRT_5 + 724/35. * SQRT_3 - 976/315. * SQRT_2
        coeffs[4] = 220/21. * SQRT_5 - 1448/105. * SQRT_3 + 244/315. * SQRT_2
        coeffs[5] = -164/63. * SQRT_5 + 362/105. * SQRT_3

    elif n == 6:
        coeffs[0] = 244/315. * SQRT_2
        coeffs[1] = 362/105. * SQRT_3 - 976/315. * SQRT_2
        coeffs[2] = 5584/315. - 1448/105. * SQRT_3 + 488/105. * SQRT_2
        coeffs[3] = 344/21. * SQRT_6 - 22336/315. + 724/35. * SQRT_3 \
                    - 976/315. * SQRT_2
        coeffs[4] = -1188/35. * SQRT_6 + 11168/105. - 1448/105. * SQRT_3 \
                    + 244/315. * SQRT_2
        coeffs[5] = 936/35. * SQRT_6 - 22336/315. + 362/105. * SQRT_3
        coeffs[6] = -754/105. * SQRT_6 + 5584/315.
