# Arthur's Journal 2022

## 2022-03-04

### 4:11 PM

It's hard to believe, but I made no progress on this project in 2021.
I'm now in the mood to reboot my efforts.
It would be nice if I had something to share at David Rowe's
memorial event which is scheduled for 2022-06-04.
That gives me three months to accomplish something.

My main goal is to convert the Maple ACM code to Python.
A less ambitious goal is to implement the SO(5) code in
Python.

I have spent a lot of time understanding the Python 
ecosystem, specifically SymPy, Sphinx, pytest, mypy.
I now have much more Python programming experience under
my belt and should be able to be more productive.

To resume development, here is a short list of 
housekeeping tasks:
- run the tests - DONE
- generate the Sphinx docs - DONE
- update the venv to Python 3.10 - DONE
- update the README.md file to include the dependencies - DONE

### 4:27 pm

The venv is already upgraded to Python 3.10.

Upgraded pip.

pip installed pytest.

Run pytest - OK.

### 4:34 pm

error trying to build Sphinx docs:

```text
/bin/sh: sphinx-build: command not found
make: *** [html] Error 127
```

pip install Sphinx and friends.

That helped. Now get a new error:

```
Running Sphinx v4.4.0
making output directory... done

Extension error (sympylive):
Handler <function builder_inited at 0x10e48de10> for event 'builder-inited' threw an exception (exception: 'Sphinx' object has no attribute 'add_javascript')
make: *** [html] Error 2
```

This error may be caused by a version mismatch.
I pip installed the latest version of Sphinx,
but I think the makefile is looking for it in a place outside the venv.
Yes, the extensions are stored in the `doc/ext` directory and I must have an
obsolete version of `sympylive.py` there.

I can comment out the reference to sympylive in the `doc/src/conf.py` file.

I can now run `make html` but I get some warnings:

```text
Running Sphinx v4.4.0
making output directory... done
building [mo]: targets for 0 po files that are out of date
building [html]: targets for 4 source files that are out of date
updating environment: [new config] 4 added, 0 changed, 0 removed
reading sources... [100%] modules/so5cg                                                                                                                                            
looking for now-outdated files... none found
pickling environment... done
checking consistency... done
preparing documents... done
writing output... [100%] modules/so5cg                                                                                                                                             
/Users/arthurryman/Documents/repositories/agryman/acmpy/acmpy/so5cg.py:docstring of acmpy.so5cg.datafile_dict:: WARNING: py:class reference target not found: pathlib.Path
/Users/arthurryman/Documents/repositories/agryman/acmpy/acmpy/so5cg.py:docstring of acmpy.so5cg.dir2_dict:: WARNING: py:class reference target not found: pathlib.Path
/Users/arthurryman/Documents/repositories/agryman/acmpy/acmpy/so5cg.py:docstring of acmpy.so5cg.is_datafile_path:: WARNING: py:class reference target not found: pathlib.Path
/Users/arthurryman/Documents/repositories/agryman/acmpy/acmpy/so5cg.py:docstring of acmpy.so5cg.is_dir1_path:: WARNING: py:class reference target not found: pathlib.Path
/Users/arthurryman/Documents/repositories/agryman/acmpy/acmpy/so5cg.py:docstring of acmpy.so5cg.is_dir2_path:: WARNING: py:class reference target not found: pathlib.Path
/Users/arthurryman/Documents/repositories/agryman/acmpy/acmpy/so5cg.py:docstring of acmpy.so5cg.load_datafile:: WARNING: py:class reference target not found: pathlib.Path
generating indices... genindex py-modindex done
writing additional pages... search done
copying static files... done
copying extra files... done
dumping search index in English (code: en)... done
dumping object inventory... done
build succeeded, 6 warnings.

The HTML pages are in _build/html.
```

There is a discussion of sympylive at: https://github.com/sympy/sympy/issues/22629

```text
Update: I obtained the sympylive Sphinx extension from https://github.com/sympy/sympy-live and followed the installation instructions:

$ git clone git://github.com/sympy/sympy-live.git
$ cd sympy-live
$ git submodule init
$ git submodule update
but $ sphinx-build -b html sourcedir builddir still throws the Could not import extension sympylive error. Do I have to import sympy-live into Sphinx somehow?
```

The Sphinx error is a version mismatch: https://github.com/sphinx-doc/sphinx/issues/7026

```text
It seems you've been used Sphinx-1.6.7. But add_js_file was added since 1.8. So please upgrade your Sphinx.
https://readthedocs.org/projects/webasedoc/builds/10269740/
https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_js_file
```

I have Sphinx v4.4.0 installed in my venv but perhaps my doc directory is out-of-date.
Defer fixing this for now.

5:46 pm break

## 2022-03-05

### 3:40 pm

Housekeeping
- set up the directory structure properly for a Python package - DONE
- move the Jupyter notebooks into a separate directory - DONE
- pip install the acmpy package as an editable package in the venv - DONE

Next: refactor project structure using best practices for Python packages, 
notebooks, articles as in centrifuge project. - DONE

What is the correct way to set up a Python package directory structure?
Follow the structure used in the `centrifuge` project repo:
- create a library root folder named `src` and put the Python code there
- add a `setup.py` file
- add a `README.md`
- add a `mypy.ini` file

### 5:15 pm

I committed and pushed the current changes.

break at 5:20 pm

## 2022-03-06

### 3:17 pm

After the above housekeeping, implement some new Python code, e.g.
- `show_CG_file()`
- work through `acm1.4a-examples.mw`
- note that the source file `acm1_4.py` is very long
  - it is copied from `acm1.4a-examples.mw` which contains eight sections
  - split up the Python code into the corresponding eight sections - DONE

Start implementation of `show_CG_file()`.
Since this function involves the SO5 Clebsch-Gordan coefficients,
put it in `so5cg.py`.

Actually, it would be better to split up the huge `acm1_4.py` file into the
eight sections and then incrementally implement the functions in their "proper"
files.

### 3:53 pm

Splitting up `acm1_4.py`. - DONE

### 4:40 pm

Focus on `so5_so3_cg.py` and implement `show_CG_file()`.
The Maple code used the keyword `local` to declare some
variables.
I've also seen the keywork `global`.
Understand the Maple semantics and map these onto Python
semantics.

I've found the latest Maple Programming Guide (2011).
The semantics is standard and aligns with Python.
Basically, to modify a variable that is declared
outside a function (procedure) you must declare it to be
global.

break 5:36 pm