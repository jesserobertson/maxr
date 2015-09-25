""" file: generators.py (maxr.flow)
    author: Jess Robertimeson
            CSIRO Mineral Resources
    date:   September 25, 2015

    description: Generators for managing flow snapshots
"""

from __future__ import print_function, division

import h5py
from numpy import linspace, float64, gradient, diff, meshgrid


def from_function(flow, filename=None, xgrid=None, ygrid=None, tgrid=None):
    """ Write a flow function to file
    """
    filename = filename or 'flow.hdf5'

    # Define the grid
    xgrid = xgrid or (-2, 2, 40)
    ygrid = ygrid or (-2, 2, 40)
    tgrid = tgrid or (0, 2, 20)
    shape = xgrid[-1], ygrid[-1], tgrid[-1]

    # Write to file
    with h5py.File(filename, 'w') as fhandle:
        # Create axes datasets
        fhandle['x'] = linspace(*xgrid)
        fhandle['y'] = linspace(*ygrid)
        fhandle['t'] = times = linspace(*tgrid)

        # Create velocity datasets
        for comp in 'uv':
            fhandle.require_dataset(comp, shape=shape, dtype=float64)
            for idx, axis in enumerate('xyt'):
                fhandle[comp].dims[idx].label = axis

        # Write velocity datasets to file
        xxs, yys = meshgrid(fhandle['x'], fhandle['y'])
        for idx, time in enumerate(times):
            uus, vus = flow(xxs, yys, time)
            fhandle['u'][:, :, idx] = uus
            fhandle['v'][:, :, idx] = vus

        # Create derivative datasets
        for idx, axis in enumerate('xyt'):
            for comp in 'uv':
                key = 'd{0}/d{1}'.format(comp, axis)
                fhandle.require_dataset(key, shape=shape, dtype=float64)
                fhandle[key].dims[idx].label = axis

        # x and y derivatives
        ddx = fhandle['x'][1] - fhandle['x'][0]
        ddy = fhandle['y'][1] - fhandle['y'][0]
        for idx, time in enumerate(fhandle['time']):
            for comp in 'uv':
                key = 'd{0}/d'.format(comp)
                dcdx, dcdy = gradient(fhandle[comp][:, :, idx],
                                      ddx, ddy, edge_order=2)
                fhandle[key + 'x'][:, :, idx] = dcdx
                fhandle[key + 'y'][:, :, idx] = dcdy

        # time derivative
        ddt = diff(fhandle['time'])
        for comp in 'uv':
            key = 'd{0}/dt'.format(comp)
            fhandle[key][..., 0] = 0
            fhandle[key][..., 1:] = diff(fhandle[comp], axis=2) / ddt
