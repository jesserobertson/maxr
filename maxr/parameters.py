""" file: parameters.py
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   September 2015

    description: Parameter classes for maxr
"""

from __future__ import print_function, division

class Parameters(dict):

    """ Manages parameters for integration of the Maxey-Riley equations

        To see what parameters you can change, check out 
        `Parameters.allowed_keys. All keys can be set as attributes as well, 
        and most have short values (e.g. `Parameters.a` and 
        `Parameters.particle_radius` point to the same thing). Dimensionless
        values are automatically calculated, but can also be set if required.

        For default values, see `Parameters.default_parameters`.
    """

    default_parameters = dict(
        # Integration scheme properties
        timestep=1e-3,
        n_steps=1000,

        # Particle/fluid properties
        fluid_density=1,
        fluid_viscosity=1,
        particle_density=2,
        particle_radius=0.01,
        velocity_scale=1,
        time_scale=1
    )

    # Define symbols for quick reference
    equivalent = [
        ('dt', 'timestep'),
        ('N', 'n_steps'),
        ('R', 'density_parameter'),
        ('S', 'relaxation_parameter'),
        ('U', 'velocity_scale'),
        ('T', 'time_scale'),
        ('a', 'particle_radius'),
        ('rhof', 'fluid_density'),
        ('nuf', 'fluid_viscosity'),
        ('rhop', 'particle_density')
    ]
    _keys = []

    def __init__(self, **kwargs):
        super(Parameters, self).__init__()
        self.update(self.default_parameters)
        self.update(kwargs)
        self.nondimensionalise()

    @property
    def allowed_keys(self):
        "Return the list of parameter keys"
        if self._keys == []:
            for pair in self.equivalent:
                self._keys.extend(pair)
            self._keys = set(self._keys)
        return self._keys

    def __setitem__(self, key, value):
        # Check that the key is one that we can set
        if key not in self.allowed_keys:
            raise KeyError('Unknown parameter key {0}'.format(key))

        # Set the given key value
        super(Parameters, self).__setitem__(key, value)
        
        # Update the equivalent pair if required
        for pair in self.equivalent:
            if key in pair:
                # Get the pair member we _don't_ have
                [other] = [p for p in pair if p != key]
                super(Parameters, self).__setitem__(other, value)

        # Recalculate non-dimensional parameters if required
        if key not in ('R', 'S'):
            self.nondimensionalise()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return super(Parameters, self).__getattr__(key)

    def __setattr__(self, key, value):
        if key in self.allowed_keys:
            self[key] = value
        else:
            super(Parameters, self).__setattr__(key, value)

    def nondimensionalise(self):
        """ Calculate non dimensional parameters for the integration
        """
        pass