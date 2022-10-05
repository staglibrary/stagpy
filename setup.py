from setuptools import setup, find_packages
from distutils.core import setup, Extension

VERSION = '0.1'
DESCRIPTION = 'STAG - Spectral Algorithms for Graphs'
LONG_DESCRIPTION =\
    "This library provides several methods and algorithms relating to spectral graph theory in python."

# specify the name of the extension and source files
# required to compile this
# ext_modules = [Extension(name='swig.stag_internal',
#                          sources=["swig/stag_internal.i"],
#                          swig_opts=["-c++"],
#                          # libraries=['Eigen'],
#                          # library_dirs=["eigen-3.3.9"],
#                          include_dirs=["eigen-3.3.9", "stag_lib"])]

ext_modules = [Extension(name='swig._stag_internal',
                         sources=["swig/stag_internal_wrap.cxx", "stag_lib/stag.cpp", "stag_lib/utility.cpp"],
                         include_dirs=["eigen-3.3.9", "stag_lib"])]

# Setting up
setup(
    name="stag",
    ext_modules=ext_modules,
    version=VERSION,
    author="Peter Macgregor",
    author_email="<macgregor.pr@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["scipy"],
    long_description_content_type='text/markdown',

    keywords=['python', 'spectral', 'graph', 'algorithms', 'clustering', 'cheeger'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        'Operating System :: POSIX :: Linux'
    ]
)
