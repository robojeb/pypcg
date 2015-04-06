# pypcg
Version: 0.0.1

PCG Version: 0.94

A python CFFI wrapper around the pcg random number generator library


# Installation Note
Currently the setup.py script may build the extension module in the wrong
location. If this happens and you get an import error you can fix this by
running python as superuser and importing the library once. This will allow
the required module to be built and all other imports should work.
