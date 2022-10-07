/* SWIG interface file for STAG library */
%module stag_internal
%{
//     #include "eigen-3.3.9/Eigen/Core"
//     #include "eigen-3.3.9/Eigen/Sparse"
    #include "stag_lib/stag.h"
    #include "stag_lib/utility.h"

%}

%include <std_vector.i>
namespace std {
    // Create the bindings for the std::vector types
    %template(vectori) vector<int>;
    %template(vectord) vector<double>;

    // Add missing types
//     typedef ::size_t size_t;
//     typedef ::ptrdiff_t ptrdiff_t;
}

// Include the complete STAG library
// #define EIGEN_DONT_INLINE
// #define EIGEN_STRONG_INLINE
// %include "eigen-3.3.9/Eigen/Core"
// %include "eigen-3.3.9/Eigen/Sparse"
// %include "eigen-3.3.9/Eigen/src/Core"
// %include "eigen-3.3.9/Eigen/src/SparseCore/SparseMatrixBase.h"
// %include "eigen-3.3.9/Eigen/src/SparseCore/SparseMatrix.h"

// namespace Eigen {
//     %template(sparsemat) SparseMatrix<double,Eigen::RowMajor,long>;
// }

// Add a dummy definition and destructor for the eigen sparse matrix
// %nodefaultctor SprsMat;
// %extend Eigen::SparseMatrix {
//     ~SprsMat() {
//         DestroySprsMat(self);
//     }
//     void test() {
//         cout << "test" << std::endl;
//     }
// }
// %ignore DestroySprsMat;

%include "stag_lib/stag.h"
%include "stag_lib/utility.h"

// Metadata about the python interface
#define VERSION "0.1.0"
