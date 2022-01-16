#!/usr/bin/env python
import os
import sys
from setuptools import setup, Extension
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist
from distutils.spawn import find_executable
from glob import glob

if not find_executable('pytest'):
    print("Error:  please install pytest for running tests after build done\n"
          "        you can try: pip install pytest\n")
    sys.exit(1)
    
sources = glob('wiringOP/devLib/*.c')
sources += glob('wiringOP/wiringPi/*.c')
sources += ['wiringpi.i']

try:
    sources.remove('wiringOP/devLib/piFaceOld.c')
except ValueError:
    # the file is already excluded in the source distribution
    pass

# Fix so that build_ext runs before build_py
# Without this, wiringpi.py is generated too late and doesn't
# end up in the distribution when running setup.py bdist or bdist_wheel.
# Based on:
#  https://stackoverflow.com/a/29551581/7938656
#  and
#  https://blog.niteoweb.com/setuptools-run-custom-code-in-setup-py/
class build_py_ext_first(build_py):
    def run(self):
        self.run_command("build_ext")
        return build_py.run(self)

# Make sure wiringpi_wrap.c is available for the source dist, also.
class sdist_ext_first(sdist):
    def run(self):
        self.run_command("build_ext")
        return sdist.run(self)

_wiringpi = Extension(
    '_wiringpi',
    include_dirs=['wiringOP','wiringOP/wiringPi','wiringOP/devLib'],
    extra_compile_args = ["-DCONFIG_ORANGEPI_ZERO2", "-DCONFIG_ORANGEPI"],    
    swig_opts=['-threads'],
    extra_link_args=['-lcrypt', '-lrt'],
    sources=sources
)

setup(
    name = 'wiringpi',
    version = '2.60.1',
    ext_modules = [ _wiringpi ],
    py_modules = ["wiringpi"],
    install_requires=[],
    cmdclass = {'build_py' : build_py_ext_first, 'sdist' : sdist_ext_first}
)
