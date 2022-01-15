from os.path import dirname, basename, isfile, join
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))

__all__ = []
for file in modules:
    if isfile(file) and not file.endswith('__init__.py') and not basename(file)[:-3] in __all__:
        __all__.append(basename(file)[:-3])
        print(f"- Importing {file}")


from . import *