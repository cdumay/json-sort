# Configuration for Sphinx (json-sort documentation)
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

project = "json-sort"
copyright = "Cédric Dumay"
author = "Cédric Dumay"
release = "0.1"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode", "sphinx.ext.napoleon"]
templates_path = ["_templates"]
exclude_patterns = ["_build"]
html_theme = "alabaster"
autodoc_default_options = {"members": True, "undoc-members": False, "show-inheritance": True}
