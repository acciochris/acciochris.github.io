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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "Chris Liu's Blog"
copyright = "2023, Chris Liu"
author = "Chris Liu"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "ablog",
    "sphinx_design",
]
myst_enable_extensions = [
    "dollarmath",
    "deflist",
    "colon_fence",
    "linkify",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_title = project
html_logo = "_static/avatar.png"
html_favicon = "_static/avatar.png"
html_theme_options = {
    "repository_url": "https://github.com/acciochris/acciochris.github.io",
    "use_repository_button": True,
    "logo": {
        "text": project,
    }
    #    "footer_icons": [
    #        {
    #            "name": "GitHub",
    #            "url": "https://github.com/acciochris",
    #            "html": "",
    #            "class": "fa-brands fa-solid fa-github fa-2x",
    #        },
    #    ],
}
html_copy_source = False
html_sidebars = {
    "**": [
        "navbar-logo.html",
        "search-field.html",
        "sbt-sidebar-nav.html",
        "ablog/postcard.html",
        "ablog/recentposts.html",
        "ablog/tagcloud.html",
        "ablog/categories.html",
        "ablog/archives.html",
    ]
}
html_css_files = [
    "giscus-custom.css",
]

# Myst configuration
myst_heading_anchors = 3

# ABlog configuration
blog_path = "posts"
blog_title = project
blog_post_pattern = "posts/*.md"
blog_baseurl = "https://acciochris.github.io"
