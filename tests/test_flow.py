""" file: test_flow.py
"""

from __future__ import print_function, division

import unittest
import numpy
import matplotlib.pyplot as plt
import os

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


class TestFlow(unittest.TestCase):

    """ Tests for Flow class
    """

    def setUp(self):
        self.fname = 'blink_test.hdf5'
        flow.from_function(blink(gamma=1, period=0.5), self.fname)
        self.flow = flow.Flow(self.fname)

    def tearDown(self):
        if os.path.exists(self.fname):
            os.remove(self.fname)

    def test_makefile(self):
        "Flow file should be created"
        self.assertTrue(os.path.exists(self.fname))

    def test_readifle(self):
        "Flow variables should be accessible"
        for key in 'tuvxy':
            self.assertTrue(self.flow.data[key] is not None)

    def test_interp(self):
        "Flow interpolations should be accessible"
        for key in ('u', 'v', 'du/dx', 'dv/dy', 'du/dt'):
            self.assertTrue(self.flow(key) is not None)

    def test_flow_info(self):
        "Flow info should be accessible"
        self.flow.info()

    def test_plot_data(self):
        "Flow data should be accessible to plot"
        xps, yps = self.flow.grid()
        _, axes = plt.subplots(2, 3)
        for iidx in (0, 1):
            dfunc = 'dv' if iidx else 'du'
            for jidx in (0, 1):
                dps = 'dy' if jidx else 'dx'
                axis = axes[iidx, jidx]
                key = dfunc + '/' + dps
                axis.contourf(xps, yps, self.flow.data[key][..., 5])
                axis.set_aspect('equal')
                axis.set_axis_off()
                axis.set_title(key)

            axis = axes[iidx, 2]
            key = dfunc + '/dt'
            axis.contourf(xps, yps, self.flow.data[key][..., 5])
            axis.set_axis_off()
            axis.set_title(key)

    def test_snapshots(self):
        "Plotting snapshots should work ok"
        self.flow.plot_snapshots(plot_every=1)
