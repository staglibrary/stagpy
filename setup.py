import os
import platform

from setuptools import setup, find_packages
from distutils.core import setup, Extension

import numpy

VERSION = '1.1.1'
DESCRIPTION = 'STAG: Spectral Toolkit of Algorithms for Graphs'
LONG_DESCRIPTION =\
    "This library provides several methods and algorithms relating to spectral graph theory in python."
URL = "https://staglibrary.io"

# Depending on the build platform, the required compiler flags are slightly
# different.
numpy_path = ""
if platform.system() == 'Linux':
    compile_args = ['-std=c++2a']
    numpy_path = os.path.join(numpy.__path__[0], 'core/include')
elif platform.system() == 'Windows':
    compile_args = ['/std:c++20']
    numpy_path = os.path.join(numpy.__path__[0], 'core\\include')
else:
    # Compile with clang on MacOS
    compile_args = ['-std=c++2a']
    numpy_path = os.path.join(numpy.__path__[0], 'core/include')

# specify the name of the extension and source files
# required to compile this
ext_modules = [Extension(name='stag._stag_internal',
                         sources=["stag/stag_internal_wrap.cxx",
                                  "stag/stag_lib/graph.cpp",
                                  "stag/stag_lib/random.cpp",
                                  "stag/stag_lib/graphio.cpp",
                                  "stag/stag_lib/cluster.cpp",
                                  "stag/stag_lib/utility.cpp",
                                  "stag/stag_lib/spectrum.cpp",
                                  "stag/stag_lib/KMeansRex/KMeansRexCore.cpp"
                                  ],
                         include_dirs=["stag/eigen-3.3.9",
                                       "stag/spectra-1.0.1",
                                       "stag/stag_lib",
                                       "stag/stag_lib/KMeansRex",
                                       numpy_path
                                       ],
                         extra_compile_args=compile_args)]

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
    install_requires=["scipy", "networkx", "matplotlib", "neo4j", "numpy"],
    long_description_content_type='text/markdown',
    url=URL,
    include_package_data=True,

    keywords=['python', 'spectral', 'graph', 'algorithms', 'clustering', 'cheeger'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        'Operating System :: POSIX :: Linux'
    ]
)
