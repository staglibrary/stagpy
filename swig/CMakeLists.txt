cmake_minimum_required(VERSION 3.14)
project(stag)

set(CMAKE_CXX_STANDARD 14)

# Tell the compiler where to find the python bindings
set(CMAKE_CXX_FLAGS "-I/usr/include/python3.8")

set(SOURCE_FILES stag_wrap.cxx)
add_library(_stag SHARED ${SOURCE_FILES})

# Add libraries
include_directories(../eigen-3.3.9) # Eigen - header-only
include_directories(../stag_lib)
add_subdirectory(../stag_lib stag)

target_link_libraries(_stag stag)

# Set the name of the output library
set_target_properties(_stag PROPERTIES PREFIX "")
