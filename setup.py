#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages, Extension
from distutils.spawn import find_executable
from glob import glob

if not find_executable('pytest'):
    print("Error:  please install pytest for running tests after build done\n"
          "        you can try: pip install pytest\n")
    sys.exit(1)
    
sources = glob('wiringOP/devLib/*.c')
sources += glob('wiringOP/wiringPi/*.c')
sources += ['wiringpi_wrap.c']

sources.remove('wiringOP/devLib/piFaceOld.c')

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
    version = '2.32.1',
    author = "Philip Howard",
    author_email = "phil@gadgetoid.com",
    url = 'https://github.com/WiringPi/WiringPi-Python/',
    description = """A python interface to WiringPi 2.0 library which allows for
    easily interfacing with the GPIO pins of the Raspberry Pi. Also supports
    i2c and SPI""",
    long_description=open('README.md').read(),
    ext_modules = [ _wiringpi ],
    py_modules = ["wiringpi"],
    install_requires=[],
    headers=glob('wiringOP/wiringPi/*.h')+glob('wiringOP/devLib/*.h')
)
