# Fetch pybind11
cd cnake_mem/cnake
./getpybind.sh
# Make python module
cd .. && cd ..
mkdir build && cd build
export BUILD_TARGET=linux && cmake ..
cmake --build .


