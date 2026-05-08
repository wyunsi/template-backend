"""
Cython compilation — compiles core/license/ and core/security/ to .so
Run: python setup_cython.py build_ext --inplace
"""

from Cython.Build import cythonize
from setuptools import Extension, setup

extensions = [
    Extension("core.license.*",   sources=["core/license/*.py"]),
    Extension("core.security.*",  sources=["core/security/*.py"]),
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},
        nthreads=4,
    )
)
