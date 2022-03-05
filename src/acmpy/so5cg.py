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

from typing import Dict, List, Optional, Tuple
from pathlib import Path
from os.path import expanduser
import re

SO5IrrepLabel = Tuple[int, int, int]
#: an SO5 irrep is labelled by the integer triple (v, a, L)

SO5CoeffLabel = Tuple[SO5IrrepLabel, SO5IrrepLabel, SO5IrrepLabel]
#: an SO5CG coefficient is labelled by three irreps ((v1, a1, L1), (v2, a2, L2), (v3, a3, L3))

# Lines in SO5CG data files, e.g. +7.237469e-01      1    1    2      2    1    2      3    1    4
SO5FileLine = Tuple[float, SO5CoeffLabel]


def parse_line(line: str) -> SO5FileLine:
    """
    Parse ``line`` and if valid return the SO5CG data, else raise an exception.

    :param line: A string containing a float SO5CG coefficient and the 9 integers that label it.
    :return: A tuple (coeff, ((v1, a1, L1), (v2, a2, L2), (v3, a3, L3)))

    """
    if not type(line) is str:
        raise TypeError("line must be a str")

    fields = re.split(r'\s+', line.strip())

    if (len(fields) != 10):
        raise ValueError("line must have have 10 fields")

    coeff = float(fields[0])
    labels = [int(x) for x in fields[1:]]

    label1 = labels[0], labels[1], labels[2]
    label2 = labels[3], labels[4], labels[5]
    label3 = labels[6], labels[7], labels[8]

    return coeff, (label1, label2, label3)


def load_datafile(path: Path) -> List[SO5FileLine]:
    """
    Read the SO5CG data file at the given path, parse each line, and return as a list.

    :param path: The path of the SO5CG data file.
    :return: A list of the parsed data lines in the file.
    """
    f = path.open()
    lines = [parse_line(line) for line in f]
    f.close()
    return lines


def datafile_dict(path: Path) -> Dict[SO5CoeffLabel, float]:
    """
    Return the SO5CG data file contents as a dictionary of {label: coeff} entries.

    :param path: the SO5CG data file path
    :returns: a dictionary of {label: coeff} entries corresponding to the lines in the file where
        label is a triple of triples of integers ((v1, a1, L1), (v2, a2, L2), (v3, a3, L3)) and
        coeff is the float SO5CG coefficient for the label

    """
    lines = load_datafile(path)
    return {line[1]: line[0] for line in lines}


# SO5CG data files, e.g. named like 'SO5CG_1_2-1-4_3'
# The data files are labelled by (v1,v2,a2,L2,v3)
SO5FileLabel = Tuple[int, int, int, int, int]

datafile_name_re = re.compile(r'^SO5CG_(\d+)_(\d+)-(\d+)-(\d+)_(\d+)$')


#: compiled regex for SO5CG data file names


def is_datafile_path(path: Path) -> bool:
    """
    Return ``True`` if ``path`` is a valid SO5CG data file path, else ``False``.

    """
    return path.is_file() and (datafile_name_re.match(path.name) != None)


def parse_datafile_name(name: str) -> Optional[SO5FileLabel]:
    """
    Return the SO5FileLabel (v1,v2,a2,L2,v3) encoded in name if valid, otherwise None.
    :param name: The string data file name, e.g. 'SO5CG_1_2-1-4_3'
    :return: The label, e.g. (1,2,1,4,3) or None
    """
    m = datafile_name_re.match(name)
    if (m):
        labels = [int(m.group(i)) for i in range(1, 6)]
        return labels[0], labels[1], labels[2], labels[3], labels[4]
    return None


def is_dir_name(name: str) -> bool:
    """
    Return ``True`` if ``name`` is the name of a directory, else ``False``.

    """
    return Path(name).is_dir()


# Level 2 directories, e.g. SO5CG_1_2_3
# The labels are (v1, v2, v3)

SO5Dir2Label = Tuple[int, int, int]
#: SO5 level 2 directory label (v1,v2,v3)

dir2_name_re = re.compile(r'^SO5CG_(\d+)_(\d+)_(\d+)$')


#: compiled regex for level 2 directory names

def is_dir2_path(path: Path) -> bool:
    """
    Return ``True`` if and only if path is a directory whose name is like 'SO5CG_1_2_3'.

    """
    return path.is_dir() and (dir2_name_re.match(path.name) != None)


def parse_dir2_name(name: str) -> Optional[SO5Dir2Label]:
    m = dir2_name_re.match(name)
    if (m):
        labels = [int(m.group(i)) for i in range(1, 4)]
        return labels[0], labels[1], labels[2]
    return None


def dir2_dict(path: Path) -> dict:
    """
    Return a dictionary of file paths for the SO5CG data files in a level 2 directory.

    """
    return {parse_datafile_name(file.name): file for file in path.iterdir() if is_datafile_path(file)}


# Level 1 directories like "v2=1", "v2=2", etc.

dir1_name_re = re.compile(r'^v2=(\d+)$')


#: compiled regex pattern to match level 1 directory names

def is_dir1_path(path: Path) -> bool:
    """
    Return ``True`` if path is a directory whose name is like 'v2=6', else ``False``.

    """
    return path.is_dir() and (dir1_name_re.match(path.name) != None)


def parse_dir1_name(name: str) -> Optional[int]:
    """
    Return the value of v2 encoded in the level 1 directory name if matched, else None.
    :param name: str, the level 1 directory name, e.g. "v2=3"
    :return: the integer value of v2 if name is valid, else None

    Examples
    ========

    >>> from acmpy.so5cg import parse_dir1_name
    >>> parse_dir1_name("v2=3")
    3
    >>> parse_dir1_name("xxx")

    """
    m = dir1_name_re.match(name)
    if (m):
        return int(m.group(1))
    return None


def dir1_dict(path: Path) -> dict:
    return {parse_dir2_name(dir2.name): dir2_dict(dir2) for dir2 in path.iterdir() if is_dir2_path(dir2)}


# SO5CG database base directory

default_base_name = expanduser('~/so5cg-data/')


def base_dict(base_path: Path) -> dict:
    return {parse_dir1_name(dir1.name): dir1_dict(dir1) for dir1 in base_path.iterdir() if is_dir1_path(dir1)}
