from setuptools import setup

name = "types-protobuf"
description = "Typing stubs for protobuf"
long_description = '''
## Typing stubs for protobuf

This is a PEP 561 type stub package for the `protobuf` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `protobuf`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/protobuf. All fixes for
types and metadata should be contributed there.

Generated with aid from mypy-protobuf v3.4.0

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `1733c460582e6bf83a3592e5b24f9fd0e3fdeddc`.
'''.lstrip()

setup(name=name,
      version="3.20.4.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/protobuf.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['google-stubs'],
      package_data={'google-stubs': ['__init__.pyi', 'protobuf/__init__.pyi', 'protobuf/any_pb2.pyi', 'protobuf/api_pb2.pyi', 'protobuf/compiler/__init__.pyi', 'protobuf/compiler/plugin_pb2.pyi', 'protobuf/descriptor.pyi', 'protobuf/descriptor_pb2.pyi', 'protobuf/descriptor_pool.pyi', 'protobuf/duration_pb2.pyi', 'protobuf/empty_pb2.pyi', 'protobuf/field_mask_pb2.pyi', 'protobuf/internal/__init__.pyi', 'protobuf/internal/api_implementation.pyi', 'protobuf/internal/containers.pyi', 'protobuf/internal/decoder.pyi', 'protobuf/internal/encoder.pyi', 'protobuf/internal/enum_type_wrapper.pyi', 'protobuf/internal/extension_dict.pyi', 'protobuf/internal/message_listener.pyi', 'protobuf/internal/python_message.pyi', 'protobuf/internal/type_checkers.pyi', 'protobuf/internal/well_known_types.pyi', 'protobuf/internal/wire_format.pyi', 'protobuf/json_format.pyi', 'protobuf/message.pyi', 'protobuf/message_factory.pyi', 'protobuf/reflection.pyi', 'protobuf/service.pyi', 'protobuf/source_context_pb2.pyi', 'protobuf/struct_pb2.pyi', 'protobuf/symbol_database.pyi', 'protobuf/text_format.pyi', 'protobuf/timestamp_pb2.pyi', 'protobuf/type_pb2.pyi', 'protobuf/util/__init__.pyi', 'protobuf/wrappers_pb2.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
