# /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>

"""
from setuptools import setup, find_packages

setup(
    name='json-sort',
    version=open('VERSION', 'r').read().strip(),
    description="Just a tiny tool to sort keys in a json file",
    long_description=open('README.rst', 'r').read().strip(),
    classifiers=["Programming Language :: Python"],
    keywords='',
    author='Cedric DUMAY',
    author_email='cedric.dumay@gmail.com',
    url='https://github.com/cdumay/json-sort',
    license='Apache License',
    py_modules=['json_sort'],
    include_package_data=True,
    zip_safe=True,
    install_requires=open('requirements.txt', 'r').readlines(),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points="""
[console_scripts]
json-sort-fromfile = json_sort.scripts:fromlocal
json-sort-fromremote = json_sort.scripts:fromurl
"""
)
