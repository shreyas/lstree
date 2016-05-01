#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

test_requirements = [
    'pytest'
]

setup(
    name='lstree',
    version='0.1.0',
    description="lstree is for ls what pstree is for ps, and some more",
    long_description=readme + '\n\n' + history,
    author="Shreyas Kulkarni",
    author_email='shyran@gmail.com',
    url='https://github.com/shreyas/lstree',
    packages=[
        'lstree',
        'lstree.nodes',
        'lstree.nodetree'
    ],
    package_dir={'lstree': 'lstree'},
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'lstree = lstree.__main__:main',
        ],
    },
    license="MIT",
    zip_safe=False,
    keywords='lstree',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
