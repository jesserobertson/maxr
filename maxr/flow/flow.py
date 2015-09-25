""" file: flow.py (maxr.flow)
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   September 25, 2015

    description: Utilities for managing flow snapshots
"""

class Flow(object):
    
    def __init__(self, filename):
        self.data = h5py.File(filename)
    
    def close(self):
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
        return numpy.meshgrid(self.data['x'], self.data['y'])
    
    def plot_snapshots(self, plot_every=1):
        """ Plot the snapshots
        """
        # Get info on axes from file
        ts = self.data['t'][::plot_every]
        x, y = self.grid()

        # Make figure
        nplots, ncol = len(ts), 5
        fig, axes = plt.subplots(nplots // ncol, ncol)
        fig.set_size_inches(3 * ncol, 3 * (nplots // ncol))
        for idx, (t, ax) in enumerate(zip(ts, axes.ravel())):
            u, v = self.snapshot(idx * plot_every)
            ax.quiver(x, y, u, v, 
                      pivot='mid', angles='xy', 
                      scale_units='xy', scale=1.5)
            ax.set_axis_off()
            ax.set_aspect('equal')
            ax.set_title('t={0:0.2}'.format(t))