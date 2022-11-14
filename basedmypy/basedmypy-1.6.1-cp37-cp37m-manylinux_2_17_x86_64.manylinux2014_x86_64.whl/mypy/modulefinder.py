"""Low-level infrastructure to find modules.

This builds on fscache.py; find_sources.py builds on top of this.
"""

from __future__ import annotations

import ast
import collections
import functools
import os
import re
import subprocess
import sys
from enum import Enum, unique

from mypy.errors import CompileError

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from typing import Dict, List, NamedTuple, Optional, Tuple, Union
from typing_extensions import Final, TypeAlias as _TypeAlias

from mypy import pyinfo
from mypy.fscache import FileSystemCache
from mypy.nodes import MypyFile
from mypy.options import Options
from mypy.stubinfo import approved_stub_package_exists


# Paths to be searched in find_module().
class SearchPaths(NamedTuple):
    python_path: tuple[str, ...]  # where user code is found
    mypy_path: tuple[str, ...]  # from $MYPYPATH or config variable
    package_path: tuple[str, ...]  # from get_site_packages_dirs()
    typeshed_path: tuple[str, ...]  # paths in typeshed


# Package dirs are a two-tuple of path to search and whether to verify the module
OnePackageDir = Tuple[str, bool]
PackageDirs = List[OnePackageDir]

# Minimum and maximum Python versions for modules in stdlib as (major, minor)
StdlibVersions: _TypeAlias = Dict[str, Tuple[Tuple[int, int], Optional[Tuple[int, int]]]]

PYTHON_EXTENSIONS: Final = [".pyi", ".py"]


# TODO: Consider adding more reasons here?
# E.g. if we deduce a module would likely be found if the user were
# to set the --namespace-packages flag.
@unique
class ModuleNotFoundReason(Enum):
    # The module was not found: we found neither stubs nor a plausible code
    # implementation (with or without a py.typed file).
    NOT_FOUND = 0

    # The implementation for this module plausibly exists (e.g. we
    # found a matching folder or *.py file), but either the parent package
    # did not contain a py.typed file or we were unable to find a
    # corresponding *-stubs package.
    FOUND_WITHOUT_TYPE_HINTS = 1

    # The module was not found in the current working directory, but
    # was able to be found in the parent directory.
    WRONG_WORKING_DIRECTORY = 2

    # Stub PyPI package (typically types-pkgname) known to exist but not installed.
    APPROVED_STUBS_NOT_INSTALLED = 3

    def error_message_templates(self, daemon: bool) -> tuple[str, list[str]]:
        doc_link = "See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports"
        if self is ModuleNotFoundReason.NOT_FOUND:
            msg = 'Cannot find implementation or library stub for module named "{module}"'
            notes = [doc_link]
        elif self is ModuleNotFoundReason.WRONG_WORKING_DIRECTORY:
            msg = 'Cannot find implementation or library stub for module named "{module}"'
            notes = [
                "You may be running mypy in a subpackage, "
                "mypy should be run on the package root"
            ]
        elif self is ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS:
            msg = (
                'Skipping analyzing "{module}": module is installed, but missing library stubs '
                "or py.typed marker"
            )
            notes = [doc_link]
        elif self is ModuleNotFoundReason.APPROVED_STUBS_NOT_INSTALLED:
            msg = 'Library stubs not installed for "{module}"'
            notes = ['Hint: "python3 -m pip install {stub_dist}"']
            if not daemon:
                notes.append(
                    '(or run "mypy --install-types" to install all missing stub packages)'
                )
            notes.append(doc_link)
        else:
            assert False
        return msg, notes


# If we found the module, returns the path to the module as a str.
# Otherwise, returns the reason why the module wasn't found.
ModuleSearchResult = Union[str, ModuleNotFoundReason]


class BuildSource:
    """A single source file."""

    def __init__(
        self,
        path: str | None,
        module: str | None,
        text: str | None = None,
        base_dir: str | None = None,
        followed: bool = False,
    ) -> None:
        self.path = path  # File where it's found (e.g. 'xxx/yyy/foo/bar.py')
        self.module = module or "__main__"  # Module name (e.g. 'foo.bar')
        self.text = text  # Source code, if initially supplied, else None
        self.base_dir = base_dir  # Directory where the package is rooted (e.g. 'xxx/yyy')
        self.followed = followed  # Was this found by following imports?

    def __repr__(self) -> str:
        return (
            "BuildSource(path={!r}, module={!r}, has_text={}, base_dir={!r}, followed={})".format(
                self.path, self.module, self.text is not None, self.base_dir, self.followed
            )
        )


class BuildSourceSet:
    """Helper to efficiently test a file's membership in a set of build sources."""

    def __init__(self, sources: list[BuildSource]) -> None:
        self.source_text_present = False
        self.source_modules: dict[str, str] = {}
        self.source_paths: set[str] = set()

        for source in sources:
            if source.text is not None:
                self.source_text_present = True
            if source.path:
                self.source_paths.add(source.path)
            if source.module:
                self.source_modules[source.module] = source.path or ""

    def is_source(self, file: MypyFile) -> bool:
        if file.path and file.path in self.source_paths:
            return True
        elif file._fullname in self.source_modules:
            return True
        elif self.source_text_present:
            return True
        else:
            return False


class FindModuleCache:
    """Module finder with integrated cache.

    Module locations and some intermediate results are cached internally
    and can be cleared with the clear() method.

    All file system accesses are performed through a FileSystemCache,
    which is not ever cleared by this class. If necessary it must be
    cleared by client code.
    """

    def __init__(
        self,
        search_paths: SearchPaths,
        fscache: FileSystemCache | None,
        options: Options | None,
        stdlib_py_versions: StdlibVersions | None = None,
        source_set: BuildSourceSet | None = None,
    ) -> None:
        self.search_paths = search_paths
        self.source_set = source_set
        self.fscache = fscache or FileSystemCache()
        # Cache for get_toplevel_possibilities:
        # search_paths -> (toplevel_id -> list(package_dirs))
        self.initial_components: dict[tuple[str, ...], dict[str, list[str]]] = {}
        # Cache find_module: id -> result
        self.results: dict[str, ModuleSearchResult] = {}
        self.ns_ancestors: dict[str, str] = {}
        self.options = options
        custom_typeshed_dir = None
        if options:
            custom_typeshed_dir = options.custom_typeshed_dir
        self.stdlib_py_versions = stdlib_py_versions or load_stdlib_py_versions(
            custom_typeshed_dir
        )

    def clear(self) -> None:
        self.results.clear()
        self.initial_components.clear()
        self.ns_ancestors.clear()

    def find_module_via_source_set(self, id: str) -> ModuleSearchResult | None:
        """Fast path to find modules by looking through the input sources

        This is only used when --fast-module-lookup is passed on the command line."""
        if not self.source_set:
            return None

        p = self.source_set.source_modules.get(id, None)
        if p and self.fscache.isfile(p):
            # We need to make sure we still have __init__.py all the way up
            # otherwise we might have false positives compared to slow path
            # in case of deletion of init files, which is covered by some tests.
            # TODO: are there some combination of flags in which this check should be skipped?
            d = os.path.dirname(p)
            for _ in range(id.count(".")):
                if not any(
                    self.fscache.isfile(os.path.join(d, "__init__" + x)) for x in PYTHON_EXTENSIONS
                ):
                    return None
                d = os.path.dirname(d)
            return p

        idx = id.rfind(".")
        if idx != -1:
            # When we're looking for foo.bar.baz and can't find a matching module
            # in the source set, look up for a foo.bar module.
            parent = self.find_module_via_source_set(id[:idx])
            if parent is None or not isinstance(parent, str):
                return None

            basename, ext = os.path.splitext(parent)
            if not any(parent.endswith("__init__" + x) for x in PYTHON_EXTENSIONS) and (
                ext in PYTHON_EXTENSIONS and not self.fscache.isdir(basename)
            ):
                # If we do find such a *module* (and crucially, we don't want a package,
                # hence the filtering out of __init__ files, and checking for the presence
                # of a folder with a matching name), then we can be pretty confident that
                # 'baz' will either be a top-level variable in foo.bar, or will not exist.
                #
                # Either way, spelunking in other search paths for another 'foo.bar.baz'
                # module should be avoided because:
                #  1. in the unlikely event that one were found, it's highly likely that
                #     it would be unrelated to the source being typechecked and therefore
                #     more likely to lead to erroneous results
                #  2. as described in _find_module, in some cases the search itself could
                #  potentially waste significant amounts of time
                return ModuleNotFoundReason.NOT_FOUND
        return None

    def find_lib_path_dirs(self, id: str, lib_path: tuple[str, ...]) -> PackageDirs:
        """Find which elements of a lib_path have the directory a module needs to exist.

        This is run for the python_path, mypy_path, and typeshed_path search paths.
        """
        components = id.split(".")
        dir_chain = os.sep.join(components[:-1])  # e.g., 'foo/bar'

        dirs = []
        for pathitem in self.get_toplevel_possibilities(lib_path, components[0]):
            # e.g., '/usr/lib/python3.4/foo/bar'
            dir = os.path.normpath(os.path.join(pathitem, dir_chain))
            if self.fscache.isdir(dir):
                dirs.append((dir, True))
        return dirs

    def get_toplevel_possibilities(self, lib_path: tuple[str, ...], id: str) -> list[str]:
        """Find which elements of lib_path could contain a particular top-level module.

        In practice, almost all modules can be routed to the correct entry in
        lib_path by looking at just the first component of the module name.

        We take advantage of this by enumerating the contents of all of the
        directories on the lib_path and building a map of which entries in
        the lib_path could contain each potential top-level module that appears.
        """

        if lib_path in self.initial_components:
            return self.initial_components[lib_path].get(id, [])

        # Enumerate all the files in the directories on lib_path and produce the map
        components: dict[str, list[str]] = {}
        for dir in lib_path:
            try:
                contents = self.fscache.listdir(dir)
            except OSError:
                contents = []
            # False positives are fine for correctness here, since we will check
            # precisely later, so we only look at the root of every filename without
            # any concern for the exact details.
            for name in contents:
                name = os.path.splitext(name)[0]
                components.setdefault(name, []).append(dir)

        self.initial_components[lib_path] = components
        return components.get(id, [])

    def find_module(self, id: str, *, fast_path: bool = False) -> ModuleSearchResult:
        """Return the path of the module source file or why it wasn't found.

        If fast_path is True, prioritize performance over generating detailed
        error descriptions.
        """
        if id not in self.results:
            top_level = id.partition(".")[0]
            use_typeshed = True
            if id in self.stdlib_py_versions:
                use_typeshed = self._typeshed_has_version(id)
            elif top_level in self.stdlib_py_versions:
                use_typeshed = self._typeshed_has_version(top_level)
            self.results[id] = self._find_module(id, use_typeshed)
            if (
                not (fast_path or (self.options is not None and self.options.fast_module_lookup))
                and self.results[id] is ModuleNotFoundReason.NOT_FOUND
                and self._can_find_module_in_parent_dir(id)
            ):
                self.results[id] = ModuleNotFoundReason.WRONG_WORKING_DIRECTORY
        return self.results[id]

    def _typeshed_has_version(self, module: str) -> bool:
        if not self.options:
            return True
        version = typeshed_py_version(self.options)
        min_version, max_version = self.stdlib_py_versions[module]
        return version >= min_version and (max_version is None or version <= max_version)

    def _find_module_non_stub_helper(
        self, components: list[str], pkg_dir: str
    ) -> OnePackageDir | ModuleNotFoundReason:
        plausible_match = False
        dir_path = pkg_dir
        for index, component in enumerate(components):
            dir_path = os.path.join(dir_path, component)
            if self.fscache.isfile(os.path.join(dir_path, "py.typed")):
                return os.path.join(pkg_dir, *components[:-1]), index == 0
            elif not plausible_match and (
                self.fscache.isdir(dir_path) or self.fscache.isfile(dir_path + ".py")
            ):
                plausible_match = True
            # If this is not a directory then we can't traverse further into it
            if not self.fscache.isdir(dir_path):
                break
        if approved_stub_package_exists(components[0]):
            if len(components) == 1 or (
                self.find_module(components[0])
                is ModuleNotFoundReason.APPROVED_STUBS_NOT_INSTALLED
            ):
                return ModuleNotFoundReason.APPROVED_STUBS_NOT_INSTALLED
        if approved_stub_package_exists(".".join(components[:2])):
            return ModuleNotFoundReason.APPROVED_STUBS_NOT_INSTALLED
        if plausible_match:
            return ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS
        else:
            return ModuleNotFoundReason.NOT_FOUND

    def _update_ns_ancestors(self, components: list[str], match: tuple[str, bool]) -> None:
        path, verify = match
        for i in range(1, len(components)):
            pkg_id = ".".join(components[:-i])
            if pkg_id not in self.ns_ancestors and self.fscache.isdir(path):
                self.ns_ancestors[pkg_id] = path
            path = os.path.dirname(path)

    def _can_find_module_in_parent_dir(self, id: str) -> bool:
        """Test if a module can be found by checking the parent directories
        of the current working directory.
        """
        working_dir = os.getcwd()
        parent_search = FindModuleCache(
            SearchPaths((), (), (), ()),
            self.fscache,
            self.options,
            stdlib_py_versions=self.stdlib_py_versions,
        )
        while any(is_init_file(file) for file in os.listdir(working_dir)):
            working_dir = os.path.dirname(working_dir)
            parent_search.search_paths = SearchPaths((working_dir,), (), (), ())
            if not isinstance(parent_search._find_module(id, False), ModuleNotFoundReason):
                return True
        return False

    def _find_module(self, id: str, use_typeshed: bool) -> ModuleSearchResult:
        fscache = self.fscache

        # Fast path for any modules in the current source set.
        # This is particularly important when there are a large number of search
        # paths which share the first (few) component(s) due to the use of namespace
        # packages, for instance:
        # foo/
        #    company/
        #        __init__.py
        #        foo/
        # bar/
        #    company/
        #        __init__.py
        #        bar/
        # baz/
        #    company/
        #        __init__.py
        #        baz/
        #
        # mypy gets [foo/company/foo, bar/company/bar, baz/company/baz, ...] as input
        # and computes [foo, bar, baz, ...] as the module search path.
        #
        # This would result in O(n) search for every import of company.*, leading to
        # O(n**2) behavior in load_graph as such imports are unsurprisingly present
        # at least once, and usually many more times than that, in each and every file
        # being parsed.
        #
        # Thankfully, such cases are efficiently handled by looking up the module path
        # via BuildSourceSet.
        p = (
            self.find_module_via_source_set(id)
            if (self.options is not None and self.options.fast_module_lookup)
            else None
        )
        if p:
            return p

        # If we're looking for a module like 'foo.bar.baz', it's likely that most of the
        # many elements of lib_path don't even have a subdirectory 'foo/bar'.  Discover
        # that only once and cache it for when we look for modules like 'foo.bar.blah'
        # that will require the same subdirectory.
        components = id.split(".")
        dir_chain = os.sep.join(components[:-1])  # e.g., 'foo/bar'

        # We have two sets of folders so that we collect *all* stubs folders and
        # put them in the front of the search path
        third_party_inline_dirs: PackageDirs = []
        third_party_stubs_dirs: PackageDirs = []
        found_possible_third_party_missing_type_hints = False
        need_installed_stubs = False
        # Third-party stub/typed packages
        for pkg_dir in self.search_paths.package_path:
            stub_name = components[0] + "-stubs"
            stub_dir = os.path.join(pkg_dir, stub_name)
            if fscache.isdir(stub_dir) and self._is_compatible_stub_package(stub_dir):
                stub_typed_file = os.path.join(stub_dir, "py.typed")
                stub_components = [stub_name] + components[1:]
                path = os.path.join(pkg_dir, *stub_components[:-1])
                if fscache.isdir(path):
                    if fscache.isfile(stub_typed_file):
                        # Stub packages can have a py.typed file, which must include
                        # 'partial\n' to make the package partial
                        # Partial here means that mypy should look at the runtime
                        # package if installed.
                        if fscache.read(stub_typed_file).decode().strip() == "partial":
                            runtime_path = os.path.join(pkg_dir, dir_chain)
                            third_party_inline_dirs.append((runtime_path, True))
                            # if the package is partial, we don't verify the module, as
                            # the partial stub package may not have a __init__.pyi
                            third_party_stubs_dirs.append((path, False))
                        else:
                            # handle the edge case where people put a py.typed file
                            # in a stub package, but it isn't partial
                            third_party_stubs_dirs.append((path, True))
                    else:
                        third_party_stubs_dirs.append((path, True))
            non_stub_match = self._find_module_non_stub_helper(components, pkg_dir)
            if isinstance(non_stub_match, ModuleNotFoundReason):
                if non_stub_match is ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS:
                    found_possible_third_party_missing_type_hints = True
                elif non_stub_match is ModuleNotFoundReason.APPROVED_STUBS_NOT_INSTALLED:
                    need_installed_stubs = True
            else:
                third_party_inline_dirs.append(non_stub_match)
                self._update_ns_ancestors(components, non_stub_match)
        if self.options and self.options.use_builtins_fixtures:
            # Everything should be in fixtures.
            third_party_inline_dirs.clear()
            third_party_stubs_dirs.clear()
            found_possible_third_party_missing_type_hints = False
        python_mypy_path = self.search_paths.mypy_path + self.search_paths.python_path
        candidate_base_dirs = self.find_lib_path_dirs(id, python_mypy_path)
        if use_typeshed:
            # Search for stdlib stubs in typeshed before installed
            # stubs to avoid picking up backports (dataclasses, for
            # example) when the library is included in stdlib.
            candidate_base_dirs += self.find_lib_path_dirs(id, self.search_paths.typeshed_path)
        candidate_base_dirs += third_party_stubs_dirs + third_party_inline_dirs

        # If we're looking for a module like 'foo.bar.baz', then candidate_base_dirs now
        # contains just the subdirectories 'foo/bar' that actually exist under the
        # elements of lib_path.  This is probably much shorter than lib_path itself.
        # Now just look for 'baz.pyi', 'baz/__init__.py', etc., inside those directories.
        seplast = os.sep + components[-1]  # so e.g. '/baz'
        sepinit = os.sep + "__init__"
        near_misses = []  # Collect near misses for namespace mode (see below).
        for base_dir, verify in candidate_base_dirs:
            base_path = base_dir + seplast  # so e.g. '/usr/lib/python3.4/foo/bar/baz'
            has_init = False
            dir_prefix = base_dir
            for _ in range(len(components) - 1):
                dir_prefix = os.path.dirname(dir_prefix)
            # Prefer package over module, i.e. baz/__init__.py* over baz.py*.
            for extension in PYTHON_EXTENSIONS:
                path = base_path + sepinit + extension
                path_stubs = base_path + "-stubs" + sepinit + extension
                if fscache.isfile_case(path, dir_prefix):
                    has_init = True
                    if verify and not verify_module(fscache, id, path, dir_prefix):
                        near_misses.append((path, dir_prefix))
                        continue
                    return path
                elif fscache.isfile_case(path_stubs, dir_prefix):
                    if verify and not verify_module(fscache, id, path_stubs, dir_prefix):
                        near_misses.append((path_stubs, dir_prefix))
                        continue
                    return path_stubs

            # In namespace mode, register a potential namespace package
            if self.options and self.options.namespace_packages:
                if fscache.exists_case(base_path, dir_prefix) and not has_init:
                    near_misses.append((base_path, dir_prefix))

            # No package, look for module.
            for extension in PYTHON_EXTENSIONS:
                path = base_path + extension
                if fscache.isfile_case(path, dir_prefix):
                    if verify and not verify_module(fscache, id, path, dir_prefix):
                        near_misses.append((path, dir_prefix))
                        continue
                    return path

        # In namespace mode, re-check those entries that had 'verify'.
        # Assume search path entries xxx, yyy and zzz, and we're
        # looking for foo.bar.baz.  Suppose near_misses has:
        #
        # - xxx/foo/bar/baz.py
        # - yyy/foo/bar/baz/__init__.py
        # - zzz/foo/bar/baz.pyi
        #
        # If any of the foo directories has __init__.py[i], it wins.
        # Else, we look for foo/bar/__init__.py[i], etc.  If there are
        # none, the first hit wins.  Note that this does not take into
        # account whether the lowest-level module is a file (baz.py),
        # a package (baz/__init__.py), or a stub file (baz.pyi) -- for
        # these the first one encountered along the search path wins.
        #
        # The helper function highest_init_level() returns an int that
        # indicates the highest level at which a __init__.py[i] file
        # is found; if no __init__ was found it returns 0, if we find
        # only foo/bar/__init__.py it returns 1, and if we have
        # foo/__init__.py it returns 2 (regardless of what's in
        # foo/bar).  It doesn't look higher than that.
        if self.options and self.options.namespace_packages and near_misses:
            levels = [
                highest_init_level(fscache, id, path, dir_prefix)
                for path, dir_prefix in near_misses
            ]
            index = levels.index(max(levels))
            return near_misses[index][0]

        # Finally, we may be asked to produce an ancestor for an
        # installed package with a py.typed marker that is a
        # subpackage of a namespace package.  We only fess up to these
        # if we would otherwise return "not found".
        ancestor = self.ns_ancestors.get(id)
        if ancestor is not None:
            return ancestor

        if need_installed_stubs:
            return ModuleNotFoundReason.APPROVED_STUBS_NOT_INSTALLED
        elif found_possible_third_party_missing_type_hints:
            return ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS
        else:
            return ModuleNotFoundReason.NOT_FOUND

    def _is_compatible_stub_package(self, stub_dir: str) -> bool:
        """Does a stub package support the target Python version?

        Stub packages may contain a metadata file which specifies
        whether the stubs are compatible with Python 2 and 3.
        """
        metadata_fnam = os.path.join(stub_dir, "METADATA.toml")
        if os.path.isfile(metadata_fnam):
            with open(metadata_fnam, "rb") as f:
                metadata = tomllib.load(f)
            return bool(metadata.get("python3", True))
        return True

    def find_modules_recursive(self, module: str) -> list[BuildSource]:
        module_path = self.find_module(module)
        if isinstance(module_path, ModuleNotFoundReason):
            return []
        sources = [BuildSource(module_path, module, None)]

        package_path = None
        if is_init_file(module_path):
            package_path = os.path.dirname(module_path)
        elif self.fscache.isdir(module_path):
            package_path = module_path
        if package_path is None:
            return sources

        # This logic closely mirrors that in find_sources. One small but important difference is
        # that we do not sort names with keyfunc. The recursive call to find_modules_recursive
        # calls find_module, which will handle the preference between packages, pyi and py.
        # Another difference is it doesn't handle nested search paths / package roots.

        seen: set[str] = set()
        names = sorted(self.fscache.listdir(package_path))
        for name in names:
            # Skip certain names altogether
            if name in ("__pycache__", "site-packages", "node_modules") or name.startswith("."):
                continue
            subpath = os.path.join(package_path, name)

            if self.options and matches_exclude(
                subpath, self.options.exclude, self.fscache, self.options.verbosity >= 2
            ):
                continue

            if self.fscache.isdir(subpath):
                # Only recurse into packages
                if (self.options and self.options.namespace_packages) or (
                    self.fscache.isfile(os.path.join(subpath, "__init__.py"))
                    or self.fscache.isfile(os.path.join(subpath, "__init__.pyi"))
                ):
                    seen.add(name)
                    sources.extend(self.find_modules_recursive(module + "." + name))
            else:
                stem, suffix = os.path.splitext(name)
                if stem == "__init__":
                    continue
                if stem not in seen and "." not in stem and suffix in PYTHON_EXTENSIONS:
                    # (If we sorted names by keyfunc) we could probably just make the BuildSource
                    # ourselves, but this ensures compatibility with find_module / the cache
                    seen.add(stem)
                    sources.extend(self.find_modules_recursive(module + "." + stem))
        return sources


def matches_exclude(
    subpath: str, excludes: list[str], fscache: FileSystemCache, verbose: bool
) -> bool:
    if not excludes:
        return False
    subpath_str = os.path.relpath(subpath).replace(os.sep, "/")
    if fscache.isdir(subpath):
        subpath_str += "/"
    for exclude in excludes:
        if re.search(exclude, subpath_str):
            if verbose:
                print(
                    f"TRACE: Excluding {subpath_str} (matches pattern {exclude})", file=sys.stderr
                )
            return True
    return False


def is_init_file(path: str) -> bool:
    return os.path.basename(path) in ("__init__.py", "__init__.pyi")


def verify_module(fscache: FileSystemCache, id: str, path: str, prefix: str) -> bool:
    """Check that all packages containing id have a __init__ file."""
    if is_init_file(path):
        path = os.path.dirname(path)
    for i in range(id.count(".")):
        path = os.path.dirname(path)
        if not any(
            fscache.isfile_case(os.path.join(path, f"__init__{extension}"), prefix)
            for extension in PYTHON_EXTENSIONS
        ):
            return False
    return True


def highest_init_level(fscache: FileSystemCache, id: str, path: str, prefix: str) -> int:
    """Compute the highest level where an __init__ file is found."""
    if is_init_file(path):
        path = os.path.dirname(path)
    level = 0
    for i in range(id.count(".")):
        path = os.path.dirname(path)
        if any(
            fscache.isfile_case(os.path.join(path, f"__init__{extension}"), prefix)
            for extension in PYTHON_EXTENSIONS
        ):
            level = i + 1
    return level


def mypy_path() -> list[str]:
    path_env = os.getenv("MYPYPATH")
    if not path_env:
        return []
    return path_env.split(os.pathsep)


def default_lib_path(
    data_dir: str, pyversion: tuple[int, int], custom_typeshed_dir: str | None
) -> list[str]:
    """Return default standard library search paths."""
    path: list[str] = []

    if custom_typeshed_dir:
        typeshed_dir = os.path.join(custom_typeshed_dir, "stdlib")
        mypy_extensions_dir = os.path.join(custom_typeshed_dir, "stubs", "mypy-extensions")
        versions_file = os.path.join(typeshed_dir, "VERSIONS")
        if not os.path.isdir(typeshed_dir) or not os.path.isfile(versions_file):
            print(
                "error: --custom-typeshed-dir does not point to a valid typeshed ({})".format(
                    custom_typeshed_dir
                )
            )
            sys.exit(2)
    else:
        auto = os.path.join(data_dir, "stubs-auto")
        if os.path.isdir(auto):
            data_dir = auto
        typeshed_dir = os.path.join(data_dir, "typeshed", "stdlib")
        mypy_extensions_dir = os.path.join(data_dir, "typeshed", "stubs", "mypy-extensions")
    path.append(typeshed_dir)

    # Get mypy-extensions stubs from typeshed, since we treat it as an
    # "internal" library, similar to typing and typing-extensions.
    path.append(mypy_extensions_dir)

    # Add fallback path that can be used if we have a broken installation.
    if sys.platform != "win32":
        path.append("/usr/local/lib/mypy")
    if not path:
        print(
            "Could not resolve typeshed subdirectories. Your mypy install is broken.\n"
            "Python executable is located at {}.\nMypy located at {}".format(
                sys.executable, data_dir
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    return path


@functools.lru_cache(maxsize=None)
def get_search_dirs(python_executable: str | None) -> tuple[list[str], list[str]]:
    """Find package directories for given python.

    This runs a subprocess call, which generates a list of the directories in sys.path.
    To avoid repeatedly calling a subprocess (which can be slow!) we
    lru_cache the results.
    """

    if python_executable is None:
        return ([], [])
    elif python_executable == sys.executable:
        # Use running Python's package dirs
        sys_path, site_packages = pyinfo.getsearchdirs()
    else:
        # Use subprocess to get the package directory of given Python
        # executable
        try:
            sys_path, site_packages = ast.literal_eval(
                subprocess.check_output(
                    [python_executable, pyinfo.__file__, "getsearchdirs"], stderr=subprocess.PIPE
                ).decode()
            )
        except OSError as err:
            reason = os.strerror(err.errno)
            raise CompileError(
                [f"mypy: Invalid python executable '{python_executable}': {reason}"]
            ) from err
    return sys_path, site_packages


def compute_search_paths(
    sources: list[BuildSource], options: Options, data_dir: str, alt_lib_path: str | None = None
) -> SearchPaths:
    """Compute the search paths as specified in PEP 561.

    There are the following 4 members created:
    - User code (from `sources`)
    - MYPYPATH (set either via config or environment variable)
    - installed package directories (which will later be split into stub-only and inline)
    - typeshed
    """
    # Determine the default module search path.
    lib_path = collections.deque(
        default_lib_path(
            data_dir, options.python_version, custom_typeshed_dir=options.custom_typeshed_dir
        )
    )

    if options.use_builtins_fixtures:
        # Use stub builtins (to speed up test cases and to make them easier to
        # debug).  This is a test-only feature, so assume our files are laid out
        # as in the source tree.
        # We also need to allow overriding where to look for it. Argh.
        root_dir = os.getenv("MYPY_TEST_PREFIX", None)
        if not root_dir:
            root_dir = os.path.dirname(os.path.dirname(__file__))
        lib_path.appendleft(os.path.join(root_dir, "test-data", "unit", "lib-stub"))
    # alt_lib_path is used by some tests to bypass the normal lib_path mechanics.
    # If we don't have one, grab directories of source files.
    python_path: list[str] = []
    if not alt_lib_path:
        for source in sources:
            # Include directory of the program file in the module search path.
            if source.base_dir:
                dir = source.base_dir
                if dir not in python_path:
                    python_path.append(dir)

        # Do this even if running as a file, for sanity (mainly because with
        # multiple builds, there could be a mix of files/modules, so its easier
        # to just define the semantics that we always add the current director
        # to the lib_path
        # TODO: Don't do this in some cases; for motivation see see
        # https://github.com/python/mypy/issues/4195#issuecomment-341915031
        if options.bazel:
            dir = "."
        else:
            dir = os.getcwd()
        if dir not in lib_path:
            python_path.insert(0, dir)

    # Start with a MYPYPATH environment variable at the front of the mypy_path, if defined.
    mypypath = mypy_path()

    # Add a config-defined mypy path.
    mypypath.extend(options.mypy_path)

    # If provided, insert the caller-supplied extra module path to the
    # beginning (highest priority) of the search path.
    if alt_lib_path:
        mypypath.insert(0, alt_lib_path)

    sys_path, site_packages = get_search_dirs(options.python_executable)
    # We only use site packages for this check
    for site in site_packages:
        assert site not in lib_path
        if (
            site in mypypath
            or any(p.startswith(site + os.path.sep) for p in mypypath)
            or (os.path.altsep and any(p.startswith(site + os.path.altsep) for p in mypypath))
        ):
            print(f"{site} is in the MYPYPATH. Please remove it.", file=sys.stderr)
            print(
                "See https://mypy.readthedocs.io/en/stable/running_mypy.html"
                "#how-mypy-handles-imports for more info",
                file=sys.stderr,
            )
            sys.exit(1)

    return SearchPaths(
        python_path=tuple(reversed(python_path)),
        mypy_path=tuple(mypypath),
        package_path=tuple(sys_path + site_packages),
        typeshed_path=tuple(lib_path),
    )


def load_stdlib_py_versions(custom_typeshed_dir: str | None) -> StdlibVersions:
    """Return dict with minimum and maximum Python versions of stdlib modules.

    The contents look like
    {..., 'secrets': ((3, 6), None), 'symbol': ((2, 7), (3, 9)), ...}

    None means there is no maximum version.
    """
    typeshed_dir = custom_typeshed_dir or os.path.join(os.path.dirname(__file__), "typeshed")
    stdlib_dir = os.path.join(typeshed_dir, "stdlib")
    result = {}

    versions_path = os.path.join(stdlib_dir, "VERSIONS")
    assert os.path.isfile(versions_path), (custom_typeshed_dir, versions_path, __file__)
    with open(versions_path) as f:
        for line in f:
            line = line.split("#")[0].strip()
            if line == "":
                continue
            module, version_range = line.split(":")
            versions = version_range.split("-")
            min_version = parse_version(versions[0])
            max_version = (
                parse_version(versions[1]) if len(versions) >= 2 and versions[1].strip() else None
            )
            result[module] = min_version, max_version
    return result


def parse_version(version: str) -> tuple[int, int]:
    major, minor = version.strip().split(".")
    return int(major), int(minor)


def typeshed_py_version(options: Options) -> tuple[int, int]:
    """Return Python version used for checking whether module supports typeshed."""
    # Typeshed no longer covers Python 3.x versions before 3.7, so 3.7 is
    # the earliest we can support.
    return max(options.python_version, (3, 7))
