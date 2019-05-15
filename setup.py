#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


install_requires = ['graphql-core>=2.1,<3']
tests_require = ['pytest', 'pytest-benchmark', 'snapshottest', 'wheel']

setup(
    name='graphql-core-printers',
    version='0.0.1',
    author='Tomasz Kontusz',
    author_email='tomasz.kontusz@gmail.com',
    maintainer='Tomasz Kontusz',
    maintainer_email='tomasz.kontusz@gmail.com',
    license='MIT',
    url='https://github.com/ktosiek/graphql-core-printers',
    description="Print GraphQL queries while masking secrets. Useful for logging with graphql-core.",
    long_description=read('README.rst'),
    packages=['graphql_printers'],
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
)
