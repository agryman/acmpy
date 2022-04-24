# Arthur's Journal

## 2020-01-08

### 9:23 PM

- I have read the Maple code and found the API declaration for the
reduced SO(5) > SO(3) Clebsch-Gordan coefficients
- The Maple code is one large source file, internally divided into
five sections
- as a first pass, attempt to translate the code verbatim into Python
- after that is accomplished, refactor the code into modules and classes
- The treatment of the operators used to define a Hamiltonian requires
the use of symbolic computation
- read the SymPy tutorial at <https://docs.sympy.org/1.5.1/tutorial/index.html>

### 10:23 PM - break

- next: <https://docs.sympy.org/1.5.1/tutorial/intro.html>, A More Interesting Example

---

## 2020-01-18

### 5:13 PM

- I have finished reading the SymPy tutorial
- now I'm ready to begin the conversion from Maple to Python
- as a first attempt, start with the main Maple source file
which is acm1.4.mpl, copy it to acm.py, and comment out every line so it becomes 
valid (but useless) Python code
- need to understand what the Maple op function does when acting on table indices

### 6:54 PM - break

---

## 2020-01-19

### 11:35 AM

- start a Maple session, load acm1.4.mpl, and inspect SpTable and the op function
- conversions are more or less straightforward so far
- some question about Convert_112 being redefined after use
- converted up to Convert_red

### 1:06 PM - break

---

## 2020-01-24

### 12:00 PM

- thinking ahead, if I expect this code to be used by other people then it needs to be
clearly documented
- the SymPy project has very clear documentation guidelines at
<https://docs.sympy.org/1.5.1/documentation-style-guide.html>
- the SymPy documentation allows LaTeX expressions to be embedded
- spend some time reading the style guide and understand how to generate HTML from the Python source
code
- I forked and cloned sympy from github to try running the documentation generation tools
- I created a new IntelliJ project from the sympy sources, creating a new virtual environment
- I ran `pip install mpmath` in the sympy virtual environment
- I ran `bin/test` which runs all the sympy tests, looks OK but is taking time to complete
- while the tests were still running in the sympy project I viewed `README.rst` but the preview window showed errors
associated with `.. code-block:: python` directives, `Cannot analyze code. Pygments package not found.`
- I presume that I need to `pip install Pygments` in the sympy virtual environment since it is the
project interpreter
- when the tests finish, run `bin/doctest` and install any missing dependencies
- tests completed ok
- ran `brew install imagemagick graphviz docbook librsvg` but this had the side-effect of
rebuilding Python
- in the sympy virtual environment, `pip install Pygments` fails, as does `pip list` with the error message
`dyld: Library not loaded: /usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/Python
   Referenced from: /Users/arthurryman/.virtualenvs/sympy/bin/python
   Reason: image not found
 Abort trap: 6`
    - looks like brew may have deleted an older version of Python
    - installing the packages triggered a run of `brew cleanup`
    - yes, `3.7.5` is gone, `3.7.6_1` has replaced it
    - can I update a virtual environment, or do I need to recreate it?
 
### 12:24 PM - break

---

## 2020-01-25
 
### 10:00 AM
 
#### Virtual Environment Problem
 
 - Recall that while setting up my fork of the `sympy` repo I had to run `brew` to install several
 dependencies, and this had the side-effect of building a new version of Python, namely `3.7.6_1`.
 - `brew cleanup` automatically deleted the previous version `3.7.5`, 
 which broke two virtual environments, `sean` and `sympy`
 - today I tried to fix the problem and first checked three other virtual environments, 
 `acmpy	myvenv	sandbox` which were OK
 - I believe the difference between these environments is that I created the three OK ones 
 via the command line, but the broken ones via the IntelliJ project creation wizard
 - on closer inspection, the IntelliJ wizard refers to `Virtualenv` which is another tool for
 creating virtual environments
 - Apparently `virtualenv` was created first and then partially integrated into Python 3.3 as `venv`
 - I created a new directory named `.venv` to make it clear that I used the `venv` module to create
 the virtual environments
 - I used the `venv` module which is a standard part of Python, like so:
 
 > `python3 -m venv sympy`
 
 - Perhaps `venv` is more compatble with `brew`?
 - now the virtual environments are working correctly
 
#### SymPy - Getting Started
 
 - Recall that I am setting up a SymPy development environment so I can understand how 
 modules are documented, especially the ability to include math
 - I'd like to include math in the `acmpy` documentation to link it with the papers that
 describe the theory
 - Also, good documentation is required for engaging the community
 - I had to install `Pygments` to get the `README.rst` file to display Python code blocks
 and I can preview the RST documents
 - Continue with the Getting Started intructions at
 <https://docs.sympy.org/1.5.1/documentation-style-guide.html#getting-started>
 - run `pip install mpmath matplotlib sphinx sphinx-math-dollar`
 - Installation complete
 - was able to generate the HTML version of the `sympy` docs
 
#### SymPy - Narrative Documentation Guidelines
 
 - next read 4. Parameters Section at
 <https://docs.sympy.org/1.5.1/documentation-style-guide.html#parameters-section>
 
### 12:00 PM - break
 
### 5:30 PM
 
 - finished reading the sympy doc guidelines
 - initially, acmpy is standalone, not a contribution to sympy
 - learn how to set up documentation generation in acmpy using Sphinx
 - API documentation is generated from docstrings, see
 <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>
 - browse the main site:
 <https://www.sphinx-doc.org/en/master/index.html>
 - activate `acmpy` and run `pip install -U Sphinx`
 - I also ran `brew install sphinx-doc` but this was probably unnecessary - it doesn't put Sphinx
 on the PATH
 - I can run `sphinx-build --version` successfully in the acmpy virtual environment
 - I reorganized the `acmpy` project by creating a top level Python package named `acmpy`
 and moving all the Python source files into it
 - recall that after activating the `acmpy` virtual environment, I can interactively
 test modules, e.g. `acm1_4.py` by running `python -i -m acm1_4` 
 - I am overloading the name `acmpy` - it is a GitHub repo, an IntelliJ project,
 a Python venv, a Python package, and a Python module.
 
### 6:15 PM - break

---
 
## 2020-01-26
 
### 10:57 AM
 
- I have read enough about Sphinx to get started
- active acmpy and run `sphinx-quickstart` to set up the Sphinx documentation structure in the project
- the command ran successfully but when I view `index.rst` I see error messages like
 `System Message: ERROR/3 (<stdin>, line 9) Unknown directive type "toctree"` and a similar one for the
 "ref" directive.
- these errors must be a problem with the IntelliJ ReST plugin - it is not using the project virtual
 environment
- apparently the IntelliJ plugin uses docutils to generate the preview so the Sphinx directives
 are not recognized
- I deleted the files and directories that were created so I can regenerate using a separate doc directory
- Now the Sphinx files are in the `source` directory, the make files are still in the root
- I ran `make html` in the terminal window and 
 successfully generated the skeleton of the documentation
- there is integrated support for Sphinx described here:
 <https://www.jetbrains.com/help/pycharm/generating-reference-documentation.html>
- there is support for creating a Run Configuration under Python Docs -> Sphinx Task which
is described here: <https://www.jetbrains.com/help/pycharm/run-debug-configuration-sphinx-task.html>
- add a docstring to a Python source file and include it in the API documentation
- I am going to use the Sphinx project structure as a model, but it differs from the 
structure generated by `sphinx-quickstart`
- align the `acmpy` structure with that of Sphinx

### 12:24 PM - break

### 3:12 PM

- I created a test module named `acmpy.gamma` and added docstrings to it, including math
- I replicated more of the structure of SymPy, including a `modules` directory and created an index and
page for gamma. This seems very manual in contrast to say javadoc but it does provide a lot
of control over the page content. Docstrings from the module are pulled into the rst file
using several directives such as `automodule` and `autofunction`. I assume that each doctring in
a module can be accessed individually. I need to read the Sphinx documentation more closely.
- I copied much of the Sphinx `conf.py` content, pip installed various extensions, and eventually
succeeded in building the html for the `gamma` module including the typeset math.
I was unable to get the `sympylive` extension working, but I don't need it yet.
Now I have a template to work from.
- add a `clean` target to the make file and rebuild from scratch. Success.
Remember that the build requires that the acmpy virtual environment be activated

### 5:18 PM - break

---

## 2020-02-01

### 5:04 PM

- DONE: Move the makefile into the `doc` directory like in SymPy. That may simplify the paths
and enable the build to find the `sympylive` extension.
- yes, the build now finds the `sympylive` extension

- I tried running the `acmpy.gamma` example in SymPy Live from the generated html pages, 
but got this error `ImportError: No module named acmpy.gamma`

- DEFERRED: Determine how SymPy Live searches for modules to import.
    - I haven't solved this but I assume that I need to install the `acmpy` package in the Python
    environment that SymPy Live uses.
    - Defer this since what I really need to do at development time is run doctest on the example.
    - I can run doctest in IntelliJ using the context menu or a Run Configuration

- DONE: split out the tests from the `so5cg` module into a separate file and learn how to run the
tests. Copy the test approach from SymPy.
    - SymPy appears to use embedded `assert` statements which means it doesn't use a test runner.
    - IntelliJ has nice integrated support for the `unittest` library, so I'll uses that.
    - I created a test class for `acmpy.gamma` and ran it.
    
### 7:09 PM - break

### 8:15 PM

- DONE: Review the `unittest` docs at:
<https://docs.python.org/2/library/unittest.html>
- DONE: Review the PyCharm documentation for unit testing at:
<https://www.jetbrains.com/help/pycharm/testing-your-first-python-application.html>
- DONE: Investigate using `doctest` with `unittest` at:
<https://docs.python.org/2/library/doctest.html>
    - I added examples to so5cg.py and called doctest at the bottom of the file, when called as the main module
    - I added the -v parameter to the Run Configuration to see the doctest progress
- I created docstrings in so5cg.py and created a Sphinx documentation page for it, including some good math markup
- DONE: check if the SymPy contribution guidelines allow unittest, or do they require pytest? If pytest is required
then cut over now before profilerating a lot of unittest test cases
    - looks like SymPy uses it's own variant of pytest:
    <https://github.com/sympy/sympy/wiki/Running-tests>
    - although it might make sense in the long run to contribute acmpy to sympy, they may feel it is too niche
    - I'd prefer to use unittest since it is more mainstream
    - if there ever is an appreciable user base for acmpy then we can convert the tests
    - it's premature to assume SymPy would want acmpy
    - Conclusion: stay with unittest, and add doctests to unittest
        - NOTE: I reversed this decision and am using pytest

### 11:23 PM - break

---

## 2020-02-02

### 4:07 PM
- Happy Palindrome Day!
- I am reconsidering the test technology. I read the docs for `pytest` at:
<https://docs.pytest.org/en/latest/getting-started.html>
- pytest seems to be more modern than unittest, and is certainly less verbose
- DONE: understand the SymPy variant of pytest. See:
<https://github.com/sympy/sympy/wiki/Running-tests>
    - I believe `py.test` is a variant spelling of `pytest`, or perhaps a shell command
    - I believe that SymPy uses the pytest syntax, namely just include `assert` statements in the code
    - To run all tests or doctests, copy the files `bin/test` and `bin/doctest` from SymPy
    - No, it seems that the commands from SymPy test the `sympy` code base
    - Just use vanilla `pytest` and `doctest`
- in the terminal, activated the acmpy venv and ran: `pip install -U pytest`
- created `tests/test_sample.py`
- in the terminal, ran `pytest`
    - pytest found and ran all the tests, including the ones defined using `unittest`
- I converted my tests to pytest. All ran as expected. pytest is much simpler.
- added an exception test - OK
- Run doctests using pytest: `pytest --doctest-modules`
    - this runs all the tests in both the test functions and the docstrings
- Conclusion: pytest has a simpler syntax, integrates doctests easily, and is compatible with
the SymPy guidelines
docstrings from a module

### 6:03 PM - break

---

## 2020-02-05

### 2:34 PM
- DONE: Simplify the Sphinx documentation by using a directive that pulls in all the members.
    - I added the :members: option to so5cg.py

### 2:51 PM - break

---

## 2020-03-01

### 2:51 PM
- Updated README.md to refer to .venv, and described testing and documentation.
- IN PROGRESS: complete the documentation and test creation for so5cg.py as is.
    - Reviewed the Maple code and determine the meaing of the parameters.
- TO DO: refactor so5cg.py as a class.

### 5:45 PM - break

## 2020-03-02

### 11:24 AM
- continue defining tests and docs for so5cg.py

### 11:36 AM - break

---

## 2020-03-03

### 9:49 AM
- continue defining tests and docs for so5cg.py

### 12:26 PM - break

---

## 2020-03-04

### 10:11 AM
- continue refactoring docs and tests for so5cg.py
- organize code bottom-up since Python does not allow forward references 

### 11:00 AM - break

---

## 2020-03-05

### 11:10 AM
- continue refactoring docs and tests for so5cg.py
- TO DO: write a test SO5CG database in a temporary directory 
to use as a test fixture

### 12:15 PM - break

---

## 2020-03-14

### 5:21 PM

- Happy International Day of Mathematics (IDM) 
aka Pi Day!
- continue writing tests for so5cg.py
- I am putting type annotations on all functions as part of
their documentation
- In Progress: Read https://www.python.org/dev/peps/pep-0483/
- In Progress: This is a good cheat sheet: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html

### 6:06 PM - break

---

## 2020-03-15

- continue reading about type annotations:
https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
    - this cheat sheet is for a Python package names `mypy`
    - Mypy is a static type checker for Python 3 and Python 2.7.
    - finished reading the cheat sheet
- pytest seems to understand the type annotations, or maybe raw Python does
    - probably not, but there is a package that integrates mypy into pytest:
    https://pypi.org/project/pytest-mypy/
- continue reading PEP 483:
https://www.python.org/dev/peps/pep-0483/
    - DONE
    - it gets very complicated, however the typing theory for Python meshes well with Z
    in the sense that I can express the Z type constructors in Python
- skim PEP 484 Type Hints:
https://www.python.org/dev/peps/pep-0484/ 
    - strongly inspired by `mypy`
    - types are implemented in the module `typing` 
    - this is a very long PEP
    - I know enough now to annotate the functions in `acmpy`
- NEXT: finish the test fixtures by creating an SO5CG database in a temporary directory

### 12:25 PM - break

---

## 2020-03-22

### 11:00 AM

- continue developing tests for SO5CG
- I added type annotations to so5cg.py
- pytest has built-in fixtures for temporary directories, namely pass in
the argument named `tmpdir` or `tmp_path` to the test function or method
- see https://docs.pytest.org/en/latest/fixture.html#fixtures

### 1:05 PM - break
    
### 3:30 PM

- review pytest fixtures
- wrote tests in test_so5cg.py
- TODO: document the meaning of the labels for level 2 directories and data files

### 6:19 PM - break

---

## 2020-04-02

### 10:59 AM

- document the meaning of the labels for level 2 directories and 
data files - DONE
- TODO: implement the on-demand file loading

### 11:53 AM break

---

## 2020-04-09

### 5:15 PM Update to IntelliJ 2020.1

- moved virtual environment into project and captured project requirements
- updated README.md with new procedure for creating a virtual environment

### 6:45 pm break

---

## 2020-04-10

### 11:15 am

- finish so5cg.py
    - remove obsolete code from so5cg.py
    - remove print statements from test_so5cg.py
    - create a Jupyter notebook to document so5cg.py

### 12:22 pm break

### 4:18 pm
- created notebook and described group theory basis for ACM

### 6:44 pm break

---

## 2020-04-13

### 10:36 am

- I am refreshing my memory about group representation
theory, reading the references on SO(5) > SO(3)
- Write up my notes in a Jupyter notebook, and use SymPy
- Start by creating a notebook for the SymPy tutorial
- The tutorial is based on the one given at SciPy 2013 
http://certik.github.io/scipy-2013-tutorial/html/index.html
- The tutorial cites Sage which aims to be a full-featured system
for mathematics. It uses SymPy. Going forward, I will look into Sage.
It may be a better way to present acmpy to nuclear physicists.
The acmpy code will be based on SymPy and not have any dependencies
on Sage, but there may be benefits to using Sage.
- read up to: Basic Operations

### 12:30 pm break

### 1:36 pm

- I downloaded and installed the Mac app version of Sage-0.9.
    - I immediately ran into a security error. The app is not signed so
macOS Catalina 10.15.4 won't open it.
    - The workaround was described in AskSage.
You have to open System Preferences -> Security & Privacy -> General where
the app is now listed. Click its button to allow it to be opened.
    - I launched the app and got the error "Jupyter Server failed to start".
    Again, the workaround was in AskSage at
    https://ask.sagemath.org/question/49381/sagemath-90-app-macos-jupyter-server-fails-to-start/
    You have to open a Terminal and launch the sage app. 
    This fixes up all the paths. 
    Type quit(). 
    Then launch the app. 
    Now it opens a Jupyter server.
    - My first impression is very negative. 
    SageMath appears to be a poorly integrated
    grab bag of every piece of open source software that can be used for math. 
    It even includes R. 
    What's the advantage of using it versus the individual pieces?
    Is it just a packaging effort?
    - I am going to defer further investigate. 
    Maybe read the PDF book I downloaded.
    It might provide some motivation.
- continue with SymPy tutorial: Basic Operations
- read up to: Simplification

### 3:45 pm break

---

## 2020-04-14

### 5:17 am

- SymPy tutorial: Simplification
- read up to: Special Functions

### 6:28 am break

### 9:24 pm
- SymPy tutorial: Special Functions
- read up to: Solvers

### 11:07 pm break

---

## 2020-04-16

### 4:44 pm

- SymPy tutorial: Solvers
- finished reading Matrices
- next: Advanced Expression Manipulation
- finished tutorial

### 6:39 pm break

---

## 2020-04-18

- Sympy Module Reference: Vector 
https://docs.sympy.org/latest/modules/vector/index.html
- next: Dyadics

### 2:30 pm break

### 3:00 pm
- reading: https://docs.sympy.org/latest/modules/vector/examples.html

### 5:48 pm break

### 8:04 pm
- reading: https://docs.sympy.org/latest/modules/vector/examples.html
- reading: https://docs.sympy.org/latest/modules/vector/api/classes.html

### 9:20 pm break

---

## 2020-04-19

### 9:30 am
- scanned handwritten notes on SO(3) < SO(5) geometry
- Jupyter notebooks do not allow me to define LaTeX macros using \newcommand
    - I recall that this used to work
    - find where I used this previously
    - if this is a bug, learn how to report it to the Jupyter project
- work on using SymPy to decompose representations of SO(3) and explicitly
construct the subgroup inclusion SO(3) < SO(5)
- use Matrix class to represent vectors, dual vectors, linear transformations,
tensor products, etc.

### 1:00 pm break

### 4:51 pm
- continue writing SO(3) < SO(5) notebook

### 6:10 pm break

### 9:18 pm
- continue writing SO(3) < SO(5)

### 9:53 pm break

---

## 2020-04-24

### 2:33 pm

- I wrote up some notes using my tablet and would like to create a nice article
using Z notation, illustrated by SymPy examples
- How can I combine Z and Jupyter?
- In the `acmpy/so5cg-notebook.ipynb`, some `\newcommand` macros work, 
others are rendered as `undefined` in the IntelliJ notebook viewer,
but all macros do work correctly in Jupyter.
- Compare to `notes/so3-so5-subgroup-chain.ipynb` 
- Is there a difference in the virtual environments I've been using?
- Compare the in-project `venv` to  `~/.venv/acmpy`
    - I was NOT using Jupyter in `~/.venv/acmpy`
- I copied the `\newcommand` syntax from `acmpy/so5cg-notebook.ipynb` into
`notes/so3-so5-subgroup-chain.ipynb`
    - it appears to work correctly now
    - NO, it is erratic. Sometimes the macros are executed and sometimes
    they get inlined as red text.
- I added the macros to a Raw NBConvert Cell
    - sometimes they get picked up, sometimes they don't
    - they do get picked up when I save the notebook as PDF or LaTeX
- I think the correct way to get the macros to render is to use MathJax
    - create a MathJax extension that contains the macros
    - this will allow sharing across notebooks and the Web
- read MathJax docs
- This is getting too complicated
- There is a JavaScript hook for Jupyter that allows the definition of
MathJax macros
    - `~/.jupyter/custom/custom.js`
    - try to put common MathJax macros there
    - see https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/JavaScript%20Notebook%20Extensions.html#
    
### 5:40 pm break

---

## 2020-04-25

### 10:42 pm

- I have been running into problems with how Jupyter notebooks render
LaTeX `\newcommand`. It's been very erratic. Sometimes the macros are
handled. Sometimes that are simply rendered as red text.
- The problem may be in either Jupyter or MathJax.
- Try to recreate the problem in MathJax. 
    - See https://docs.mathjax.org/en/latest/index.html
    - Today the notebook is behaving correctly!
    - Perhaps the red text was really caused by syntax errors?
    - Defer further investigation of MathJax until I encounter a reproducible error.
- Write up my notes on SO(3) < SO(5) in a Z spec.
    - Use pure LaTeX
    - Use a Jupyter notebook for examples
    - Maybe use TikZ for drawings
    - Maybe create a Jupyter extension to render Z, implement this like
    the TiKZ extension 
        - use LaTeX directly to render the Z notation instead of 
        trying to induce MathJax to do it.
    - created `so3-so5.tex` and friends

### 12:08 pm break

### 1:00 pm

- write `so3-so5.tex`
- while writing the spec, I looked for some standard notation
and found this wiki dedicated to mathematical proofs:
https://proofwiki.org/wiki/Symbols:R

### 6:09 pm break

---

## 2020-04-26

### 11:00 am
- continuing writing `so3-so5.tex`
- TODO: develop the approach of asserting that a binary operation
defines a group, and then producing the unique identity element and
inverse operation from it, e.g. for addition define 0 to be the unique identity
element and -x to be the unique inverse of x.

### 12:32 am break

### 1:43 pm

- defer going into depth of abstract algebra
- focus on group representations
- change of plan: there are no shortcuts so develop the foundations

### 6:20 pm

---

## 2020-04-27

### 7:23 am

- write `so3-so5.tex`

### 8:00 am break

### 10:30 am

- continue

### 12:27 pm break

### 3:13 pm

- continue

### 4:00 pm break

---

## 2020-04-29

### 10:30 am

- created new repo named `mathz` to contain articles on standard
mathematical objects such as real numbers and vector spaces
- moved articles from other repos into `mathz`
- TODO: refactor `so3-so5.tex` article to use definitions from `mathz` - DONE

### 12:00 pm break

### 1:37 pm

- refactor `so3-so5.tex`
- all common definitions have been moved to `mathz` repo
- TODO: simplify definitions in `mathz`

### 5:49 pm break

### 7:52 pm

- continue with `groups.tex`

### 9:16 pm break

---

## 2020-05-01

### 11:42 am

- continue with `groups.tex`

### 12:25 pm break

### 1:49 pm

- continue with `groups.tex` - DONE
- TODO: `vectors.tex` - use Abelian groups as base

### 4:43 pm break

---

## 2020-05-02

### 1:12 pm

- continue work on `mathz` repo
- refactor `real-numbers.tex` - DONE
- refactor `vector-spaces.tex`

### 2:27 pm break

---

## 2020-05-03

### 2:34 pm

- refactor `vector-spaces.tex`

### 6:25 pm break

---

## 2020-05-23

### 3:26 pm

- refactor `vector-spaces.tex`

### 5:57 pm break

---

## 2020-05-24

### 1:23 pm

- refactor `vector-spaces.tex`
- refactored definitions for real vector spaces
- TODO: improve consistency of naming - DONE
- TODO: refactor definitions for continuity and differentiability - DONE

### 5:28 pm break

---

## 2020-05-25

### 10:30 am

- improve consistency of naming in vector-spaces.tex - DONE

### 12:41 pm break

### 3:31 pm

- improve definitions of continuous functions - DONE

### 4:12 pm

- improve definitions of differentiable functions - DONE

### 6:04 pm break