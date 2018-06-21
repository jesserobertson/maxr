""" file: test_history_cython.py
"""

import unittest
import numpy as np

from maxr.integrator.history import coefficients
from maxr.ext.coefficients import IntegratorCoeffs

class BaseHarness(unittest.TestCase):

    "Base test class for history integrators"

    order = 1

    def test_equal_py_cy(self):
        "Python and Cython implementations should give the same coefficients"
        for length in range(1, 40):
            self.assertTrue(np.allclose(
                IntegratorCoeffs(length, self.order).as_array(),
                coefficients(length, self.order)))

class TestFirstOrderIntegrator(BaseHarness):
    order = 1

class TestSecondOrderIntegrator(BaseHarness):
    order = 2

class TestThirdOrderIntegrator(BaseHarness):
    order = 3

del BaseHarness

if __name__ == '__main__':
    unittest.main()
