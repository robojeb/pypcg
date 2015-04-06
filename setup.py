# coding=utf-8

from distutils.command.build import build
from setuptools import setup
from setuptools.command.install import install


def get_ext_modules():
    import pypcg
    return [pypcg.ffi.verifier.get_extension()]


class CFFIBuild(build):
    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        build.finalize_options(self)


class CFFIInstall(install):
    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        install.finalize_options(self)

setup(name='pypcg',
      version='0.0.2',
      license='MIT',

      author="Jeb Brooks",
      author_email="jbrooks+pypcg@hmc.edu",
      url="https://github.com/robojeb/pypcg",

      zip_safe=False,

      # ext_package='pypcg',
      # ext_modules=[pypcg.ffi.verifier.get_extension()],

      packages=['pypcg'],
      package_dir={'pypcg': 'pypcg'},
      package_data={'pypcg': ['pcg_basic/pcg_basic.*']},

      install_requires=['cffi'],
      setup_requires=['cffi'],

      cmdclass={
        "build": CFFIBuild,
        "install": CFFIInstall,
      }

      )
