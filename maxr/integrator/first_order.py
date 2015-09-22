""" file: first_order.py (maxr.stepper)
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   September 2015

    description: First order integrator
"""

from __future__ import print_function, division

from .integrator import IntegratorBase

class Stepper(StepperBase):

    """ First order integrator for MR equations

        See Eqn 15, p.9 in paper for details.

        Parameters:
            params - a maxr.Parameters instance with the parameters for the 
                integration.
    """

    def rnext(self):
        """ Return next particle location
        """
        self.position.append(
            r + self.params.dt * (w + self.flow(r)) )
        return self.position[-1]

    def wnext(self, r, w):
        """ Return next velocity difference
        """
        self.velocity_diff.append(
            None)
