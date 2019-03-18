REM Get pybind
cd cnake_mem/cnake
wget https://github.com/pybind/pybind11/archive/master.zip
7z x master.zip -opybind11-master
REM Make pybind
mkdir -p pybind11-master/build
cd pybind11-master/build
cmake -A x64 ..
cmake --build . --config Release --target check
REM Make python module
cd .. && cd ..
mkdir build && cd build
set BUILD_TARGET=windows && cmake -A x64 ..
cmake --build . --config Release
xcopy Release\*.pyd ..\..\..