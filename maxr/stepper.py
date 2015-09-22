""" file: maxr.py
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   September 2015

    description: Integration of particle paths in chaotic flows
"""

from __future__ import print_function, division

from .parameters import Parameters

def Stepper(object):

    """ The class which does the integration!

        Parameters: 
            flow - a function which, when given (x, t), returns a 
                velocity vector u.  
            parameters - an instance of maxr.Parameters which contains
                the parameters for the integration.
    """

    def __init__(self, flow, parameters):
        super(Stepper, self).__init__()
        self.flow = flow

    def r_next(self, r, w, v, order=1):
        """ Get the next particle position r, given the current location, the velocity difference w and the fluid velocity v.

            We use the scheme from Daitsche (2013; http://arxiv.org/pdf/1210.2576.pdf) which is third-order accurate in the timestep

            Parameters:
                r - the current position of the particle
                w - the current velocity mismatch of the particle
                v - the current velocity of the fluid flow at r

            Returns:
                the new position for the particle
        """
        pass

    def w_next(self, r, v, order=1):
        """ Get the next particle velocity difference, w, given the current location, the velocity of the fluid flow at 
        """
        pass

    def velocity_kernel(self, x, t):
        """ Return the velocity part of the the Maxey-Riley equations 
        
            The velocity kernel is:

            \[
                G(t) = (R-1)\frac{du}{dt} - Rw\cdot \nabla u - \frac{R}{S}w
            \]
        """
        pass

    def history_kernel(self, x, t):
        """ Return the history part of the Maxey-Riley equations
        
            The history kernel is:

            \[
                H(t) = -R \sqrt{\frac{3}{\pi S}} \int_{t_0}^{t+\delta t} \frac{w(\tau)}{\sqrt{t-\tau}}d\tau
            \]

            (see Daitsche, 2013).
        """
        pass