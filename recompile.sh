#!/usr/bin/env bash
# Helper bash script for recompiling the C++ side of the library
# For local testing only!
cd stag
swig -c++ -python -verbose stag_internal.i
cd ..
python setup.py build_ext --inplace
