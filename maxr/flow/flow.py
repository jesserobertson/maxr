""" file: flow.py (maxr.flow)
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   September 25, 2015

    description: Utilities for managing flow snapshots
"""

from __future__ import print_function, division

import h5py
from numpy import meshgrid
from scipy.interpolate import RegularGridInterpolator


class Flow(object):

    """ Manager for gridded flow data
    """

    def __init__(self, filename):
        self.data = h5py.File(filename)

    def close(self):
        """ Close files gracefully
        """
        self.data.close()

    def __call__(self, key):
        """ Returns an interpolation for the given value for the snapshot at idx
        """
        return RegularGridInterpolator(
            points=(self.data['x'], self.data['y'], self.data['t']),
            values=self.data[key])

    def info(self):
        """ Print some info about the keys defined here
        """
        for key in self.data.keys():
            try:
                print(key, self.data[key].shape)
            except AttributeError:
                # We have a group
                group = self.data[key]
                for key2 in group.keys():
                    print(key + '/' + key2, group[key2].shape)

    def snapshot(self, idx):
        """ Return a velocity field snapshot
        """
        return self.data['u'][:, :, idx], self.data['v'][:, :, idx]

    def grid(self):
        """ Return the spatial sampling grid
        """
        return meshgrid(self.data['x'], self.data['y'])

    def plot_snapshots(self, plot_every=1):
        """ Plot the snapshots
        """
        from matplotlib.pyplot import subplots
        # Get info on axes from file
        times = self.data['t'][::plot_every]
        xxs, yys = self.grid()

        # Make figure
        nplots, ncol = len(times), 5
        fig, axes = subplots(nplots // ncol, ncol)
        fig.set_size_inches(3 * ncol, 3 * (nplots // ncol))
        for idx, (time, axis) in enumerate(zip(times, axes.ravel())):
            uus, vvs = self.snapshot(idx * plot_every)
            axis.quiver(xxs, yys, uus, vvs,
                        pivot='mid', angles='xy',
                        scale_units='xy', scale=1.5)
            axis.set_axis_off()
            axis.set_aspect('equal')
            axis.set_title('t={0:0.2}'.format(time))
