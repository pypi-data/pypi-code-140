# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/inventory/v1/cloud_service_tag.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v1 import query_pb2 as spaceone_dot_api_dot_core_dot_v1_dot_query__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1spaceone/api/inventory/v1/cloud_service_tag.proto\x12\x19spaceone.api.inventory.v1\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"\xb0\x01\n\x14\x43loudServiceTagQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x18\n\x10\x63loud_service_id\x18\x02 \x01(\t\x12\x0b\n\x03key\x18\x03 \x01(\t\x12\x0c\n\x04type\x18\x04 \x01(\t\x12\x10\n\x08provider\x18\x05 \x01(\t\x12\x12\n\nproject_id\x18\x06 \x01(\t\x12\x11\n\tdomain_id\x18\n \x01(\t\"\xa6\x01\n\x13\x43loudServiceTagInfo\x12\x18\n\x10\x63loud_service_id\x18\x02 \x01(\t\x12\x0b\n\x03key\x18\x03 \x01(\t\x12\r\n\x05value\x18\x04 \x01(\t\x12\x0c\n\x04type\x18\x05 \x01(\t\x12\x10\n\x08provider\x18\x06 \x01(\t\x12\x12\n\nproject_id\x18\x07 \x01(\t\x12\x11\n\tdomain_id\x18\x0b \x01(\t\x12\x12\n\ncreated_at\x18\x15 \x01(\t\"l\n\x14\x43loudServiceTagsInfo\x12?\n\x07results\x18\x01 \x03(\x0b\x32..spaceone.api.inventory.v1.CloudServiceTagInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"c\n\x18\x43loudServiceTagStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\xd7\x02\n\x0f\x43loudServiceTag\x12\xbd\x01\n\x04list\x12/.spaceone.api.inventory.v1.CloudServiceTagQuery\x1a/.spaceone.api.inventory.v1.CloudServiceTagsInfo\"S\x82\xd3\xe4\x93\x02M\x12 /inventory/v1/cloud-service-tagsZ)\"\'/inventory/v1/cloud-service-tags/search\x12\x83\x01\n\x04stat\x12\x33.spaceone.api.inventory.v1.CloudServiceTagStatQuery\x1a\x17.google.protobuf.Struct\"-\x82\xd3\xe4\x93\x02\'\"%/inventory/v1/cloud-service-tags/statb\x06proto3')



_CLOUDSERVICETAGQUERY = DESCRIPTOR.message_types_by_name['CloudServiceTagQuery']
_CLOUDSERVICETAGINFO = DESCRIPTOR.message_types_by_name['CloudServiceTagInfo']
_CLOUDSERVICETAGSINFO = DESCRIPTOR.message_types_by_name['CloudServiceTagsInfo']
_CLOUDSERVICETAGSTATQUERY = DESCRIPTOR.message_types_by_name['CloudServiceTagStatQuery']
CloudServiceTagQuery = _reflection.GeneratedProtocolMessageType('CloudServiceTagQuery', (_message.Message,), {
  'DESCRIPTOR' : _CLOUDSERVICETAGQUERY,
  '__module__' : 'spaceone.api.inventory.v1.cloud_service_tag_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.inventory.v1.CloudServiceTagQuery)
  })
_sym_db.RegisterMessage(CloudServiceTagQuery)

CloudServiceTagInfo = _reflection.GeneratedProtocolMessageType('CloudServiceTagInfo', (_message.Message,), {
  'DESCRIPTOR' : _CLOUDSERVICETAGINFO,
  '__module__' : 'spaceone.api.inventory.v1.cloud_service_tag_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.inventory.v1.CloudServiceTagInfo)
  })
_sym_db.RegisterMessage(CloudServiceTagInfo)

CloudServiceTagsInfo = _reflection.GeneratedProtocolMessageType('CloudServiceTagsInfo', (_message.Message,), {
  'DESCRIPTOR' : _CLOUDSERVICETAGSINFO,
  '__module__' : 'spaceone.api.inventory.v1.cloud_service_tag_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.inventory.v1.CloudServiceTagsInfo)
  })
_sym_db.RegisterMessage(CloudServiceTagsInfo)

CloudServiceTagStatQuery = _reflection.GeneratedProtocolMessageType('CloudServiceTagStatQuery', (_message.Message,), {
  'DESCRIPTOR' : _CLOUDSERVICETAGSTATQUERY,
  '__module__' : 'spaceone.api.inventory.v1.cloud_service_tag_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.inventory.v1.CloudServiceTagStatQuery)
  })
_sym_db.RegisterMessage(CloudServiceTagStatQuery)

_CLOUDSERVICETAG = DESCRIPTOR.services_by_name['CloudServiceTag']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CLOUDSERVICETAG.methods_by_name['list']._options = None
  _CLOUDSERVICETAG.methods_by_name['list']._serialized_options = b'\202\323\344\223\002M\022 /inventory/v1/cloud-service-tagsZ)\"\'/inventory/v1/cloud-service-tags/search'
  _CLOUDSERVICETAG.methods_by_name['stat']._options = None
  _CLOUDSERVICETAG.methods_by_name['stat']._serialized_options = b'\202\323\344\223\002\'\"%/inventory/v1/cloud-service-tags/stat'
  _CLOUDSERVICETAGQUERY._serialized_start=175
  _CLOUDSERVICETAGQUERY._serialized_end=351
  _CLOUDSERVICETAGINFO._serialized_start=354
  _CLOUDSERVICETAGINFO._serialized_end=520
  _CLOUDSERVICETAGSINFO._serialized_start=522
  _CLOUDSERVICETAGSINFO._serialized_end=630
  _CLOUDSERVICETAGSTATQUERY._serialized_start=632
  _CLOUDSERVICETAGSTATQUERY._serialized_end=731
  _CLOUDSERVICETAG._serialized_start=734
  _CLOUDSERVICETAG._serialized_end=1077
# @@protoc_insertion_point(module_scope)
