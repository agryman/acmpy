# Arthur's Journal

## 2019-12-08

### 8:28 AM

#### Recap

I started this project on 2019-06-24 after a conversation
with David Rowe.
David said that he had published a Maple program that
performed Algebraic Collective Model (ACM) computations in 2016,
but few other researchers were using it.
David thought that that main obstacle to adoption
was that Maple required the purchase of a licence.
David expressed a desired to see the program reimplemented in 
freely available computer language.
Since I was looking for a way to get re-engaged in math and physics,
I offerred to take on the task.

David published the ACM program in the journal Computer Physics
Communications (CPC).
I searched the CPC program library and found that Python was the most
popular language.
The Maple ACM program did both symbolic and numerical
computation so next I confirmed that Python had this capability.
The numerical computations were done to find the eigenvalues 
of the Hamiltonian matrix and used an industry standard Fortran library.
This same library was available in the Python numpy package.
Symbolic computation can be done in Python using the SymPy package. 
Furthermore, Maple notebooks could be replaced by Python Jupyter notebooks.
I therefore recommended that we selected Python as the target language.

I gathered all the Maple code and stored it in the GitHub repository
named acm14.
This repo contains both version 16 and 1.4 which is the published version.
I collected relevant publications there too.

David generously purchased a Maple licence for me.
Was able to run the Maple code.

I then created the acmpy repo to store the Python code.

### 8:47 AM - break

---

## 2019-12-09

### 5:08 PM

The ACM makes use of pre-computer SO(5) > SO(3) Clebsch-Gordan coefficients
that are stored in disk files.
My first Python programming goal is to read these files.
I created so5cg.py for that purpose.

### 5:13 PM break

---

## 2019-12-14

### 10:57 AM
- implement so5cg.py
- use regex
- see <https://docs.python.org/3/howto/regex.html#regex-howto>
- read this article
- coded parsing function parse_v2
- next <https://docs.python.org/3/howto/regex.html#grouping>

### 12:18 PM - break

---

### 1:03 PM
- continue reading


### 2:39 PM
- finished regex article
- work on parsing a single line of the data file
- does Python have C-line scanf?
- no, but I can split the line by whitespace using the re.split() function
- trim the leading leading and trailing whitespace using string strip() function
- convert to float and int using float() and int()

### 3:00 PM - break

###8:38 PM
- continue parsing line of file
- done
- read file and parse lines
- done

### 9:51 PM - break

---

## 2019-12-15

### 4:12 PM

- continue coding so5cg.py
- I implemented loading of all the files into a dictionary
- it takes around 1 minute to load all CG files
- change this to lazy loading since some calculations won't need all the files
- just scan the directories initially and save the Path in the dictionary
- on a request to retrieve the CG coefficient, check the existence of the Path entry on load it, 
replacing the Path with the CG values loaded from the file
- done loading just the file paths, this is very fast
- next implement the retrieval operation
- the theory behind the calculation is described in 
Construction of SO(5) ⊃ SO(3) spherical harmonics and 
Clebsch–Gordan coefficients by M.A. Caprio , D.J. Rowe , T.A. Welsh
- that paper gives Mathmatica code and some calculated values
- Welsh calculated the values provided here with unpublished C++ code
- skim the paper
- read the Maple code to understand the API

---

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
- while the tests were stilling in the sympy project I viewed `README.rst` but the preview window showed errors
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
 
 ### SymPy - Getting Started
 
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
 
 ### SymPy - Narrative Documentation Guidelines
 
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
 and moving al the Python source files into it
 - recall that after activating the `acmpy` virtual environment, I can interactively
 test modules, e.g. `acm1_4.py` by running `python -i -m acm1_4` 
 - I am overloading the name `acmpy` - it is a GitHub repo, an IntelliJ project,
 a Python venv, a Python package, and a Python module.
 
 ### 6:15 PM - break
 
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
- there is a support for creating a Run Configuration under Python Docs -> Sphinx Task which
is described here: <https://www.jetbrains.com/help/pycharm/run-debug-configuration-sphinx-task.html>
- add a docstring to a Python source file and include it in the API documentation
- I am going to use the Sphinx project structure as a model, but it differs from the 
structure generated by `sphinx-quickstart`
- align the `acmpy` structure with that of Sphinx

### 12:24 PM - break

### 3:12 PM

- I created a test module name `acmpy.gamma` and added docstrings to it, including math
- I replicated more of the structure of SymPy, including a `modules` directory and created an index and
page for gamma. This seems very manual in contrast to say javadoc but it does provide a lot
of control over the page content. Docstrings from the module are pulled into the rst file
using several directives such as `automodule` and `autofunction`. I assume that each doctring in
a module can be assessed individually. I need to read the Sphinx documentation more closely.
- I copied much of the Sphinx `conf.py` content, pip installed various extensions, and eventually
succeeded in building the html for the `gamma` module including the typeset math.
I was unable to get the `sympylive` extension working, but I don't need it yet.
Now I have a template to work from.
- add a `clean` target to the make file and rebuild from scratch. Success.
Remember that the build requires that the acmpy virtual environment be activated

### 5:18 PM - break

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
    - allow it might make sense in the log run to contribute acmpy to sympy, they may feel it is too niche
    - I'd prefer to use unittest since it is more mainstream
    - if there ever is an appreciable user base for acmpy then we can convert the tests
    - it's premature to assume SymPy would want acmpy
    - Conclusion: stay with unittest, and add doctests to unittest
        - NOTE: I reversed this decision and am using pytest

### 11:23 PM - break

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
- I converted my tests to pytest. All ran as expected. pytest much simpler.
- added an exception test - OK
- Run doctests using pytest: `pytest --doctest-modules`
    - this runs all the tests in both the test functions and the docstrings
- Conclusion: pytest has a simpler syntax, integrates doctests easily, and is compatible with
the SymPy guidelines
docstrings from a module

### 6:03 PM - break

## 2020-02-05

### 2:34 PM
- DONE: Simplify the Sphinx documentation by using a directive that pulls in all the members.
    - I added the :members: option to so5cg.py

### 2:51 PM - break

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

## 2020-03-03

### 9:49 AM
- continue defining tests and docs for so5cg.py

### 12:26 PM - break

## 2020-03-04

### 10:11 AM
- continue refactoring docs and tests for so5cg.py
- organize code bottom-up since Python does not allow forward references 

### 11:00 AM - break
