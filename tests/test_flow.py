""" file: test_flow.py
"""

from __future__ import print_function, division

import unittest
import numpy
import matplotlib.pyplot as plt

from maxr import flow
from maxr.flow.blink import blink, tick, tock


class TestBlink(unittest.TestCase):
    
    """ Tests for Blink functions
    """

    def setUp(self):
        self.times = numpy.linspace(0, 1, 1000)
        self.period = 0.1

    def test_ticktock(self):
        """ Check that tick and tock work ok
        """
        plt.plot(self.times, tick(self.times, self.period), label='tick')
        plt.plot(self.times, tock(self.times, self.period), label='tock')
        plt.legend(loc='best')

    def test_blink(self):
        """ Check that blink works ok
        """
        _flow = blink(gamma=1, period=0.5)
        uus, vus = _flow(0.25, 0.5, self.times)
        plt.plot(self.times, uus, label='u')
        plt.plot(self.times, vus, label='v')
        plt.legend(loc='best')
