#!/usr/bin/env python

from setuptools import setup, find_packages
setup(
    name="dbc-data-generator",
    version="0.1",
    packages=find_packages(),
    scripts = ['bin/main.py']
)
