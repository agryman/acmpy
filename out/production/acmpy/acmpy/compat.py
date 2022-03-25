"""This module defines functions to achieve compatibility with Maple."""

from acmpy.types import require_nonnegint, require_posint, posint, nonnegint


def iquo(m: nonnegint, n: posint) -> int:
    """Return the integer quotient of m/n for m nonnegative and n positive."""
    require_nonnegint('m', m)
    require_posint('n', n)

    return m // n


def irem(m: nonnegint, n: posint) -> int:
    """Return the integer remainder of m/n for m nonnegative and n positive."""
    require_nonnegint('m', m)
    require_posint('n', n)

    return m % n
