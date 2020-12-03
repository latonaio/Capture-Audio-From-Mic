# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from setuptools import setup, find_packages

setup(
    name="capture-audio",
    version="0.0.1",
    author="Latona",
    packages=find_packages("./src"),
    package_dir={"":"src"},
    install_requires=[],
    tests_require=[]
)
