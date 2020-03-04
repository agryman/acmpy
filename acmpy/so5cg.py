r"""
Read precomputed $\textrm{SO}(5) \supset \textrm{SO}(3)$ Clebsch-Gordan (CG) coefficients from files.

Explanation
===========

CG coefficients for $\textrm{SO}(5) \supset \textrm{SO}(3)$ arise in nuclear physics collective model calculations [1]_.
In this model basis vectors for the angular part of the quadrapole moment wave function are labeled by
the parameters $(v, a, L)$ where
$v$ is the boson seniority which labels an irreducible representation (irrep) of $\textrm{SO}(5)$,
$L$ is the total angular momentum which labels an irrep of $\textrm{SO}(3)$ and
$a$ is a multiplicity index which distinguishes the irreps of $\textrm{SO}(3)$ that have
the same $L$ under the restriction $\textrm{SO}(5) \supset \textrm{SO}(3)$.
See [2]_ (available online at [3]_) for a definition of this basis and how to compute the associated CG coefficients.

In order to speed up collective model computations
it is useful to precompute these coefficients and store them in disk files
so they can be quickly accessed as required.
Each precomputed CG coefficient is stored as a floating point number
and is labeled by the 9 integers $(v_1, a_1, L_1, v_2, a_2, L_2, v_3, a_3, L_3)$

The files are arranged as a set of nested subdirectories of some base directory.
The file and directory names encode some of the parameters that label the coefficients.
Each file contains a sequence of lines.
Each line contains a coefficient value followed by the 9 integers that define its label.

We'll refer to this precomputed data as an SO5CG database.
The database is stored in some base directory which can be located anywhere on the file system,
e.g. in the directory ``~/so5cg-data/``.

The base directory contains a set of subdirectories named like ``v2=*``, e.g. ``v2=4``,
and may contain other files and directories.
Only those subdirectories whose names match the pattern, are significant.
We refer to those as level 1 directories.
Each level 1 directory name encodes an integer, namely the value of the $v_2$ parameter.
For example, the name ``v2=4`` encodes the value $v_2 = 4$.

Each level 1 directory contains a set of subdirectories named like ``SO5CG_*_*_*``, e.g. ``SO5CG_1_2_3``,
and may contain other files and directories.
Only those subdirectories whose names match the pattern are significant.
We refer to those as level 2 directories.
Each level 2 directory name encodes 3 integers, namely the values of the $v_1$, $v_2$, and $v_3$ parameters.
For example, the name ``SO5CG_1_2_3`` encodes the values $v_1 = 1$, $v_2 = 2$, and $v_3 = 3$.

Each level 2 directory contains a set of files named like ``SO5CG_*_*-*-*_*``, e.g. ``SO5CG_1_2-1-2_3``,
and may contain other files and directories.
Only those files whose names match the pattern are significant.
We refer to those as SO5CG files.
Each SO5CG file name encodes 5 integers, namely the values of the $v_1$, $v_2$, $a_2$, $L_2$, and $v_3$ parameters.
For example, the name ``SO5CG_1_2-1-2_3`` encodes the values $v_1 = 1$, $v_2 = 2$, $a_2 = 1$, $L_2 = 2$, and $v_3 = 3$.

Each SO5CG file contains a set of lines.
Each line contains the float value of a SO5CG coefficient followed by the 9 integer values that label the coefficient,
namely $(v_1, a_1, L_1, v_2, a_2, L_2, v_3, a_3, L_3)$.

The following list illustrates a fragment of a SO5CG database.

- dir1: ``v2=2``
    - dir2: ``SO5CG_1_2_3``
        - file: ``SO5CG_1_2-1-2_3``
            - line: +1.000000e+00      1    1    2      2    1    2      3    1    0
            - line: +8.451543e-01      1    1    2      2    1    2      3    1    3
            - line: +7.237469e-01      1    1    2      2    1    2      3    1    4
        - file: ``SO5CG_1_2-1-4_3``
            - line: +5.345225e-01      1    1    2      2    1    4      3    1    3
            - line: -6.900656e-01      1    1    2      2    1    4      3    1    4
            - line: +1.000000e+00      1    1    2      2    1    4      3    1    6


Mathematically, an SO5GC database is a function that maps a 9-tuple integers to a float.
We could implement it as a 9-dimensional Python array of floats.
However, most of the 9-tuples map to zero, so this array would be very sparse.
Instead we implement the database using nested Python dictionaries.

The Maple code contains the procedures
``show_CG_file(v1, v2, a2, L2, v3)`` which prints the file contents and
``load_CG_table(v1, v2, a2, L2, v3)`` which loads a file from disk.

The files are loaded on demand since there are many files and not all of them are used
in any given calculation.
The contents of the files are stored in a Maple table named ``CG_coeffs`` which is like a Python
dictionary.
``CG_coeffs[v1, v2, a2, L2, v3]`` is a table of CG coefficient values contained in a single data file.
``CG_coeffs[v1, v2, a2, L2, v3][a1, L1, a3, L3]`` is the actual CG coefficient value.

The parameters have the following Maple types:

- ``v1``, ``v2``, ``v3``: ``nonnegint``
- ``a1``, ``a2``, ``a3``: ``posint``
- ``L1``, ``L2``, ``L3``: ``nonnegint``

The data is stored in the file named SO5CG_v1_v2-a2-L2_v3.

The Maple procedure SO5CG_filename(v1, v2, a2, L2, v3) generates the file path as follows:
cat(SO5CG_directory, "v2=", v2, "/SO5CG_", v1, "_", v2, "_", v3, "/SO5CG_", v1, "_", v2, "-", a2, "-", L2, "_", v3);

References
==========

.. [1] D.J. Rowe, A computationally tractable version of the collective model,
       Nuclear Physics A 735 (2004), pp. 372-392
.. [2] M.A. Caprio , D.J. Rowe , T.A. Welsh,
       Construction of $\textrm{SO}(5) \supset \textrm{SO}(3)$ spherical harmonics and Clebsch–Gordan coefficients,
       Computer Physics Communications 180 (2009), pp. 1150-1163
.. [3] http://www.sciencedirect.com/science/journal/00104655

"""

from pathlib import Path
from os.path import expanduser
import os
import re

# Lines in SO5CG data files, e.g. +7.237469e-01      1    1    2      2    1    2      3    1    4

def parse_line(line: str):
    """
    Parse ``line`` and if valid return the SO5CG data, else raise an exception.

    :param line: A string containing a float SO5CG coefficient and the 9 integers that label it.
    :return: A tuple (coeff, (v1, a1, L1, v2, a2, L2, v3, a3, L3))

    """
    if not type(line) is str:
        raise TypeError("line must be a str")

    fields = re.split(r'\s+', line.strip())

    if(len(fields) != 10):
        raise("line must have have 10 fields")

    return float(fields[0]), tuple(int(x) for x in fields[1:])

# SO5CG data files, e.g. named like 'SO5CG_1_2-1-4_3'

#: compiled regex for SO5CG data file names
datafile_name_re = re.compile(r'^SO5CG_(\d+)_(\d+)-(\d+)-(\d+)_(\d+)$')


def is_datafile_path(path: Path):
    """
    Return ``True`` if ``path`` is a valid SO5CG data file path, else ``False``.

    """
    return path.is_file() and (datafile_name_re.match(path.name) != None)


def parse_datafile_name(name: str) -> tuple:
    m = datafile_name_re.match(name)
    if(m):
        return tuple(int(m.group(i)) for i in range(1,6))
    return None


def load_datafile(file: Path):
    f = file.open()
    lines = [parse_line(line) for line in f]
    f.close()
    return lines


def dict_level_3(file: Path) -> dict:
    """
    Return the SO5CG data file contents as a dictionary of lines.



    """
    lines = load_datafile(file)
    return {line[1]: line[0] for line in lines}


def is_dir(name: str) -> bool:
    """
    Return ``True`` if ``name`` is the name of a directory, else ``False``.

    """
    return Path(name).is_dir()

# Level 2 directories

level_2_re = re.compile(r'^SO5CG_(\d+)_(\d+)_(\d+)$')

def is_level_2(path):
    """
    Return ``True`` if and only if path is a directory whose name is like 'SO5CG_1_2_3'.

    """
    return path.is_dir() and (level_2_re.match(path.name) != None)

def parse_level_2(name: str) -> tuple:
    m = level_2_re.match(name)
    if(m):
        return tuple(int(m.group(i)) for i in range(1,4))
    return None


def dict_level_2(dir: Path) -> dict:
    """
    Return a dictionary of file paths for the level 3 files.

    """
    return {parse_datafile_name(file.name): file for file in dir.iterdir() if is_datafile_path(file)}


# Level 1 directories

# level 1 is a directory whose name is like v2=1
dir1_name_re = re.compile(r'^v2=(\d+)$')

def is_dir1_path(path: Path) -> bool:
    """
    Return ``True`` if path is a directory whose name is like 'v2=6', else ``False``.

    """
    return path.is_dir() and (dir1_name_re.match(path.name) != None)


def parse_dir1_name(name: str) -> int:
    """
    Return the value of v2 encoded in the level 1 directory name if matched, else None.
    :param name:
    :return:

    """
    m = dir1_name_re.match(name)
    if(m):
        return int(m.group(1))
    return None


#: regex pattern to match v2 directory names like "v2=1", "v2=2", etc.
v2_dir_pattern = r'^v2=(\d+)$'

#: compiled regex to match v2 directory names
v2_dir_re = re.compile(v2_dir_pattern)

def parse_v2(name: str) -> int:
    """
    Return the value of v2 encoded in the v2 directory name if matched, else None.

    Parameters
    ==========

    name : str, the v2 directory name, e.g. "v2=3"

    Returns
    =======

    int or NoneType, the integer value of v2, e.g. 3, if the directory name is valid, else None

    Examples
    ========

    >>> from acmpy.so5cg import parse_v2
    >>> parse_v2("v2=3")
    3
    >>> parse_v2("xxx")

    """
    m = v2_dir_re.match(name)
    if(m):
        v2_str = m.group(1)
        return int(v2_str)
    return None

def dict_level_1(dir1: Path) -> dict:
    return {parse_level_2(dir2.name): dict_level_2(dir2) for dir2 in dir1.iterdir() if is_level_2(dir2)}

# Base directory

default_SO5CG_directory = expanduser('~/so5cg-data/')

def dict_level_0(dir0: Path) -> dict:
    return {parse_dir1_name(dir1.name): dict_level_1(dir1) for dir1 in dir0.iterdir() if is_dir1_path(dir1)}
