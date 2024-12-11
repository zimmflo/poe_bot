import setuptools
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import glob

files_to_compile = glob.glob("./*.py")
ext_modules = []
files_to_compile = list(map(lambda file_path: file_path.split('\\')[1], files_to_compile))
for file in files_to_compile:
  module_name = file.split(".py")[0]
  if module_name == "setup":
    continue
  print(f'going to compile {file}')
  ext_modules.append(Extension(module_name, [file]))

setup(name='My Cython App',
      cmdclass={'build_ext': build_ext},
      ext_modules=cythonize(ext_modules),
      compiler_directives={'language_level': 3},
      zip_safe=False
      )