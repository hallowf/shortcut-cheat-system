# Fetch pybind11
cd cnake_mem/cnake
./getpybind.sh
mkdir -p pybind11-master/build
cd pybind11-master/build
# Make pybind11
cmake ..
make check -j 4
sudo make install
# Make python module
cd .. && cd ..
mkdir build && cd build
export BUILD_TARGET=linux && cmake ..
cmake --build .


