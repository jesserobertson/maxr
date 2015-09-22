""" file: maxr.py
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   September 2015

    description: Integration of particle paths in chaotic flows
"""

def r_next(r, w, v, order=1):
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

def w_next(r, v, order=1)
    """ Get the next particle velocity difference, w, given the current location, the velocity of the fluid flow at 
    """