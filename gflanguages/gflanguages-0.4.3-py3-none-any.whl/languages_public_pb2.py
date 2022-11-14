# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: languages_public.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='languages_public.proto',
  package='google.languages_public',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16languages_public.proto\x12\x17google.languages_public\"Q\n\x0bRegionProto\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x12\n\npopulation\x18\x03 \x01(\x05\x12\x14\n\x0cregion_group\x18\x04 \x03(\t\"\'\n\x0bScriptProto\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"\xb0\x02\n\rLanguageProto\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08language\x18\x02 \x01(\t\x12\x0e\n\x06script\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x16\n\x0epreferred_name\x18\x05 \x01(\t\x12\x0f\n\x07\x61utonym\x18\x06 \x01(\t\x12\x12\n\npopulation\x18\x07 \x01(\x05\x12\x0e\n\x06region\x18\x08 \x03(\t\x12\x43\n\x0e\x65xemplar_chars\x18\t \x01(\x0b\x32+.google.languages_public.ExemplarCharsProto\x12=\n\x0bsample_text\x18\n \x01(\x0b\x32(.google.languages_public.SampleTextProto\x12\x12\n\nhistorical\x18\x0b \x01(\x08\"z\n\x12\x45xemplarCharsProto\x12\x0c\n\x04\x62\x61se\x18\x01 \x01(\t\x12\x11\n\tauxiliary\x18\x02 \x01(\t\x12\r\n\x05marks\x18\x03 \x01(\t\x12\x10\n\x08numerals\x18\x04 \x01(\t\x12\x13\n\x0bpunctuation\x18\x05 \x01(\t\x12\r\n\x05index\x18\x06 \x01(\t\"\x84\x02\n\x0fSampleTextProto\x12\x15\n\rmasthead_full\x18\x01 \x01(\t\x12\x18\n\x10masthead_partial\x18\x02 \x01(\t\x12\x0e\n\x06styles\x18\x03 \x01(\t\x12\x0e\n\x06tester\x18\x04 \x01(\t\x12\x11\n\tposter_sm\x18\x05 \x01(\t\x12\x11\n\tposter_md\x18\x06 \x01(\t\x12\x11\n\tposter_lg\x18\x07 \x01(\t\x12\x13\n\x0bspecimen_48\x18\x08 \x01(\t\x12\x13\n\x0bspecimen_36\x18\t \x01(\t\x12\x13\n\x0bspecimen_32\x18\n \x01(\t\x12\x13\n\x0bspecimen_21\x18\x0b \x01(\t\x12\x13\n\x0bspecimen_16\x18\x0c \x01(\t'
)




_REGIONPROTO = _descriptor.Descriptor(
  name='RegionProto',
  full_name='google.languages_public.RegionProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='google.languages_public.RegionProto.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='google.languages_public.RegionProto.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='population', full_name='google.languages_public.RegionProto.population', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='region_group', full_name='google.languages_public.RegionProto.region_group', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=51,
  serialized_end=132,
)


_SCRIPTPROTO = _descriptor.Descriptor(
  name='ScriptProto',
  full_name='google.languages_public.ScriptProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='google.languages_public.ScriptProto.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='google.languages_public.ScriptProto.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=134,
  serialized_end=173,
)


_LANGUAGEPROTO = _descriptor.Descriptor(
  name='LanguageProto',
  full_name='google.languages_public.LanguageProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='google.languages_public.LanguageProto.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='language', full_name='google.languages_public.LanguageProto.language', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='script', full_name='google.languages_public.LanguageProto.script', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='google.languages_public.LanguageProto.name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='preferred_name', full_name='google.languages_public.LanguageProto.preferred_name', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='autonym', full_name='google.languages_public.LanguageProto.autonym', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='population', full_name='google.languages_public.LanguageProto.population', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='region', full_name='google.languages_public.LanguageProto.region', index=7,
      number=8, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='exemplar_chars', full_name='google.languages_public.LanguageProto.exemplar_chars', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sample_text', full_name='google.languages_public.LanguageProto.sample_text', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='historical', full_name='google.languages_public.LanguageProto.historical', index=10,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=176,
  serialized_end=480,
)


_EXEMPLARCHARSPROTO = _descriptor.Descriptor(
  name='ExemplarCharsProto',
  full_name='google.languages_public.ExemplarCharsProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='base', full_name='google.languages_public.ExemplarCharsProto.base', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='auxiliary', full_name='google.languages_public.ExemplarCharsProto.auxiliary', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='marks', full_name='google.languages_public.ExemplarCharsProto.marks', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='numerals', full_name='google.languages_public.ExemplarCharsProto.numerals', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='punctuation', full_name='google.languages_public.ExemplarCharsProto.punctuation', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='index', full_name='google.languages_public.ExemplarCharsProto.index', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=482,
  serialized_end=604,
)


_SAMPLETEXTPROTO = _descriptor.Descriptor(
  name='SampleTextProto',
  full_name='google.languages_public.SampleTextProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='masthead_full', full_name='google.languages_public.SampleTextProto.masthead_full', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='masthead_partial', full_name='google.languages_public.SampleTextProto.masthead_partial', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='styles', full_name='google.languages_public.SampleTextProto.styles', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tester', full_name='google.languages_public.SampleTextProto.tester', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='poster_sm', full_name='google.languages_public.SampleTextProto.poster_sm', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='poster_md', full_name='google.languages_public.SampleTextProto.poster_md', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='poster_lg', full_name='google.languages_public.SampleTextProto.poster_lg', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='specimen_48', full_name='google.languages_public.SampleTextProto.specimen_48', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='specimen_36', full_name='google.languages_public.SampleTextProto.specimen_36', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='specimen_32', full_name='google.languages_public.SampleTextProto.specimen_32', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='specimen_21', full_name='google.languages_public.SampleTextProto.specimen_21', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='specimen_16', full_name='google.languages_public.SampleTextProto.specimen_16', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=607,
  serialized_end=867,
)

_LANGUAGEPROTO.fields_by_name['exemplar_chars'].message_type = _EXEMPLARCHARSPROTO
_LANGUAGEPROTO.fields_by_name['sample_text'].message_type = _SAMPLETEXTPROTO
DESCRIPTOR.message_types_by_name['RegionProto'] = _REGIONPROTO
DESCRIPTOR.message_types_by_name['ScriptProto'] = _SCRIPTPROTO
DESCRIPTOR.message_types_by_name['LanguageProto'] = _LANGUAGEPROTO
DESCRIPTOR.message_types_by_name['ExemplarCharsProto'] = _EXEMPLARCHARSPROTO
DESCRIPTOR.message_types_by_name['SampleTextProto'] = _SAMPLETEXTPROTO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RegionProto = _reflection.GeneratedProtocolMessageType('RegionProto', (_message.Message,), {
  'DESCRIPTOR' : _REGIONPROTO,
  '__module__' : 'languages_public_pb2'
  # @@protoc_insertion_point(class_scope:google.languages_public.RegionProto)
  })
_sym_db.RegisterMessage(RegionProto)

ScriptProto = _reflection.GeneratedProtocolMessageType('ScriptProto', (_message.Message,), {
  'DESCRIPTOR' : _SCRIPTPROTO,
  '__module__' : 'languages_public_pb2'
  # @@protoc_insertion_point(class_scope:google.languages_public.ScriptProto)
  })
_sym_db.RegisterMessage(ScriptProto)

LanguageProto = _reflection.GeneratedProtocolMessageType('LanguageProto', (_message.Message,), {
  'DESCRIPTOR' : _LANGUAGEPROTO,
  '__module__' : 'languages_public_pb2'
  # @@protoc_insertion_point(class_scope:google.languages_public.LanguageProto)
  })
_sym_db.RegisterMessage(LanguageProto)

ExemplarCharsProto = _reflection.GeneratedProtocolMessageType('ExemplarCharsProto', (_message.Message,), {
  'DESCRIPTOR' : _EXEMPLARCHARSPROTO,
  '__module__' : 'languages_public_pb2'
  # @@protoc_insertion_point(class_scope:google.languages_public.ExemplarCharsProto)
  })
_sym_db.RegisterMessage(ExemplarCharsProto)

SampleTextProto = _reflection.GeneratedProtocolMessageType('SampleTextProto', (_message.Message,), {
  'DESCRIPTOR' : _SAMPLETEXTPROTO,
  '__module__' : 'languages_public_pb2'
  # @@protoc_insertion_point(class_scope:google.languages_public.SampleTextProto)
  })
_sym_db.RegisterMessage(SampleTextProto)


# @@protoc_insertion_point(module_scope)
