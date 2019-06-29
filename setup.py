from setuptools import setup, find_packages

setup(
    name='2pm',
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
        commodity = 2pm.assets.commodities:commodity
        stock     = 2pm.assets.stocks:stock
        reit      = 2pm.assets.reits:reit
        fund      = 2pm.assets.funds:fund
        currency  = 2pm.referentials.currencies:currency
        industry  = 2pm.referentials.industries:industry
    ''',
)
