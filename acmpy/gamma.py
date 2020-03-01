"""
The module is a test for docstrings.

Caveats
=======

1. It doesn't do anything useful.

2. Really, it's completely useless

"""

from math import sqrt

def norm(x, y):
    r"""
    Returns the norm $\sqrt{x^2+y^2}$ of a real 2-vector $(x,y)$.

    .. math::

        \mbox{norm}(x,y) = \sqrt{x^2 + y^2}

    Parameters
    ==========

    x : int, the x component of the 2-vector
    y : int, the y component of the 2-vector

    Returns
    =======

    float
        the norm of the 2-vector

    Examples
    ========

    >>> from acmpy.gamma import norm
    >>> norm(3,4)
    5.0

    """
    return sqrt(x**2 + y**2)