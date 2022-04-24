"""This module defines functions to achieve compatibility with Maple."""

import re
from pathlib import Path
from sympy import Expr, Matrix

IntFloatExpr = int | float | Expr
"""IntFloatExpr is a convenience type for function arguments that 
are passed in by the user. They will get sympified, so users
can pass in integers and floating point numbers without first converting them
into SymPy expressions."""

# define Python type aliases that approximate Maple types
nonnegint = int
posint = int


def require_algebraic(name: str, value: Expr) -> None:
    """Raise an exception if value is not algebraic."""
    if not isinstance(value, Expr):
        raise TypeError(f'type of {name} is not Expr: {value}')
    if not value.is_algebraic:
        raise ValueError(f'value of {name} is not algebraic: {value}')


def require_int(name: str, value: int) -> None:
    """Raise an exception if value is not an integer."""
    if not isinstance(value, int):
        raise TypeError(f'type of {name} is not an int: {value}')


def require_nonnegint(name: str, value: nonnegint) -> None:
    """Raise an exception if value is not a nonnegative integer."""
    require_int(name, value)
    if value < 0:
        raise ValueError(f'value of {name} is not a nonnegative integer: {value}')


def require_nonnegint_range(name: str, value_min: nonnegint, value_max: nonnegint) -> None:
    """Raise and exception if values are not nonnegative integers or min exceeds max."""
    name_min: str = f'{name}_min'
    require_nonnegint(name_min, value_min)

    name_max: str = f'{name}_max'
    require_nonnegint(name_max, value_max)

    if value_min > value_max:
        raise ValueError(f'{name_min}({value_min}) > {name_max}({value_max})')


def require_posint(name: str, value: posint) -> None:
    """Raise an exception if value is not a positive integer."""
    require_nonnegint(name, value)
    if value == 0:
        raise ValueError(f'value of {name} is not a positive integer: {value}')


def is_even(n: int) -> bool:
    """Return True if and only if n is an even integer."""
    require_int('n', n)

    return n % 2 == 0


def is_odd(n: int) -> bool:
    """Return True if and only if n is an odd integer."""
    require_int('n', n)

    return n % 2 == 1


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


def parse_line_float(line: str) -> float:
    """Parse the first field in line as a float and return it."""
    fields: list[str] = re.split(r'\s+', line.strip())
    value: float = float(fields[0])

    return value


def readdata_float(filename: str) -> list[float]:
    """Read the named text file and return the first column as a list of floats."""
    filepath: Path = Path(filename)
    with filepath.open() as f:
        data: list[float] = [parse_line_float(line) for line in f]

    return data
