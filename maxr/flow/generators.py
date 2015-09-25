""" file: generators.py (maxr.flow)
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   September 25, 2015

    description: Generators for managing flow snapshots
"""

from __future__ import print_function, division

import h5py
import numpy

def from_function(flow, filename=None, xgrid=None, ygrid=None, tgrid=None):
    """ Write a flow function to file
    """
    filename = filename or 'flow.hdf5'
    
    # Define the grid
    minx, maxx, nx = xgrid or (-2, 2, 40)
    miny, maxy, ny = ygrid or (-2, 2, 40)
    mint, maxt, nt = tgrid or (0, 2, 20)
    
    # Write to file
    with h5py.File(filename, 'w') as fhandle:
        # Create axes datasets
        fhandle['x'] = numpy.linspace(minx, maxx, nx)
        fhandle['y'] = numpy.linspace(miny, maxy, ny)
        fhandle['t'] = ts = numpy.linspace(mint, maxt, nt)

        # Create velocity datasets
        u = fhandle.require_dataset('u', shape=(nx, ny, nt), dtype=numpy.float32)
        v = fhandle.require_dataset('v', shape=(nx, ny, nt), dtype=numpy.float32)
        for comp in (u, v):
            for idx, ax in enumerate('xyt'):
                comp.dims[idx].label = ax

        # Write velocity datasets to file
        xs, ys = grid(fhandle)
        for idx, t in enumerate(ts):
            u, v = flow(xs, ys, t)
            fhandle['u'][:, :, idx] = u
            fhandle['v'][:, :, idx] = v
        
        # Create derivative datasets
        for idx, ax in enumerate('xyt'):
            for comp in 'uv':
                key = 'd{0}/d{1}'.format(comp, ax)
                fhandle.require_dataset(key, shape=(nx, ny, nt), dtype=numpy.float32)
                fhandle[key].dims[idx].label = ax
        
        # x and y derivatives
        dx = fhandle['x'][1] - fhandle['x'][0]
        dy = fhandle['y'][1] - fhandle['y'][0]
        for idx, t in enumerate(fhandle['t']):
            for comp in 'uv':
                key = 'd{0}/d'.format(comp)
                dcdx, dcdy = numpy.gradient(fhandle[comp][:, :, idx], 
                                            dx, dy, edge_order=2)
                fhandle[key + 'x'][:, :, idx] = dcdx
                fhandle[key + 'y'][:, :, idx] = dcdy
        
        # t derivative
        dt = numpy.diff(fhandle['t'])
        for comp in 'uv':
            key = 'd{0}/dt'.format(comp)
            fhandle[key][..., 0] = 0
            fhandle[key][..., 1:] = numpy.diff(fhandle[comp], axis=2) / dt
