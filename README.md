# acmpy: Algebraic Collective Model in Python
*Arthur Ryman, last updated 2026-10-28*

## Project Structure

The code for this project is stored in a GitHub repository named
[`agryman/acmpy`](https://github.com/agryman/acmpy).

The code is developed using PyCharm. 
The `.idea` directory contains PyCharm files.

The Python code is contained in the `src/acmpy` directory.

## Virtual Environment

This project runs in a Python 3 virtual environment
named `venv` that is created using the `venv` module.
See <https://docs.python.org/3/tutorial/venv.html> for information
about using virtual environments.

Create the virtual environment as follows.
Open a terminal window and change the current directory to the root directory of the `acmpy` project.
Then run the following command.

```shell script
python3 -m venv venv
```

This creates the `venv` directory and copies a set of files and directories into it.
The `venv` directory will not be checked in to git because it is excluded by the `.gitignore` file.

Activate the `venv` virtual environment:

```shell script
source venv/bin/activate
```

Alternatively, the `acmpy` project `bin` directory contains the `activate.sh`
shell script for activating the `venv` virtual environment:

```shell script
. bin/activate.sh
```

Install the required Python packages using `pip` as follows.
First install the latest version of `pip`.

```shell script
pip install -U pip
```

Next install the Python packages required to run, test, type check, and document the code:

```shell script
pip install numpy pandas matplotlib jupyter mypy pytest pytest-mypy
pip install Sphinx sphinx-math-dollar numpydoc
pip install sympy scipy
pip install setuptools build twine
```

Note that since Python 3.12, `venv` no longer installs `setuptools` by default.
It is required by `src/setup.py`.

Install the source code as an editable package.

```shell
cd src
pip install -e .
```

Finally, save the exact version information, so you can reliably reproduce the environment:

```shell script
pip freeze > requirements.txt
```

The virtual environment is now set up.
If you are using an integrated development environment like IntelliJ or PyCharm, configure
the project to use the Python interpreter in the virtual environment.
Its path relative to the project root is `venv/bin/python`.

To install the packages listed in `requirements.txt` into a new virtual environment:

```shell script
pip install -r requirements.txt
```

To list the installed modules:

```shell script
pip list
```

To launch the Python interpreter:

```shell script
python
```

To launch the Jupyter notebook server:

```shell script
jupyter notebook
```

To deactivate the virtual environment:

```shell script
deactivate
```

## Building and Publishing

The package metadata is defined in `src/setup.py`.
To build the source distribution and wheel:

```shell script
cd src
python -m build
```

The distribution files are written to the `src/dist` directory.
To upload them to PyPI:

```shell script
twine upload dist/*
```

Remember to increment `version` in `src/setup.py` before each upload,
because PyPI won't accept a version that has already been uploaded.

## Documentation

This project uses `Sphinx` for documentation.

The documentation is contained in the `doc` directory.
The documentation is generated from docstrings embedded in the Python source code.
To build the HTML documentation, do the following:

```shell script
cd doc
make html
```

The HTML documentation will be generated in the `doc/_build/html` directory.
Open the `index.html` file in a Web browser.

## Tests

This project uses `pytest` for testing.

Tests are placed in the `tests` directory within each module directory
and are named using the prefix `test_`. For example, the tests for `so5cg.py`
are defined in the file `tests/test_so5cg.py`.

To run all the tests, run the following command in the project root directory:

> pytest

Tests are also included in the docstrings of the Python source files.
To run the docstring tests, run the following command.

> pytest --doctest-modules

## Data Files

This project requires precomputed SO(5) > SO(3) Clebsch-Gordan coefficients.
They were computed by T.A. Welsh and distributed with the Maple ACM code
described in [WR2015](https://doi.org/10.1016/j.cpc.2015.10.017)
(CPC Program Library catalogue identifier AEYO_v1_0).

The coefficients are supplied in three zip files, which are stored in the
`data/so5cg` directory:

| File | Contents |
|------|----------|
| `so5cg-data13.zip` | coefficients for v2 = 1 and v2 = 3 |
| `so5cg-data24.zip` | coefficients for v2 = 2 and v2 = 4 |
| `so5cg-data56.zip` | coefficients for v2 = 5 and v2 = 6 |

Each zip file extracts into a top-level `so5cg-data/` directory.
To install the data in the default location `~/so5cg-data/`,
run the following commands in the project root directory:

```shell script
for z in data/so5cg/*.zip; do unzip -n "$z" -d ~; done
```

This creates the subdirectories `v2=1` through `v2=6`
(about 2,400 files, 244 MB).

To use a different location, extract the files there and configure
the base directory before computing any coefficients:

```python
from acmpy.so5_so3_cg import SO5CGConfig
SO5CGConfig.set_base_directory('/path/to/so5cg-data/')
```

Note that the tests in `src/acmpy/tests/test_so5cg.py` always read from `~/so5cg-data/`.
