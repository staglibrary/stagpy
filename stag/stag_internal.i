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
    #include "stag_lib/data.h"
    #include "stag_lib/definitions.h"
    #include "stag_lib/lsh.h"
    #include "stag_lib/kde.h"
%}

// We intend to make C++ vectors interface seamlessly with numpy arrays
// from the perspective of the end user.
%init %{
    import_array();
%}
%eigen_typemaps(Eigen::VectorXd)
%eigen_typemaps(Eigen::MatrixXd)

// Create bindings for tuples
%include <std_tuple.i>
%std_tuple(TupleMM, SprsMat, SprsMat)
%std_tuple(Tupleii, StagInt, StagInt)
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

// Create typemaps for StagInt
%typemap(out) StagInt {
    // StagInt typemap (out)
    $result = PyLong_FromLongLong((long long) $1);
}
%typemap(in) StagInt {
    // StagInt typemap (in)
    if (!PyLong_Check((PyObject *) $input)) {
        PyErr_SetString(PyExc_TypeError, "Expected an integer.");
        return NULL;
    }
    $1 = (StagInt) PyLong_AsLong((PyObject*) $input);
}
%typemap(typecheck, precedence=SWIG_TYPECHECK_INT64) StagInt {
    // Typecheck for StagInt
    $1 = PyLong_Check((PyObject*) $input);
}

// Create a typemap for a vector of Edge objects
%typemap(out) std::vector<stag::edge> {
    // Return a vector of edges as a list of tuples
    StagInt outer_length = $1.size();
    $result = PyList_New(outer_length);

    // Construct a new 3-tuple for each inner object, and add to the list.
    for (StagInt i = 0; i < outer_length; i++) {
        PyObject* new_tuple_object = PyTuple_Pack(
          3,
          PyLong_FromLongLong($1.at(i).v1),
          PyLong_FromLongLong($1.at(i).v2),
          PyFloat_FromDouble($1.at(i).weight));

        PyList_SET_ITEM($result, i, new_tuple_object);
    }
}

// Create an 'out' typemap for a vector of DataPoint objects
%typemap(out) std::vector<stag::DataPoint> {
    // Construct a python list of data point objects
    StagInt outer_length = $1.size();
    $result = PyList_New(outer_length);

    // Construct a new DataPoint for each inner object, and add to the list.
    for (StagInt i = 0; i < outer_length; i++) {
        PyObject* new_datapoint_object = SWIG_NewPointerObj(
           (new stag::DataPoint($1.at(i).dimension, $1.at(i).coordinates)),
           SWIGTYPE_p_stag__DataPoint, SWIG_POINTER_OWN |  0 );

        PyList_SET_ITEM($result, i, new_datapoint_object);
    }
}

// Create an 'in' typemap for a vector of DataPoint objects
%typemap(in) std::vector<stag::DataPoint>
  (PyArrayObject* array=NULL, int is_new_object=0, std::vector<stag::DataPoint> temp_vec)
{
    // Typemap (in) for std::vector<stag::DataPoint>

    // Get the number of elements in the python list.
    StagInt list_size = PyList_Size((PyObject*) $input);
    temp_vec.reserve(list_size);

    // Construct a new DataPoint for each list object, and add to the vector
    for (StagInt i = 0; i < list_size; i++) {
        PyObject* python_datapoint = PyList_GetItem((PyObject*) $input, i);
        void* cpp_datapoint = 0;
        int res = SWIG_ConvertPtr(python_datapoint, &cpp_datapoint, SWIGTYPE_p_stag__DataPoint, 0 | 0);
        temp_vec.push_back(*(reinterpret_cast<stag::DataPoint*>(cpp_datapoint)));
    }

    $1 = temp_vec;
}

%typemap(in) std::vector<stag::DataPoint> &
  (PyArrayObject* array=NULL, int is_new_object=0, std::vector<stag::DataPoint> temp_vec)
{
    // Typemap (in) for std::vector<stag::DataPoint>&

    // Get the number of elements in the python list.
    StagInt list_size = PyList_Size((PyObject*) $input);
    temp_vec.reserve(list_size);

    // Construct a new DataPoint for each list object, and add to the vector
    for (StagInt i = 0; i < list_size; i++) {
        PyObject* python_datapoint = PyList_GetItem((PyObject*) $input, i);
        void* cpp_datapoint = 0;
        int res = SWIG_ConvertPtr(python_datapoint, &cpp_datapoint, SWIGTYPE_p_stag__DataPoint, 0 | 0);
        temp_vec.push_back(*(reinterpret_cast<stag::DataPoint*>(cpp_datapoint)));
    }

    $1 = &temp_vec;
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_COMPLEX) std::vector<stag::DataPoint>& {
    // Typecheck for std::vector<stag::DataPoint>&
    $1 = 1;
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
%include "stag_lib/data.h"
%include "stag_lib/kde.h"
%include "stag_lib/lsh.h"
%include "stag_lib/definitions.h"

// Include a destructor for the dense matrix type
class DenseMat {
public:
    ~DenseMat();
};

// Allow use of operators for DenseMat objects
%extend DenseMat {
    StagInt get_rows() {
        return $self->rows();
    }

    StagInt get_cols() {
        return $self->cols();
    }

    DenseMat __add__(DenseMat* other) {
        return *$self + *other;
    }

    DenseMat __sub__(DenseMat* other) {
        return *$self - *other;
    }

    DenseMat __mul__(DenseMat* other) {
        return *$self * *other;
    }

    DenseMat __mulfloat__(double other) {
        return other * *$self;
    }

    DenseMat __mulint__(StagInt other) {
        return other * *$self;
    }

    DenseMat __neg__() {
        return - *$self;
    }

    bool __eq__(DenseMat* other) {
        return *$self == *other;
    }

    DenseMat __truedivfloat__(double other) {
        return *$self / other;
    }

    DenseMat __truedivint__(StagInt other) {
        return *$self / other;
    }

    // This is not a standard Python operator!
    // We add it for convenience.
    DenseMat __transpose__() {
        return $self->transpose();
    }
}


// Allow use of operators for DenseMat objects

// Include a destructor for the sparse matrix type
class SprsMat {
public:
    ~SprsMat();
};

// Allow use of operators for SprsMat objects
%extend SprsMat {
    StagInt get_rows() {
        return $self->rows();
    }

    StagInt get_cols() {
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

    SprsMat __mulint__(StagInt other) {
        return other * *$self;
    }

    SprsMat __neg__() {
        return - *$self;
    }

    SprsMat __truedivfloat__(double other) {
        return *$self / other;
    }

    SprsMat __truedivint__(StagInt other) {
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
SprsMat sprsMatFromVectorsDims(long rows,
                               long cols,
                               std::vector<StagInt>& column_starts,
                               std::vector<StagInt>& row_indices,
                               std::vector<double>& values) {
  // The length of the row_indices and values vectors should be the same
  if (row_indices.size() != values.size()) {
    throw std::invalid_argument("Sparse matrix indices and values array length mismatch.");
  }

  // The last value in the column_starts vector should be equal to the length
  // of the data vectors.
  if (column_starts.back() != (StagInt) row_indices.size()) {
    throw std::invalid_argument("Final column starts entry should equal size of data vectors.");
  }

  if (column_starts.size() - 1 != cols) {
    throw std::invalid_argument("Number of columns should match length of column starts.");
  }

  SprsMat constructed_mat = Eigen::Map<SprsMat>(rows,
                                                cols,
                                                (StagInt) values.size(),
                                                column_starts.data(),
                                                row_indices.data(),
                                                values.data());
  constructed_mat.makeCompressed();
  return constructed_mat;
}

%}

// Construct stag DenseMat matrices from numpy ndarrays.
// We use the fact that we've implemented typemaps to and from numpy arrays
// for the Eigen::MatrixXd type, but not the DenseMat type.
%inline %{
DenseMat denseMatFromNdarray(const Eigen::MatrixXd& mat) {
    DenseMat newDenseMat = mat;
    return newDenseMat;
}

Eigen::MatrixXd ndArrayFromDenseMat(const DenseMat& mat) {
    Eigen::MatrixXd new_mat = mat;
    return new_mat;
}
%}

// Metadata about the python interface
#define VERSION "2.1.1"
