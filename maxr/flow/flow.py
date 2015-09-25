""" file: flow.py (maxr.flow)
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   September 25, 2015

    description: Utilities for managing flow snapshots
"""

from __future__ import print_function, division

import h5py
from numpy import meshgrid, sqrt
from scipy.interpolate import RegularGridInterpolator
import matplotlib.pyplot as plt


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
        # Get info on axes from file
        times = self.data['t'][::plot_every]
        xxs, yys = self.grid()

        # Make figure
        nplots, ncol = len(times), 5
        fig, axes = plt.subplots(nplots // ncol, ncol)
        fig.set_size_inches(3 * ncol, 3 * (nplots // ncol))
        for idx, (time, axis) in enumerate(zip(times, axes.ravel())):
            uus, vvs = self.snapshot(idx * plot_every)
            axis.quiver(xxs, yys, uus, vvs,
                        pivot='mid', angles='xy',
                        scale_units='xy', scale=1.5)
            axis.set_axis_off()
            axis.set_aspect('equal')
            axis.set_title('t={0:0.2}'.format(time))

    def plot_fields(self, index):
        """ Plot fields for the flows
        """
        xps, yps = self.grid()
        gspec = plt.GridSpec(2, 4, width_ratios=(2, 1, 1, 1))
        plt.gcf().set_size_inches(10, 4)

        # Fields
        axis = plt.subplot(gspec[:, 0])
        axis.quiver(xps, yps,
                    self.data['u'][..., index],
                    self.data['v'][..., index])
        axis.contourf(xps, yps,
                      sqrt(self.data['u'][..., index] ** 2
                           + self.data['v'][..., index] ** 2),
                      cmap='coolwarm', alpha=0.3)
        axis.set_title('Velocity field (contours ~ abs(u))')
        axis.set_aspect('equal')
        axis.set_axis_off()

        for i in (0, 1):
            # Spatial derivatives
            dfunc = 'dv' if i else 'du'
            for j in (0, 1):
                dps = 'dy' if j else 'dx'
                axis = plt.subplot(gspec[i, j+1])
                key = dfunc + '/' + dps
                axis.contourf(xps, yps, self.data[key][..., index],
                              cmap='coolwarm')
                axis.set_title(key)
                axis.set_aspect('equal')
                axis.set_axis_off()

            # Time derivative
            axis = plt.subplot(gspec[i, 3])
            key = dfunc + '/dt'
            axis.contourf(xps, yps, self.data[key][..., index],
                          cmap='coolwarm')
            axis.set_title(key)
            axis.set_aspect('equal')
            axis.set_axis_off()
