/* SWIG interface file for STAG library */
%module stag_internal
%{
    #include "stag_lib/stag.h"
    #include "stag_lib/graph.h"
    #include "stag_lib/utility.h"
%}

%include <std_vector.i>
namespace std {
    // Create the bindings for the std::vector types
    %template(vectori) vector<int>;
    %template(vectord) vector<double>;
}

// Include the complete STAG library
%include "stag_lib/stag.h"
%include "stag_lib/graph.h"
%include "stag_lib/utility.h"

// Metadata about the python interface
#define VERSION "0.1.6"
