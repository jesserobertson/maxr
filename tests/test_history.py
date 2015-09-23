""" file: test_history.py
"""

from __future__ import print_function, division

import unittest
import numpy
from scipy.special import fresnel
from collections import defaultdict

from maxr.integrator import history


def solution(t):
    """ Solution to sinusoidal history term
    """
    ssc, csc = fresnel(numpy.sqrt(2 * t / numpy.pi)) 
    return numpy.sqrt(2 * numpy.pi) * (
        csc * numpy.sin(t) - ssc * numpy.cos(t))


def evaluate_history_integral(f, ts, order=1):
    """ Evaluate the history integral for a given driving function f
    """
    return numpy.array([0] + [
        history.integrator(f(ts[:idx+1]), ts[:idx+1], order=order)
        for idx in range(1, len(ts))])


class TestHistory(unittest.TestCase):
    
    """ Tests to test integrator.history module

        Check accuracy of convergence. We use a sinusoidal forcing and plot the response
        $$ 
        \int_0^{t} \frac{\sin{(\tau)}}{\sqrt{t - \tau}}d\tau = \sqrt{2 \pi}\left[C{\left(\sqrt{\frac{2t}{\pi}}\right)}\sin{t} - S{\left(\sqrt{\frac{2t}{\pi}}\right)}\cos{t}\right]
        $$
        where $C$ is the Fresnel C (cos) integral, and $S$ is the Fresnel $S$ (sin) integral. Note the solution in the paper is **WRONG**
    """

    tmin, tmax = 0, 30
    
    def test_integrator(self):
        """ Integrator should function ok
        """
        expected = -1.2492166377597749
        ts = numpy.linspace(self.tmin, self.tmax, 1000)
        self.assertTrue(
            history.integrator(numpy.sin(ts), ts) - expected < 1e-5)

    def test_integrator_solution(self):
        """ Integrator should work over a range of values
        """
        nsteps = 1280
        order = 3
        for tmax in (10, 20, 50):
            ts = numpy.linspace(self.tmin, tmax, nsteps)
            numeric = evaluate_history_integral(numpy.sin, ts, order=order)
            exact = solution(ts)
            self.assertTrue(
                numpy.median(numeric - exact) < 1e-5)

    def test_range_steps(self):
        """ Integrators should work for all orders at all steps
        """
        # Set up steps
        nstepstep = 25
        nsteps = numpy.arange(nstepstep, 500, nstepstep)
        spacing = 10 / (nsteps - 1)

        # Calculate error
        error = defaultdict(list)
        for order in (1, 2, 3):
            for N in nsteps:
                ts = numpy.linspace(self.tmin, self.tmax, N)
                err = evaluate_history_integral(numpy.sin, ts, order=order) - solution(ts)
                error[order].append(abs(err).max())