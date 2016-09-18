""" file: blink.py (maxr.flow)
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   September 25, 2015

    description: Blinking vortex flow
"""

from __future__ import print_function, division

from numpy import asarray, clip, pi, sin, newaxis


def vortex(x_center, y_center, gamma):
    """ Returns a function to give a vortex flow centered at r,
        with strength Gamma
    """
    def _flow(xxs, yys):
        "Wrapped flow function"
        xxs = asarray(xxs)
        yys = asarray(yys)
        rsq = (xxs - x_center) ** 2 + (yys - y_center) ** 2
        return (-gamma * (xxs - x_center) / (2 * pi * rsq),
                gamma * (yys - y_center) / (2 * pi * rsq))
    return _flow


def tick(time, period):
    """ Adding some time dependence!
    """
    return clip(sin(2 * pi * time / period), 0, 1.01)


def tock(time, period):
    """ Adding some time dependence!
    """
    return clip(-sin(2 * pi * time / period), 0, 1.01)


def blink(gamma, period):
    """ The blinking vortex flow
    """
    # Generate two vortices
    vortices = [vortex(x, 0, gamma) for x in (-0.5, 0.5)]

    # Wrap in flow with time dependence
    def _flow(xxs, yys, time):
        "Wrapped flow function"
        _vortex = [v(xxs, yys) for v in vortices]
        return _vortex[0][0][..., newaxis] * tick(time, period) \
               + _vortex[1][0][..., newaxis] * tock(time, period), \
               _vortex[0][1][..., newaxis] * tick(time, period) \
               + _vortex[1][1][..., newaxis] * tock(time, period)
    return _flow
