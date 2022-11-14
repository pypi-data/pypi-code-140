#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements, dependency_links = [], []
with open('requirements.txt') as f:
    for line in f.read().splitlines():
        requirements.append(line)

test_requirements = [ ]

setup(
    author="Bhanu Pallakonda",
    author_email='pvbhanuteja@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Convert form based PDF documents to web based froms or editable pdf forms. ",
    entry_points={
        'console_scripts': [
            'repaper=repaper.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='repaper',
    name='repaper',
    packages=find_packages(include=['repaper', 'repaper.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/pvbhanuteja/repaper',
    version='0.1.1',
    zip_safe=False,
)
