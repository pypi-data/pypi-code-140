"""For space rocks."""

import inspect
from pathlib import Path

from . import config

# Welcome to rocks
__version__ = "1.6.7"

# Only define user API if rocks is not called via command line
context = inspect.stack()[-1].code_context
if context is None or "rocks.cli" not in context[0]:

    # Expose API to user
    from .core import Rock
    from .core import rocks_ as rocks
    from .resolve import identify

    # Alias id to identify
    id = identify

# Ensure the asteroid name-number index exists
if not config.PATH_INDEX.is_dir():
    from . import index

    index._ensure_index_exists()
