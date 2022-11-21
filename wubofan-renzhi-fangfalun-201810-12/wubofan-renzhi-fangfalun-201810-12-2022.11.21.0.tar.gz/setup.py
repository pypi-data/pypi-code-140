#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import WubofanRenzhiFangfalun20181012
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('WubofanRenzhiFangfalun20181012'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="wubofan-renzhi-fangfalun-201810-12",
    version=WubofanRenzhiFangfalun20181012.__version__,
    url="https://github.com/apachecn/wubofan-renzhi-fangfalun-201810-12",
    author=WubofanRenzhiFangfalun20181012.__author__,
    author_email=WubofanRenzhiFangfalun20181012.__email__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Documentation",
        "Topic :: Documentation",
    ],
    description="吴伯凡认知方法论201810-12",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "wubofan-renzhi-fangfalun-201810-12=WubofanRenzhiFangfalun20181012.__main__:main",
            "WubofanRenzhiFangfalun20181012=WubofanRenzhiFangfalun20181012.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
