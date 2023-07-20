/* SWIG interface file for STAG library */
%module stag_internal
%module(directors="1") stag_internal

// This block allows numpy arrays to be cast to C++ vectors
// using the vector template maps (e.g. vectorl).
//
// See stagpy Issue #33.
%begin %{
#define SWIG_PYTHON_CAST_MODE
%}

// Eigen / numpy stuff
%include <typemaps.i>
%include eigen.i
%include numpy.i

%{
    #include "stag_lib/stag.h"
    #include "stag_lib/graph.h"
    #include "stag_lib/utility.h"
    #include "stag_lib/cluster.h"
    #include "stag_lib/graphio.h"
    #include "stag_lib/random.h"
    #include "stag_lib/spectrum.h"
%}

// Eigen / numpy stuff
%init %{
    import_array();
%}
%eigen_typemaps(Eigen::VectorXd)
%eigen_typemaps(Eigen::MatrixXd)
%eigen_typemaps(DenseMat)

%include <std_vector.i>
namespace std {
    // Create the bindings for the std::vector types
    %template(vectori) vector<int>;
    %template(vectorl) vector<long long>;
    %template(vectord) vector<double>;
    %template(vectore) vector<stag::edge>;
    %template(vectorvecl) vector<vector<long long>>;
}

// Create bindings for tuples
%include <std_tuple.i>
%std_tuple(TupleMM, SprsMat, SprsMat)

// Define typemaps for passing by reference
%include <std_string.i>
%apply std::string& INPUT {std::string& filename};
%apply std::string& INPUT {std::string& edgelist_fname};
%apply std::string& INPUT {std::string& adjacencylist_fname};

// Add a director for the local graph object
%feature("director") LocalGraph;

// Handle C++ exceptions
%exception {
    try {
        $action
    } catch (std::invalid_argument &e) {
      PyErr_SetString(PyExc_AttributeError, const_cast<char*>(e.what()));
      return NULL;
    } catch (std::domain_error &e) {
      PyErr_SetString(PyExc_AttributeError, const_cast<char*>(e.what()));
      return NULL;
    }
}

// Include the complete STAG library
%include "stag_lib/stag.h"
%include "stag_lib/graph.h"
%include "stag_lib/utility.h"
%include "stag_lib/cluster.h"
%include "stag_lib/graphio.h"
%include "stag_lib/random.h"
%include "stag_lib/spectrum.h"

// Include a destructor for the sparse matrix type
class SprsMat {
public:
    ~SprsMat();
};

// Allow use of operators for SprsMat objects
%extend SprsMat {
    SprsMat __add__(SprsMat* other) {
        return *$self + *other;
    }

    SprsMat __sub__(SprsMat* other) {
        return *$self - *other;
    }

    SprsMat __mul__(double other) {
        return other * *$self;
    }

    SprsMat __mul__(stag_int other) {
        return other * *$self;
    }

    SprsMat __neg__() {
        return - *$self;
    }
}

// Metadata about the python interface
#define VERSION "1.2.1"
