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
- note that the source file `acm1_4.py` is very long - DONE
  - it is copied from `acm1.4a-examples.mw` which contains eight sections
  - split up the Python code into the corresponding eight sections

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
I've also seen the keyword `global`.
Understand the Maple semantics and map these onto Python
semantics.

I've found the latest Maple Programming Guide (2011).
The semantics is standard and aligns with Python.
Basically, to modify a variable that is declared
outside a function (procedure) you must declare it to be
global.

break 5:36 pm

## 2022-03-07

## 10:44 am

Focus on `so5_so3_cg.py` and implement `show_CG_file()`.

Maple programs declare the types of arguments,
e.g. 

```text
show_CG_file:=proc(v1::nonnegint,
                   v2::nonnegint,a2::posint,L2::nonnegint,
                   v3::nonnegint)
```

Create Python functions to check the types. - DONE

The functions that read the Clebsch-Gordan coefficients
need to know the name of the base directory that contains
the files.
This name is stored in the global variable
`SO5CG_directory` and has the following
typical values:

```text
"/Users/arthurryman/so5cg-data/"
"/home/trevor/progs/so5/data/so5cg-data/"
"/home/twelsh1/projects/toronto/acm/so5cg-data/"
"/home/hs/staff/twelsh1/projects/toronto/acm/so5cg-data/"
```

Decide how to read this configuration value,
e.g. using `conf.py` as in Sphinx. - DEFER

See: https://www.doc.ic.ac.uk/~nuric/coding/how-to-handle-configuration-in-python.html

See: https://stackoverflow.com/questions/5055042/whats-the-best-practice-using-a-settings-file-in-python

Decide on the default value, and implement this. - DONE

I think `~/so5cg-data/` is a reasonable default value.
The following code is in `so5cg.py`:

```python
# SO5CG database base directory
from os.path import expanduser
default_base_name = expanduser('~/so5cg-data/')
```

break 1:00 pm

## 3:30 pm

I implemented the class `SO5CGConfig` to manage the
base directory, `SO5CG_directory`.
Use the following call:

```python
from acmpy.so5_so3_cg import SO5CGConfig
SO5CG_directory = SO5CGConfig.get_base_directory()
```

Implemented `SO5CG_filename()`.

Implement `label_list:=[]`.
What does the Maple expression `[]` mean?
Answer: the empty list.
Maple appears to be similar to Python
with respect to lists and sets.
List indexing starts at 1 in Maple, 0 in Python.

Are Maple `for` loop limits inclusive?
```text
for L1 from 0 to 2*v1 do
```

Answer: The loop limits are inclusive.
```text
1) Print even numbers from "6" to "10".

for i from 6 by 2 to 10 do  
    print(i)  
    end do;

                               6
                               8
                               10
```

break 5:30 pm

## 2022-03-08

### 4:17 pm

Understand Maple division.
Does it keep integers as integers or
does it convert them to floats? - DONE

Answer: Maple performs exact arithmetic.

This question arose while I was implementing
the function `dimSO5r3()`.
It uses integer quotient and remainder, but
one of the arguments would be a noninteger in general.

Review the code for `dimSO5r3()` and determine the mathematical
specification for it. - DONE

Here is the code:
```text
# The following procedure gives the multiplicity of SO(3) irreps of
# angular momentum L in the SO(5) irrep of seniority v. It uses (6).
# It then provides the maximum value of the "missing" label alpha
# (the minimum value is 1).

dimSO5r3:=proc(v::integer,L::integer,$)
  local b,d;

  if v<0 or L<0 or L>2*v then
    0:
  else
    b:=(L+3*irem(L,2))/2;
    if v>=b then
      d:=1+iquo(v-b,3);
    else
      d:=0;
    fi:
    if v>=L-2 then
      d:=d-iquo(v-L+2,3);
    fi:
    d:
  fi:
end:
```

The suspicious line is:
```text
    b:=(L+3*irem(L,2))/2;
```

We know that L is a positive integer.
There are two cases for L according to whether it is even or odd.

Case 1: L is even. Let L = 2n.
```text
b   = (2n + 3 * irem(2n, 2)) / 2
    = (2n + 3 * 0) / 2
    = (2n) / 2
    = n
    = L // 2
```

Case 2: L is odd. Let L = 2n + 1.
```text
b   = (2n + 1 + 3 * irem(2n + 1, 2)) / 2
    = (2n + 1 + 3 * 1) / 2
    = (2n + 4) / 2
    = n + 2
    = (L + 3) // 2
```

Therefore, in all cases the result of dividing by 2 results in an integer.
We can therefore correctly replace Python floating point division by Python integer division.

The code comments reference equation (6).
The file header comments state:
```text
# The equation numbers, section numbers and tables referred to in
# this file are those of the manuscript (version 1.4).
```

The file header identifies the manuscript as:
```text
# This code implements the ACM version of the Bohr model of the
# atomic nucleus. The manuscript
#   "A computer code for calculations in the algebraic collective
#    model of the atomic nucleus",
# by T.A. Welsh and D.J. Rowe [WR2015],
# describes the mathematical foundations of the code, and also
# serves as a manual. The manuscript (version 1.2) is available from
#   http://arxiv.org/abs/1408.3824 (v2).
# (A slightly improved version 1.3 was submitted for publication;
#  this is being updated to version 1.4 following referees' comments.)
```

I assume that version 1.4 is the most correct one. This is the version
that was published in Computer Physics Communications,
Volume 200, March 2016, Pages 220-253,
https://doi.org/10.1016/j.cpc.2015.10.017
and is available as v3 in the arXiv,
https://arxiv.org/abs/1408.3824.

Read (6). - DONE

The article refers to a book titled "Angular Momentum in Quantum Mechanics"
which defines Euler angles, Wigner D functions, etc.
I'll read that in order to get the definitions of these objects.

break 6:15 pm

## 2022-03-09

### 11:45 am

Implement dependencies of `show_CG_file()`:
- `get_CG_file()` - DONE

break 1:18 pm

### 3:43 pm

Implement
- `readdata_float()` - DONE
- `get_CG_file()` - DONE
- `show_CG_file()` - DONE

Implement the Maple worksheet `acm1.4a-examples.mw` 
as a Jupyter notebook - TODO

The Maple worksheet has 15 sections,
so it's probably a good idea to create one Jupyter
notebook per section.

break 6:30 pm

### 8:50 pm

Continue creating notebook.
- Section 1 created

- Section 1.1 - DONE

break 9:28 pm

## 2022-03-10

### 2:00 pm

- Section 1.2 - TODO: implement functions
  - start 2022-03-10 2:00 pm
  - implemented up to quad_rat_fun()
  - break 5:45 pm

break 5:45 pm

## 2022-03-11

### 3:07 pm

I've started to read the Maple Programming Guide.

- a Maple list is an immutable sequence so it is like a Python tuple
- a Maple unevaluated name is like a SymPy symbol

Defer further reading and make more progress converting the code.

- Section 1.2
  - continue to convert Maple code in the `globals.py` module
  - implemented up to the following proc:

```text
# lambda_davi_fun:=proc(C::constant)
#   local difffun:
#
#     difffun:=proc(v::nonnegint) option operator,arrow;
#        local diffint:
#        diffint:=floor(sqrt((v+1.5)^2+C)-sqrt(2.25+C)):
#        if type(diffint-v,odd) then
#          diffint+1:
#        else
#          diffint:
#        fi:
#     end:
#
#    difffun:
# end:
```
- What does this mean?: `difffun:=proc(v::nonnegint) option operator,arrow;`

Read Maple Help for `option`.

```text
Option operator declares to the Maple system that the 
procedure was entered and is to be printed and otherwise 
manipulated as an operator. Thus,
f := x -> x^2-1;
  is equivalent to
f := proc(x) option operator, arrow; x^2-1 
end proc;
Option arrow, in conjunction with option operator, indicates 
that the operator was initially entered using the -> notation. 
The use of option arrow also disables Maple simplification 
rules that add any non-local names in the operator 
expression to the parameter list. This option has no meaning 
for modules.
```

### 5:40 pm

Implemented up to `ACM_show_scales`.

break 5:40 pm

## 2022-03-12

### 5:27 pm

Next: continue implementing `ACM_*` functions in `globals.py`.

break 5:57 pm

## 2022-03-13

### 5:08 pm

Continue implementing `ACM_*` functions in `globals.py`.

### 6:51 pm

I have created stubs for all the remaining functions in `globals.py`.
Next, implement them.

break 6:56 pm

## 2022-03-14

### 9:21 pm

Merry Pi Day!

Q: What is the correct way to add docstrings for variables? 
A: Not possible. Only possible for modules, functions, classes, and methods.

Q: Do they follow the variable?
A: Docstrings are only associated with the module, function, class, or method.

Q: What about freestanding docstrings? 
A: Any string not assigned to a variable is treated like a comment.

Q: How do you get all the docstrings in a module?
A: Use the `__doc__` attribute of the module, function, class, or method.

Continue converting `globals.py`.
13 functions remain to be converted.

break 11:07 pm

## 2022-03-15

### 10:56 am

Next: `ACM_set_rat_lst` - DONE

break 11:30 am

## 2022-03-16

### 4:57 pm

Next: `ACM_show_rat_lst` - DONE

break 6:06 pm

### 9:12 pm

Next: `ACM_add_amp_lst` - DONE

Implemented up to `ACM_set_transition`

break 10:37 pm

## 2022-03-17

6 functions left

Next: `ACM_set_rat_form` - DONE

Implemented up to `ACM_set_basis_type`

break 5:36 pm

## 2022-03-18

### 2:29 pm

Next: `ACM_show_lambda_fun` - DONE

### 3:21 pm

I've implemented all functions in `globals.py`.
These call the following functions defined elsewhere:
* `Op_AM` - DONE
* `dimSO3` - DONE
* `CG_SO3` - DONE

`CG_SO3` calls `Wigner_3j`

Next: `Op_AM` - DONE

Next: `CG_SO3` - DONE

break 5:21 pm

## 2022-03-20

### 3:32 pm

Next: `Wigner_3j` - DONE

## 4:15 pm

All the functions called by the `ACM_*` functions are now implemented.

Continue: Implement the Maple worksheet `acm1.4a-examples.mw`
as a Jupyter notebook - TODO

Continue implementing notebook: `section-01-preliminaries`

Next: 1.2 Setting the default output format

After splitting up the code I am not hitting a circular import error:

```text
---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
Input In [1], in <module>
----> 1 from acmpy.globals import ACM_version
      3 ACM_version

File ~/Documents/repositories/agryman/acmpy/src/acmpy/globals.py:8, in <module>
      4 from typing import Callable, Optional
      6 from sympy import Symbol, pi, sqrt, Integer, Rational, Expr
----> 8 from acmpy.internal_operators import Operator, Op_AM
      9 from acmpy.spherical_space import dimSO3
     10 from acmpy.so5_so3_cg import CG_SO3, SO5Quintet, SO5Quartet

File ~/Documents/repositories/agryman/acmpy/src/acmpy/internal_operators.py:5, in <module>
      1 """5. Procedures that obtain the internal representation of operators."""
      3 from sympy import Expr
----> 5 from acmpy.globals import SpHarm_Operators, SpHarm_Table, Xspace_Pi, Xspace_PiPi2, Xspace_PiPi4
      7 Operator = tuple[tuple[Expr, tuple[Expr, ...]]]
      9 # ###########################################################################
     10 # ################# Representations of spherical harmonics ##################
     11 # ###########################################################################
   (...)
    575 #
    576 #

ImportError: cannot import name 'SpHarm_Operators' from partially initialized module 'acmpy.globals' (most likely due to a circular import) (/Users/arthurryman/Documents/repositories/agryman/acmpy/src/acmpy/globals.py)
```

* `globals.py` imports `internal_operators.py` for `Operator` and `Op_AM`
* `internal_operators.py` imports `globals.py` for `SpHarm_Operators`, `SpHarm_Table`, etc.

I think `globals.py` should be refactored.
* Move the definitions of the internal operators into `internal_operators.py` - DONE

### 5:46 pm

Determine the best type hint for angular momentum L, m - TODO.
In some places it if `nonnegint`, while in others it is `Rational`.
Does the Maple code ever allow it to be more general?
Do half odd integer values occur?

I've resolved the circular imports problem.
Continue implementing the notebook, section 1.2.

### 5:56 pm

Implemented up to `ACM_set_eig_fit` call in notebook.

break 5:56 pm

### 8:08 pm

Continue implementing notebook.

Error:

```text
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
Input In [14], in <module>
----> 1 ACM_set_rat_fit(100.0, 2, 0, 1, 1)

File ~/Documents/repositories/agryman/acmpy/src/acmpy/globals.py:792, in ACM_set_rat_fit(rat_fit, rat_L1, rat_L2, rat_1dx, rat_2dx, show)
    790     tran_fmat: str = glb_tran_format.format('{:d}', '{:d}', '{:d}', '{:d}')
    791     rat_fmt: str = glb_rat_format.format(tran_fmat, '{f}')
--> 792     rat_this: str = rat_fmt.format(glb_rat_L1, glb_rat_1dx,
    793                                    glb_rat_L2, glb_rat_2dx, glb_rat_fit)
    795     print(f'In ACM_Adapt, the scaling factor for "{glb_rat_desg}" ' +
    796           f'is chosen such that\n{rat_this}')
    798 return glb_rat_fit, glb_rat_L1, glb_rat_L2, glb_rat_1dx, glb_rat_2dx

KeyError: 'f'
```

Fixed '{f}' -> '{:f}'

Completed notebook section 1.

### 9:29 pm

Create notebook for section 2.

Implement `ACM_Hamiltonian()` - DONE

Completed notebook section 2.1.

break 11:12 pm

## 2022-03-21

### 2:00 pm

Implement notebook section 2.2. - TODO

`ACM_Scale` - DONE

Completed up to `RepSO5_Y_rem`

break 6:10 pm

## 2022-03-22

### 2:54 pm

Implement `RepSO5_Y_rem` - IN-PROGRESS

Implement all functions in `spherical_space.py` - DONE

Define stubs for all functions in `internal_operators.py` - DONE

break 7:00 pm

## 2022-03-23

### 5:10 pm

Implement `RepSO5_Y_rem` - DONE

Implement functions in `internal_operators.py` - TODO

break 6:27 pm

### 9:03 pm

Implement functions in `internal_operators.py` - IN-PROGRESS

`RepSO5_Y_alg` - DONE

`RepSO5_sqLdim` - DONE

`RepSO5_sqLdiv` - DONE

`RepSO5r3_Prod` - DONE

`RepSO5r3_Prod_rem` - DONE

`RepSO5r3_Prod_wrk` - DONE

break 11:00 am

## 2022-03-24

### 4:14 pm

Found bug in `RepSO5r3_Prod_wrk`.
See GitHub issue: https://github.com/agryman/acm16/issues/1

break 6:00 pm

### 7:30 pm

Implement functions in `internal_operators.py` - IN-PROGRESS

`NumSO5r3_Prod` - DONE

`ACM_HamRigidBeta` - DONE

Resolved bug: I was conflating two distinct lists, `SpHarm_Operators` and `Spherical_Operators`.

I am going to change the type of OperatorProduct and OperatorSum to
use lists instead of tuples for repeated elements.
Run `mypy` before this change: DONE
Make change: DONE
Run `mypy` after this change: DONE

break 9:42 pm

## 2022-03-25

### 2:22 pm

`ACM_HamSH3` - DONE

`ACM_HamSH6` - DONE

`Op_Parity` - DONE

`Op_Tame` - DONE

There is a bug in the Maple source for `Op_Tame`.
See https://github.com/agryman/acm16/issues/2

Implement functions in `internal_operators.py` - DONE

### 4:44 pm

Modules:

* `full_operators.py` - TODO
* `full_space.py` - TODO
* `globals.py` - DONE
* `hamiltonian_data.py` - TODO
* `internal_operators.py` - DONE
* `radial_space.py` - TODO
* `so5_so3_cg.py` - DONE
* `spherical_space.py` - DONE

### 5:21 pm

`full_operators.py` - IN-PROGRESS

Implemented up to `lbsXspace`.

break 5:58 pm

## 2022-03-26

### 3:13 pm

`full_operators.py` - IN-PROGRESS

* `RepXspace` - IN-PROGRESS

break 6:04 pm

### 7:37 pm 

* `RepXspace` - DONE

commit changes 9:18 pm
