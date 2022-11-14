# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/cdn/v1/raw_logs_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2
from yandex.cloud.cdn.v1 import raw_logs_pb2 as yandex_dot_cloud_dot_cdn_dot_v1_dot_raw__logs__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yandex/cloud/cdn/v1/raw_logs_service.proto',
  package='yandex.cloud.cdn.v1',
  syntax='proto3',
  serialized_options=b'\n\027yandex.cloud.api.cdn.v1Z;github.com/yandex-cloud/go-genproto/yandex/cloud/cdn/v1;cdn',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n*yandex/cloud/cdn/v1/raw_logs_service.proto\x12\x13yandex.cloud.cdn.v1\x1a\x1cgoogle/api/annotations.proto\x1a yandex/cloud/api/operation.proto\x1a\"yandex/cloud/cdn/v1/raw_logs.proto\x1a&yandex/cloud/operation/operation.proto\x1a\x1dyandex/cloud/validation.proto\"s\n\x16\x41\x63tivateRawLogsRequest\x12!\n\x0bresource_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x36\n\x08settings\x18\x02 \x01(\x0b\x32$.yandex.cloud.cdn.v1.RawLogsSettings\".\n\x17\x41\x63tivateRawLogsMetadata\x12\x13\n\x0bresource_id\x18\x01 \x01(\t\"\x85\x01\n\x17\x41\x63tivateRawLogsResponse\x12\x32\n\x06status\x18\x01 \x01(\x0e\x32\".yandex.cloud.cdn.v1.RawLogsStatus\x12\x36\n\x08settings\x18\x02 \x01(\x0b\x32$.yandex.cloud.cdn.v1.RawLogsSettings\"=\n\x18\x44\x65\x61\x63tivateRawLogsRequest\x12!\n\x0bresource_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"0\n\x19\x44\x65\x61\x63tivateRawLogsMetadata\x12\x13\n\x0bresource_id\x18\x01 \x01(\t\"6\n\x11GetRawLogsRequest\x12!\n\x0bresource_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"\x80\x01\n\x12GetRawLogsResponse\x12\x32\n\x06status\x18\x01 \x01(\x0e\x32\".yandex.cloud.cdn.v1.RawLogsStatus\x12\x36\n\x08settings\x18\x02 \x01(\x0b\x32$.yandex.cloud.cdn.v1.RawLogsSettings\"q\n\x14UpdateRawLogsRequest\x12!\n\x0bresource_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x36\n\x08settings\x18\x02 \x01(\x0b\x32$.yandex.cloud.cdn.v1.RawLogsSettings\"\x83\x01\n\x15UpdateRawLogsResponse\x12\x32\n\x06status\x18\x01 \x01(\x0e\x32\".yandex.cloud.cdn.v1.RawLogsStatus\x12\x36\n\x08settings\x18\x02 \x01(\x0b\x32$.yandex.cloud.cdn.v1.RawLogsSettings\",\n\x15UpdateRawLogsMetadata\x12\x13\n\x0bresource_id\x18\x01 \x01(\t2\xba\x05\n\x0eRawLogsService\x12\xb5\x01\n\x08\x41\x63tivate\x12+.yandex.cloud.cdn.v1.ActivateRawLogsRequest\x1a!.yandex.cloud.operation.Operation\"Y\x82\xd3\xe4\x93\x02\x1d\"\x18/cdn/v1/rawLogs:activate:\x01*\xb2\xd2*2\n\x17\x41\x63tivateRawLogsMetadata\x12\x17\x41\x63tivateRawLogsResponse\x12\xbb\x01\n\nDeactivate\x12-.yandex.cloud.cdn.v1.DeactivateRawLogsRequest\x1a!.yandex.cloud.operation.Operation\"[\x82\xd3\xe4\x93\x02\x1f\"\x1d/cdn/v1/rawLogs/{resource_id}\xb2\xd2*2\n\x19\x44\x65\x61\x63tivateRawLogsMetadata\x12\x15google.protobuf.Empty\x12}\n\x03Get\x12&.yandex.cloud.cdn.v1.GetRawLogsRequest\x1a\'.yandex.cloud.cdn.v1.GetRawLogsResponse\"%\x82\xd3\xe4\x93\x02\x1f\x12\x1d/cdn/v1/rawLogs/{resource_id}\x12\xb2\x01\n\x06Update\x12).yandex.cloud.cdn.v1.UpdateRawLogsRequest\x1a!.yandex.cloud.operation.Operation\"Z\x82\xd3\xe4\x93\x02\"2\x1d/cdn/v1/rawLogs/{resource_id}:\x01*\xb2\xd2*.\n\x15UpdateRawLogsMetadata\x12\x15UpdateRawLogsResponseBV\n\x17yandex.cloud.api.cdn.v1Z;github.com/yandex-cloud/go-genproto/yandex/cloud/cdn/v1;cdnb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,yandex_dot_cloud_dot_api_dot_operation__pb2.DESCRIPTOR,yandex_dot_cloud_dot_cdn_dot_v1_dot_raw__logs__pb2.DESCRIPTOR,yandex_dot_cloud_dot_operation_dot_operation__pb2.DESCRIPTOR,yandex_dot_cloud_dot_validation__pb2.DESCRIPTOR,])




_ACTIVATERAWLOGSREQUEST = _descriptor.Descriptor(
  name='ActivateRawLogsRequest',
  full_name='yandex.cloud.cdn.v1.ActivateRawLogsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_id', full_name='yandex.cloud.cdn.v1.ActivateRawLogsRequest.resource_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='settings', full_name='yandex.cloud.cdn.v1.ActivateRawLogsRequest.settings', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=238,
  serialized_end=353,
)


_ACTIVATERAWLOGSMETADATA = _descriptor.Descriptor(
  name='ActivateRawLogsMetadata',
  full_name='yandex.cloud.cdn.v1.ActivateRawLogsMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_id', full_name='yandex.cloud.cdn.v1.ActivateRawLogsMetadata.resource_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=355,
  serialized_end=401,
)


_ACTIVATERAWLOGSRESPONSE = _descriptor.Descriptor(
  name='ActivateRawLogsResponse',
  full_name='yandex.cloud.cdn.v1.ActivateRawLogsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='yandex.cloud.cdn.v1.ActivateRawLogsResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='settings', full_name='yandex.cloud.cdn.v1.ActivateRawLogsResponse.settings', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=404,
  serialized_end=537,
)


_DEACTIVATERAWLOGSREQUEST = _descriptor.Descriptor(
  name='DeactivateRawLogsRequest',
  full_name='yandex.cloud.cdn.v1.DeactivateRawLogsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_id', full_name='yandex.cloud.cdn.v1.DeactivateRawLogsRequest.resource_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=539,
  serialized_end=600,
)


_DEACTIVATERAWLOGSMETADATA = _descriptor.Descriptor(
  name='DeactivateRawLogsMetadata',
  full_name='yandex.cloud.cdn.v1.DeactivateRawLogsMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_id', full_name='yandex.cloud.cdn.v1.DeactivateRawLogsMetadata.resource_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=602,
  serialized_end=650,
)


_GETRAWLOGSREQUEST = _descriptor.Descriptor(
  name='GetRawLogsRequest',
  full_name='yandex.cloud.cdn.v1.GetRawLogsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_id', full_name='yandex.cloud.cdn.v1.GetRawLogsRequest.resource_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=652,
  serialized_end=706,
)


_GETRAWLOGSRESPONSE = _descriptor.Descriptor(
  name='GetRawLogsResponse',
  full_name='yandex.cloud.cdn.v1.GetRawLogsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='yandex.cloud.cdn.v1.GetRawLogsResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='settings', full_name='yandex.cloud.cdn.v1.GetRawLogsResponse.settings', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=709,
  serialized_end=837,
)


_UPDATERAWLOGSREQUEST = _descriptor.Descriptor(
  name='UpdateRawLogsRequest',
  full_name='yandex.cloud.cdn.v1.UpdateRawLogsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_id', full_name='yandex.cloud.cdn.v1.UpdateRawLogsRequest.resource_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='settings', full_name='yandex.cloud.cdn.v1.UpdateRawLogsRequest.settings', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=839,
  serialized_end=952,
)


_UPDATERAWLOGSRESPONSE = _descriptor.Descriptor(
  name='UpdateRawLogsResponse',
  full_name='yandex.cloud.cdn.v1.UpdateRawLogsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='yandex.cloud.cdn.v1.UpdateRawLogsResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='settings', full_name='yandex.cloud.cdn.v1.UpdateRawLogsResponse.settings', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=955,
  serialized_end=1086,
)


_UPDATERAWLOGSMETADATA = _descriptor.Descriptor(
  name='UpdateRawLogsMetadata',
  full_name='yandex.cloud.cdn.v1.UpdateRawLogsMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_id', full_name='yandex.cloud.cdn.v1.UpdateRawLogsMetadata.resource_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=1088,
  serialized_end=1132,
)

_ACTIVATERAWLOGSREQUEST.fields_by_name['settings'].message_type = yandex_dot_cloud_dot_cdn_dot_v1_dot_raw__logs__pb2._RAWLOGSSETTINGS
_ACTIVATERAWLOGSRESPONSE.fields_by_name['status'].enum_type = yandex_dot_cloud_dot_cdn_dot_v1_dot_raw__logs__pb2._RAWLOGSSTATUS
_ACTIVATERAWLOGSRESPONSE.fields_by_name['settings'].message_type = yandex_dot_cloud_dot_cdn_dot_v1_dot_raw__logs__pb2._RAWLOGSSETTINGS
_GETRAWLOGSRESPONSE.fields_by_name['status'].enum_type = yandex_dot_cloud_dot_cdn_dot_v1_dot_raw__logs__pb2._RAWLOGSSTATUS
_GETRAWLOGSRESPONSE.fields_by_name['settings'].message_type = yandex_dot_cloud_dot_cdn_dot_v1_dot_raw__logs__pb2._RAWLOGSSETTINGS
_UPDATERAWLOGSREQUEST.fields_by_name['settings'].message_type = yandex_dot_cloud_dot_cdn_dot_v1_dot_raw__logs__pb2._RAWLOGSSETTINGS
_UPDATERAWLOGSRESPONSE.fields_by_name['status'].enum_type = yandex_dot_cloud_dot_cdn_dot_v1_dot_raw__logs__pb2._RAWLOGSSTATUS
_UPDATERAWLOGSRESPONSE.fields_by_name['settings'].message_type = yandex_dot_cloud_dot_cdn_dot_v1_dot_raw__logs__pb2._RAWLOGSSETTINGS
DESCRIPTOR.message_types_by_name['ActivateRawLogsRequest'] = _ACTIVATERAWLOGSREQUEST
DESCRIPTOR.message_types_by_name['ActivateRawLogsMetadata'] = _ACTIVATERAWLOGSMETADATA
DESCRIPTOR.message_types_by_name['ActivateRawLogsResponse'] = _ACTIVATERAWLOGSRESPONSE
DESCRIPTOR.message_types_by_name['DeactivateRawLogsRequest'] = _DEACTIVATERAWLOGSREQUEST
DESCRIPTOR.message_types_by_name['DeactivateRawLogsMetadata'] = _DEACTIVATERAWLOGSMETADATA
DESCRIPTOR.message_types_by_name['GetRawLogsRequest'] = _GETRAWLOGSREQUEST
DESCRIPTOR.message_types_by_name['GetRawLogsResponse'] = _GETRAWLOGSRESPONSE
DESCRIPTOR.message_types_by_name['UpdateRawLogsRequest'] = _UPDATERAWLOGSREQUEST
DESCRIPTOR.message_types_by_name['UpdateRawLogsResponse'] = _UPDATERAWLOGSRESPONSE
DESCRIPTOR.message_types_by_name['UpdateRawLogsMetadata'] = _UPDATERAWLOGSMETADATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ActivateRawLogsRequest = _reflection.GeneratedProtocolMessageType('ActivateRawLogsRequest', (_message.Message,), {
  'DESCRIPTOR' : _ACTIVATERAWLOGSREQUEST,
  '__module__' : 'yandex.cloud.cdn.v1.raw_logs_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.cdn.v1.ActivateRawLogsRequest)
  })
_sym_db.RegisterMessage(ActivateRawLogsRequest)

ActivateRawLogsMetadata = _reflection.GeneratedProtocolMessageType('ActivateRawLogsMetadata', (_message.Message,), {
  'DESCRIPTOR' : _ACTIVATERAWLOGSMETADATA,
  '__module__' : 'yandex.cloud.cdn.v1.raw_logs_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.cdn.v1.ActivateRawLogsMetadata)
  })
_sym_db.RegisterMessage(ActivateRawLogsMetadata)

ActivateRawLogsResponse = _reflection.GeneratedProtocolMessageType('ActivateRawLogsResponse', (_message.Message,), {
  'DESCRIPTOR' : _ACTIVATERAWLOGSRESPONSE,
  '__module__' : 'yandex.cloud.cdn.v1.raw_logs_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.cdn.v1.ActivateRawLogsResponse)
  })
_sym_db.RegisterMessage(ActivateRawLogsResponse)

DeactivateRawLogsRequest = _reflection.GeneratedProtocolMessageType('DeactivateRawLogsRequest', (_message.Message,), {
  'DESCRIPTOR' : _DEACTIVATERAWLOGSREQUEST,
  '__module__' : 'yandex.cloud.cdn.v1.raw_logs_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.cdn.v1.DeactivateRawLogsRequest)
  })
_sym_db.RegisterMessage(DeactivateRawLogsRequest)

DeactivateRawLogsMetadata = _reflection.GeneratedProtocolMessageType('DeactivateRawLogsMetadata', (_message.Message,), {
  'DESCRIPTOR' : _DEACTIVATERAWLOGSMETADATA,
  '__module__' : 'yandex.cloud.cdn.v1.raw_logs_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.cdn.v1.DeactivateRawLogsMetadata)
  })
_sym_db.RegisterMessage(DeactivateRawLogsMetadata)

GetRawLogsRequest = _reflection.GeneratedProtocolMessageType('GetRawLogsRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETRAWLOGSREQUEST,
  '__module__' : 'yandex.cloud.cdn.v1.raw_logs_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.cdn.v1.GetRawLogsRequest)
  })
_sym_db.RegisterMessage(GetRawLogsRequest)

GetRawLogsResponse = _reflection.GeneratedProtocolMessageType('GetRawLogsResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETRAWLOGSRESPONSE,
  '__module__' : 'yandex.cloud.cdn.v1.raw_logs_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.cdn.v1.GetRawLogsResponse)
  })
_sym_db.RegisterMessage(GetRawLogsResponse)

UpdateRawLogsRequest = _reflection.GeneratedProtocolMessageType('UpdateRawLogsRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATERAWLOGSREQUEST,
  '__module__' : 'yandex.cloud.cdn.v1.raw_logs_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.cdn.v1.UpdateRawLogsRequest)
  })
_sym_db.RegisterMessage(UpdateRawLogsRequest)

UpdateRawLogsResponse = _reflection.GeneratedProtocolMessageType('UpdateRawLogsResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATERAWLOGSRESPONSE,
  '__module__' : 'yandex.cloud.cdn.v1.raw_logs_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.cdn.v1.UpdateRawLogsResponse)
  })
_sym_db.RegisterMessage(UpdateRawLogsResponse)

UpdateRawLogsMetadata = _reflection.GeneratedProtocolMessageType('UpdateRawLogsMetadata', (_message.Message,), {
  'DESCRIPTOR' : _UPDATERAWLOGSMETADATA,
  '__module__' : 'yandex.cloud.cdn.v1.raw_logs_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.cdn.v1.UpdateRawLogsMetadata)
  })
_sym_db.RegisterMessage(UpdateRawLogsMetadata)


DESCRIPTOR._options = None
_ACTIVATERAWLOGSREQUEST.fields_by_name['resource_id']._options = None
_DEACTIVATERAWLOGSREQUEST.fields_by_name['resource_id']._options = None
_GETRAWLOGSREQUEST.fields_by_name['resource_id']._options = None
_UPDATERAWLOGSREQUEST.fields_by_name['resource_id']._options = None

_RAWLOGSSERVICE = _descriptor.ServiceDescriptor(
  name='RawLogsService',
  full_name='yandex.cloud.cdn.v1.RawLogsService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1135,
  serialized_end=1833,
  methods=[
  _descriptor.MethodDescriptor(
    name='Activate',
    full_name='yandex.cloud.cdn.v1.RawLogsService.Activate',
    index=0,
    containing_service=None,
    input_type=_ACTIVATERAWLOGSREQUEST,
    output_type=yandex_dot_cloud_dot_operation_dot_operation__pb2._OPERATION,
    serialized_options=b'\202\323\344\223\002\035\"\030/cdn/v1/rawLogs:activate:\001*\262\322*2\n\027ActivateRawLogsMetadata\022\027ActivateRawLogsResponse',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Deactivate',
    full_name='yandex.cloud.cdn.v1.RawLogsService.Deactivate',
    index=1,
    containing_service=None,
    input_type=_DEACTIVATERAWLOGSREQUEST,
    output_type=yandex_dot_cloud_dot_operation_dot_operation__pb2._OPERATION,
    serialized_options=b'\202\323\344\223\002\037\"\035/cdn/v1/rawLogs/{resource_id}\262\322*2\n\031DeactivateRawLogsMetadata\022\025google.protobuf.Empty',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Get',
    full_name='yandex.cloud.cdn.v1.RawLogsService.Get',
    index=2,
    containing_service=None,
    input_type=_GETRAWLOGSREQUEST,
    output_type=_GETRAWLOGSRESPONSE,
    serialized_options=b'\202\323\344\223\002\037\022\035/cdn/v1/rawLogs/{resource_id}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Update',
    full_name='yandex.cloud.cdn.v1.RawLogsService.Update',
    index=3,
    containing_service=None,
    input_type=_UPDATERAWLOGSREQUEST,
    output_type=yandex_dot_cloud_dot_operation_dot_operation__pb2._OPERATION,
    serialized_options=b'\202\323\344\223\002\"2\035/cdn/v1/rawLogs/{resource_id}:\001*\262\322*.\n\025UpdateRawLogsMetadata\022\025UpdateRawLogsResponse',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_RAWLOGSSERVICE)

DESCRIPTOR.services_by_name['RawLogsService'] = _RAWLOGSSERVICE

# @@protoc_insertion_point(module_scope)
