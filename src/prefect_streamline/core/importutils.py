import importlib
import importlib.util
import os
from os.path import basename
from types import ModuleType
from typing import List, Optional


def import_module(module: str) -> None:
    importlib.import_module(module)
    return


def import_path(path: str, discover: bool = False) -> None:
    if discover is True:
        _import_modules_from_path(path, recursive=True)
    else:
        module_name = basename(path).split(".")[0]
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is not None and spec.loader is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        return


def _import_modules_from_path(path: str,
                              module_fullname=None,
                              ignore_files: Optional[List[str]] = None,
                              recursive=False) -> List[ModuleType]:
    if ignore_files is None:
        ignore_files = []

    full_path = os.path.realpath(path)
    assert os.path.isdir(full_path), f"{full_path} is not a directory"

    python_files = [f for f in os.listdir(full_path)
                    if os.path.isfile(os.path.join(full_path, f)) and f.endswith(".py")]

    modules = []
    for python_file in python_files:
        if python_file not in ignore_files:
            python_module = python_file.replace('.py', '')

            package_def = [] if module_fullname is None else [module_fullname]
            package_def.append(python_module)
            python_module_full_name = ".".join(package_def)

            spec = importlib.util.spec_from_file_location(python_module_full_name, os.path.join(full_path, python_file))
            if spec is not None and spec.loader is not None:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                modules.append(module)

    if recursive:
        packages = [f for f in os.listdir(full_path) if os.path.isdir(os.path.join(full_path, f))]
        for package in packages:
            modules += _import_modules_from_path(os.path.join(path, package),
                                                 f"{module_fullname}.{package}",
                                                 ignore_files=ignore_files,
                                                 recursive=recursive)

    return modules
