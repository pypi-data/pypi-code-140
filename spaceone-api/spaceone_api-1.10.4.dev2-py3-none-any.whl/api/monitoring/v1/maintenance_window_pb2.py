# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/monitoring/v1/maintenance_window.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3spaceone/api/monitoring/v1/maintenance_window.proto\x12\x1aspaceone.api.monitoring.v1\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"\xa1\x01\n\x1e\x43reateMaintenanceWindowRequest\x12\r\n\x05title\x18\x01 \x01(\t\x12\x10\n\x08projects\x18\x02 \x03(\t\x12\x12\n\nstart_time\x18\x03 \x01(\t\x12\x10\n\x08\x65nd_time\x18\x04 \x01(\t\x12%\n\x04tags\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"\xc0\x01\n\x1eUpdateMaintenanceWindowRequest\x12\x1d\n\x15maintenance_window_id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x10\n\x08projects\x18\x03 \x03(\t\x12\x12\n\nstart_time\x18\x04 \x01(\t\x12\x10\n\x08\x65nd_time\x18\x05 \x01(\t\x12%\n\x04tags\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"L\n\x18MaintenanceWindowRequest\x12\x1d\n\x15maintenance_window_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"]\n\x1bGetMaintenanceWindowRequest\x12\x1d\n\x15maintenance_window_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"\xc1\x02\n\x16MaintenanceWindowQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x1d\n\x15maintenance_window_id\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\x12X\n\x05state\x18\x04 \x01(\x0e\x32I.spaceone.api.monitoring.v1.MaintenanceWindowQuery.MaintenanceWindowState\x12\x12\n\nproject_id\x18\x05 \x01(\t\x12\x12\n\ncreated_by\x18\x06 \x01(\t\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"8\n\x16MaintenanceWindowState\x12\x08\n\x04NONE\x10\x00\x12\x08\n\x04OPEN\x10\x01\x12\n\n\x06\x43LOSED\x10\x02\"\x99\x03\n\x15MaintenanceWindowInfo\x12\x1d\n\x15maintenance_window_id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12W\n\x05state\x18\x03 \x01(\x0e\x32H.spaceone.api.monitoring.v1.MaintenanceWindowInfo.MaintenanceWindowState\x12\x12\n\nstart_time\x18\x04 \x01(\t\x12\x10\n\x08\x65nd_time\x18\x05 \x01(\t\x12%\n\x04tags\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x10\n\x08projects\x18\x0b \x03(\t\x12\x11\n\tdomain_id\x18\x0c \x01(\t\x12\x12\n\ncreated_by\x18\r \x01(\t\x12\x12\n\ncreated_at\x18\x15 \x01(\t\x12\x12\n\nupdated_at\x18\x16 \x01(\t\x12\x11\n\tclosed_at\x18\x17 \x01(\t\"8\n\x16MaintenanceWindowState\x12\x08\n\x04NONE\x10\x00\x12\x08\n\x04OPEN\x10\x01\x12\n\n\x06\x43LOSED\x10\x02\"q\n\x16MaintenanceWindowsInfo\x12\x42\n\x07results\x18\x01 \x03(\x0b\x32\x31.spaceone.api.monitoring.v1.MaintenanceWindowInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"e\n\x1aMaintenanceWindowStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\xbe\x08\n\x11MaintenanceWindow\x12\xa3\x01\n\x06\x63reate\x12:.spaceone.api.monitoring.v1.CreateMaintenanceWindowRequest\x1a\x31.spaceone.api.monitoring.v1.MaintenanceWindowInfo\"*\x82\xd3\xe4\x93\x02$\"\"/monitoring/v1/maintenance-windows\x12\xba\x01\n\x06update\x12:.spaceone.api.monitoring.v1.UpdateMaintenanceWindowRequest\x1a\x31.spaceone.api.monitoring.v1.MaintenanceWindowInfo\"A\x82\xd3\xe4\x93\x02;\x1a\x39/monitoring/v1/maintenance-window/{maintenance_window_id}\x12\xb9\x01\n\x05\x63lose\x12\x34.spaceone.api.monitoring.v1.MaintenanceWindowRequest\x1a\x31.spaceone.api.monitoring.v1.MaintenanceWindowInfo\"G\x82\xd3\xe4\x93\x02\x41\x1a?/monitoring/v1/maintenance-window/{maintenance_window_id}/close\x12\xb4\x01\n\x03get\x12\x37.spaceone.api.monitoring.v1.GetMaintenanceWindowRequest\x1a\x31.spaceone.api.monitoring.v1.MaintenanceWindowInfo\"A\x82\xd3\xe4\x93\x02;\x12\x39/monitoring/v1/maintenance-window/{maintenance_window_id}\x12\xc7\x01\n\x04list\x12\x32.spaceone.api.monitoring.v1.MaintenanceWindowQuery\x1a\x32.spaceone.api.monitoring.v1.MaintenanceWindowsInfo\"W\x82\xd3\xe4\x93\x02Q\x12\"/monitoring/v1/maintenance-windowsZ+\")/monitoring/v1/maintenance-windows/search\x12\x88\x01\n\x04stat\x12\x36.spaceone.api.monitoring.v1.MaintenanceWindowStatQuery\x1a\x17.google.protobuf.Struct\"/\x82\xd3\xe4\x93\x02)\"\'/monitoring/v1/maintenance-windows/statb\x06proto3')



_CREATEMAINTENANCEWINDOWREQUEST = DESCRIPTOR.message_types_by_name['CreateMaintenanceWindowRequest']
_UPDATEMAINTENANCEWINDOWREQUEST = DESCRIPTOR.message_types_by_name['UpdateMaintenanceWindowRequest']
_MAINTENANCEWINDOWREQUEST = DESCRIPTOR.message_types_by_name['MaintenanceWindowRequest']
_GETMAINTENANCEWINDOWREQUEST = DESCRIPTOR.message_types_by_name['GetMaintenanceWindowRequest']
_MAINTENANCEWINDOWQUERY = DESCRIPTOR.message_types_by_name['MaintenanceWindowQuery']
_MAINTENANCEWINDOWINFO = DESCRIPTOR.message_types_by_name['MaintenanceWindowInfo']
_MAINTENANCEWINDOWSINFO = DESCRIPTOR.message_types_by_name['MaintenanceWindowsInfo']
_MAINTENANCEWINDOWSTATQUERY = DESCRIPTOR.message_types_by_name['MaintenanceWindowStatQuery']
_MAINTENANCEWINDOWQUERY_MAINTENANCEWINDOWSTATE = _MAINTENANCEWINDOWQUERY.enum_types_by_name['MaintenanceWindowState']
_MAINTENANCEWINDOWINFO_MAINTENANCEWINDOWSTATE = _MAINTENANCEWINDOWINFO.enum_types_by_name['MaintenanceWindowState']
CreateMaintenanceWindowRequest = _reflection.GeneratedProtocolMessageType('CreateMaintenanceWindowRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEMAINTENANCEWINDOWREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.maintenance_window_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.CreateMaintenanceWindowRequest)
  })
_sym_db.RegisterMessage(CreateMaintenanceWindowRequest)

UpdateMaintenanceWindowRequest = _reflection.GeneratedProtocolMessageType('UpdateMaintenanceWindowRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEMAINTENANCEWINDOWREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.maintenance_window_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.UpdateMaintenanceWindowRequest)
  })
_sym_db.RegisterMessage(UpdateMaintenanceWindowRequest)

MaintenanceWindowRequest = _reflection.GeneratedProtocolMessageType('MaintenanceWindowRequest', (_message.Message,), {
  'DESCRIPTOR' : _MAINTENANCEWINDOWREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.maintenance_window_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.MaintenanceWindowRequest)
  })
_sym_db.RegisterMessage(MaintenanceWindowRequest)

GetMaintenanceWindowRequest = _reflection.GeneratedProtocolMessageType('GetMaintenanceWindowRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETMAINTENANCEWINDOWREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.maintenance_window_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.GetMaintenanceWindowRequest)
  })
_sym_db.RegisterMessage(GetMaintenanceWindowRequest)

MaintenanceWindowQuery = _reflection.GeneratedProtocolMessageType('MaintenanceWindowQuery', (_message.Message,), {
  'DESCRIPTOR' : _MAINTENANCEWINDOWQUERY,
  '__module__' : 'spaceone.api.monitoring.v1.maintenance_window_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.MaintenanceWindowQuery)
  })
_sym_db.RegisterMessage(MaintenanceWindowQuery)

MaintenanceWindowInfo = _reflection.GeneratedProtocolMessageType('MaintenanceWindowInfo', (_message.Message,), {
  'DESCRIPTOR' : _MAINTENANCEWINDOWINFO,
  '__module__' : 'spaceone.api.monitoring.v1.maintenance_window_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.MaintenanceWindowInfo)
  })
_sym_db.RegisterMessage(MaintenanceWindowInfo)

MaintenanceWindowsInfo = _reflection.GeneratedProtocolMessageType('MaintenanceWindowsInfo', (_message.Message,), {
  'DESCRIPTOR' : _MAINTENANCEWINDOWSINFO,
  '__module__' : 'spaceone.api.monitoring.v1.maintenance_window_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.MaintenanceWindowsInfo)
  })
_sym_db.RegisterMessage(MaintenanceWindowsInfo)

MaintenanceWindowStatQuery = _reflection.GeneratedProtocolMessageType('MaintenanceWindowStatQuery', (_message.Message,), {
  'DESCRIPTOR' : _MAINTENANCEWINDOWSTATQUERY,
  '__module__' : 'spaceone.api.monitoring.v1.maintenance_window_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.MaintenanceWindowStatQuery)
  })
_sym_db.RegisterMessage(MaintenanceWindowStatQuery)

_MAINTENANCEWINDOW = DESCRIPTOR.services_by_name['MaintenanceWindow']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MAINTENANCEWINDOW.methods_by_name['create']._options = None
  _MAINTENANCEWINDOW.methods_by_name['create']._serialized_options = b'\202\323\344\223\002$\"\"/monitoring/v1/maintenance-windows'
  _MAINTENANCEWINDOW.methods_by_name['update']._options = None
  _MAINTENANCEWINDOW.methods_by_name['update']._serialized_options = b'\202\323\344\223\002;\0329/monitoring/v1/maintenance-window/{maintenance_window_id}'
  _MAINTENANCEWINDOW.methods_by_name['close']._options = None
  _MAINTENANCEWINDOW.methods_by_name['close']._serialized_options = b'\202\323\344\223\002A\032?/monitoring/v1/maintenance-window/{maintenance_window_id}/close'
  _MAINTENANCEWINDOW.methods_by_name['get']._options = None
  _MAINTENANCEWINDOW.methods_by_name['get']._serialized_options = b'\202\323\344\223\002;\0229/monitoring/v1/maintenance-window/{maintenance_window_id}'
  _MAINTENANCEWINDOW.methods_by_name['list']._options = None
  _MAINTENANCEWINDOW.methods_by_name['list']._serialized_options = b'\202\323\344\223\002Q\022\"/monitoring/v1/maintenance-windowsZ+\")/monitoring/v1/maintenance-windows/search'
  _MAINTENANCEWINDOW.methods_by_name['stat']._options = None
  _MAINTENANCEWINDOW.methods_by_name['stat']._serialized_options = b'\202\323\344\223\002)\"\'/monitoring/v1/maintenance-windows/stat'
  _CREATEMAINTENANCEWINDOWREQUEST._serialized_start=178
  _CREATEMAINTENANCEWINDOWREQUEST._serialized_end=339
  _UPDATEMAINTENANCEWINDOWREQUEST._serialized_start=342
  _UPDATEMAINTENANCEWINDOWREQUEST._serialized_end=534
  _MAINTENANCEWINDOWREQUEST._serialized_start=536
  _MAINTENANCEWINDOWREQUEST._serialized_end=612
  _GETMAINTENANCEWINDOWREQUEST._serialized_start=614
  _GETMAINTENANCEWINDOWREQUEST._serialized_end=707
  _MAINTENANCEWINDOWQUERY._serialized_start=710
  _MAINTENANCEWINDOWQUERY._serialized_end=1031
  _MAINTENANCEWINDOWQUERY_MAINTENANCEWINDOWSTATE._serialized_start=975
  _MAINTENANCEWINDOWQUERY_MAINTENANCEWINDOWSTATE._serialized_end=1031
  _MAINTENANCEWINDOWINFO._serialized_start=1034
  _MAINTENANCEWINDOWINFO._serialized_end=1443
  _MAINTENANCEWINDOWINFO_MAINTENANCEWINDOWSTATE._serialized_start=975
  _MAINTENANCEWINDOWINFO_MAINTENANCEWINDOWSTATE._serialized_end=1031
  _MAINTENANCEWINDOWSINFO._serialized_start=1445
  _MAINTENANCEWINDOWSINFO._serialized_end=1558
  _MAINTENANCEWINDOWSTATQUERY._serialized_start=1560
  _MAINTENANCEWINDOWSTATQUERY._serialized_end=1661
  _MAINTENANCEWINDOW._serialized_start=1664
  _MAINTENANCEWINDOW._serialized_end=2750
# @@protoc_insertion_point(module_scope)
