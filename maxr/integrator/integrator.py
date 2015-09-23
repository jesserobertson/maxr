""" file: maxr.py
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   September 2015

    description: Integration of particle paths in chaotic flows
"""

from __future__ import print_function, division

from ..parameters import Parameters
from . import history


def Integrator(object):

    """ The class which does the integration!

        We use the scheme from Daitsche (2013; http://arxiv.org/pdf/1210.2576.pdf) which is third-order accurate in the timestep

        Parameters: 
            flow - a function which, when given (x, t), returns a 
                velocity vector u.  
            parameters - an instance of maxr.Parameters which contains
                the parameters for the integration.
    """

    def __init__(self, flow, parameters):
        super(Integrator, self).__init__()
        