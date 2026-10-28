# acmpy

This package implements Python code for the Algebraic Collective Model.

## venv

Create a virtual environment as follows.

```shell script
cd <acmpy project root directory>
python3 -m venv venv
```

Start the venv and install the required packages

```shell script
source ./venv/bin/activate
pip install --upgrade pip
pip install setuptools build twine
pip install jupyter matplotlib seaborn sympy scipy mypy pytest numpy pandas
deactivate
```

Note that since Python 3.12, `venv` no longer installs `setuptools` by default.
It is required by `setup.py`.

To use this package in Jupyter notebooks, tests, etc, install it in your venv
as follows:
1. Start the venv in a command window, 
2. cd to the `src` directory, and
3. run the following command:

```shell script
pip install -e .
```

To use `tikzmagic` in a Jupyter notebook,
run the following command:

```shell script
pip install git+https://github.com/mkrphys/ipython-tikzmagic.git
```

To run the notebooks, activate the venv and do the following.

```shell script
cd <notebooks directory>
jupyter notebook
```

## Building and Publishing

To build the source distribution and wheel, activate the venv,
cd to the `src` directory, and run:

```shell script
python -m build
```

The distribution files are written to the `dist` directory.
To upload them to PyPI:

```shell script
twine upload dist/*
```

Remember to increment `version` in `setup.py` before each upload.
