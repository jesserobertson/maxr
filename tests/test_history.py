""" file: test_history.py
"""

from __future__ import print_function, division

import unittest
from collections import defaultdict

from numpy import array, sqrt, pi, linspace, sin, cos, arange, median
from scipy.special import fresnel

from maxr.integrator import history


def solution(time):
    """ Solution to sinusoidal history term
    """
    ssc, csc = fresnel(sqrt(2 * time / pi))
    return sqrt(2 * pi) * (
        csc * sin(time) - ssc * cos(time))


def evaluate_history_integral(func, times, order=1):
    """ Evaluate the history integral for a given driving function func
    """
    return array([0] + [
        history.integrator(func(times[:idx+1]), times[:idx+1],
                           order=order)
        for idx in range(1, len(times))])


class TestHistory(unittest.TestCase):

    r""" Tests to test integrator.history module

        Check accuracy of convergence. We use a sinusoidal forcing and plot the response
        $$
        \int_0^{t} \frac{\sin{(\tau)}}{\sqrt{t - \tau}}d\tau =
            \sqrt{2 \pi}\left[
                C{\left(\sqrt{\frac{2t}{\pi}}\right)}\sin{t}
                - S{\left(\sqrt{\frac{2t}{\pi}}\right)}\cos{t}
            \right]
        $$
        where $C$ is the Fresnel C (cos) integral, and $S$ is the Fresnel 
        $S$ (sin) integral. Note the solution in the paper is **WRONG**
    """

    tmin, tmax = 0, 30

    def test_integrator(self):
        """ Integrator should function ok
        """
        expected = -1.2492166377597749
        times = linspace(self.tmin, self.tmax, 1000)
        self.assertTrue(
            history.integrator(sin(times), times) - expected < 1e-5)

    def test_integrator_solution(self):
        """ Integrator should work over a range of values
        """
        nsteps = 1280
        order = 3
        for tmax in (10, 20, 50):
            times = linspace(self.tmin, tmax, nsteps)
            numeric = evaluate_history_integral(sin, times, order=order)
            exact = solution(times)
            self.assertTrue(
                median(numeric - exact) < 1e-5)

    def test_range_steps(self):
        """ Integrators should work for all orders at all steps
        """
        # Set up steps
        nstepstep = 25
        nsteps = arange(nstepstep, 500, nstepstep)

        # Calculate error
        error = defaultdict(list)
        for order in (1, 2, 3):
            for num in nsteps:
                times = linspace(self.tmin, self.tmax, num)
                err = evaluate_history_integral(sin, times, order=order) - solution(times)
                error[order].append(abs(err).max())
