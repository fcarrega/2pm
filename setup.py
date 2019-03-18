# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='2:00 PM',
    version='0.1',
    description='Personal Portfolio Manager',
    author='F. Carrega',
    author_email='fabrice.carrega@gmail.com',
    packages=find_packages(),

    install_requires=[
        'Click',
    ],

    entry_points='''
        [console_scripts]
        help      = 2pm.2pm:help
        currency  = 2pm.currencies:currency
        industry  = 2pm.industries:industry
        commodity = 2pm.commodities:commodity
        stock     = 2pm.stocks:stock
        reit      = 2pm.reits:reit
        fund      = 2pm.funds:fund
        order     = 2pm.orders:order
        position  = 2pm.positions:position
    ''',
)
