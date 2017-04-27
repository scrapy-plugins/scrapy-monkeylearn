#!/usr/bin/env python
from setuptools import setup

setup(
    name='scrapy-monkeylearn',
    version='0.3.0',
    description='MonkeyLearn pipeline for Scrapy',
    author='Fernando Borretti',
    author_email='fernando@tryolabs.com',
    maintainer='Scrapinghub',
    maintainer_email='opensource@scrapinghub.com',
    packages=['scrapy_monkeylearn'],
    install_requires=[
        'Scrapy>=1.0',
        'monkeylearn>=0.2.4',
        'six>=1.5.2'
    ],
    classifiers=[
        'Framework :: Scrapy',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
