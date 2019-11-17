#!/usr/bin/env python

import io
import os
from setuptools import setup

# Package meta-data.
VERSION = "1.3.2"
DESCRIPTION = "p2j: Convert Python scripts to Jupyter notebook with minimal intervention"

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
HERE = os.path.abspath(os.path.dirname(__file__))
try:
    with io.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
        LONG_DESCRIPTION = '\n' + f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION

# This call to setup() does all the work
setup(
    name="p2j",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/raibosome/python2jupyter",
    author="Raimi bin Karim",
    author_email="raimi.bkarim@gmail.com",
    python_requires=">=3.6.0",
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
