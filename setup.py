# coding=utf-8

from distutils.core import setup
import pypcg

setup(name='pypcg',
      version=pypcg.VERSION,
      license='MIT',

      author="Jeb Brooks",
      author_email="jbrooks+pypcg@hmc.edu",
      url="https://github.com/robojeb/pypcg",

      zip_safe=False,

      ext_package='pypcg',
      ext_modules=[pypcg.ffi.verifier.get_extension()],

      packages=['pypcg'],
      package_dir={'pypcg': 'pypcg'},
      package_data={'pypcg': ['pcg_basic/pcg_basic.*']},

      install_requires=['cffi'],
      setup_required=['cffi']

      )
