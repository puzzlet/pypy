import py, os

from pypy.rlib import libffi
from pypy.translator.tool.cbuild import ExternalCompilationInfo

__all__ = ['identify', 'eci', 'c_load_dictionary']

pkgpath = py.path.local(__file__).dirpath().join(os.pardir)
srcpath = pkgpath.join("src")
incpath = pkgpath.join("include")

if os.environ.get("ROOTSYS"):
    import commands
    (stat, incdir) = commands.getstatusoutput("root-config --incdir")
    if stat != 0:        # presumably Reflex-only
        rootincpath = [os.path.join(os.environ["ROOTSYS"], "include")]
        rootlibpath = [os.path.join(os.environ["ROOTSYS"], "lib64"), os.path.join(os.environ["ROOTSYS"], "lib")]
    else:
        rootincpath = [incdir]
        rootlibpath = commands.getoutput("root-config --libdir").split()
else:
    rootincpath = []
    rootlibpath = []

def identify():
    return 'Reflex'

threadsafe='auto'

eci = ExternalCompilationInfo(
    separate_module_files=[srcpath.join("reflexcwrapper.cxx")],
    include_dirs=[incpath] + rootincpath,
    includes=["reflexcwrapper.h"],
    library_dirs=rootlibpath,
    link_extra=["-lReflex"],
    use_cpp_linker=True,
)

def c_load_dictionary(name):
    return libffi.CDLL(name)
