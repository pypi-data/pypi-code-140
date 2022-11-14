# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/dashboard/v1/domain_dashboard.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v1 import query_pb2 as spaceone_dot_api_dot_core_dot_v1_dot_query__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0spaceone/api/dashboard/v1/domain_dashboard.proto\x12\x19spaceone.api.dashboard.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"+\n\x18\x44omainDashboardDateRange\x12\x0f\n\x07\x65nabled\x18\x01 \x01(\x08\"*\n\x17\x44omainDashboardCurrency\x12\x0f\n\x07\x65nabled\x18\x01 \x01(\x08\"\xa8\x01\n\x17\x44omainDashboardSettings\x12G\n\ndate_range\x18\x01 \x01(\x0b\x32\x33.spaceone.api.dashboard.v1.DomainDashboardDateRange\x12\x44\n\x08\x63urrency\x18\x02 \x01(\x0b\x32\x32.spaceone.api.dashboard.v1.DomainDashboardCurrency\"\x85\x03\n\x1c\x43reateDomainDashboardRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12+\n\x07layouts\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12\x32\n\x11\x64\x61shboard_options\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x44\n\x08settings\x18\x06 \x01(\x0b\x32\x32.spaceone.api.dashboard.v1.DomainDashboardSettings\x12\x39\n\x18\x64\x61shboard_options_schema\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\x12*\n\x06labels\x18\n \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12%\n\x04tags\x18\x0b \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0f\n\x07user_id\x18\x14 \x01(\t\x12\x11\n\tdomain_id\x18\x15 \x01(\t\"\x91\x03\n\x1cUpdateDomainDashboardRequest\x12\x1b\n\x13\x64omain_dashboard_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12+\n\x07layouts\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12\x32\n\x11\x64\x61shboard_options\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x44\n\x08settings\x18\x06 \x01(\x0b\x32\x32.spaceone.api.dashboard.v1.DomainDashboardSettings\x12\x39\n\x18\x64\x61shboard_options_schema\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\x12*\n\x06labels\x18\n \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12%\n\x04tags\x18\x0b \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x15 \x01(\t\"H\n\x16\x44omainDashboardRequest\x12\x1b\n\x13\x64omain_dashboard_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"Y\n\x19GetDomainDashboardRequest\x12\x1b\n\x13\x64omain_dashboard_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"`\n\x1d\x44omainDashboardVersionRequest\x12\x1b\n\x13\x64omain_dashboard_id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x04 \x01(\x05\x12\x11\n\tdomain_id\x18\x15 \x01(\t\"q\n GetDomainDashboardVersionRequest\x12\x1b\n\x13\x64omain_dashboard_id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x05\x12\x11\n\tdomain_id\x18\n \x01(\t\x12\x0c\n\x04only\x18\x0b \x03(\t\"\x8a\x01\n\x1b\x44omainDashboardVersionQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x1b\n\x13\x64omain_dashboard_id\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\x05\x12\x11\n\tdomain_id\x18\n \x01(\t\"\x86\x02\n\x14\x44omainDashboardQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x1b\n\x13\x64omain_dashboard_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x44\n\x05scope\x18\x04 \x01(\x0e\x32\x35.spaceone.api.dashboard.v1.DomainDashboardQuery.Scope\x12\x0f\n\x07user_id\x18\n \x01(\t\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"-\n\x05Scope\x12\x0e\n\nSCOPE_NONE\x10\x00\x12\n\n\x06\x44OMAIN\x10\x01\x12\x08\n\x04USER\x10\x02\"\xc6\x04\n\x13\x44omainDashboardInfo\x12\x1b\n\x13\x64omain_dashboard_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x43\n\x05scope\x18\x03 \x01(\x0e\x32\x34.spaceone.api.dashboard.v1.DomainDashboardInfo.Scope\x12\x0f\n\x07version\x18\x04 \x01(\x05\x12+\n\x07layouts\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12\x32\n\x11\x64\x61shboard_options\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x44\n\x08settings\x18\x07 \x01(\x0b\x32\x32.spaceone.api.dashboard.v1.DomainDashboardSettings\x12\x39\n\x18\x64\x61shboard_options_schema\x18\x08 \x01(\x0b\x32\x17.google.protobuf.Struct\x12*\n\x06labels\x18\n \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12%\n\x04tags\x18\x0b \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0f\n\x07user_id\x18\x14 \x01(\t\x12\x11\n\tdomain_id\x18\x15 \x01(\t\x12\x12\n\ncreated_at\x18\x16 \x01(\t\x12\x12\n\nupdated_at\x18\x17 \x01(\t\"-\n\x05Scope\x12\x0e\n\nSCOPE_NONE\x10\x00\x12\n\n\x06\x44OMAIN\x10\x01\x12\x08\n\x04USER\x10\x02\"l\n\x14\x44omainDashboardsInfo\x12?\n\x07results\x18\x01 \x03(\x0b\x32..spaceone.api.dashboard.v1.DomainDashboardInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"c\n\x18\x44omainDashboardStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"\xe3\x02\n\x1a\x44omainDashboardVersionInfo\x12\x1b\n\x13\x64omain_dashboard_id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x05\x12\x0e\n\x06latest\x18\x03 \x01(\x08\x12+\n\x07layouts\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12\x32\n\x11\x64\x61shboard_options\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x44\n\x08settings\x18\x07 \x01(\x0b\x32\x32.spaceone.api.dashboard.v1.DomainDashboardSettings\x12\x39\n\x18\x64\x61shboard_options_schema\x18\x08 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x15 \x01(\t\x12\x12\n\ncreated_at\x18\x16 \x01(\t\"z\n\x1b\x44omainDashboardVersionsInfo\x12\x46\n\x07results\x18\x01 \x03(\x0b\x32\x35.spaceone.api.dashboard.v1.DomainDashboardVersionInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\x32\xd3\x0e\n\x0f\x44omainDashboard\x12\x9a\x01\n\x06\x63reate\x12\x37.spaceone.api.dashboard.v1.CreateDomainDashboardRequest\x1a..spaceone.api.dashboard.v1.DomainDashboardInfo\"\'\x82\xd3\xe4\x93\x02!\"\x1f/dashboard/v1/domain-dashboards\x12\xaf\x01\n\x06update\x12\x37.spaceone.api.dashboard.v1.UpdateDomainDashboardRequest\x1a..spaceone.api.dashboard.v1.DomainDashboardInfo\"<\x82\xd3\xe4\x93\x02\x36\x1a\x34/dashboard/v1/domain-dashboard/{domain_dashboard_id}\x12\x91\x01\n\x06\x64\x65lete\x12\x31.spaceone.api.dashboard.v1.DomainDashboardRequest\x1a\x16.google.protobuf.Empty\"<\x82\xd3\xe4\x93\x02\x36*4/dashboard/v1/domain-dashboard/{domain_dashboard_id}\x12\xa9\x01\n\x03get\x12\x34.spaceone.api.dashboard.v1.GetDomainDashboardRequest\x1a..spaceone.api.dashboard.v1.DomainDashboardInfo\"<\x82\xd3\xe4\x93\x02\x36\x12\x34/dashboard/v1/domain-dashboard/{domain_dashboard_id}\x12\xb2\x01\n\x0e\x64\x65lete_version\x12\x38.spaceone.api.dashboard.v1.DomainDashboardVersionRequest\x1a\x16.google.protobuf.Empty\"N\x82\xd3\xe4\x93\x02H*F/dashboard/v1/domain-dashboard/{domain_dashboard_id}/version/{version}\x12\xd1\x01\n\x0erevert_version\x12\x38.spaceone.api.dashboard.v1.DomainDashboardVersionRequest\x1a..spaceone.api.dashboard.v1.DomainDashboardInfo\"U\x82\xd3\xe4\x93\x02O\"M/dashboard/v1/domain-dashboard/{domain_dashboard_id}/version/{version}/revert\x12\xd1\x01\n\x0bget_version\x12;.spaceone.api.dashboard.v1.GetDomainDashboardVersionRequest\x1a\x35.spaceone.api.dashboard.v1.DomainDashboardVersionInfo\"N\x82\xd3\xe4\x93\x02H\x12\x46/dashboard/v1/domain-dashboard/{domain_dashboard_id}/version/{version}\x12\x90\x02\n\rlist_versions\x12\x36.spaceone.api.dashboard.v1.DomainDashboardVersionQuery\x1a\x36.spaceone.api.dashboard.v1.DomainDashboardVersionsInfo\"\x8e\x01\x82\xd3\xe4\x93\x02\x87\x01\x12=/dashboard/v1/domain-dashboard/{domain_dashboard_id}/versionsZF\"D/dashboard/v1/domain-dashboard/{domain_dashboard_id}/versions/search\x12\xbb\x01\n\x04list\x12/.spaceone.api.dashboard.v1.DomainDashboardQuery\x1a/.spaceone.api.dashboard.v1.DomainDashboardsInfo\"Q\x82\xd3\xe4\x93\x02K\x12\x1f/dashboard/v1/domain-dashboardsZ(\"&/dashboard/v1/domain-dashboards/search\x12\x82\x01\n\x04stat\x12\x33.spaceone.api.dashboard.v1.DomainDashboardStatQuery\x1a\x17.google.protobuf.Struct\",\x82\xd3\xe4\x93\x02&\"$/dashboard/v1/domain-dashboards/statb\x06proto3')



_DOMAINDASHBOARDDATERANGE = DESCRIPTOR.message_types_by_name['DomainDashboardDateRange']
_DOMAINDASHBOARDCURRENCY = DESCRIPTOR.message_types_by_name['DomainDashboardCurrency']
_DOMAINDASHBOARDSETTINGS = DESCRIPTOR.message_types_by_name['DomainDashboardSettings']
_CREATEDOMAINDASHBOARDREQUEST = DESCRIPTOR.message_types_by_name['CreateDomainDashboardRequest']
_UPDATEDOMAINDASHBOARDREQUEST = DESCRIPTOR.message_types_by_name['UpdateDomainDashboardRequest']
_DOMAINDASHBOARDREQUEST = DESCRIPTOR.message_types_by_name['DomainDashboardRequest']
_GETDOMAINDASHBOARDREQUEST = DESCRIPTOR.message_types_by_name['GetDomainDashboardRequest']
_DOMAINDASHBOARDVERSIONREQUEST = DESCRIPTOR.message_types_by_name['DomainDashboardVersionRequest']
_GETDOMAINDASHBOARDVERSIONREQUEST = DESCRIPTOR.message_types_by_name['GetDomainDashboardVersionRequest']
_DOMAINDASHBOARDVERSIONQUERY = DESCRIPTOR.message_types_by_name['DomainDashboardVersionQuery']
_DOMAINDASHBOARDQUERY = DESCRIPTOR.message_types_by_name['DomainDashboardQuery']
_DOMAINDASHBOARDINFO = DESCRIPTOR.message_types_by_name['DomainDashboardInfo']
_DOMAINDASHBOARDSINFO = DESCRIPTOR.message_types_by_name['DomainDashboardsInfo']
_DOMAINDASHBOARDSTATQUERY = DESCRIPTOR.message_types_by_name['DomainDashboardStatQuery']
_DOMAINDASHBOARDVERSIONINFO = DESCRIPTOR.message_types_by_name['DomainDashboardVersionInfo']
_DOMAINDASHBOARDVERSIONSINFO = DESCRIPTOR.message_types_by_name['DomainDashboardVersionsInfo']
_DOMAINDASHBOARDQUERY_SCOPE = _DOMAINDASHBOARDQUERY.enum_types_by_name['Scope']
_DOMAINDASHBOARDINFO_SCOPE = _DOMAINDASHBOARDINFO.enum_types_by_name['Scope']
DomainDashboardDateRange = _reflection.GeneratedProtocolMessageType('DomainDashboardDateRange', (_message.Message,), {
  'DESCRIPTOR' : _DOMAINDASHBOARDDATERANGE,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.DomainDashboardDateRange)
  })
_sym_db.RegisterMessage(DomainDashboardDateRange)

DomainDashboardCurrency = _reflection.GeneratedProtocolMessageType('DomainDashboardCurrency', (_message.Message,), {
  'DESCRIPTOR' : _DOMAINDASHBOARDCURRENCY,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.DomainDashboardCurrency)
  })
_sym_db.RegisterMessage(DomainDashboardCurrency)

DomainDashboardSettings = _reflection.GeneratedProtocolMessageType('DomainDashboardSettings', (_message.Message,), {
  'DESCRIPTOR' : _DOMAINDASHBOARDSETTINGS,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.DomainDashboardSettings)
  })
_sym_db.RegisterMessage(DomainDashboardSettings)

CreateDomainDashboardRequest = _reflection.GeneratedProtocolMessageType('CreateDomainDashboardRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEDOMAINDASHBOARDREQUEST,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.CreateDomainDashboardRequest)
  })
_sym_db.RegisterMessage(CreateDomainDashboardRequest)

UpdateDomainDashboardRequest = _reflection.GeneratedProtocolMessageType('UpdateDomainDashboardRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEDOMAINDASHBOARDREQUEST,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.UpdateDomainDashboardRequest)
  })
_sym_db.RegisterMessage(UpdateDomainDashboardRequest)

DomainDashboardRequest = _reflection.GeneratedProtocolMessageType('DomainDashboardRequest', (_message.Message,), {
  'DESCRIPTOR' : _DOMAINDASHBOARDREQUEST,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.DomainDashboardRequest)
  })
_sym_db.RegisterMessage(DomainDashboardRequest)

GetDomainDashboardRequest = _reflection.GeneratedProtocolMessageType('GetDomainDashboardRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETDOMAINDASHBOARDREQUEST,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.GetDomainDashboardRequest)
  })
_sym_db.RegisterMessage(GetDomainDashboardRequest)

DomainDashboardVersionRequest = _reflection.GeneratedProtocolMessageType('DomainDashboardVersionRequest', (_message.Message,), {
  'DESCRIPTOR' : _DOMAINDASHBOARDVERSIONREQUEST,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.DomainDashboardVersionRequest)
  })
_sym_db.RegisterMessage(DomainDashboardVersionRequest)

GetDomainDashboardVersionRequest = _reflection.GeneratedProtocolMessageType('GetDomainDashboardVersionRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETDOMAINDASHBOARDVERSIONREQUEST,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.GetDomainDashboardVersionRequest)
  })
_sym_db.RegisterMessage(GetDomainDashboardVersionRequest)

DomainDashboardVersionQuery = _reflection.GeneratedProtocolMessageType('DomainDashboardVersionQuery', (_message.Message,), {
  'DESCRIPTOR' : _DOMAINDASHBOARDVERSIONQUERY,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.DomainDashboardVersionQuery)
  })
_sym_db.RegisterMessage(DomainDashboardVersionQuery)

DomainDashboardQuery = _reflection.GeneratedProtocolMessageType('DomainDashboardQuery', (_message.Message,), {
  'DESCRIPTOR' : _DOMAINDASHBOARDQUERY,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.DomainDashboardQuery)
  })
_sym_db.RegisterMessage(DomainDashboardQuery)

DomainDashboardInfo = _reflection.GeneratedProtocolMessageType('DomainDashboardInfo', (_message.Message,), {
  'DESCRIPTOR' : _DOMAINDASHBOARDINFO,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.DomainDashboardInfo)
  })
_sym_db.RegisterMessage(DomainDashboardInfo)

DomainDashboardsInfo = _reflection.GeneratedProtocolMessageType('DomainDashboardsInfo', (_message.Message,), {
  'DESCRIPTOR' : _DOMAINDASHBOARDSINFO,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.DomainDashboardsInfo)
  })
_sym_db.RegisterMessage(DomainDashboardsInfo)

DomainDashboardStatQuery = _reflection.GeneratedProtocolMessageType('DomainDashboardStatQuery', (_message.Message,), {
  'DESCRIPTOR' : _DOMAINDASHBOARDSTATQUERY,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.DomainDashboardStatQuery)
  })
_sym_db.RegisterMessage(DomainDashboardStatQuery)

DomainDashboardVersionInfo = _reflection.GeneratedProtocolMessageType('DomainDashboardVersionInfo', (_message.Message,), {
  'DESCRIPTOR' : _DOMAINDASHBOARDVERSIONINFO,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.DomainDashboardVersionInfo)
  })
_sym_db.RegisterMessage(DomainDashboardVersionInfo)

DomainDashboardVersionsInfo = _reflection.GeneratedProtocolMessageType('DomainDashboardVersionsInfo', (_message.Message,), {
  'DESCRIPTOR' : _DOMAINDASHBOARDVERSIONSINFO,
  '__module__' : 'spaceone.api.dashboard.v1.domain_dashboard_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.dashboard.v1.DomainDashboardVersionsInfo)
  })
_sym_db.RegisterMessage(DomainDashboardVersionsInfo)

_DOMAINDASHBOARD = DESCRIPTOR.services_by_name['DomainDashboard']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _DOMAINDASHBOARD.methods_by_name['create']._options = None
  _DOMAINDASHBOARD.methods_by_name['create']._serialized_options = b'\202\323\344\223\002!\"\037/dashboard/v1/domain-dashboards'
  _DOMAINDASHBOARD.methods_by_name['update']._options = None
  _DOMAINDASHBOARD.methods_by_name['update']._serialized_options = b'\202\323\344\223\0026\0324/dashboard/v1/domain-dashboard/{domain_dashboard_id}'
  _DOMAINDASHBOARD.methods_by_name['delete']._options = None
  _DOMAINDASHBOARD.methods_by_name['delete']._serialized_options = b'\202\323\344\223\0026*4/dashboard/v1/domain-dashboard/{domain_dashboard_id}'
  _DOMAINDASHBOARD.methods_by_name['get']._options = None
  _DOMAINDASHBOARD.methods_by_name['get']._serialized_options = b'\202\323\344\223\0026\0224/dashboard/v1/domain-dashboard/{domain_dashboard_id}'
  _DOMAINDASHBOARD.methods_by_name['delete_version']._options = None
  _DOMAINDASHBOARD.methods_by_name['delete_version']._serialized_options = b'\202\323\344\223\002H*F/dashboard/v1/domain-dashboard/{domain_dashboard_id}/version/{version}'
  _DOMAINDASHBOARD.methods_by_name['revert_version']._options = None
  _DOMAINDASHBOARD.methods_by_name['revert_version']._serialized_options = b'\202\323\344\223\002O\"M/dashboard/v1/domain-dashboard/{domain_dashboard_id}/version/{version}/revert'
  _DOMAINDASHBOARD.methods_by_name['get_version']._options = None
  _DOMAINDASHBOARD.methods_by_name['get_version']._serialized_options = b'\202\323\344\223\002H\022F/dashboard/v1/domain-dashboard/{domain_dashboard_id}/version/{version}'
  _DOMAINDASHBOARD.methods_by_name['list_versions']._options = None
  _DOMAINDASHBOARD.methods_by_name['list_versions']._serialized_options = b'\202\323\344\223\002\207\001\022=/dashboard/v1/domain-dashboard/{domain_dashboard_id}/versionsZF\"D/dashboard/v1/domain-dashboard/{domain_dashboard_id}/versions/search'
  _DOMAINDASHBOARD.methods_by_name['list']._options = None
  _DOMAINDASHBOARD.methods_by_name['list']._serialized_options = b'\202\323\344\223\002K\022\037/dashboard/v1/domain-dashboardsZ(\"&/dashboard/v1/domain-dashboards/search'
  _DOMAINDASHBOARD.methods_by_name['stat']._options = None
  _DOMAINDASHBOARD.methods_by_name['stat']._serialized_options = b'\202\323\344\223\002&\"$/dashboard/v1/domain-dashboards/stat'
  _DOMAINDASHBOARDDATERANGE._serialized_start=202
  _DOMAINDASHBOARDDATERANGE._serialized_end=245
  _DOMAINDASHBOARDCURRENCY._serialized_start=247
  _DOMAINDASHBOARDCURRENCY._serialized_end=289
  _DOMAINDASHBOARDSETTINGS._serialized_start=292
  _DOMAINDASHBOARDSETTINGS._serialized_end=460
  _CREATEDOMAINDASHBOARDREQUEST._serialized_start=463
  _CREATEDOMAINDASHBOARDREQUEST._serialized_end=852
  _UPDATEDOMAINDASHBOARDREQUEST._serialized_start=855
  _UPDATEDOMAINDASHBOARDREQUEST._serialized_end=1256
  _DOMAINDASHBOARDREQUEST._serialized_start=1258
  _DOMAINDASHBOARDREQUEST._serialized_end=1330
  _GETDOMAINDASHBOARDREQUEST._serialized_start=1332
  _GETDOMAINDASHBOARDREQUEST._serialized_end=1421
  _DOMAINDASHBOARDVERSIONREQUEST._serialized_start=1423
  _DOMAINDASHBOARDVERSIONREQUEST._serialized_end=1519
  _GETDOMAINDASHBOARDVERSIONREQUEST._serialized_start=1521
  _GETDOMAINDASHBOARDVERSIONREQUEST._serialized_end=1634
  _DOMAINDASHBOARDVERSIONQUERY._serialized_start=1637
  _DOMAINDASHBOARDVERSIONQUERY._serialized_end=1775
  _DOMAINDASHBOARDQUERY._serialized_start=1778
  _DOMAINDASHBOARDQUERY._serialized_end=2040
  _DOMAINDASHBOARDQUERY_SCOPE._serialized_start=1995
  _DOMAINDASHBOARDQUERY_SCOPE._serialized_end=2040
  _DOMAINDASHBOARDINFO._serialized_start=2043
  _DOMAINDASHBOARDINFO._serialized_end=2625
  _DOMAINDASHBOARDINFO_SCOPE._serialized_start=1995
  _DOMAINDASHBOARDINFO_SCOPE._serialized_end=2040
  _DOMAINDASHBOARDSINFO._serialized_start=2627
  _DOMAINDASHBOARDSINFO._serialized_end=2735
  _DOMAINDASHBOARDSTATQUERY._serialized_start=2737
  _DOMAINDASHBOARDSTATQUERY._serialized_end=2836
  _DOMAINDASHBOARDVERSIONINFO._serialized_start=2839
  _DOMAINDASHBOARDVERSIONINFO._serialized_end=3194
  _DOMAINDASHBOARDVERSIONSINFO._serialized_start=3196
  _DOMAINDASHBOARDVERSIONSINFO._serialized_end=3318
  _DOMAINDASHBOARD._serialized_start=3321
  _DOMAINDASHBOARD._serialized_end=5196
# @@protoc_insertion_point(module_scope)
