/* SWIG interface file for STAG library */
%module stag_internal
%module(directors="1") stag_internal

%{
    #include "stag_lib/stag.h"
    #include "stag_lib/graph.h"
    #include "stag_lib/utility.h"
    #include "stag_lib/cluster.h"
    #include "stag_lib/graphio.h"
    #include "stag_lib/random.h"
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
%include "stag_lib/cluster.h"
%include "stag_lib/graphio.h"
%include "stag_lib/random.h"

// Add a director for the local graph object
%feature("director") LocalGraph;

// Metadata about the python interface
#define VERSION "0.1.6"
