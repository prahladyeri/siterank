#!/usr/bin/env python3
import os
import siterank
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

s = setup(
	name='siterank',
	version=siterank.__version__,
	license='MIT',
	description=siterank.__title__,
	long_description=read("README.md"),
	long_description_content_type='text/markdown',
	keywords="internet",
	url='https://github.com/prahladyeri/siterank',
	packages=find_packages(),
	include_package_data=True,
	entry_points={
		"console_scripts": [
			"siterank = siterank.siterank:main",
		],
	},
	install_requires=['requests'],
	author='Prahlad Yeri',
	author_email='prahladyeri@yahoo.com',
	)
