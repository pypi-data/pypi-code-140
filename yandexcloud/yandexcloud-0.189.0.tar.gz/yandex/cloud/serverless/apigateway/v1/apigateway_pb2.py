# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/serverless/apigateway/v1/apigateway.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yandex/cloud/serverless/apigateway/v1/apigateway.proto',
  package='yandex.cloud.serverless.apigateway.v1',
  syntax='proto3',
  serialized_options=b'\n)yandex.cloud.api.serverless.apigateway.v1ZTgithub.com/yandex-cloud/go-genproto/yandex/cloud/serverless/apigateway/v1;apigateway',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n6yandex/cloud/serverless/apigateway/v1/apigateway.proto\x12%yandex.cloud.serverless.apigateway.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\xeb\x04\n\nApiGateway\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tfolder_id\x18\x02 \x01(\t\x12.\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12M\n\x06labels\x18\x07 \x03(\x0b\x32=.yandex.cloud.serverless.apigateway.v1.ApiGateway.LabelsEntry\x12H\n\x06status\x18\x08 \x01(\x0e\x32\x38.yandex.cloud.serverless.apigateway.v1.ApiGateway.Status\x12\x0e\n\x06\x64omain\x18\t \x01(\t\x12\x14\n\x0clog_group_id\x18\n \x01(\t\x12O\n\x10\x61ttached_domains\x18\x0b \x03(\x0b\x32\x35.yandex.cloud.serverless.apigateway.v1.AttachedDomain\x12I\n\x0c\x63onnectivity\x18\x0c \x01(\x0b\x32\x33.yandex.cloud.serverless.apigateway.v1.Connectivity\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"a\n\x06Status\x12\x16\n\x12STATUS_UNSPECIFIED\x10\x00\x12\x0c\n\x08\x43REATING\x10\x01\x12\n\n\x06\x41\x43TIVE\x10\x02\x12\x0c\n\x08\x44\x45LETING\x10\x03\x12\t\n\x05\x45RROR\x10\x04\x12\x0c\n\x08UPDATING\x10\x05\"\\\n\x0e\x41ttachedDomain\x12\x11\n\tdomain_id\x18\x01 \x01(\t\x12\x16\n\x0e\x63\x65rtificate_id\x18\x02 \x01(\t\x12\x0f\n\x07\x65nabled\x18\x03 \x01(\x08\x12\x0e\n\x06\x64omain\x18\x05 \x01(\t\"5\n\x0c\x43onnectivity\x12\x12\n\nnetwork_id\x18\x01 \x01(\t\x12\x11\n\tsubnet_id\x18\x02 \x03(\tB\x81\x01\n)yandex.cloud.api.serverless.apigateway.v1ZTgithub.com/yandex-cloud/go-genproto/yandex/cloud/serverless/apigateway/v1;apigatewayb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])



_APIGATEWAY_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.Status',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STATUS_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CREATING', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ACTIVE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DELETING', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UPDATING', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=653,
  serialized_end=750,
)
_sym_db.RegisterEnumDescriptor(_APIGATEWAY_STATUS)


_APIGATEWAY_LABELSENTRY = _descriptor.Descriptor(
  name='LabelsEntry',
  full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.LabelsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.LabelsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.LabelsEntry.value', index=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=606,
  serialized_end=651,
)

_APIGATEWAY = _descriptor.Descriptor(
  name='ApiGateway',
  full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='folder_id', full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.folder_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.created_at', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.description', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='labels', full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.labels', index=5,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.status', index=6,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain', full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.domain', index=7,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='log_group_id', full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.log_group_id', index=8,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='attached_domains', full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.attached_domains', index=9,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='connectivity', full_name='yandex.cloud.serverless.apigateway.v1.ApiGateway.connectivity', index=10,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_APIGATEWAY_LABELSENTRY, ],
  enum_types=[
    _APIGATEWAY_STATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=131,
  serialized_end=750,
)


_ATTACHEDDOMAIN = _descriptor.Descriptor(
  name='AttachedDomain',
  full_name='yandex.cloud.serverless.apigateway.v1.AttachedDomain',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='yandex.cloud.serverless.apigateway.v1.AttachedDomain.domain_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='certificate_id', full_name='yandex.cloud.serverless.apigateway.v1.AttachedDomain.certificate_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='enabled', full_name='yandex.cloud.serverless.apigateway.v1.AttachedDomain.enabled', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain', full_name='yandex.cloud.serverless.apigateway.v1.AttachedDomain.domain', index=3,
      number=5, type=9, cpp_type=9, label=1,
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
  serialized_start=752,
  serialized_end=844,
)


_CONNECTIVITY = _descriptor.Descriptor(
  name='Connectivity',
  full_name='yandex.cloud.serverless.apigateway.v1.Connectivity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='network_id', full_name='yandex.cloud.serverless.apigateway.v1.Connectivity.network_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='subnet_id', full_name='yandex.cloud.serverless.apigateway.v1.Connectivity.subnet_id', index=1,
      number=2, type=9, cpp_type=9, label=3,
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
  serialized_start=846,
  serialized_end=899,
)

_APIGATEWAY_LABELSENTRY.containing_type = _APIGATEWAY
_APIGATEWAY.fields_by_name['created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_APIGATEWAY.fields_by_name['labels'].message_type = _APIGATEWAY_LABELSENTRY
_APIGATEWAY.fields_by_name['status'].enum_type = _APIGATEWAY_STATUS
_APIGATEWAY.fields_by_name['attached_domains'].message_type = _ATTACHEDDOMAIN
_APIGATEWAY.fields_by_name['connectivity'].message_type = _CONNECTIVITY
_APIGATEWAY_STATUS.containing_type = _APIGATEWAY
DESCRIPTOR.message_types_by_name['ApiGateway'] = _APIGATEWAY
DESCRIPTOR.message_types_by_name['AttachedDomain'] = _ATTACHEDDOMAIN
DESCRIPTOR.message_types_by_name['Connectivity'] = _CONNECTIVITY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ApiGateway = _reflection.GeneratedProtocolMessageType('ApiGateway', (_message.Message,), {

  'LabelsEntry' : _reflection.GeneratedProtocolMessageType('LabelsEntry', (_message.Message,), {
    'DESCRIPTOR' : _APIGATEWAY_LABELSENTRY,
    '__module__' : 'yandex.cloud.serverless.apigateway.v1.apigateway_pb2'
    # @@protoc_insertion_point(class_scope:yandex.cloud.serverless.apigateway.v1.ApiGateway.LabelsEntry)
    })
  ,
  'DESCRIPTOR' : _APIGATEWAY,
  '__module__' : 'yandex.cloud.serverless.apigateway.v1.apigateway_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.serverless.apigateway.v1.ApiGateway)
  })
_sym_db.RegisterMessage(ApiGateway)
_sym_db.RegisterMessage(ApiGateway.LabelsEntry)

AttachedDomain = _reflection.GeneratedProtocolMessageType('AttachedDomain', (_message.Message,), {
  'DESCRIPTOR' : _ATTACHEDDOMAIN,
  '__module__' : 'yandex.cloud.serverless.apigateway.v1.apigateway_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.serverless.apigateway.v1.AttachedDomain)
  })
_sym_db.RegisterMessage(AttachedDomain)

Connectivity = _reflection.GeneratedProtocolMessageType('Connectivity', (_message.Message,), {
  'DESCRIPTOR' : _CONNECTIVITY,
  '__module__' : 'yandex.cloud.serverless.apigateway.v1.apigateway_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.serverless.apigateway.v1.Connectivity)
  })
_sym_db.RegisterMessage(Connectivity)


DESCRIPTOR._options = None
_APIGATEWAY_LABELSENTRY._options = None
# @@protoc_insertion_point(module_scope)
