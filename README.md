# acmpy: Algebraic Collective Model in Python

## Project Structure

The code for this project is stored in a GitHub repository named
[`agryman/acmpy`](https://github.com/agryman/acmpy).

The code is developed using IntelliJ. 
The `.idea` directory contains IntelliJ files.

The Python code is contains in the `acmpy` directory.

## Virtual Environment

This project runs in a Python 3 virtual environment
named `venv` that is created using the `venv` module.
See <https://docs.python.org/3/tutorial/venv.html> for information
about using virtual environments.

Create the virtual environment as follows.
Open a terminal window and change the current directory to the root directory ot the `acmpy` project.
The run the following command.

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
pip install numpy
pip install sympy
pip install Sphinx
pip install sphinx-math-dollar
pip install pytest
pip install mypy
pip install pytest-mypy
pip install matplotlib
pip install numpydoc
pip install jupyter
```

Finally, save the exact version information, so you can reliably reproduce the environment:

```shell script
pip freeze > requirements.txt
```

The virtual environment is now set up.
If you are using an integrated development environment like IntelliJ or PyCharm, configure
the project to use the Python interpretter in the virtual environment.
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
and defined in the file `tests/test_so5cg.py`.

To run all the tests, run the following command in the project root directory:

> pytest

Tests are also included in the docstrings of the Python source files.
To run the docstring tests, run the following command.

> pytest --doctest-modules

## Data Files

This project assumes that the precomputed SO5 > SO3 Clebsch-Gordan coefficients
have been installed in a directory outside of this project, e.g. `~/so5cg-data`.
