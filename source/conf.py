import os
import sys
import django

sys.path.insert(0, os.path.abspath('..'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'dj.settings'
django.setup()

html_baseurl = 'https://delovoyb.github.io/dj_first/'

project = 'dj_first'
copyright = '2024, DanilaB'
author = 'DanilaB'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
