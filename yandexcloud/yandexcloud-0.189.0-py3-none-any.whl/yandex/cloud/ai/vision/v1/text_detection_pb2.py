# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/ai/vision/v1/text_detection.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from yandex.cloud.ai.vision.v1 import primitives_pb2 as yandex_dot_cloud_dot_ai_dot_vision_dot_v1_dot_primitives__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yandex/cloud/ai/vision/v1/text_detection.proto',
  package='yandex.cloud.ai.vision.v1',
  syntax='proto3',
  serialized_options=b'\n\035yandex.cloud.api.ai.vision.v1ZDgithub.com/yandex-cloud/go-genproto/yandex/cloud/ai/vision/v1;vision',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n.yandex/cloud/ai/vision/v1/text_detection.proto\x12\x19yandex.cloud.ai.vision.v1\x1a*yandex/cloud/ai/vision/v1/primitives.proto\"@\n\x0eTextAnnotation\x12.\n\x05pages\x18\x01 \x03(\x0b\x32\x1f.yandex.cloud.ai.vision.v1.Page\"\x8c\x01\n\x04Page\x12\r\n\x05width\x18\x01 \x01(\x03\x12\x0e\n\x06height\x18\x02 \x01(\x03\x12\x30\n\x06\x62locks\x18\x03 \x03(\x0b\x32 .yandex.cloud.ai.vision.v1.Block\x12\x33\n\x08\x65ntities\x18\x04 \x03(\x0b\x32!.yandex.cloud.ai.vision.v1.Entity\"$\n\x06\x45ntity\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t\"q\n\x05\x42lock\x12\x38\n\x0c\x62ounding_box\x18\x01 \x01(\x0b\x32\".yandex.cloud.ai.vision.v1.Polygon\x12.\n\x05lines\x18\x02 \x03(\x0b\x32\x1f.yandex.cloud.ai.vision.v1.Line\"\x84\x01\n\x04Line\x12\x38\n\x0c\x62ounding_box\x18\x01 \x01(\x0b\x32\".yandex.cloud.ai.vision.v1.Polygon\x12.\n\x05words\x18\x02 \x03(\x0b\x32\x1f.yandex.cloud.ai.vision.v1.Word\x12\x12\n\nconfidence\x18\x03 \x01(\x01\"\xfc\x01\n\x04Word\x12\x38\n\x0c\x62ounding_box\x18\x01 \x01(\x0b\x32\".yandex.cloud.ai.vision.v1.Polygon\x12\x0c\n\x04text\x18\x02 \x01(\t\x12\x12\n\nconfidence\x18\x03 \x01(\x01\x12\x43\n\tlanguages\x18\x04 \x03(\x0b\x32\x30.yandex.cloud.ai.vision.v1.Word.DetectedLanguage\x12\x14\n\x0c\x65ntity_index\x18\x05 \x01(\x03\x1a=\n\x10\x44\x65tectedLanguage\x12\x15\n\rlanguage_code\x18\x01 \x01(\t\x12\x12\n\nconfidence\x18\x02 \x01(\x01\x42\x65\n\x1dyandex.cloud.api.ai.vision.v1ZDgithub.com/yandex-cloud/go-genproto/yandex/cloud/ai/vision/v1;visionb\x06proto3'
  ,
  dependencies=[yandex_dot_cloud_dot_ai_dot_vision_dot_v1_dot_primitives__pb2.DESCRIPTOR,])




_TEXTANNOTATION = _descriptor.Descriptor(
  name='TextAnnotation',
  full_name='yandex.cloud.ai.vision.v1.TextAnnotation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pages', full_name='yandex.cloud.ai.vision.v1.TextAnnotation.pages', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=121,
  serialized_end=185,
)


_PAGE = _descriptor.Descriptor(
  name='Page',
  full_name='yandex.cloud.ai.vision.v1.Page',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='width', full_name='yandex.cloud.ai.vision.v1.Page.width', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='height', full_name='yandex.cloud.ai.vision.v1.Page.height', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='blocks', full_name='yandex.cloud.ai.vision.v1.Page.blocks', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entities', full_name='yandex.cloud.ai.vision.v1.Page.entities', index=3,
      number=4, type=11, cpp_type=10, label=3,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=188,
  serialized_end=328,
)


_ENTITY = _descriptor.Descriptor(
  name='Entity',
  full_name='yandex.cloud.ai.vision.v1.Entity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='yandex.cloud.ai.vision.v1.Entity.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='text', full_name='yandex.cloud.ai.vision.v1.Entity.text', index=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=330,
  serialized_end=366,
)


_BLOCK = _descriptor.Descriptor(
  name='Block',
  full_name='yandex.cloud.ai.vision.v1.Block',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bounding_box', full_name='yandex.cloud.ai.vision.v1.Block.bounding_box', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lines', full_name='yandex.cloud.ai.vision.v1.Block.lines', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=368,
  serialized_end=481,
)


_LINE = _descriptor.Descriptor(
  name='Line',
  full_name='yandex.cloud.ai.vision.v1.Line',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bounding_box', full_name='yandex.cloud.ai.vision.v1.Line.bounding_box', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='words', full_name='yandex.cloud.ai.vision.v1.Line.words', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='confidence', full_name='yandex.cloud.ai.vision.v1.Line.confidence', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=484,
  serialized_end=616,
)


_WORD_DETECTEDLANGUAGE = _descriptor.Descriptor(
  name='DetectedLanguage',
  full_name='yandex.cloud.ai.vision.v1.Word.DetectedLanguage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='language_code', full_name='yandex.cloud.ai.vision.v1.Word.DetectedLanguage.language_code', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='confidence', full_name='yandex.cloud.ai.vision.v1.Word.DetectedLanguage.confidence', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=810,
  serialized_end=871,
)

_WORD = _descriptor.Descriptor(
  name='Word',
  full_name='yandex.cloud.ai.vision.v1.Word',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bounding_box', full_name='yandex.cloud.ai.vision.v1.Word.bounding_box', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='text', full_name='yandex.cloud.ai.vision.v1.Word.text', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='confidence', full_name='yandex.cloud.ai.vision.v1.Word.confidence', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='languages', full_name='yandex.cloud.ai.vision.v1.Word.languages', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity_index', full_name='yandex.cloud.ai.vision.v1.Word.entity_index', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_WORD_DETECTEDLANGUAGE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=619,
  serialized_end=871,
)

_TEXTANNOTATION.fields_by_name['pages'].message_type = _PAGE
_PAGE.fields_by_name['blocks'].message_type = _BLOCK
_PAGE.fields_by_name['entities'].message_type = _ENTITY
_BLOCK.fields_by_name['bounding_box'].message_type = yandex_dot_cloud_dot_ai_dot_vision_dot_v1_dot_primitives__pb2._POLYGON
_BLOCK.fields_by_name['lines'].message_type = _LINE
_LINE.fields_by_name['bounding_box'].message_type = yandex_dot_cloud_dot_ai_dot_vision_dot_v1_dot_primitives__pb2._POLYGON
_LINE.fields_by_name['words'].message_type = _WORD
_WORD_DETECTEDLANGUAGE.containing_type = _WORD
_WORD.fields_by_name['bounding_box'].message_type = yandex_dot_cloud_dot_ai_dot_vision_dot_v1_dot_primitives__pb2._POLYGON
_WORD.fields_by_name['languages'].message_type = _WORD_DETECTEDLANGUAGE
DESCRIPTOR.message_types_by_name['TextAnnotation'] = _TEXTANNOTATION
DESCRIPTOR.message_types_by_name['Page'] = _PAGE
DESCRIPTOR.message_types_by_name['Entity'] = _ENTITY
DESCRIPTOR.message_types_by_name['Block'] = _BLOCK
DESCRIPTOR.message_types_by_name['Line'] = _LINE
DESCRIPTOR.message_types_by_name['Word'] = _WORD
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TextAnnotation = _reflection.GeneratedProtocolMessageType('TextAnnotation', (_message.Message,), {
  'DESCRIPTOR' : _TEXTANNOTATION,
  '__module__' : 'yandex.cloud.ai.vision.v1.text_detection_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.ai.vision.v1.TextAnnotation)
  })
_sym_db.RegisterMessage(TextAnnotation)

Page = _reflection.GeneratedProtocolMessageType('Page', (_message.Message,), {
  'DESCRIPTOR' : _PAGE,
  '__module__' : 'yandex.cloud.ai.vision.v1.text_detection_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.ai.vision.v1.Page)
  })
_sym_db.RegisterMessage(Page)

Entity = _reflection.GeneratedProtocolMessageType('Entity', (_message.Message,), {
  'DESCRIPTOR' : _ENTITY,
  '__module__' : 'yandex.cloud.ai.vision.v1.text_detection_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.ai.vision.v1.Entity)
  })
_sym_db.RegisterMessage(Entity)

Block = _reflection.GeneratedProtocolMessageType('Block', (_message.Message,), {
  'DESCRIPTOR' : _BLOCK,
  '__module__' : 'yandex.cloud.ai.vision.v1.text_detection_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.ai.vision.v1.Block)
  })
_sym_db.RegisterMessage(Block)

Line = _reflection.GeneratedProtocolMessageType('Line', (_message.Message,), {
  'DESCRIPTOR' : _LINE,
  '__module__' : 'yandex.cloud.ai.vision.v1.text_detection_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.ai.vision.v1.Line)
  })
_sym_db.RegisterMessage(Line)

Word = _reflection.GeneratedProtocolMessageType('Word', (_message.Message,), {

  'DetectedLanguage' : _reflection.GeneratedProtocolMessageType('DetectedLanguage', (_message.Message,), {
    'DESCRIPTOR' : _WORD_DETECTEDLANGUAGE,
    '__module__' : 'yandex.cloud.ai.vision.v1.text_detection_pb2'
    # @@protoc_insertion_point(class_scope:yandex.cloud.ai.vision.v1.Word.DetectedLanguage)
    })
  ,
  'DESCRIPTOR' : _WORD,
  '__module__' : 'yandex.cloud.ai.vision.v1.text_detection_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.ai.vision.v1.Word)
  })
_sym_db.RegisterMessage(Word)
_sym_db.RegisterMessage(Word.DetectedLanguage)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
