""" file:   coefficients.pyx
    author: Jess Robertson, CSIRO Minerals
    date:   June 2018

    description: Cython implementation of history integral terms
"""

from libc.stdlib cimport malloc, free
from libc.math cimport sqrt
import numpy as np
cimport numpy as np

from common cimport uint_t, real_t
from alpha cimport alpha
from beta cimport beta
from gamma cimport gamma

# Wrapper class
cdef class IntegratorCoeffs:

    """
    Manages history coefficients for the particle integrator

    Parameters:
        n (uint_t) - the number of coefficients to return
        order (uint_t) - the order of the integrator
    """

    def __cinit__(self, uint_t n, uint_t order):
        "Constructor"
        self.n = n
        self.order = order
        self._coeffs = <real_t*> malloc((n+1) * sizeof(real_t))
        if self._coeffs == NULL:
            raise MemoryError()

        # Update coefficients
        if self.order == 1:
            alpha(self._coeffs, self.n)
        elif self.order == 2:
            beta(self._coeffs, self.n)
        elif self.order == 3:
            gamma(self._coeffs, self.n)

    def __getitem__(self, uint_t index):
        return self._coeffs[index]

    def __dealloc__(self):
        "Clean up memory on dealloc"
        if self._coeffs != NULL:
            free(self._coeffs)

    def as_array(self):
        "Return a copy of the coefficients as a numpy array"
        copy = np.empty(self.n + 1, dtype=np.double)
        cdef uint_t i
        for i in range(self.n + 1):
            copy[i] = self._coeffs[i]
        return copy




