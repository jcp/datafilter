#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys

from io import open
from setuptools import find_packages, setup


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    shutil.rmtree("dist")
    shutil.rmtree("build")
    shutil.rmtree("datafilter.egg-info")
    sys.exit()

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "datafilter/__init__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name=about["__package_name__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    description=about["__description__"],
    include_package_data=True,
    license=about["__license__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.6",
    url=about["__url__"],
    version=about["__version__"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
