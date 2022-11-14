# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/mdb/mysql/v1/maintenance.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yandex/cloud/mdb/mysql/v1/maintenance.proto',
  package='yandex.cloud.mdb.mysql.v1',
  syntax='proto3',
  serialized_options=b'\n\035yandex.cloud.api.mdb.mysql.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/mysql/v1;mysql',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n+yandex/cloud/mdb/mysql/v1/maintenance.proto\x12\x19yandex.cloud.mdb.mysql.v1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1dyandex/cloud/validation.proto\"\xc4\x01\n\x11MaintenanceWindow\x12\x46\n\x07\x61nytime\x18\x01 \x01(\x0b\x32\x33.yandex.cloud.mdb.mysql.v1.AnytimeMaintenanceWindowH\x00\x12W\n\x19weekly_maintenance_window\x18\x02 \x01(\x0b\x32\x32.yandex.cloud.mdb.mysql.v1.WeeklyMaintenanceWindowH\x00\x42\x0e\n\x06policy\x12\x04\xc0\xc1\x31\x01\"\x1a\n\x18\x41nytimeMaintenanceWindow\"\xde\x01\n\x17WeeklyMaintenanceWindow\x12G\n\x03\x64\x61y\x18\x01 \x01(\x0e\x32:.yandex.cloud.mdb.mysql.v1.WeeklyMaintenanceWindow.WeekDay\x12\x16\n\x04hour\x18\x02 \x01(\x03\x42\x08\xfa\xc7\x31\x04\x31-24\"b\n\x07WeekDay\x12\x18\n\x14WEEK_DAY_UNSPECIFIED\x10\x00\x12\x07\n\x03MON\x10\x01\x12\x07\n\x03TUE\x10\x02\x12\x07\n\x03WED\x10\x03\x12\x07\n\x03THU\x10\x04\x12\x07\n\x03\x46RI\x10\x05\x12\x07\n\x03SAT\x10\x06\x12\x07\n\x03SUN\x10\x07\"b\n\x14MaintenanceOperation\x12\x17\n\x04info\x18\x01 \x01(\tB\t\x8a\xc8\x31\x05<=256\x12\x31\n\rdelayed_until\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampBd\n\x1dyandex.cloud.api.mdb.mysql.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/mysql/v1;mysqlb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,yandex_dot_cloud_dot_validation__pb2.DESCRIPTOR,])



_WEEKLYMAINTENANCEWINDOW_WEEKDAY = _descriptor.EnumDescriptor(
  name='WeekDay',
  full_name='yandex.cloud.mdb.mysql.v1.WeeklyMaintenanceWindow.WeekDay',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='WEEK_DAY_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MON', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TUE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WED', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='THU', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FRI', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SAT', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SUN', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=490,
  serialized_end=588,
)
_sym_db.RegisterEnumDescriptor(_WEEKLYMAINTENANCEWINDOW_WEEKDAY)


_MAINTENANCEWINDOW = _descriptor.Descriptor(
  name='MaintenanceWindow',
  full_name='yandex.cloud.mdb.mysql.v1.MaintenanceWindow',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='anytime', full_name='yandex.cloud.mdb.mysql.v1.MaintenanceWindow.anytime', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='weekly_maintenance_window', full_name='yandex.cloud.mdb.mysql.v1.MaintenanceWindow.weekly_maintenance_window', index=1,
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
    _descriptor.OneofDescriptor(
      name='policy', full_name='yandex.cloud.mdb.mysql.v1.MaintenanceWindow.policy',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[], serialized_options=b'\300\3011\001'),
  ],
  serialized_start=139,
  serialized_end=335,
)


_ANYTIMEMAINTENANCEWINDOW = _descriptor.Descriptor(
  name='AnytimeMaintenanceWindow',
  full_name='yandex.cloud.mdb.mysql.v1.AnytimeMaintenanceWindow',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=337,
  serialized_end=363,
)


_WEEKLYMAINTENANCEWINDOW = _descriptor.Descriptor(
  name='WeeklyMaintenanceWindow',
  full_name='yandex.cloud.mdb.mysql.v1.WeeklyMaintenanceWindow',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='day', full_name='yandex.cloud.mdb.mysql.v1.WeeklyMaintenanceWindow.day', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hour', full_name='yandex.cloud.mdb.mysql.v1.WeeklyMaintenanceWindow.hour', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372\3071\0041-24', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _WEEKLYMAINTENANCEWINDOW_WEEKDAY,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=366,
  serialized_end=588,
)


_MAINTENANCEOPERATION = _descriptor.Descriptor(
  name='MaintenanceOperation',
  full_name='yandex.cloud.mdb.mysql.v1.MaintenanceOperation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='yandex.cloud.mdb.mysql.v1.MaintenanceOperation.info', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\212\3101\005<=256', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='delayed_until', full_name='yandex.cloud.mdb.mysql.v1.MaintenanceOperation.delayed_until', index=1,
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
  serialized_start=590,
  serialized_end=688,
)

_MAINTENANCEWINDOW.fields_by_name['anytime'].message_type = _ANYTIMEMAINTENANCEWINDOW
_MAINTENANCEWINDOW.fields_by_name['weekly_maintenance_window'].message_type = _WEEKLYMAINTENANCEWINDOW
_MAINTENANCEWINDOW.oneofs_by_name['policy'].fields.append(
  _MAINTENANCEWINDOW.fields_by_name['anytime'])
_MAINTENANCEWINDOW.fields_by_name['anytime'].containing_oneof = _MAINTENANCEWINDOW.oneofs_by_name['policy']
_MAINTENANCEWINDOW.oneofs_by_name['policy'].fields.append(
  _MAINTENANCEWINDOW.fields_by_name['weekly_maintenance_window'])
_MAINTENANCEWINDOW.fields_by_name['weekly_maintenance_window'].containing_oneof = _MAINTENANCEWINDOW.oneofs_by_name['policy']
_WEEKLYMAINTENANCEWINDOW.fields_by_name['day'].enum_type = _WEEKLYMAINTENANCEWINDOW_WEEKDAY
_WEEKLYMAINTENANCEWINDOW_WEEKDAY.containing_type = _WEEKLYMAINTENANCEWINDOW
_MAINTENANCEOPERATION.fields_by_name['delayed_until'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['MaintenanceWindow'] = _MAINTENANCEWINDOW
DESCRIPTOR.message_types_by_name['AnytimeMaintenanceWindow'] = _ANYTIMEMAINTENANCEWINDOW
DESCRIPTOR.message_types_by_name['WeeklyMaintenanceWindow'] = _WEEKLYMAINTENANCEWINDOW
DESCRIPTOR.message_types_by_name['MaintenanceOperation'] = _MAINTENANCEOPERATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MaintenanceWindow = _reflection.GeneratedProtocolMessageType('MaintenanceWindow', (_message.Message,), {
  'DESCRIPTOR' : _MAINTENANCEWINDOW,
  '__module__' : 'yandex.cloud.mdb.mysql.v1.maintenance_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1.MaintenanceWindow)
  })
_sym_db.RegisterMessage(MaintenanceWindow)

AnytimeMaintenanceWindow = _reflection.GeneratedProtocolMessageType('AnytimeMaintenanceWindow', (_message.Message,), {
  'DESCRIPTOR' : _ANYTIMEMAINTENANCEWINDOW,
  '__module__' : 'yandex.cloud.mdb.mysql.v1.maintenance_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1.AnytimeMaintenanceWindow)
  })
_sym_db.RegisterMessage(AnytimeMaintenanceWindow)

WeeklyMaintenanceWindow = _reflection.GeneratedProtocolMessageType('WeeklyMaintenanceWindow', (_message.Message,), {
  'DESCRIPTOR' : _WEEKLYMAINTENANCEWINDOW,
  '__module__' : 'yandex.cloud.mdb.mysql.v1.maintenance_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1.WeeklyMaintenanceWindow)
  })
_sym_db.RegisterMessage(WeeklyMaintenanceWindow)

MaintenanceOperation = _reflection.GeneratedProtocolMessageType('MaintenanceOperation', (_message.Message,), {
  'DESCRIPTOR' : _MAINTENANCEOPERATION,
  '__module__' : 'yandex.cloud.mdb.mysql.v1.maintenance_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.mysql.v1.MaintenanceOperation)
  })
_sym_db.RegisterMessage(MaintenanceOperation)


DESCRIPTOR._options = None
_MAINTENANCEWINDOW.oneofs_by_name['policy']._options = None
_WEEKLYMAINTENANCEWINDOW.fields_by_name['hour']._options = None
_MAINTENANCEOPERATION.fields_by_name['info']._options = None
# @@protoc_insertion_point(module_scope)
