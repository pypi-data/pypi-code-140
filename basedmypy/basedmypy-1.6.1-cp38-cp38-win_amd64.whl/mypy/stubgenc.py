#!/usr/bin/env python3
"""Stub generator for C modules.

The public interface is via the mypy.stubgen module.
"""

from __future__ import annotations

import importlib
import inspect
import os.path
import re
from abc import abstractmethod
from types import ModuleType
from typing import Any, Iterable, Mapping
from typing_extensions import Final

from mypy.moduleinspect import is_c_module
from mypy.stubdoc import (
    ArgSig,
    FunctionSig,
    infer_arg_sig_from_anon_docstring,
    infer_prop_type_from_docstring,
    infer_ret_type_sig_from_anon_docstring,
    infer_ret_type_sig_from_docstring,
    infer_sig_from_docstring,
)

# Members of the typing module to consider for importing by default.
_DEFAULT_TYPING_IMPORTS: Final = (
    "Any",
    "Callable",
    "ClassVar",
    "Dict",
    "Iterable",
    "Iterator",
    "List",
    "Optional",
    "Tuple",
    "Union",
)


class SignatureGenerator:
    """Abstract base class for extracting a list of FunctionSigs for each function."""

    @abstractmethod
    def get_function_sig(
        self, func: object, module_name: str, name: str
    ) -> list[FunctionSig] | None:
        pass

    @abstractmethod
    def get_method_sig(
        self, func: object, module_name: str, class_name: str, name: str, self_var: str
    ) -> list[FunctionSig] | None:
        pass


class ExternalSignatureGenerator(SignatureGenerator):
    def __init__(
        self, func_sigs: dict[str, str] | None = None, class_sigs: dict[str, str] | None = None
    ):
        """
        Takes a mapping of function/method names to signatures and class name to
        class signatures (usually corresponds to __init__).
        """
        self.func_sigs = func_sigs or {}
        self.class_sigs = class_sigs or {}

    def get_function_sig(
        self, func: object, module_name: str, name: str
    ) -> list[FunctionSig] | None:
        if name in self.func_sigs:
            return [
                FunctionSig(
                    name=name,
                    args=infer_arg_sig_from_anon_docstring(self.func_sigs[name]),
                    ret_type="Any",
                )
            ]
        else:
            return None

    def get_method_sig(
        self, func: object, module_name: str, class_name: str, name: str, self_var: str
    ) -> list[FunctionSig] | None:
        if (
            name in ("__new__", "__init__")
            and name not in self.func_sigs
            and class_name in self.class_sigs
        ):
            return [
                FunctionSig(
                    name=name,
                    args=infer_arg_sig_from_anon_docstring(self.class_sigs[class_name]),
                    ret_type="None" if name == "__init__" else "Any",
                )
            ]
        return self.get_function_sig(func, module_name, name)


class DocstringSignatureGenerator(SignatureGenerator):
    def get_function_sig(
        self, func: object, module_name: str, name: str
    ) -> list[FunctionSig] | None:
        docstr = getattr(func, "__doc__", None)
        inferred = infer_sig_from_docstring(docstr, name)
        if inferred:
            assert docstr is not None
            if is_pybind11_overloaded_function_docstring(docstr, name):
                # Remove pybind11 umbrella (*args, **kwargs) for overloaded functions
                del inferred[-1]
        return inferred

    def get_method_sig(
        self, func: object, module_name: str, class_name: str, name: str, self_var: str
    ) -> list[FunctionSig] | None:
        return self.get_function_sig(func, module_name, name)


class FallbackSignatureGenerator(SignatureGenerator):
    def get_function_sig(
        self, func: object, module_name: str, name: str
    ) -> list[FunctionSig] | None:
        return [
            FunctionSig(
                name=name,
                args=infer_arg_sig_from_anon_docstring("(*args, **kwargs)"),
                ret_type="Any",
            )
        ]

    def get_method_sig(
        self, func: object, module_name: str, class_name: str, name: str, self_var: str
    ) -> list[FunctionSig] | None:
        return [
            FunctionSig(
                name=name,
                args=infer_method_sig(name, self_var),
                ret_type="None" if name == "__init__" else "Any",
            )
        ]


def generate_stub_for_c_module(
    module_name: str, target: str, sig_generators: Iterable[SignatureGenerator]
) -> None:
    """Generate stub for C module.

    Signature generators are called in order until a list of signatures is returned.  The order
    is:
    - signatures inferred from .rst documentation (if given)
    - simple runtime introspection (looking for docstrings and attributes
      with simple builtin types)
    - fallback based special method names or "(*args, **kwargs)"

    If directory for target doesn't exist it will be created. Existing stub
    will be overwritten.
    """
    module = importlib.import_module(module_name)
    assert is_c_module(module), f"{module_name} is not a C module"
    subdir = os.path.dirname(target)
    if subdir and not os.path.isdir(subdir):
        os.makedirs(subdir)
    imports: list[str] = []
    functions: list[str] = []
    done = set()
    items = sorted(module.__dict__.items(), key=lambda x: x[0])
    for name, obj in items:
        if is_c_function(obj):
            generate_c_function_stub(
                module, name, obj, functions, imports=imports, sig_generators=sig_generators
            )
            done.add(name)
    types: list[str] = []
    for name, obj in items:
        if name.startswith("__") and name.endswith("__"):
            continue
        if is_c_type(obj):
            generate_c_type_stub(
                module, name, obj, types, imports=imports, sig_generators=sig_generators
            )
            done.add(name)
    variables = []
    for name, obj in items:
        if name.startswith("__") and name.endswith("__"):
            continue
        if name not in done and not inspect.ismodule(obj):
            type_str = strip_or_import(get_type_fullname(type(obj)), module, imports)
            variables.append(f"{name}: {type_str}")
    output = sorted(set(imports))
    for line in variables:
        output.append(line)
    for line in types:
        if line.startswith("class") and output and output[-1]:
            output.append("")
        output.append(line)
    if output and functions:
        output.append("")
    for line in functions:
        output.append(line)
    output = add_typing_import(output)
    with open(target, "w") as file:
        for line in output:
            file.write(f"{line}\n")


def add_typing_import(output: list[str]) -> list[str]:
    """Add typing imports for collections/types that occur in the generated stub."""
    names = []
    for name in _DEFAULT_TYPING_IMPORTS:
        if any(re.search(r"\b%s\b" % name, line) for line in output):
            names.append(name)
    if names:
        return [f"from typing import {', '.join(names)}", ""] + output
    else:
        return output[:]


def is_c_function(obj: object) -> bool:
    return inspect.isbuiltin(obj) or type(obj) is type(ord)


def is_c_method(obj: object) -> bool:
    return inspect.ismethoddescriptor(obj) or type(obj) in (
        type(str.index),
        type(str.__add__),
        type(str.__new__),
    )


def is_c_classmethod(obj: object) -> bool:
    return inspect.isbuiltin(obj) or type(obj).__name__ in (
        "classmethod",
        "classmethod_descriptor",
    )


def is_c_property(obj: object) -> bool:
    return inspect.isdatadescriptor(obj) or hasattr(obj, "fget")


def is_c_property_readonly(prop: Any) -> bool:
    return hasattr(prop, "fset") and prop.fset is None


def is_c_type(obj: object) -> bool:
    return inspect.isclass(obj) or type(obj) is type(int)


def is_pybind11_overloaded_function_docstring(docstr: str, name: str) -> bool:
    return docstr.startswith(f"{name}(*args, **kwargs)\n" + "Overloaded function.\n\n")


def generate_c_function_stub(
    module: ModuleType,
    name: str,
    obj: object,
    output: list[str],
    imports: list[str],
    sig_generators: Iterable[SignatureGenerator],
    self_var: str | None = None,
    class_name: str | None = None,
) -> None:
    """Generate stub for a single function or method.

    The result (always a single line) will be appended to 'output'.
    If necessary, any required names will be added to 'imports'.
    The 'class_name' is used to find signature of __init__ or __new__ in
    'class_sigs'.
    """
    inferred: list[FunctionSig] | None = None
    if class_name:
        # method:
        assert self_var is not None, "self_var should be provided for methods"
        for sig_gen in sig_generators:
            inferred = sig_gen.get_method_sig(obj, module.__name__, class_name, name, self_var)
            if inferred:
                # add self/cls var, if not present
                for sig in inferred:
                    if not sig.args or sig.args[0].name != self_var:
                        sig.args.insert(0, ArgSig(name=self_var))
                break
    else:
        # function:
        for sig_gen in sig_generators:
            inferred = sig_gen.get_function_sig(obj, module.__name__, name)
            if inferred:
                break

    if not inferred:
        raise ValueError(
            "No signature was found. This should never happen "
            "if FallbackSignatureGenerator is provided"
        )

    is_classmethod = self_var == "cls"
    is_overloaded = len(inferred) > 1 if inferred else False
    if is_overloaded:
        imports.append("from typing import overload")
    if inferred:
        for signature in inferred:
            args: list[str] = []
            for arg in signature.args:
                if arg.name == self_var:
                    arg_def = self_var
                else:
                    arg_def = arg.name
                    if arg_def == "None":
                        arg_def = "_none"  # None is not a valid argument name

                    if arg.type:
                        arg_def += ": " + strip_or_import(arg.type, module, imports)

                    if arg.default:
                        arg_def += " = ..."

                args.append(arg_def)

            if is_overloaded:
                output.append("@overload")
            if is_classmethod:
                output.append("@classmethod")
            output.append(
                "def {function}({args}) -> {ret}: ...".format(
                    function=name,
                    args=", ".join(args),
                    ret=strip_or_import(signature.ret_type, module, imports),
                )
            )


def strip_or_import(typ: str, module: ModuleType, imports: list[str]) -> str:
    """Strips unnecessary module names from typ.

    If typ represents a type that is inside module or is a type coming from builtins, remove
    module declaration from it. Return stripped name of the type.

    Arguments:
        typ: name of the type
        module: in which this type is used
        imports: list of import statements (may be modified during the call)
    """
    stripped_type = typ
    if any(c in typ for c in "[,"):
        for subtyp in re.split(r"[\[,\]]", typ):
            strip_or_import(subtyp.strip(), module, imports)
        if module:
            stripped_type = re.sub(r"(^|[\[, ]+)" + re.escape(module.__name__ + "."), r"\1", typ)
    elif module and typ.startswith(module.__name__ + "."):
        stripped_type = typ[len(module.__name__) + 1 :]
    elif "." in typ:
        arg_module = typ[: typ.rindex(".")]
        if arg_module == "builtins":
            stripped_type = typ[len("builtins") + 1 :]
        else:
            imports.append(f"import {arg_module}")
    if stripped_type == "NoneType":
        stripped_type = "None"
    return stripped_type


def is_static_property(obj: object) -> bool:
    return type(obj).__name__ == "pybind11_static_property"


def generate_c_property_stub(
    name: str,
    obj: object,
    static_properties: list[str],
    rw_properties: list[str],
    ro_properties: list[str],
    readonly: bool,
    module: ModuleType | None = None,
    imports: list[str] | None = None,
) -> None:
    """Generate property stub using introspection of 'obj'.

    Try to infer type from docstring, append resulting lines to 'output'.
    """

    def infer_prop_type(docstr: str | None) -> str | None:
        """Infer property type from docstring or docstring signature."""
        if docstr is not None:
            inferred = infer_ret_type_sig_from_anon_docstring(docstr)
            if not inferred:
                inferred = infer_ret_type_sig_from_docstring(docstr, name)
            if not inferred:
                inferred = infer_prop_type_from_docstring(docstr)
            return inferred
        else:
            return None

    # Ignore special properties/attributes.
    if is_skipped_attribute(name):
        return

    inferred = infer_prop_type(getattr(obj, "__doc__", None))
    if not inferred:
        fget = getattr(obj, "fget", None)
        inferred = infer_prop_type(getattr(fget, "__doc__", None))
    if not inferred:
        inferred = "Any"

    if module is not None and imports is not None:
        inferred = strip_or_import(inferred, module, imports)

    if is_static_property(obj):
        trailing_comment = "  # read-only" if readonly else ""
        static_properties.append(f"{name}: ClassVar[{inferred}] = ...{trailing_comment}")
    else:  # regular property
        if readonly:
            ro_properties.append("@property")
            ro_properties.append(f"def {name}(self) -> {inferred}: ...")
        else:
            rw_properties.append(f"{name}: {inferred}")


def generate_c_type_stub(
    module: ModuleType,
    class_name: str,
    obj: type,
    output: list[str],
    imports: list[str],
    sig_generators: Iterable[SignatureGenerator],
) -> None:
    """Generate stub for a single class using runtime introspection.

    The result lines will be appended to 'output'. If necessary, any
    required names will be added to 'imports'.
    """
    # typeshed gives obj.__dict__ the not quite correct type Dict[str, Any]
    # (it could be a mappingproxy!), which makes mypyc mad, so obfuscate it.
    obj_dict: Mapping[str, Any] = getattr(obj, "__dict__")  # noqa: B009
    items = sorted(obj_dict.items(), key=lambda x: method_name_sort_key(x[0]))
    methods: list[str] = []
    types: list[str] = []
    static_properties: list[str] = []
    rw_properties: list[str] = []
    ro_properties: list[str] = []
    done: set[str] = set()
    for attr, value in items:
        if is_c_method(value) or is_c_classmethod(value):
            done.add(attr)
            if not is_skipped_attribute(attr):
                if attr == "__new__":
                    # TODO: We should support __new__.
                    if "__init__" in obj_dict:
                        # Avoid duplicate functions if both are present.
                        # But is there any case where .__new__() has a
                        # better signature than __init__() ?
                        continue
                    attr = "__init__"
                if is_c_classmethod(value):
                    self_var = "cls"
                else:
                    self_var = "self"
                generate_c_function_stub(
                    module,
                    attr,
                    value,
                    methods,
                    imports=imports,
                    self_var=self_var,
                    class_name=class_name,
                    sig_generators=sig_generators,
                )
        elif is_c_property(value):
            done.add(attr)
            generate_c_property_stub(
                attr,
                value,
                static_properties,
                rw_properties,
                ro_properties,
                is_c_property_readonly(value),
                module=module,
                imports=imports,
            )
        elif is_c_type(value):
            generate_c_type_stub(
                module, attr, value, types, imports=imports, sig_generators=sig_generators
            )
            done.add(attr)

    for attr, value in items:
        if is_skipped_attribute(attr):
            continue
        if attr not in done:
            static_properties.append(
                "{}: ClassVar[{}] = ...".format(
                    attr, strip_or_import(get_type_fullname(type(value)), module, imports)
                )
            )
    all_bases = type.mro(obj)
    if all_bases[-1] is object:
        # TODO: Is this always object?
        del all_bases[-1]
    # remove pybind11_object. All classes generated by pybind11 have pybind11_object in their MRO,
    # which only overrides a few functions in object type
    if all_bases and all_bases[-1].__name__ == "pybind11_object":
        del all_bases[-1]
    # remove the class itself
    all_bases = all_bases[1:]
    # Remove base classes of other bases as redundant.
    bases: list[type] = []
    for base in all_bases:
        if not any(issubclass(b, base) for b in bases):
            bases.append(base)
    if bases:
        bases_str = "(%s)" % ", ".join(
            strip_or_import(get_type_fullname(base), module, imports) for base in bases
        )
    else:
        bases_str = ""
    if types or static_properties or rw_properties or methods or ro_properties:
        output.append(f"class {class_name}{bases_str}:")
        for line in types:
            if (
                output
                and output[-1]
                and not output[-1].startswith("class")
                and line.startswith("class")
            ):
                output.append("")
            output.append("    " + line)
        for line in static_properties:
            output.append(f"    {line}")
        for line in rw_properties:
            output.append(f"    {line}")
        for line in methods:
            output.append(f"    {line}")
        for line in ro_properties:
            output.append(f"    {line}")
    else:
        output.append(f"class {class_name}{bases_str}: ...")


def get_type_fullname(typ: type) -> str:
    return f"{typ.__module__}.{getattr(typ, '__qualname__', typ.__name__)}"


def method_name_sort_key(name: str) -> tuple[int, str]:
    """Sort methods in classes in a typical order.

    I.e.: constructor, normal methods, special methods.
    """
    if name in ("__new__", "__init__"):
        return 0, name
    if name.startswith("__") and name.endswith("__"):
        return 2, name
    return 1, name


def is_pybind_skipped_attribute(attr: str) -> bool:
    return attr.startswith("__pybind11_module_local_")


def is_skipped_attribute(attr: str) -> bool:
    return attr in (
        "__getattribute__",
        "__str__",
        "__repr__",
        "__doc__",
        "__dict__",
        "__module__",
        "__weakref__",
    ) or is_pybind_skipped_attribute(  # For pickling
        attr
    )


def infer_method_sig(name: str, self_var: str | None = None) -> list[ArgSig]:
    args: list[ArgSig] | None = None
    if name.startswith("__") and name.endswith("__"):
        name = name[2:-2]
        if name in (
            "hash",
            "iter",
            "next",
            "sizeof",
            "copy",
            "deepcopy",
            "reduce",
            "getinitargs",
            "int",
            "float",
            "trunc",
            "complex",
            "bool",
            "abs",
            "bytes",
            "dir",
            "len",
            "reversed",
            "round",
            "index",
            "enter",
        ):
            args = []
        elif name == "getitem":
            args = [ArgSig(name="index")]
        elif name == "setitem":
            args = [ArgSig(name="index"), ArgSig(name="object")]
        elif name in ("delattr", "getattr"):
            args = [ArgSig(name="name")]
        elif name == "setattr":
            args = [ArgSig(name="name"), ArgSig(name="value")]
        elif name == "getstate":
            args = []
        elif name == "setstate":
            args = [ArgSig(name="state")]
        elif name in (
            "eq",
            "ne",
            "lt",
            "le",
            "gt",
            "ge",
            "add",
            "radd",
            "sub",
            "rsub",
            "mul",
            "rmul",
            "mod",
            "rmod",
            "floordiv",
            "rfloordiv",
            "truediv",
            "rtruediv",
            "divmod",
            "rdivmod",
            "pow",
            "rpow",
            "xor",
            "rxor",
            "or",
            "ror",
            "and",
            "rand",
            "lshift",
            "rlshift",
            "rshift",
            "rrshift",
            "contains",
            "delitem",
            "iadd",
            "iand",
            "ifloordiv",
            "ilshift",
            "imod",
            "imul",
            "ior",
            "ipow",
            "irshift",
            "isub",
            "itruediv",
            "ixor",
        ):
            args = [ArgSig(name="other")]
        elif name in ("neg", "pos", "invert"):
            args = []
        elif name == "get":
            args = [ArgSig(name="instance"), ArgSig(name="owner")]
        elif name == "set":
            args = [ArgSig(name="instance"), ArgSig(name="value")]
        elif name == "reduce_ex":
            args = [ArgSig(name="protocol")]
        elif name == "exit":
            args = [ArgSig(name="type"), ArgSig(name="value"), ArgSig(name="traceback")]
    if args is None:
        args = [ArgSig(name="*args"), ArgSig(name="**kwargs")]
    return [ArgSig(name=self_var or "self")] + args
