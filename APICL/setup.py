from setuptools import setup

setup(
    name='APICL',
    version='0.1.0',
    py_modules=['APICL'],
    install_requires=[
        'Click', 'requests'
    ],
    entry_points={
        'console_scripts': [
            'APICL = APICL:cli',
        ],
    },
)
