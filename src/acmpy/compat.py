"""This module defines functions to achieve compatibility with Maple."""

from typing import TypeAlias
import re
import numpy as np
import numpy.typing as npt
from pathlib import Path
from math import isclose
from sympy import Expr, shape, MutableDenseMatrix

Matrix: TypeAlias = MutableDenseMatrix

IntFloatExpr = int | float | Expr
"""IntFloatExpr is a convenience type for function arguments that 
are passed in by the user. They will get sympified, so users
can pass in integers and floating point numbers without first converting them
into SymPy expressions."""

# define Python type aliases that approximate Maple types
nonnegint = int
posint = int

NDArrayFloat = npt.NDArray[np.float64]


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


ABS_TOL: float = 1e-14


def is_zeros(zs: list[float], abs_tol: float = ABS_TOL) -> bool:
    """Return True if and only if every element in the list zs is close to 0."""
    return all(isclose(z, 0, abs_tol=abs_tol) for z in zs)


def is_close(xs: list[float], ys: list[float], abs_tol: float = ABS_TOL) -> bool:
    """Return True if and only if every element of list xs is close to the corresponding element of list ys."""
    if len(xs) != len(ys):
        return False
    return is_zeros([x - y for x, y in zip(xs, ys)], abs_tol)


def is_sorted(vals: list) -> bool:
    """Return True if and only if the list is in ascending order."""
    return all(a <= b for (a, b) in zip(vals[:-1], vals[1:]))


def is_nd_zeros(zs: NDArrayFloat, abs_tol: float = ABS_TOL) -> bool:
    """Return True if and only if every element in the n-dimensional array of floats zs is close to 0."""
    return is_zeros(ndarray_to_list(zs), abs_tol)


def is_nd_float(x: NDArrayFloat) -> bool:
    """Return True if and only if x is an n-dimensional array of floats."""
    return x.dtype == np.float64


def is_nd_vector(v: NDArrayFloat) -> bool:
    """Return True if and only if v is a 1-dimensional array of floats."""
    return is_nd_float(v) and v.ndim == 1


def is_nd_matrix(m: NDArrayFloat) -> bool:
    """Return True if and only if m is a 2-dimensional array of floats."""
    return is_nd_float(m) and m.ndim == 2


def is_nd_square(m: NDArrayFloat) -> bool:
    """Return True if and only if m is a square 2-dimensional array of floats."""
    if not is_nd_matrix(m):
        return False
    r, c = m.shape
    return r == c


def list_to_ndarray(x: list) -> NDArrayFloat:
    return np.array(x, dtype=np.float64)


def lists_to_ndarrays(t: tuple[list, ...]) -> tuple[NDArrayFloat, ...]:
    return tuple(list_to_ndarray(x) for x in t)


def ndarray_to_list(vals: NDArrayFloat) -> list[float]:
    """Creates a flat list of floats from an NumPy ndarray of floats."""
    return [float(val) for val in vals.flat]


def Matrix_to_ndarray(M: Matrix) -> NDArrayFloat:
    """Creates an NumPy 2-dimensional ndarray of floats from a SymPy Matrix."""
    r, c = shape(M)
    return np.array([[float(M[i, j]) for j in range(c)] for i in range(r)])


def ndarray_to_Matrix(M: NDArrayFloat) -> Matrix:
    """Creates a SymPy Matrix from an NumPy 2-dimensional ndarray of floats."""
    return Matrix(*M.shape, lambda i, j: M[i, j])
