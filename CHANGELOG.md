# Changelog
All notable changes to the library are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.1] - 2025-2-11

### Added
- Add builds for Python 3.13

## [2.1.0] - 2024-07-09

### Added
- [Issue #66](https://github.com/staglibrary/stagpy/issues/66): Add save_matrix method
- Add equality checking between dense matrix objects.

### Fixed
- [Issue #68](https://github.com/staglibrary/stagpy/issues/68): Pin numpy version less than 2.0

## [2.0.2] - 2024-05-29

### Fixed
- [Issue #59](https://github.com/staglibrary/stagpy/issues/59): Allow multiplication of SprsMat objects with numpy arrays.
- Fixed issues with compiling stag library when pip installing.

## [2.0.0] - 2024-05-13

See also the release notes for the [STAG C++ 1.3.0 release](https://github.com/staglibrary/stag/releases/tag/v1.3.0)
and the [STAG C++ 2.0.0 release](https://github.com/staglibrary/stag/releases/tag/v2.0.0).

### Changed
This release changes how data is handled in the python library. Now, when possible
data is always stored on the 'C++' side of the library. The new
`stag.utility.SprsMat` object is used to represent a sparse matrix whose data is 
stored on the C++ side. This object provides easy compatibility with scipy sparse
matrices. This is tracked as [Issue #28](https://github.com/staglibrary/stagpy/issues/28).

This release changes the interface for computing eigenvalues and eigenvectors
of graph matrices. See the documentation for the release to see the new syntax.

### Added
The following changes were released in the STAG C++ 1.3.0 release.

- Add method for calculating the symmetric difference between sets
- Compute the connected components of a graph
- Add a subgraph method to stag Graph class
- Add methods to compute mutual information between clusters
- Add method to construct the graph union
- Add Cheeger cut method
- Add support for self-loops in graphs
- Allow graphs to be initialised with Laplacian matrix
- Add `is_connected` method to Graph object
- Construct the identity graph
- Implement scalar multiplication of graphs
- Add graph addition operator

### Fixed
- [STAG C++ Issue #87](https://github.com/staglibrary/stag/issues/87): Occasional bug with sorting edgelist file

## [1.2.1] - 2023-03-22

**Documentation for this release is available [here](https://staglibrary.io/docs/python/docs-1.2.1/).**

### Fixed
- [Issue #30](https://github.com/staglibrary/stagpy/issues/30): Improve the caching behaviour of the Neo4jGraph object

## [1.2.0] - 2023-03-16

See also the release notes for the [STAG C++ 1.2.0 release](https://github.com/staglibrary/stag/releases/tag/v1.2.0).
This was the release associated with the first STAG technical report.

**Documentation for this release is available [here](https://staglibrary.io/docs/python/docs-1.2.0/).**
