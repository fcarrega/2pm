# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='Finance',
    version='0.0.1',
    description='Personal Finance Management',
    long_description=readme,
    author='Fabrice Carrega',
    author_email='fabrice.carrega@gmail.com',
    url='',
    packages=find_packages(exclude=('tests', 'docs'))
)
