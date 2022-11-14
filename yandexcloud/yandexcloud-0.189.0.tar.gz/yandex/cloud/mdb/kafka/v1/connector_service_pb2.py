# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/mdb/kafka/v1/connector_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2
from yandex.cloud.mdb.kafka.v1 import connector_pb2 as yandex_dot_cloud_dot_mdb_dot_kafka_dot_v1_dot_connector__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yandex/cloud/mdb/kafka/v1/connector_service.proto',
  package='yandex.cloud.mdb.kafka.v1',
  syntax='proto3',
  serialized_options=b'\n\035yandex.cloud.api.mdb.kafka.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/kafka/v1;kafka',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n1yandex/cloud/mdb/kafka/v1/connector_service.proto\x12\x19yandex.cloud.mdb.kafka.v1\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a yandex/cloud/api/operation.proto\x1a&yandex/cloud/operation/operation.proto\x1a\x1dyandex/cloud/validation.proto\x1a)yandex/cloud/mdb/kafka/v1/connector.proto\"p\n\x13GetConnectorRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x37\n\x0e\x63onnector_name\x18\x02 \x01(\tB\x1f\xe8\xc7\x31\x01\x8a\xc8\x31\x05<=256\xf2\xc7\x31\x0e[a-zA-Z0-9_-]*\"w\n\x15ListConnectorsRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\"k\n\x16ListConnectorsResponse\x12\x38\n\nconnectors\x18\x01 \x03(\x0b\x32$.yandex.cloud.mdb.kafka.v1.Connector\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\x82\x01\n\x16\x43reateConnectorRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x46\n\x0e\x63onnector_spec\x18\x02 \x01(\x0b\x32(.yandex.cloud.mdb.kafka.v1.ConnectorSpecB\x04\xe8\xc7\x31\x01\"f\n\x17\x43reateConnectorMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\x12\x37\n\x0e\x63onnector_name\x18\x02 \x01(\tB\x1f\xe8\xc7\x31\x01\x8a\xc8\x31\x05<=256\xf2\xc7\x31\x0e[a-zA-Z0-9_-]*\"\xf2\x01\n\x16UpdateConnectorRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x37\n\x0e\x63onnector_name\x18\x02 \x01(\tB\x1f\xe8\xc7\x31\x01\x8a\xc8\x31\x05<=256\xf2\xc7\x31\x0e[a-zA-Z0-9_-]*\x12/\n\x0bupdate_mask\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12L\n\x0e\x63onnector_spec\x18\x04 \x01(\x0b\x32..yandex.cloud.mdb.kafka.v1.UpdateConnectorSpecB\x04\xe8\xc7\x31\x01\"t\n\x17UpdateConnectorMetadata\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x37\n\x0e\x63onnector_name\x18\x02 \x01(\tB\x1f\xe8\xc7\x31\x01\x8a\xc8\x31\x05<=256\xf2\xc7\x31\x0e[a-zA-Z0-9_-]*\"s\n\x16\x44\x65leteConnectorRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x37\n\x0e\x63onnector_name\x18\x02 \x01(\tB\x1f\xe8\xc7\x31\x01\x8a\xc8\x31\x05<=256\xf2\xc7\x31\x0e[a-zA-Z0-9_-]*\"E\n\x17\x44\x65leteConnectorMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\x12\x16\n\x0e\x63onnector_name\x18\x02 \x01(\t\"s\n\x16ResumeConnectorRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x37\n\x0e\x63onnector_name\x18\x02 \x01(\tB\x1f\xe8\xc7\x31\x01\x8a\xc8\x31\x05<=256\xf2\xc7\x31\x0e[a-zA-Z0-9_-]*\"f\n\x17ResumeConnectorMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\x12\x37\n\x0e\x63onnector_name\x18\x02 \x01(\tB\x1f\xe8\xc7\x31\x01\x8a\xc8\x31\x05<=256\xf2\xc7\x31\x0e[a-zA-Z0-9_-]*\"r\n\x15PauseConnectorRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x37\n\x0e\x63onnector_name\x18\x02 \x01(\tB\x1f\xe8\xc7\x31\x01\x8a\xc8\x31\x05<=256\xf2\xc7\x31\x0e[a-zA-Z0-9_-]*\"e\n\x16PauseConnectorMetadata\x12\x12\n\ncluster_id\x18\x01 \x01(\t\x12\x37\n\x0e\x63onnector_name\x18\x02 \x01(\tB\x1f\xe8\xc7\x31\x01\x8a\xc8\x31\x05<=256\xf2\xc7\x31\x0e[a-zA-Z0-9_-]*2\xa6\x0b\n\x10\x43onnectorService\x12\xa8\x01\n\x03Get\x12..yandex.cloud.mdb.kafka.v1.GetConnectorRequest\x1a$.yandex.cloud.mdb.kafka.v1.Connector\"K\x82\xd3\xe4\x93\x02\x45\x12\x43/managed-kafka/v1/clusters/{cluster_id}/connectors/{connector_name}\x12\xa7\x01\n\x04List\x12\x30.yandex.cloud.mdb.kafka.v1.ListConnectorsRequest\x1a\x31.yandex.cloud.mdb.kafka.v1.ListConnectorsResponse\":\x82\xd3\xe4\x93\x02\x34\x12\x32/managed-kafka/v1/clusters/{cluster_id}/connectors\x12\xc5\x01\n\x06\x43reate\x12\x31.yandex.cloud.mdb.kafka.v1.CreateConnectorRequest\x1a!.yandex.cloud.operation.Operation\"e\x82\xd3\xe4\x93\x02\x37\"2/managed-kafka/v1/clusters/{cluster_id}/connectors:\x01*\xb2\xd2*$\n\x17\x43reateConnectorMetadata\x12\tConnector\x12\xd6\x01\n\x06Update\x12\x31.yandex.cloud.mdb.kafka.v1.UpdateConnectorRequest\x1a!.yandex.cloud.operation.Operation\"v\x82\xd3\xe4\x93\x02H2C/managed-kafka/v1/clusters/{cluster_id}/connectors/{connector_name}:\x01*\xb2\xd2*$\n\x17UpdateConnectorMetadata\x12\tConnector\x12\xdf\x01\n\x06\x44\x65lete\x12\x31.yandex.cloud.mdb.kafka.v1.DeleteConnectorRequest\x1a!.yandex.cloud.operation.Operation\"\x7f\x82\xd3\xe4\x93\x02\x45*C/managed-kafka/v1/clusters/{cluster_id}/connectors/{connector_name}\xb2\xd2*0\n\x17\x44\x65leteConnectorMetadata\x12\x15google.protobuf.Empty\x12\xdd\x01\n\x06Resume\x12\x31.yandex.cloud.mdb.kafka.v1.ResumeConnectorRequest\x1a!.yandex.cloud.operation.Operation\"}\x82\xd3\xe4\x93\x02O\"J/managed-kafka/v1/clusters/{cluster_id}/connectors/resume/{connector_name}:\x01*\xb2\xd2*$\n\x17ResumeConnectorMetadata\x12\tConnector\x12\xd9\x01\n\x05Pause\x12\x30.yandex.cloud.mdb.kafka.v1.PauseConnectorRequest\x1a!.yandex.cloud.operation.Operation\"{\x82\xd3\xe4\x93\x02N\"I/managed-kafka/v1/clusters/{cluster_id}/connectors/pause/{connector_name}:\x01*\xb2\xd2*#\n\x16PauseConnectorMetadata\x12\tConnectorBd\n\x1dyandex.cloud.api.mdb.kafka.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/kafka/v1;kafkab\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,yandex_dot_cloud_dot_api_dot_operation__pb2.DESCRIPTOR,yandex_dot_cloud_dot_operation_dot_operation__pb2.DESCRIPTOR,yandex_dot_cloud_dot_validation__pb2.DESCRIPTOR,yandex_dot_cloud_dot_mdb_dot_kafka_dot_v1_dot_connector__pb2.DESCRIPTOR,])




_GETCONNECTORREQUEST = _descriptor.Descriptor(
  name='GetConnectorRequest',
  full_name='yandex.cloud.mdb.kafka.v1.GetConnectorRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.kafka.v1.GetConnectorRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='connector_name', full_name='yandex.cloud.mdb.kafka.v1.GetConnectorRequest.connector_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\005<=256\362\3071\016[a-zA-Z0-9_-]*', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=292,
  serialized_end=404,
)


_LISTCONNECTORSREQUEST = _descriptor.Descriptor(
  name='ListConnectorsRequest',
  full_name='yandex.cloud.mdb.kafka.v1.ListConnectorsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.kafka.v1.ListConnectorsRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='page_size', full_name='yandex.cloud.mdb.kafka.v1.ListConnectorsRequest.page_size', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372\3071\006<=1000', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='page_token', full_name='yandex.cloud.mdb.kafka.v1.ListConnectorsRequest.page_token', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\212\3101\005<=100', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=406,
  serialized_end=525,
)


_LISTCONNECTORSRESPONSE = _descriptor.Descriptor(
  name='ListConnectorsResponse',
  full_name='yandex.cloud.mdb.kafka.v1.ListConnectorsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='connectors', full_name='yandex.cloud.mdb.kafka.v1.ListConnectorsResponse.connectors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='next_page_token', full_name='yandex.cloud.mdb.kafka.v1.ListConnectorsResponse.next_page_token', index=1,
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
  serialized_start=527,
  serialized_end=634,
)


_CREATECONNECTORREQUEST = _descriptor.Descriptor(
  name='CreateConnectorRequest',
  full_name='yandex.cloud.mdb.kafka.v1.CreateConnectorRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.kafka.v1.CreateConnectorRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='connector_spec', full_name='yandex.cloud.mdb.kafka.v1.CreateConnectorRequest.connector_spec', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=637,
  serialized_end=767,
)


_CREATECONNECTORMETADATA = _descriptor.Descriptor(
  name='CreateConnectorMetadata',
  full_name='yandex.cloud.mdb.kafka.v1.CreateConnectorMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.kafka.v1.CreateConnectorMetadata.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='connector_name', full_name='yandex.cloud.mdb.kafka.v1.CreateConnectorMetadata.connector_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\005<=256\362\3071\016[a-zA-Z0-9_-]*', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=769,
  serialized_end=871,
)


_UPDATECONNECTORREQUEST = _descriptor.Descriptor(
  name='UpdateConnectorRequest',
  full_name='yandex.cloud.mdb.kafka.v1.UpdateConnectorRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.kafka.v1.UpdateConnectorRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='connector_name', full_name='yandex.cloud.mdb.kafka.v1.UpdateConnectorRequest.connector_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\005<=256\362\3071\016[a-zA-Z0-9_-]*', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='yandex.cloud.mdb.kafka.v1.UpdateConnectorRequest.update_mask', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='connector_spec', full_name='yandex.cloud.mdb.kafka.v1.UpdateConnectorRequest.connector_spec', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=874,
  serialized_end=1116,
)


_UPDATECONNECTORMETADATA = _descriptor.Descriptor(
  name='UpdateConnectorMetadata',
  full_name='yandex.cloud.mdb.kafka.v1.UpdateConnectorMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.kafka.v1.UpdateConnectorMetadata.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='connector_name', full_name='yandex.cloud.mdb.kafka.v1.UpdateConnectorMetadata.connector_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\005<=256\362\3071\016[a-zA-Z0-9_-]*', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1118,
  serialized_end=1234,
)


_DELETECONNECTORREQUEST = _descriptor.Descriptor(
  name='DeleteConnectorRequest',
  full_name='yandex.cloud.mdb.kafka.v1.DeleteConnectorRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.kafka.v1.DeleteConnectorRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='connector_name', full_name='yandex.cloud.mdb.kafka.v1.DeleteConnectorRequest.connector_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\005<=256\362\3071\016[a-zA-Z0-9_-]*', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1236,
  serialized_end=1351,
)


_DELETECONNECTORMETADATA = _descriptor.Descriptor(
  name='DeleteConnectorMetadata',
  full_name='yandex.cloud.mdb.kafka.v1.DeleteConnectorMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.kafka.v1.DeleteConnectorMetadata.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='connector_name', full_name='yandex.cloud.mdb.kafka.v1.DeleteConnectorMetadata.connector_name', index=1,
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
  serialized_start=1353,
  serialized_end=1422,
)


_RESUMECONNECTORREQUEST = _descriptor.Descriptor(
  name='ResumeConnectorRequest',
  full_name='yandex.cloud.mdb.kafka.v1.ResumeConnectorRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.kafka.v1.ResumeConnectorRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='connector_name', full_name='yandex.cloud.mdb.kafka.v1.ResumeConnectorRequest.connector_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\005<=256\362\3071\016[a-zA-Z0-9_-]*', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1424,
  serialized_end=1539,
)


_RESUMECONNECTORMETADATA = _descriptor.Descriptor(
  name='ResumeConnectorMetadata',
  full_name='yandex.cloud.mdb.kafka.v1.ResumeConnectorMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.kafka.v1.ResumeConnectorMetadata.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='connector_name', full_name='yandex.cloud.mdb.kafka.v1.ResumeConnectorMetadata.connector_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\005<=256\362\3071\016[a-zA-Z0-9_-]*', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1541,
  serialized_end=1643,
)


_PAUSECONNECTORREQUEST = _descriptor.Descriptor(
  name='PauseConnectorRequest',
  full_name='yandex.cloud.mdb.kafka.v1.PauseConnectorRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.kafka.v1.PauseConnectorRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='connector_name', full_name='yandex.cloud.mdb.kafka.v1.PauseConnectorRequest.connector_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\005<=256\362\3071\016[a-zA-Z0-9_-]*', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1645,
  serialized_end=1759,
)


_PAUSECONNECTORMETADATA = _descriptor.Descriptor(
  name='PauseConnectorMetadata',
  full_name='yandex.cloud.mdb.kafka.v1.PauseConnectorMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.kafka.v1.PauseConnectorMetadata.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='connector_name', full_name='yandex.cloud.mdb.kafka.v1.PauseConnectorMetadata.connector_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\005<=256\362\3071\016[a-zA-Z0-9_-]*', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1761,
  serialized_end=1862,
)

_LISTCONNECTORSRESPONSE.fields_by_name['connectors'].message_type = yandex_dot_cloud_dot_mdb_dot_kafka_dot_v1_dot_connector__pb2._CONNECTOR
_CREATECONNECTORREQUEST.fields_by_name['connector_spec'].message_type = yandex_dot_cloud_dot_mdb_dot_kafka_dot_v1_dot_connector__pb2._CONNECTORSPEC
_UPDATECONNECTORREQUEST.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_UPDATECONNECTORREQUEST.fields_by_name['connector_spec'].message_type = yandex_dot_cloud_dot_mdb_dot_kafka_dot_v1_dot_connector__pb2._UPDATECONNECTORSPEC
DESCRIPTOR.message_types_by_name['GetConnectorRequest'] = _GETCONNECTORREQUEST
DESCRIPTOR.message_types_by_name['ListConnectorsRequest'] = _LISTCONNECTORSREQUEST
DESCRIPTOR.message_types_by_name['ListConnectorsResponse'] = _LISTCONNECTORSRESPONSE
DESCRIPTOR.message_types_by_name['CreateConnectorRequest'] = _CREATECONNECTORREQUEST
DESCRIPTOR.message_types_by_name['CreateConnectorMetadata'] = _CREATECONNECTORMETADATA
DESCRIPTOR.message_types_by_name['UpdateConnectorRequest'] = _UPDATECONNECTORREQUEST
DESCRIPTOR.message_types_by_name['UpdateConnectorMetadata'] = _UPDATECONNECTORMETADATA
DESCRIPTOR.message_types_by_name['DeleteConnectorRequest'] = _DELETECONNECTORREQUEST
DESCRIPTOR.message_types_by_name['DeleteConnectorMetadata'] = _DELETECONNECTORMETADATA
DESCRIPTOR.message_types_by_name['ResumeConnectorRequest'] = _RESUMECONNECTORREQUEST
DESCRIPTOR.message_types_by_name['ResumeConnectorMetadata'] = _RESUMECONNECTORMETADATA
DESCRIPTOR.message_types_by_name['PauseConnectorRequest'] = _PAUSECONNECTORREQUEST
DESCRIPTOR.message_types_by_name['PauseConnectorMetadata'] = _PAUSECONNECTORMETADATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetConnectorRequest = _reflection.GeneratedProtocolMessageType('GetConnectorRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCONNECTORREQUEST,
  '__module__' : 'yandex.cloud.mdb.kafka.v1.connector_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.kafka.v1.GetConnectorRequest)
  })
_sym_db.RegisterMessage(GetConnectorRequest)

ListConnectorsRequest = _reflection.GeneratedProtocolMessageType('ListConnectorsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTCONNECTORSREQUEST,
  '__module__' : 'yandex.cloud.mdb.kafka.v1.connector_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.kafka.v1.ListConnectorsRequest)
  })
_sym_db.RegisterMessage(ListConnectorsRequest)

ListConnectorsResponse = _reflection.GeneratedProtocolMessageType('ListConnectorsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTCONNECTORSRESPONSE,
  '__module__' : 'yandex.cloud.mdb.kafka.v1.connector_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.kafka.v1.ListConnectorsResponse)
  })
_sym_db.RegisterMessage(ListConnectorsResponse)

CreateConnectorRequest = _reflection.GeneratedProtocolMessageType('CreateConnectorRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATECONNECTORREQUEST,
  '__module__' : 'yandex.cloud.mdb.kafka.v1.connector_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.kafka.v1.CreateConnectorRequest)
  })
_sym_db.RegisterMessage(CreateConnectorRequest)

CreateConnectorMetadata = _reflection.GeneratedProtocolMessageType('CreateConnectorMetadata', (_message.Message,), {
  'DESCRIPTOR' : _CREATECONNECTORMETADATA,
  '__module__' : 'yandex.cloud.mdb.kafka.v1.connector_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.kafka.v1.CreateConnectorMetadata)
  })
_sym_db.RegisterMessage(CreateConnectorMetadata)

UpdateConnectorRequest = _reflection.GeneratedProtocolMessageType('UpdateConnectorRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATECONNECTORREQUEST,
  '__module__' : 'yandex.cloud.mdb.kafka.v1.connector_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.kafka.v1.UpdateConnectorRequest)
  })
_sym_db.RegisterMessage(UpdateConnectorRequest)

UpdateConnectorMetadata = _reflection.GeneratedProtocolMessageType('UpdateConnectorMetadata', (_message.Message,), {
  'DESCRIPTOR' : _UPDATECONNECTORMETADATA,
  '__module__' : 'yandex.cloud.mdb.kafka.v1.connector_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.kafka.v1.UpdateConnectorMetadata)
  })
_sym_db.RegisterMessage(UpdateConnectorMetadata)

DeleteConnectorRequest = _reflection.GeneratedProtocolMessageType('DeleteConnectorRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETECONNECTORREQUEST,
  '__module__' : 'yandex.cloud.mdb.kafka.v1.connector_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.kafka.v1.DeleteConnectorRequest)
  })
_sym_db.RegisterMessage(DeleteConnectorRequest)

DeleteConnectorMetadata = _reflection.GeneratedProtocolMessageType('DeleteConnectorMetadata', (_message.Message,), {
  'DESCRIPTOR' : _DELETECONNECTORMETADATA,
  '__module__' : 'yandex.cloud.mdb.kafka.v1.connector_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.kafka.v1.DeleteConnectorMetadata)
  })
_sym_db.RegisterMessage(DeleteConnectorMetadata)

ResumeConnectorRequest = _reflection.GeneratedProtocolMessageType('ResumeConnectorRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESUMECONNECTORREQUEST,
  '__module__' : 'yandex.cloud.mdb.kafka.v1.connector_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.kafka.v1.ResumeConnectorRequest)
  })
_sym_db.RegisterMessage(ResumeConnectorRequest)

ResumeConnectorMetadata = _reflection.GeneratedProtocolMessageType('ResumeConnectorMetadata', (_message.Message,), {
  'DESCRIPTOR' : _RESUMECONNECTORMETADATA,
  '__module__' : 'yandex.cloud.mdb.kafka.v1.connector_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.kafka.v1.ResumeConnectorMetadata)
  })
_sym_db.RegisterMessage(ResumeConnectorMetadata)

PauseConnectorRequest = _reflection.GeneratedProtocolMessageType('PauseConnectorRequest', (_message.Message,), {
  'DESCRIPTOR' : _PAUSECONNECTORREQUEST,
  '__module__' : 'yandex.cloud.mdb.kafka.v1.connector_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.kafka.v1.PauseConnectorRequest)
  })
_sym_db.RegisterMessage(PauseConnectorRequest)

PauseConnectorMetadata = _reflection.GeneratedProtocolMessageType('PauseConnectorMetadata', (_message.Message,), {
  'DESCRIPTOR' : _PAUSECONNECTORMETADATA,
  '__module__' : 'yandex.cloud.mdb.kafka.v1.connector_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.kafka.v1.PauseConnectorMetadata)
  })
_sym_db.RegisterMessage(PauseConnectorMetadata)


DESCRIPTOR._options = None
_GETCONNECTORREQUEST.fields_by_name['cluster_id']._options = None
_GETCONNECTORREQUEST.fields_by_name['connector_name']._options = None
_LISTCONNECTORSREQUEST.fields_by_name['cluster_id']._options = None
_LISTCONNECTORSREQUEST.fields_by_name['page_size']._options = None
_LISTCONNECTORSREQUEST.fields_by_name['page_token']._options = None
_CREATECONNECTORREQUEST.fields_by_name['cluster_id']._options = None
_CREATECONNECTORREQUEST.fields_by_name['connector_spec']._options = None
_CREATECONNECTORMETADATA.fields_by_name['connector_name']._options = None
_UPDATECONNECTORREQUEST.fields_by_name['cluster_id']._options = None
_UPDATECONNECTORREQUEST.fields_by_name['connector_name']._options = None
_UPDATECONNECTORREQUEST.fields_by_name['connector_spec']._options = None
_UPDATECONNECTORMETADATA.fields_by_name['cluster_id']._options = None
_UPDATECONNECTORMETADATA.fields_by_name['connector_name']._options = None
_DELETECONNECTORREQUEST.fields_by_name['cluster_id']._options = None
_DELETECONNECTORREQUEST.fields_by_name['connector_name']._options = None
_RESUMECONNECTORREQUEST.fields_by_name['cluster_id']._options = None
_RESUMECONNECTORREQUEST.fields_by_name['connector_name']._options = None
_RESUMECONNECTORMETADATA.fields_by_name['connector_name']._options = None
_PAUSECONNECTORREQUEST.fields_by_name['cluster_id']._options = None
_PAUSECONNECTORREQUEST.fields_by_name['connector_name']._options = None
_PAUSECONNECTORMETADATA.fields_by_name['connector_name']._options = None

_CONNECTORSERVICE = _descriptor.ServiceDescriptor(
  name='ConnectorService',
  full_name='yandex.cloud.mdb.kafka.v1.ConnectorService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1865,
  serialized_end=3311,
  methods=[
  _descriptor.MethodDescriptor(
    name='Get',
    full_name='yandex.cloud.mdb.kafka.v1.ConnectorService.Get',
    index=0,
    containing_service=None,
    input_type=_GETCONNECTORREQUEST,
    output_type=yandex_dot_cloud_dot_mdb_dot_kafka_dot_v1_dot_connector__pb2._CONNECTOR,
    serialized_options=b'\202\323\344\223\002E\022C/managed-kafka/v1/clusters/{cluster_id}/connectors/{connector_name}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='List',
    full_name='yandex.cloud.mdb.kafka.v1.ConnectorService.List',
    index=1,
    containing_service=None,
    input_type=_LISTCONNECTORSREQUEST,
    output_type=_LISTCONNECTORSRESPONSE,
    serialized_options=b'\202\323\344\223\0024\0222/managed-kafka/v1/clusters/{cluster_id}/connectors',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Create',
    full_name='yandex.cloud.mdb.kafka.v1.ConnectorService.Create',
    index=2,
    containing_service=None,
    input_type=_CREATECONNECTORREQUEST,
    output_type=yandex_dot_cloud_dot_operation_dot_operation__pb2._OPERATION,
    serialized_options=b'\202\323\344\223\0027\"2/managed-kafka/v1/clusters/{cluster_id}/connectors:\001*\262\322*$\n\027CreateConnectorMetadata\022\tConnector',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Update',
    full_name='yandex.cloud.mdb.kafka.v1.ConnectorService.Update',
    index=3,
    containing_service=None,
    input_type=_UPDATECONNECTORREQUEST,
    output_type=yandex_dot_cloud_dot_operation_dot_operation__pb2._OPERATION,
    serialized_options=b'\202\323\344\223\002H2C/managed-kafka/v1/clusters/{cluster_id}/connectors/{connector_name}:\001*\262\322*$\n\027UpdateConnectorMetadata\022\tConnector',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Delete',
    full_name='yandex.cloud.mdb.kafka.v1.ConnectorService.Delete',
    index=4,
    containing_service=None,
    input_type=_DELETECONNECTORREQUEST,
    output_type=yandex_dot_cloud_dot_operation_dot_operation__pb2._OPERATION,
    serialized_options=b'\202\323\344\223\002E*C/managed-kafka/v1/clusters/{cluster_id}/connectors/{connector_name}\262\322*0\n\027DeleteConnectorMetadata\022\025google.protobuf.Empty',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Resume',
    full_name='yandex.cloud.mdb.kafka.v1.ConnectorService.Resume',
    index=5,
    containing_service=None,
    input_type=_RESUMECONNECTORREQUEST,
    output_type=yandex_dot_cloud_dot_operation_dot_operation__pb2._OPERATION,
    serialized_options=b'\202\323\344\223\002O\"J/managed-kafka/v1/clusters/{cluster_id}/connectors/resume/{connector_name}:\001*\262\322*$\n\027ResumeConnectorMetadata\022\tConnector',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Pause',
    full_name='yandex.cloud.mdb.kafka.v1.ConnectorService.Pause',
    index=6,
    containing_service=None,
    input_type=_PAUSECONNECTORREQUEST,
    output_type=yandex_dot_cloud_dot_operation_dot_operation__pb2._OPERATION,
    serialized_options=b'\202\323\344\223\002N\"I/managed-kafka/v1/clusters/{cluster_id}/connectors/pause/{connector_name}:\001*\262\322*#\n\026PauseConnectorMetadata\022\tConnector',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_CONNECTORSERVICE)

DESCRIPTOR.services_by_name['ConnectorService'] = _CONNECTORSERVICE

# @@protoc_insertion_point(module_scope)
