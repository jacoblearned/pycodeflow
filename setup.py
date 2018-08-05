""" Setup info and logic """

import os
from setuptools import find_packages, setup
from pycodeflow import NAME, VERSION, DESC, AUTHOR, AUTHOR_EMAIL, URL, LICENSE


def read(fname):
    """ Return the contents of the given filename """
    with open(os.path.join(os.path.dirname(__file__), fname)) as content:
        return content.read()


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESC,
    long_description=read("README.md"),
    license=LICENSE,
    url=URL,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=(
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ),
)
