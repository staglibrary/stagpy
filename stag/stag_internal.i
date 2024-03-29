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
// We intend to make C++ vectors interface seamlessly with numpy arrays
// from the perspective of the end user.
%init %{
    import_array();
%}
%eigen_typemaps(Eigen::VectorXd)
%eigen_typemaps(Eigen::MatrixXd)
%eigen_typemaps(DenseMat)

// Create bindings for tuples
%include <std_tuple.i>
%std_tuple(TupleMM, SprsMat, SprsMat)
%std_tuple(Tupleii, stag_int, stag_int)
%std_tuple(TupleEigensystem, Eigen::VectorXd, Eigen::MatrixXd)

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
    } catch (std::runtime_error &e) {
      PyErr_SetString(PyExc_AttributeError, const_cast<char*>(e.what()));
      return NULL;
    } catch (std::domain_error &e) {
      PyErr_SetString(PyExc_AttributeError, const_cast<char*>(e.what()));
      return NULL;
    }
}

// Create a typemap for a vector of Edge objects
%typemap(out) std::vector<stag::edge> {
    // Return a vector of edges as a list of tuples
    stag_int outer_length = $1.size();
    $result = PyList_New(outer_length);

    // Construct a new 3-tuple for each inner object, and add to the list.
    for (stag_int i = 0; i < outer_length; i++) {
        PyObject* new_tuple_object = PyTuple_Pack(
          3,
          PyLong_FromLongLong($1.at(i).v1),
          PyLong_FromLongLong($1.at(i).v2),
          PyFloat_FromDouble($1.at(i).weight));

        PyList_SET_ITEM($result, i, new_tuple_object);
    }
}

// Create a typemap for the Spectra SortRule
%typemap(in) Spectra::SortRule {
    // Assume we are given a boolean
    // False is SM, True is LM
    bool input = PyObject_IsTrue($input);
    if (input) {
        $1 = Spectra::SortRule::LargestMagn;
    } else {
        $1 = Spectra::SortRule::SmallestMagn;
    }
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_COMPLEX) Spectra::SortRule {
    $1 = 1;
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
    stag_int get_rows() {
        return $self->rows();
    }

    stag_int get_cols() {
        return $self->cols();
    }

    SprsMat __add__(SprsMat* other) {
        return *$self + *other;
    }

    SprsMat __sub__(SprsMat* other) {
        return *$self - *other;
    }

    SprsMat __mul__(SprsMat* other) {
        return *$self * *other;
    }

    SprsMat __mulfloat__(double other) {
        return other * *$self;
    }

    SprsMat __mulint__(stag_int other) {
        return other * *$self;
    }

    SprsMat __neg__() {
        return - *$self;
    }

    SprsMat __truedivfloat__(double other) {
        return *$self / other;
    }

    SprsMat __truedivint__(stag_int other) {
        return *$self / other;
    }

    // This is not a standard Python operator!
    // We add it for convenience.
    SprsMat __transpose__() {
        return $self->transpose();
    }
}

// Allow use of operators for graph objects
%extend stag::Graph {
    bool __eq__(stag::Graph* other) {
      return *$self == *other;
    }
}

// Add some code for constructing stag SprsMats from vectors.
%inline %{
SprsMat sprsMatFromVectorsDims(stag_int rows,
                               stag_int cols,
                               std::vector<stag_int>& column_starts,
                               std::vector<stag_int>& row_indices,
                               std::vector<double>& values) {
  // The length of the row_indices and values vectors should be the same
  if (row_indices.size() != values.size()) {
    throw std::invalid_argument("Sparse matrix indices and values array length mismatch.");
  }

  // The last value in the column_starts vector should be equal to the length
  // of the data vectors.
  if (column_starts.back() != (stag_int) row_indices.size()) {
    throw std::invalid_argument("Final column starts entry should equal size of data vectors.");
  }

  if (column_starts.size() - 1 != cols) {
    throw std::invalid_argument("Number of columns should match length of column starts.");
  }

  SprsMat constructed_mat = Eigen::Map<SprsMat>(rows,
                                                cols,
                                                (stag_int) values.size(),
                                                column_starts.data(),
                                                row_indices.data(),
                                                values.data());
  constructed_mat.makeCompressed();
  return constructed_mat;
}

%}

// Add some code for computing the eigensystem with the correct sort rule

// Metadata about the python interface
#define VERSION "1.2.1"
