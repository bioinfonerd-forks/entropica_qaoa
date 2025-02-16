# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../../'))

from entropica_qaoa.qaoa.parameters import shapedArray



# -- Project information -----------------------------------------------------

project = 'Entropica QAOA'
copyright = '2019, EntropicaLabs'
author = 'Ewan Munro, Jan Lukas Bosse, Tommaso Demarie'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
        "sphinx.ext.todo",
        "sphinx.ext.napoleon",
        "sphinx.ext.autodoc",
	"sphinx.ext.coverage",
        "sphinx_autodoc_typehints",
        "sphinx.ext.mathjax",
        "sphinx.ext.ifconfig",
	"sphinx.ext.intersphinx",
	"nbsphinx"
]

napoleon_google_docstring = False
napoleon_use_param = True
napoleon_use_ivar = True

todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
html_static_path = []

# -- More customizations ----------------------------------------------------
# Document __init__ and __call__ functions
def skip(app, what, name, obj, would_skip, options):
    if name == "__call__":
        print("Documenting Call")
        return False

    if type(obj) == shapedArray:
        return True
    return would_skip

def setup(app):
    app.connect("autodoc-skip-member", skip)
