### Building requirements
**python3.6(32 or 64bit)**
**pybind11**


1. Windows
* cmake

2. Debian - The wheel for wxPython takes a lot of time to build
* make
* cmake
* gcc
* libgtk-3-dev
* libwebkitgtk-dev
* libwebkitgtk-3.0-dev
* libgstreamer-gl1.0-0
* freeglut3
* freeglut3-dev
* python-gst-1.0
* python3-gst-1.0
* libglib2.0-dev
* ubuntu-restricted-extras - for Ubuntu
* libgstreamer-plugins-base1.0-dev

`pip install -r requirements.txt`

#### Building pybind11

1. Windows:
>You can specify x86_64 as the target architecture for the generated Visual Studio project using  `cmake -A x64 ..`
```
cd pybind11-master
mkdir build
cd build
cmake -A x64 ..
cmake --build . --config Release --target check
```

2. Linux
```
cd pybind11-master
mkdir build
cd build
cmake ..
make check -j 4
sudo make install
```

### Notes:
1. keyboard doesn't differentiate order
 * so 123 is the same as 321
