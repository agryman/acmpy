# acmpy - Algebraic Collective Model in Python

## Virtual Environment

See <https://docs.python.org/3/tutorial/venv.html> for information
about using virtual environments.

This project is configured to run in a python3 virtual environment
named acmpy created by venv. 
This virtual environment can be created
by the IDE or via a command. 
The Python interpretter path is, e.g.

> /Users/arthurryman/.virtualenvs/acmpy/bin/python

To activate this virtual environment run the following bash commands:

> cd /Users/arthurryman/.virtualenvs
> source acmpy/bin/activate

To deactivate it:

> deactivate

This project uses the numpy and sympy modules so install them into the
activated virtual environment using this command:

> pip install numpy
> pip install sympy

To list the installed modules:

> pip list

To launch the Python interpretter:

> python




## Data Files

This project assumes that the precomputed SO5 > SO3 Clebsch-Gordan coefficients
have been installed in a directory, e.g.

> /Users/arthurryman/so5cg-data
