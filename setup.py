from setuptools import setup, find_packages

VERSION = '0.1'
DESCRIPTION = 'STAG - Spectral Algorithms for Graphs'
LONG_DESCRIPTION =\
    "This library provides several methods and algorithms relating to spectral graph theory in python."

# Setting up
setup(
    name="stag",
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
