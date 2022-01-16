#!/bin/bash
python3 generate-bindings.py > bindings.i
swig -python wiringpi.i
python3 setup.py clean --all
sudo python3 setup.py build install
sudo python3 tests/test.py
