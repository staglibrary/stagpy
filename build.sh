# In the 'stag' directory, run 'swig -c++ -python stag_internal.i'

# Example build process - updates will be needed to e.g. version numbers
python3 setup.py build_ext --inplace
python3 setup.py sdist bdist_wheel
auditwheel repair --plat manylinux_2_24_x86_64 -w dist/ dist/stag-0.1.4-cp38-cp38-linux_x86_64.whl
rm dist/stag-0.1.4-cp38-cp38-linux_x86_64.whl

# Then, upload the build wheel with 'twine upload dist/*'
