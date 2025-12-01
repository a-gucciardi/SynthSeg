#!/usr/bin/env python

import sys
import setuptools

python_version = sys.version[:3]

if sys.version_info[:2] not in [(3, 6), (3, 8), (3, 12)]:
    raise Exception('Setup.py only works with python version 3.6, 3.8 or 3.12, not {}.{}'.format(sys.version_info.major, sys.version_info.minor))

else:

    python_version_str = '{}.{}'.format(sys.version_info.major, sys.version_info.minor)
    with open('requirements_python' + python_version_str + '.txt') as f:
        required_packages = [line.strip() for line in f.readlines()]

    print(setuptools.find_packages())

    setuptools.setup(name='SynthSeg',
                     version='2.0',
                     license='Apache 2.0',
                     description='Domain-agnostic segmentation of brain scans',
                     author='Benjamin Billot',
                     url='https://github.com/BBillot/SynthSeg',
                     keywords=['segmentation', 'domain-agnostic', 'brain'],
                     packages=setuptools.find_packages(),
                     python_requires='>=3.6',
                     install_requires=required_packages,
                     include_package_data=True)
