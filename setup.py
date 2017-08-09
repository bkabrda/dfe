#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='dfe',
    version='0.1.0',
    description='Dockerfile Expand',
    long_description=open('README.md').read(),
    keywords='dockerfile, template, render, expand',
    author='Slavek Kabrda',
    author_email='bkabrda@redhat.com',
    url='https://github.com/bkabrda/dfe',
    license='BSD',
    packages=['dfe'],
    platforms='any',
    install_requires=[
        'Jinja2',
        'PyYAML',
    ],
    entry_points={
        'console_scripts': ['dfe=dfe.bin:main'],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ]
)
