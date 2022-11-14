

""""""# start delvewheel patch
def _delvewheel_init_patch_1_1_1():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pupil_labs_uvc.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    if not is_pyinstaller or os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_init_patch_1_1_1()
del _delvewheel_init_patch_1_1_1
# end delvewheel patch

import logging

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version

# .uvc_bindings expects `logger` to be present
logger = logging.getLogger(__name__)

from .uvc_bindings import (  # noqa: E402
    Capture,
    Device_List,
    InitError,
    OpenError,
    StreamError,
    device_list,
    get_time_monotonic,
    is_accessible,
)

try:
    __version__ = version("pupil-labs-uvc")
except PackageNotFoundError:
    # package is not installed
    pass

__all__ = [
    "__version__",
    "Capture",
    "device_list",
    "Device_List",
    "get_time_monotonic",
    "InitError",
    "is_accessible",
    "OpenError",
    "StreamError",
]
