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
pip install --upgrade pip setuptools
pip install wheel 
pip install jupyter matplotlib seaborn sympy mypy pytest numpy pandas
deactivate
```

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
pip install git+git://github.com/mkrphys/ipython-tikzmagic.git
```

To run the notebooks, activate the venv and do the following.

```shell script
cd <notebooks directory>
jupyter notebook
```
