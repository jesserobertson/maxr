""" file: coefficients.py

    description: Coefficients for integration schemes
"""

from __future__ import print_function, division

from numpy import arange, empty, sqrt, array

# Just to make it easy for everyone
def coefficients(num, order=3):
    """ Return the coefficients for the given order

        Parameters:
            num - the number of coefficients to get (i.e. the length of your
                state history vector)
            order - the order of the integrator scheme.
    """
    if order == 3:
        return gamma(num)
    elif order == 2:
        return beta(num)
    elif order == 1:
        return alpha(num)
    else:
        raise ValueError("Order must be one of 1, 2 or 3")


def integrator(states, times, order=3):
    """ A history integrator which integrates a given history from the start to the end

        Parameters:
            states - a vector of states (i.e. the history) to integrate
            times - the times corresponding to each state measurement
            order - the order of the integrator (defaults to third-order)
    """
    _num = len(states)-1
    const = 2 * sqrt(times[-1] - times[0]) * states[0]
    return const + sqrt(times[1] - times[0]) \
        * (coefficients(_num, order) * states[::-1]).sum()

## COEFFICIENTS
def alpha(num):
    """ First-order integration coefficients for history term
    """
    if num > 0:
        # Left boundary
        _alpha = empty(num + 1)
        _alpha[0] = 1

        # Middle
        jidx = arange(1, num)
        _alpha[1:-1] = (jidx-1) ** (3/2) \
                       + (jidx+1) ** (3/2) - 2 * jidx ** (3/2)

        # Right boundary
        _alpha[-1] = (num-1) ** (3/2) - num ** (3/2) + 6/4 * num ** (1/2)
        return 4/3 * _alpha

    else:
        raise ValueError("num must be greater than 1")


def beta(num):
    """ Second-order integration coefficients for history term
    """
    if num > 3:
        # Left boundary
        _beta = empty(num + 1)
        _beta[0] = 4 / 5 * sqrt(2)
        _beta[1] = 14 / 5 * sqrt(3) - 12 / 5 * sqrt(2)
        _beta[2] = 176 / 15 - 42 / 5 * sqrt(3) + 12 / 5 * sqrt(2)

        # Middle
        jidx = arange(3, num - 1)
        _beta[3:-2] = 8/15 * ((jidx+2) ** (5/2) - 3 * (jidx+1) ** (5/2)
                              + 3 * jidx ** (5/2) - (jidx-1) ** (5/2)) \
                      + 2/3 * (-(jidx+2) ** (3/2) + 3 * (jidx+1) ** (3/2)
                               - 3 * jidx ** (3/2) + (jidx-1) ** (3/2))

        # Right boundary
        _beta[-2] = 8/15 * (-2 * num ** (5/2) + 3 * (num-1) ** (5/2)
                            - (num-2) ** (5/2)) \
                   + 2/3 * (4 * num ** (3/2) - 3 * (num-1) ** (3/2)
                            + (num-2) ** (3/2))
        _beta[-1] = 8/15 * (num ** (5/2) - (num-1) ** (5/2)) \
                   + 2/3 * (-3 * num ** (3/2) + (num-1) ** (3/2)) + 2 * num ** (1/2)

    # First few have to be handled specially
    elif num == 1:
        _beta = alpha(1)

    elif num == 2:
        _beta = array([12/15 * sqrt(2), 16/15 * sqrt(2), 2/15 * sqrt(2)])

    elif num == 3:
        _beta = array([
            4/5 * sqrt(2), 14/5 * sqrt(3) - 12/5 * sqrt(2),
            -8/5 * sqrt(3) + 12/5 * sqrt(2), 4/5 * sqrt(3)  - 4/5 * sqrt(2)])

    else:
        raise ValueError("num must be greater than 1")

    return _beta


def gamma(num):
    """ Third-order integration coefficients for history term
    """
    if num > 6:
        # Left boundary
        _gamma = empty(num + 1)
        _gamma[0] = 244/315 * sqrt(2)
        _gamma[1] = 362/105 * sqrt(3) - 976/315 * sqrt(2)
        _gamma[2] = 5584/315 - 1448/105 * sqrt(3) + 488/105 * sqrt(2)
        _gamma[3] = 1130/63 * sqrt(5) - 22336/315 + 724/35 * sqrt(3) \
                   - 976/315 * sqrt(2)

        # Middle
        jidx = arange(4, num - 2)
        _gamma[4:-3] = 16/105 * ((jidx+2) ** (7/2) + (jidx-2) ** (7/2)
                                 - 4 * (jidx+1) ** (7/2)
                                 - 4 * (jidx-1) ** (7/2)
                                 + 6 * jidx ** (7/2)) \
                      + 2/9 * (4 * (jidx+1) ** (3/2) + 4 * (jidx-1) ** (3/2)
                               - (jidx+2) ** (3/2) - (jidx-2) ** (3/2)
                               - 6 * jidx ** (3/2))

        # Right boundary
        _gamma[-4] = 16/105 * (num ** (7/2) - 4 * (num-2) ** (7/2)
                               + 6 * (num-3) ** (7/2) - 4 * (num-4) ** (7/2)
                               + (num-5) ** (7/2)) \
                    - 8/15 * num ** (5/2) + 4/9 * num ** (3/2) \
                    + 8/9 * (num-2) ** (3/2) - 4/3 * (num-3) ** (3/2) \
                    + 8/9 * (num-4) ** (3/2) - 2/9 * (num-5) ** (3/2)
        _gamma[-3] = 16/105 * ((num-4) ** (7/2) - 4 * (num-3) ** (7/2)
                               + 6 * (num-2) ** (7/2) - 3 * num ** (7/2)) \
                    + 32/15 * num ** (5/2) \
                    - 2 * num ** (3/2) - 4/3 * (num-2) ** (3/2) \
                    + 8/9 * (num-3) ** (3/2) - 2/9 * (num-4) ** (3/2)
        _gamma[-2] = 16/105 * (3 * num ** (7/2) - 4 * (num-2) ** (7/2)
                               + (num-3) ** (7/2)) \
                    - 8/3 * num ** (5/2) + 4 * num ** (3/2) \
                    + 8/9 * (num-2) ** (3/2) - 2/9 * (num-3) ** (3/2)
        _gamma[-1] = 16/105 * ((num-2) ** (7/2) - num ** (7/2)) \
                    + 16/15 * num ** (5/2) - 22/9 * num ** (3/2) \
                    - 2/9 * (num-2) ** (3/2) + 2 * num ** (1/2)

    # First few have to be handled specially
    elif num == 1:
        _gamma = alpha(1)

    elif num == 2:
        _gamma = beta(2)

    elif num == 3:
        _gamma = array([
            68/105 * sqrt(3), 6/7 * sqrt(3),
            12/35 * sqrt(3), 16/105 * sqrt(3)])

    elif num == 4:
        _gamma = array([
            244/315 * sqrt(2), 1888/315 - 976/315 * sqrt(2),
            -656/105 + 488/105 * sqrt(2), 544/105 - 976/315 * sqrt(2),
            -292/315 + 244/315 * sqrt(2)])

    elif num == 5:
        _gamma = array([
            244/315 * sqrt(2),
            362/105 * sqrt(3) - 976/315 * sqrt(2),
            500/63 * sqrt(5) - 1448/105 * sqrt(3) + 488/105 * sqrt(2),
            -290/21 * sqrt(5) + 724/35 * sqrt(3) - 976/315 * sqrt(2),
            220/21 * sqrt(5) - 1448/105 * sqrt(3) + 244/315 * sqrt(2),
            -164/63 * sqrt(5) + 362/105 * sqrt(3)])

    elif num == 6:
        _gamma = array([
            244/315 * sqrt(2),
            362/105 * sqrt(3) - 976/315 * sqrt(2),
            5584/315 - 1448/105 * sqrt(3) + 488/105 * sqrt(2),
            344/21 * sqrt(6) - 22336/315 + 724/35 * sqrt(3) \
                - 976/315 * sqrt(2),
            -1188/35 * sqrt(6) + 11168/105 - 1448/105 * sqrt(3) \
                + 244/315 * sqrt(2),
            936/35 * sqrt(6) - 22336/315 + 362/105 * sqrt(3),
            -754/105 * sqrt(6) + 5584/315])

    else:
        raise ValueError("num must be greater than 1")

    return _gamma

    