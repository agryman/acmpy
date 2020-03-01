# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import sys
import inspect
import os
import subprocess
import sympy

# add path the acmpy project
sys.path.insert(0, os.path.abspath('../..'))

# If your extensions are in another directory, add it here.
sys.path = ['ext'] + sys.path

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.linkcode', 'sphinx_math_dollar',
              'sphinx.ext.mathjax', 'numpydoc', 'sympylive',
              'sphinx.ext.graphviz', 'matplotlib.sphinxext.plot_directive']

# Enable warnings for all bad cross references. These are turned into errors
# with the -W flag in the Makefile.
nitpicky = True

# To stop docstrings inheritance.
autodoc_inherit_docstrings = False

# MathJax file, which is free to use.  See https://www.mathjax.org/#gettingstarted
# As explained in the link using latest.js will get the latest version even
# though it says 2.7.5.
mathjax_path = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-AMS_HTML-full'

# See https://www.sympy.org/sphinx-math-dollar/
mathjax_config = {
    'tex2jax': {
        'inlineMath': [ ["\\(","\\)"] ],
        'displayMath': [["\\[","\\]"] ],
    },
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

suppress_warnings = ['ref.citation', 'ref.footnote']

# -- Project information -----------------------------------------------------

project = 'acmpy'
copyright = '2020, Arthur Ryman'
author = 'Arthur Ryman'

# The full version, including alpha/beta/rc tags
release = '1.0'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Don't show the source code hyperlinks when using matplotlib plot directive.
plot_html_show_source_link = False


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If false, no module index is generated.
#html_use_modindex = True
html_domain_indices = ['py-modindex']

# If true, the reST sources are included in the HTML build as _sources/<name>.
#html_copy_source = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'acmpydoc'

default_role = 'math'
pngmath_divpng_args = ['-gamma 1.5', '-D 110']
# Note, this is ignored by the mathjax extension
# Any \newcommand should be defined in the file
pngmath_latex_preamble = '\\usepackage{amsmath}\n' \
                         '\\usepackage{bm}\n' \
                         '\\usepackage{amsfonts}\n' \
                         '\\usepackage{amssymb}\n' \
                         '\\setlength{\\parindent}{0pt}\n'

texinfo_documents = [
    (master_doc, 'sympy', 'SymPy Documentation', 'SymPy Development Team',
     'SymPy', 'Computer algebra system (CAS) in Python', 'Programming', 1),
]

# Use svg for graphviz
graphviz_output_format = 'svg'


# Requried for linkcode extension.
# Get commit hash from the external file.
commit_hash_filepath = '../commit_hash.txt'
commit_hash = None
if os.path.isfile(commit_hash_filepath):
    with open(commit_hash_filepath, 'r') as f:
        commit_hash = f.readline()

# Get commit hash from the external file.
if not commit_hash:
    try:
        commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
        commit_hash = commit_hash.decode('ascii')
        commit_hash = commit_hash.rstrip()
    except:
        import warnings
        warnings.warn(
            "Failed to get the git commit hash as the command " \
            "'git rev-parse HEAD' is not working. The commit hash will be " \
            "assumed as the SymPy master, but the lines may be misleading " \
            "or nonexistent as it is not the correct branch the doc is " \
            "built with. Check your installation of 'git' if you want to " \
            "resolve this warning.")
        commit_hash = 'master'

fork = 'sympy'
blobpath = \
    "https://github.com/{}/sympy/blob/{}/sympy/".format(fork, commit_hash)


def linkcode_resolve(domain, info):
    """Determine the URL corresponding to Python object."""
    if domain != 'py':
        return

    modname = info['module']
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        return

    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
        except Exception:
            return

    # strip decorators, which would resolve to the source of the decorator
    # possibly an upstream bug in getsourcefile, bpo-1764286
    try:
        unwrap = inspect.unwrap
    except AttributeError:
        pass
    else:
        obj = unwrap(obj)

    try:
        fn = inspect.getsourcefile(obj)
    except Exception:
        fn = None
    if not fn:
        return

    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:
        lineno = None

    if lineno:
        linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
    else:
        linespec = ""

    fn = os.path.relpath(fn, start=os.path.dirname(sympy.__file__))
    return blobpath + fn + linespec

