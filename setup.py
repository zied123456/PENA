#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='PENA',
    version='0.1.0',
    description="PENA's Entirely New Akinator",
    long_description=open('README.md').read(),
    license='MIT',
    keywords="artificial intelligence prolog game",
    packages=['pena'],
    install_requires=['pyswip_alt', 'flask', 'tinydb', 'jsonschema'],
    extras_require={
        'dev': ['pep8'],
    },
    entry_points={
        'console_scripts': [
            'pena=pena.bootstrap:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
