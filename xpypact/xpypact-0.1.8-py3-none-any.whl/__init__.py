"""The `xpypact` package.

Wraps FISPACT workflow. Transforms FISPACT output to xarray datasets.
"""
from importlib import metadata as _meta
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

__distribution__ = _meta.distribution(__name__)
__meta_data__ = __distribution__.metadata
__author__ = __meta_data__["Author"]
__author_email__ = __meta_data__["Author-email"]
__license__ = __meta_data__["License"]
__summary__ = __meta_data__["Summary"]
__copyright__ = f"Copyright 2021 {__author__}"
