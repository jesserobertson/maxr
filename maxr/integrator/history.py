""" file: coefficients.py

    description: Coefficients for integration schemes
"""

from __future__ import print_function, division

from numpy import arange, empty, sqrt, array

# Just to make it easy for everyone
def coefficients(n, order=3):
    """ Return the coefficients for the given order

        Parameters:
            n - the number of coefficients to get (i.e. the length of your 
                state history vector)
            order - the order of the integrator scheme.
    """
    if order == 3:
        return gamma(n)
    elif order == 2:
        return beta(n)
    elif order == 1:
        return alpha(n)
    else:
        raise ValueError("Order must be one of 1, 2 or 3")


def alpha(n):
    """ First-order integration coefficients for history term
    """
    if n > 0:
        # Left boundary
        alpha = empty(n + 1)
        alpha[0] = 1
        
        # Middle
        js = arange(1, n)
        alpha[1:-1] = (js-1) ** (3/2) + (js+1) ** (3/2) - 2 * js ** (3/2)
            
        # Right boundary
        alpha[-1] = (n-1) ** (3/2) - n ** (3/2) + 6/4 * n ** (1/2)
        return 4/3 * alpha

    else:
        raise ValueError("n must be greater than 1")


def beta(n):
    """ Second-order integration coefficients for history term
    """
    if n > 3:
        # Left boundary
        beta = empty(n + 1)
        beta[0] = 4 / 5 * sqrt(2)
        beta[1] = 14 / 5 * sqrt(3) - 12 / 5 * sqrt(2)
        beta[2] = 176 / 15 - 42 / 5 * sqrt(3) + 12 / 5 * sqrt(2)

        # Middle
        js = arange(3, n - 1)
        beta[3:-2] = 8/15 * ((js+2) ** (5/2) - 3 * (js+1) ** (5/2) 
                             + 3 * js ** (5/2) - (js-1) ** (5/2)) \
                   + 2/3 * (-(js+2) ** (3/2) + 3 * (js+1) ** (3/2) 
                            - 3 * js ** (3/2) + (js-1) ** (3/2))

        # Right boundary
        beta[-2] = 8/15 * (-2 * n ** (5/2) + 3 * (n-1) ** (5/2) 
                           - (n-2) ** (5/2)) \
                   + 2/3 * (4 * n ** (3/2) - 3 * (n-1) ** (3/2) 
                            + (n-2) ** (3/2))
        beta[-1] = 8/15 * (n ** (5/2) - (n-1) ** (5/2)) \
                   + 2/3 * (-3 * n ** (3/2) + (n-1) ** (3/2)) + 2 * n ** (1/2)
    
    # First few have to be handled specially    
    elif n == 1:
        beta = alpha(1)

    elif n == 2:
        beta = array([12/15 * sqrt(2), 16/15 * sqrt(2), 2/15 * sqrt(2)]) 
    
    elif n == 3:
        beta = array([
            4/5 * sqrt(2), 14/5 * sqrt(3) - 12/5 * sqrt(2),
            -8/5 * sqrt(3) + 12/5 * sqrt(2), 4/5 * sqrt(3)  - 4/5 * sqrt(2)])

    else:
        raise ValueError("n must be greater than 1")

    return beta


def gamma(n):
    """ Third-order integration coefficients for history term
    """
    if n > 6:
        # Left boundary
        gamma = empty(n + 1)
        gamma[0] = 244/315 * sqrt(2)
        gamma[1] = 362/105 * sqrt(3) - 976/315 * sqrt(2)
        gamma[2] = 5584/315 - 1448/105 * sqrt(3) + 488/105 * sqrt(2)
        gamma[3] = 1130/63 * sqrt(5) - 22336/315 + 724/35 * sqrt(3) \
                   - 976/315 * sqrt(2)

        # Middle
        js = arange(4, n - 2)
        gamma[4:-3] = 16/105 * ((js+2) ** (7/2) + (js-2) ** (7/2)
                                - 4 * (js+1) ** (7/2) - 4 * (js-1) ** (7/2)
                                + 6 * js ** (7/2)) \
                      + 2/9 * (4 * (js+1) ** (3/2) + 4 * (js-1) ** (3/2)
                               - (js+2) ** (3/2) - (js-2) ** (3/2)
                               - 6 * js ** (3/2))

        # Right boundary
        gamma[-4] = 16/105 * (n ** (7/2) - 4 * (n-2) ** (7/2) 
                              + 6 * (n-3) ** (7/2) - 4 * (n-4) ** (7/2) 
                              + (n-5) ** (7/2)) \
                    - 8/15 * n ** (5/2) + 4/9 * n ** (3/2) \
                    + 8/9 * (n-2) ** (3/2) - 4/3 * (n-3) ** (3/2) \
                    + 8/9 * (n-4) ** (3/2) - 2/9 * (n-5) ** (3/2)
        gamma[-3] = 16/105 * ((n-4) ** (7/2) - 4 * (n-3) ** (7/2)
                              + 6 * (n-2) ** (7/2) - 3 * n ** (7/2)) \
                    + 32/15 * n ** (5/2) \
                    - 2 * n ** (3/2) - 4/3 * (n-2) ** (3/2) \
                    + 8/9 * (n-3) ** (3/2) - 2/9 * (n-4) ** (3/2)
        gamma[-2] = 16/105 * (3 * n ** (7/2) - 4 * (n-2) ** (7/2) 
                              + (n-3) ** (7/2)) \
                    - 8/3 * n ** (5/2) + 4 * n ** (3/2) \
                    + 8/9 * (n-2) ** (3/2) - 2/9 * (n-3) ** (3/2)
        gamma[-1] = 16/105 * ((n-2) ** (7/2) - n ** (7/2)) \
                    + 16/15 * n ** (5/2) - 22/9 * n ** (3/2) \
                    - 2/9 * (n-2) ** (3/2) + 2 * n ** (1/2)

    # First few have to be handled specially
    elif n == 1:
        gamma = alpha(1)

    elif n == 2: 
        gamma = beta(2)

    elif n == 3:
        gamma = array([
            68/105 * sqrt(3), 6/7 * sqrt(3), 
            12/35 * sqrt(3), 16/105 * sqrt(3)])

    elif n == 4:
        gamma = array([
            244/315 * sqrt(2), 1888/315 - 976/315 * sqrt(2),
            -656/105 + 488/105 * sqrt(2), 544/105 - 976/315 * sqrt(2),
            -292/315 + 244/315 * sqrt(2)])

    elif n == 5:
        gamma = array([
            244/315 * sqrt(2),
            362/105 * sqrt(3) - 976/315 * sqrt(2),
            500/63 * sqrt(5) - 1448/105 * sqrt(3) + 488/105 * sqrt(2),
            -290/21 * sqrt(5) + 724/35 * sqrt(3) - 976/315 * sqrt(2),
            220/21 * sqrt(5) - 1448/105 * sqrt(3) + 244/315 * sqrt(2),
            -164/63 * sqrt(5) + 362/105 * sqrt(3)])

    elif n == 6: 
        gamma = array([
            244/315 * sqrt(2),
            362/105 * sqrt(3) - 976/315 * sqrt(2),
            5584/315 - 1448/105 * sqrt(3) + 488/105 * sqrt(2),
            344/21 * sqrt(6) - 22336/315 + 724/35 * sqrt(3) 
                - 976/315 * sqrt(2),
            -1188/35 * sqrt(6) + 11168/105 - 1448/105 * sqrt(3) 
                + 244/315 * sqrt(2),
            936/35 * sqrt(6) - 22336/315 + 362/105 * sqrt(3),
            -754/105 * sqrt(6) + 5584/315])

    else:
        raise ValueError("n must be greater than 1")

    return gamma


def integrator(states, times, order=3):
    """ A history integrator which integrates a given history from the start to the end

        Parameters:
            states - a vector of states (i.e. the history) to integrate
            times - the times corresponding to each state measurement
            order - the order of the integrator (defaults to third-order)
    """
    _n = len(states)-1
    const = 2 * sqrt(times[-1] - times[0]) * states[0]
    return const + sqrt(times[1] - times[0]) \
        * (coefficients(_n, order) * states[::-1]).sum()
    