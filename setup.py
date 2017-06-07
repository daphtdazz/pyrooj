#!/usr/bin/env python
import os
from codecs import open

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), 'r', 'utf-8') as handle:
    readme = handle.read()

setup(
    name='pyrooj',
    version='0.0.1',
    description='Implementation of RESTful Object-Oriented JSON in python',
    long_description=readme,
    author='daphtdazz',
    url='http://github.com/daphtdazz/pyrooj',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        'jsonschema~=2.6.0'
    ],
    extras_require={
        'develop': [
            "coverage==4.2",
            "flake8==3.2.1",
            "mccabe==0.6.1",
            "pycodestyle==2.3.1",
            "pyflakes==1.5.0",
            "pylint==1.7.1",
            "pytest==2.7.3",
            "pytest-cov==2.1.0",
            "pytest-timeout==0.4",
            "tox"
            # "urllib3==1.10.2",
            # "websocket-client==0.23.0",
        ],
        'docs': [
            # "pyenchant==1.6.6",
            # "Sphinx==1.3",
            # "sphinxcontrib-spelling==2.1.1",
            # "sphinx-nameko-theme==0.0.3",
        ],
    },
    entry_points={
    },
    zip_safe=True,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
