# acmpy: Algebraic Collective Model in Python

## Virtual Environment

This project is configured to run in a python3 virtual environment
named `acmpy` created using the `venv` module.
See <https://docs.python.org/3/tutorial/venv.html> for information
about using virtual environments.

To create the virtual environment, do the following.
First create a directory where you want to keep all your virtual environments,
e.g. `~/.venv`.

> mkdir ~/.venv

Then make that the current directory and create the `acmpy` virtual envirnoment
in it.

> cd ~/.venv
>
> python3 -m venv acmpy

This creates the `acmpy` dircotry and copies a set of files and directories into it.
For example, the Python interpreter path is `~/.venv/acmpy/bin/python`

To activate the `acmpy` virtual environment run the following bash command:

> source ~/.venv/acmpy/bin/activate

The `bin` directory contains a shell script for activating the `acmpy`
virtual environment, which you can run in the Terminal window as follows:

> . bin/activate

To deactivate the virtual environment run:

> deactivate

This project uses the `numpy` and `sympy` modules so install them into the
activated `acmpy` virtual environment using this command:

> pip install numpy
>
> pip install sympy

To list the installed modules:

> pip list

To launch the Python interpreter:

> python

## Project Structure

The code for this project is stored in a GitHub repository named
[`agryman/acmpy`](https://github.com/agryman/acmpy).

The code is developed using IntelliJ. 
The `.idea` directory contains IntelliJ files.

The Python code is contains in the `acmpy` directory.

## Documentation

This project uses `Sphinx` for documentation.

The documentation is contained in the `doc` directory.
The documentation is generated from docstrings embedded in the Python source code.
To build the HTML documentation, do the following:

> cd doc
>
> make html

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
