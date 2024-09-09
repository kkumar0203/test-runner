import sys
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

def import_module_from_file(file_path):
    """
    Imports and returns a module from a string file path.

    Args:
        file_path: string path to the file containing the module

    Returns:
        module: gotten module object from the file
    """
    
    abs_path = Path(file_path).resolve()
    module_name = str(abs_path.stem)

    # Import the module from the given file using the string file path and module name
    # Ref https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    spec = spec_from_file_location(module_name, abs_path)
    module = module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module