#!/usr/bin/env python

import io
import os
from setuptools import setup

# Package meta-data.
NAME = "p2j"
VERSION = "1.0.21"
DESCRIPTION = "p2j: Convert Python scripts to Jupyter notebook with minimal intervention"
URL = "https://github.com/raibosome/python2jupyter"
AUTHOR = "Raimi bin Karim"
AUTHOR_EMAIL = "raimi.bkarim@gmail.com"
PYTHON_REQUIRES = ">=3.6.0"

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
HERE = os.path.abspath(os.path.dirname(__file__))
try:
    with io.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# This call to setup() does all the work
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    python_requires=PYTHON_REQUIRES,
    license="MIT",
    entry_points={
        'console_scripts': [
            'p2j=p2j.p2j:main',
        ],
    },
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='convert python jupyter notebook script',
    packages=['p2j'],
    include_package_data=True
)
