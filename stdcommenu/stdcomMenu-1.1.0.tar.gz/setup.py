import setuptools
from setuptools import setup


setup(
    name='stdcomMenu',
    version='1.1.0',
    license_files = ('LICENSE.txt',),
    packages=['stdcomMenu','bin' ],
    package_dir={'': 'src'},
    url='http://www.vremsoft.com',
    license='',
    author='ed',
    author_email='srini_durand@yahoo.com',
    description='Stec Railway Version StandAlone Subscribers'      ,
    classifiers = [
                  "Programming Language :: Python :: 3",
                  "Programming Language :: Python :: 3.5",
                  "Programming Language :: Python :: 3.6",
                  "Programming Language :: Python :: 3.7",
                  "Programming Language :: Python :: 3.8",
                  "Programming Language :: Python :: 3.9",
                  "Programming Language :: Python :: 3.10",
                  "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                  "Operating System :: OS Independent",
              ],


    requires = ["setuptools", "wheel","PyQt5"],
    install_requires =["PyQt5"],
    include_package_data=True

)
