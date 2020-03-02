r"""
This module implements the lookup of precomputed $\textrm{SO}(5) \supset \textrm{SO}(3)$ Clebsch-Gordan coefficients.
These coefficients have been precomputed by another program and saved in a set of files.
The files are arranged as a set of nested directories.
The file and directory names encode some of the parameters of the coefficients.
Each file contains a set of coefficient values, one per line, along with the remainder of their parameters.

We'll refer to the precomputed data as the SO5CG database.

The database is stored in some base directory which can be anywhere on the file system, e.g. ~/so5cg-data/.
The base directory may contain other files and directories.
Only those directories that have a name that matches a certain pattern, e.g. v2=4, are significant.
We refer to those as level 1 directories.

The level 1 directory name encodes an integer, namely the value of the v2 parameter.
For example, the name v2=4 encodes the value 4.
The only significant contents of a level 1 directory is a level 2 directory.

The name of a level 2 directory matches a pattern that encodes 3 parameter values.
For example, the name SO5CG_1_2_3 encodes the values 1, 2, and 3.


build up the database from the bottom up
leaf nodes are text files, e.g.
dir1: v2=2
  dir2: SO5CG_1_2_3
      file: SO5CG_1_2-1-2_3
          line: +1.000000e+00      1    1    2      2    1    2      3    1    0
          line: +8.451543e-01      1    1    2      2    1    2      3    1    3
          line: +7.237469e-01      1    1    2      2    1    2      3    1    4
      file SO5CG_1_2-1-4_3
          line: +5.345225e-01      1    1    2      2    1    4      3    1    3
          line: -6.900656e-01      1    1    2      2    1    4      3    1    4
          line: +1.000000e+00      1    1    2      2    1    4      3    1    6

each dir1 name encodes 1 number, aka v2, an integer
each dir2 name encodes 3 numbers, all integers
each file name encodes 5 numbers, all integers
each line contains 10 numbers, the first is a float, the rest are integers

mathematically, we have a function that maps a tuple of 9 integers to a float.
however, most of the 9-tuples map to zero, so this is a very sparse array.
we can store it as a tower of nested dictionaries, indexed by 9-tuples

The Maple code contains a procedure show_CG_file(v1, v2, a2, L2, v3) and load_CG_table(v1, v2, a2, L2, v3)
which loads a file from disk.

The files are loaded on demand since there are many files and not all of them are used
in any given calculation.
The contents of the files are stored in a table named CG_coeffs which is like a Python
dictionary.
CG_coeffs[v1, v2, a2, L2, v3] is a table of CG coefficient values contained in a single data file.
CG_coeffs[v1, v2, a2, L2, v3][a1, L1, a3, L3] is the actual CG coefficient value.

The parameters have the following types:
v1, v2, v3: nonnegint
a2: posint
L2: nonnegint

The data is stored in the file named SO5CG_v1_v2-a2-L2_v3.

My interpretation is as follows:
Clearly, the representations of SO5 > SO3 are labelled by (v, a, L) where (v, a) label an SO5 irrep.
v is called the seniority.
a is a multiplicity parameter used to distinguish irreps that have the same v.
L is the SO3 irrep label.
When the SO5 irrep labelled by (v, a) is restricted to the SO3 subgroup, it splits into SO3 irreps labelled by L.

The Maple procedure SO5CG_filename(v1, v2, a2, L2, v3) generates the file path as follows:
cat(SO5CG_directory, "v2=", v2, "/SO5CG_", v1, "_", v2, "_", v3, "/SO5CG_", v1, "_", v2, "-", a2, "-", L2, "_", v3);

"""

from pathlib import Path
from os.path import expanduser
import os
import re

default_SO5CG_directory = expanduser('~/so5cg-data/')

def is_dir(name: str) -> bool:
    """Return True if a string is the name of a directory, else return False."""
    return Path(name).is_dir()

# regex pattern to match v2 directory names like "v2=1", "v2=2", etc.
v2_dir_pattern = r'^v2=(\d+)$'

# compiled regex to match v2 directory names
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

    >>> from acmpy.so5_cg import parse_v2
    >>> parse_v2("v2=3")
    3
    >>> parse_v2("xxx")


    """
    m = v2_dir_re.match(name)
    if(m):
        v2_str = m.group(1)
        return int(v2_str)
    return None

# TO DO: define a class to represent the database of precomputed SO5 > SO3 Clebsch Gordan coefficients
# class SO5_SO3_CG:

if __name__ == "__main__":
    v2_dirs = [(entry.name, parse_v2(entry.name)) for entry in os.scandir(default_SO5CG_directory) if entry.is_dir() and parse_v2(entry.name)]
    print(v2_dirs)

    test1_dir1_name = 'v2=2'
    test1_dir2_name = 'SO5CG_1_2_3'
    test1_file_1_name = 'SO5CG_1_2-1-2_3'
    test1_file_2_name = 'SO5CG_1_2-1-4_3'

def parse_line(line: str):
    if not type(line) is str:
        raise TypeError("line is not a str")
    fields = re.split(r'\s+', line.strip())
    if(len(fields) != 10):
        raise("line does not have 10 fields")

#    return float(fields[0]), tuple([int(x) for x in fields[1:]])
    return float(fields[0]), tuple(int(x) for x in fields[1:])

if __name__ == "__main__":

    test_line_1 = ' +1.000000e+00      1    1    2      2    1    2      3    1    0'
    test_line_2 = ' +8.451543e-01      1    1    2      2    1    2      3    1    3'
    test_line_3 = ' +7.237469e-01      1    1    2      2    1    2      3    1    4'

    print(parse_line(test_line_1))
    print(parse_line(test_line_2))
    print(parse_line(test_line_3))

    base_dir = Path(default_SO5CG_directory)
    test1_dir1 = base_dir / test1_dir1_name
    test1_dir2 = test1_dir1 / test1_dir2_name
    test1_file_1 = test1_dir2 / test1_file_1_name
    test1_file_2 = test1_dir2 / test1_file_2_name
    test1_paths = [test1_dir1, test1_dir2, test1_file_1, test1_file_2]

def load_file(file):
    f = file.open()
    lines = [parse_line(line) for line in f]
    f.close()
    return lines

if __name__ == "__main__":

    print(test1_file_1, load_file(test1_file_1))
    print(test1_file_2, load_file(test1_file_2))

# create predicates for levels 1, 2, and 3

# level 1 is a directory whose name is like v2=1
level_1_re = re.compile(r'^v2=(\d+)$')
def is_level_1(path: Path) -> bool:
    """Returns True if and only if path is a directory whose name is like 'v2=6'.

    """
    return path.is_dir() and (level_1_re.match(path.name) != None)

if __name__ == "__main__":

    print('Level 1 test:', test1_dir1.name, is_level_1(test1_dir1))
    print('Level 1 test:', test1_dir2.name, is_level_1(test1_dir2))
    print('Level 1 test:', test1_file_1.name, is_level_1(test1_file_1))
    print('Level 1 test:', test1_file_2.name, is_level_1(test1_file_2))

level_2_re = re.compile(r'^SO5CG_(\d+)_(\d+)_(\d+)$')
def is_level_2(path):
    """Returns True is and only if path is a directory whose name is like 'SO5CG_1_2_3'.

    """
    return path.is_dir() and (level_2_re.match(path.name) != None)

if __name__ == "__main__":

    print('Level 2 test:', test1_dir1.name, is_level_2(test1_dir1))
    print('Level 2 test:', test1_dir2.name, is_level_2(test1_dir2))
    print('Level 2 test:', test1_file_1.name, is_level_2(test1_file_1))
    print('Level 2 test:', test1_file_2.name, is_level_2(test1_file_2))

level_3_re = re.compile(r'^SO5CG_(\d+)_(\d+)-(\d+)-(\d+)_(\d+)$')
def is_level_3(path):
    """Returns True if and only if path is file whose name is like 'SO5CG_1_2-1-4_3'.

    """
    return path.is_file() and (level_3_re.match(path.name) != None)

if __name__ == "__main__":

    print('Level 3 test:', test1_dir1.name, is_level_3(test1_dir1))
    print('Level 3 test:', test1_dir2.name, is_level_3(test1_dir2))
    print('Level 3 test:', test1_file_1.name, is_level_3(test1_file_1))
    print('Level 3 test:', test1_file_2.name, is_level_3(test1_file_2))

    print('Level 1 test:', [(path.name, is_level_1(path)) for path in test1_paths])
    print('Level 2 test:', [(path.name, is_level_2(path)) for path in test1_paths])
    print('Level 3 test:', [(path.name, is_level_3(path)) for path in test1_paths])

# parse the names for each level

def parse_level_1(name: str) -> int:
    m = level_1_re.match(name)
    if(m):
        return int(m.group(1))
    return None

def parse_level_2(name: str) -> tuple:
    m = level_2_re.match(name)
    if(m):
        return tuple(int(m.group(i)) for i in range(1,4))
    return None

def parse_level_3(name: str) -> tuple:
    m = level_3_re.match(name)
    if(m):
        return tuple(int(m.group(i)) for i in range(1,6))
    return None

if __name__ == "__main__":

    print('Level 1 parse:', test1_dir1.name, parse_level_1(test1_dir1.name))
    print('Level 2 parse:', test1_dir2.name, parse_level_2(test1_dir2.name))
    print('Level 3 parse:', test1_file_1.name, parse_level_3(test1_file_1.name))
    print('Level 3 parse:', test1_file_2.name, parse_level_3(test1_file_2.name))

# make the dictionaries for each level, bottom up

def dict_level_3(file: Path) -> dict:
    """Returns the level 3 file contents as a dictionary of lines.

    """
    lines = load_file(file)
    return {line[1]: line[0] for line in lines}

if __name__ == "__main__":

    print('Level 3 dict:', test1_file_1.name, dict_level_3(test1_file_1))
    print('Level 3 dict:', test1_file_2.name, dict_level_3(test1_file_2))

def dict_level_2(dir: Path) -> dict:
    """Returns a dictionary of file paths for the level 3 files.

    """
    return {parse_level_3(file.name): file for file in dir.iterdir() if is_level_3(file)}

if __name__ == "__main__":

    print('Level 2 dict:', test1_dir2.name, dict_level_2(test1_dir2))

def dict_level_1(dir1: Path) -> dict:
    return {parse_level_2(dir2.name): dict_level_2(dir2) for dir2 in dir1.iterdir() if is_level_2(dir2)}

if __name__ == "__main__":

    print('Level 1 dict:', test1_dir1.name, len(dict_level_1(test1_dir1)))

def dict_level_0(dir0: Path) -> dict:
    return {parse_level_1(dir1.name): dict_level_1(dir1) for dir1 in dir0.iterdir() if is_level_1(dir1)}

if __name__ == "__main__":

    print('Level 0 dict:', base_dir.name, len(dict_level_0(base_dir)))

if __name__ == "__main__":
    import doctest
    doctest.testmod()