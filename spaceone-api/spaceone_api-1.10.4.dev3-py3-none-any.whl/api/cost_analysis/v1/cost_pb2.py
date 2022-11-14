# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/cost_analysis/v1/cost.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(spaceone/api/cost_analysis/v1/cost.proto\x12\x1dspaceone.api.cost_analysis.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"\xcf\x03\n\x11\x43reateCostRequest\x12\x15\n\roriginal_cost\x18\x01 \x01(\x02\x12\x19\n\x11original_currency\x18\x02 \x01(\t\x12\x10\n\x08usd_cost\x18\x03 \x01(\x02\x12\x16\n\x0eusage_quantity\x18\x04 \x01(\x02\x12\x10\n\x08provider\x18\x05 \x01(\t\x12\x13\n\x0bregion_code\x18\x06 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x07 \x01(\t\x12\x0f\n\x07product\x18\x08 \x01(\t\x12\x0f\n\x07\x61\x63\x63ount\x18\t \x01(\t\x12\x12\n\nusage_type\x18\n \x01(\t\x12\x16\n\x0eresource_group\x18\x0b \x01(\t\x12\x10\n\x08resource\x18\x0c \x01(\t\x12%\n\x04tags\x18\x15 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x30\n\x0f\x61\x64\x64itional_info\x18\x16 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x1a\n\x12service_account_id\x18\x1f \x01(\t\x12\x12\n\nproject_id\x18  \x01(\t\x12\x16\n\x0e\x64\x61ta_source_id\x18! \x01(\t\x12\x11\n\tdomain_id\x18\" \x01(\t\x12\x11\n\tbilled_at\x18) \x01(\t\"1\n\x0b\x43ostRequest\x12\x0f\n\x07\x63ost_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"B\n\x0eGetCostRequest\x12\x0f\n\x07\x63ost_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"\xeb\x02\n\tCostQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x0f\n\x07\x63ost_id\x18\x02 \x01(\t\x12\x19\n\x11original_currency\x18\x03 \x01(\t\x12\x10\n\x08provider\x18\x04 \x01(\t\x12\x13\n\x0bregion_code\x18\x05 \x01(\t\x12\x12\n\nregion_key\x18\x06 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x07 \x01(\t\x12\x0f\n\x07product\x18\x08 \x01(\t\x12\x0f\n\x07\x61\x63\x63ount\x18\t \x01(\t\x12\x12\n\nusage_type\x18\n \x01(\t\x12\x16\n\x0eresource_group\x18\x0b \x01(\t\x12\x10\n\x08resource\x18\x0c \x01(\t\x12\x1a\n\x12service_account_id\x18\x15 \x01(\t\x12\x12\n\nproject_id\x18\x16 \x01(\t\x12\x16\n\x0e\x64\x61ta_source_id\x18\x17 \x01(\t\x12\x11\n\tdomain_id\x18\x18 \x01(\t\"\xff\x03\n\x08\x43ostInfo\x12\x0f\n\x07\x63ost_id\x18\x01 \x01(\t\x12\x10\n\x08usd_cost\x18\x02 \x01(\x02\x12\x19\n\x11original_currency\x18\x03 \x01(\t\x12\x15\n\roriginal_cost\x18\x04 \x01(\x02\x12\x16\n\x0eusage_quantity\x18\x05 \x01(\x02\x12\x10\n\x08provider\x18\x06 \x01(\t\x12\x13\n\x0bregion_code\x18\x07 \x01(\t\x12\x12\n\nregion_key\x18\x08 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\t \x01(\t\x12\x0f\n\x07product\x18\n \x01(\t\x12\x0f\n\x07\x61\x63\x63ount\x18\x0b \x01(\t\x12\x12\n\nusage_type\x18\x0c \x01(\t\x12\x16\n\x0eresource_group\x18\r \x01(\t\x12\x10\n\x08resource\x18\x0e \x01(\t\x12%\n\x04tags\x18\x15 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x30\n\x0f\x61\x64\x64itional_info\x18\x16 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x1a\n\x12service_account_id\x18\x1f \x01(\t\x12\x12\n\nproject_id\x18  \x01(\t\x12\x16\n\x0e\x64\x61ta_source_id\x18! \x01(\t\x12\x11\n\tdomain_id\x18\" \x01(\t\x12\x11\n\tbilled_at\x18) \x01(\t\x12\x12\n\ncreated_at\x18* \x01(\t\"Z\n\tCostsInfo\x12\x38\n\x07results\x18\x01 \x03(\x0b\x32\'.spaceone.api.cost_analysis.v1.CostInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"\xbf\x03\n\x10\x43ostAnalyzeQuery\x12P\n\x0bgranularity\x18\x01 \x01(\x0e\x32;.spaceone.api.cost_analysis.v1.CostAnalyzeQuery.Granularity\x12\r\n\x05start\x18\x02 \x01(\t\x12\x0b\n\x03\x65nd\x18\x03 \x01(\t\x12\x10\n\x08group_by\x18\x04 \x03(\t\x12*\n\x06\x66ilter\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12\r\n\x05limit\x18\x06 \x01(\x05\x12(\n\x04page\x18\x07 \x01(\x0b\x32\x1a.spaceone.api.core.v1.Page\x12(\n\x04sort\x18\x08 \x01(\x0b\x32\x1a.spaceone.api.core.v1.Sort\x12\x1e\n\x16include_usage_quantity\x18\t \x01(\x08\x12\x16\n\x0einclude_others\x18\n \x01(\x08\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"Q\n\x0bGranularity\x12\r\n\tUNIT_NONE\x10\x00\x12\x0f\n\x0b\x41\x43\x43UMULATED\x10\x01\x12\t\n\x05\x44\x41ILY\x10\x02\x12\x0b\n\x07MONTHLY\x10\x03\x12\n\n\x06YEARLY\x10\x04\"X\n\rCostStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\xa2\x06\n\x04\x43ost\x12\x84\x01\n\x06\x63reate\x12\x30.spaceone.api.cost_analysis.v1.CreateCostRequest\x1a\'.spaceone.api.cost_analysis.v1.CostInfo\"\x1f\x82\xd3\xe4\x93\x02\x19\"\x17/cost-analysis/v1/costs\x12v\n\x06\x64\x65lete\x12*.spaceone.api.cost_analysis.v1.CostRequest\x1a\x16.google.protobuf.Empty\"(\x82\xd3\xe4\x93\x02\"* /cost-analysis/v1/cost/{cost_id}\x12\x87\x01\n\x03get\x12-.spaceone.api.cost_analysis.v1.GetCostRequest\x1a\'.spaceone.api.cost_analysis.v1.CostInfo\"(\x82\xd3\xe4\x93\x02\"\x12 /cost-analysis/v1/cost/{cost_id}\x12\x9d\x01\n\x04list\x12(.spaceone.api.cost_analysis.v1.CostQuery\x1a(.spaceone.api.cost_analysis.v1.CostsInfo\"A\x82\xd3\xe4\x93\x02;\x12\x17/cost-analysis/v1/costsZ \"\x1e/cost-analysis/v1/costs/search\x12|\n\x07\x61nalyze\x12/.spaceone.api.cost_analysis.v1.CostAnalyzeQuery\x1a\x17.google.protobuf.Struct\"\'\x82\xd3\xe4\x93\x02!\"\x1f/cost-analysis/v1/costs/analyze\x12s\n\x04stat\x12,.spaceone.api.cost_analysis.v1.CostStatQuery\x1a\x17.google.protobuf.Struct\"$\x82\xd3\xe4\x93\x02\x1e\"\x1c/cost-analysis/v1/costs/statb\x06proto3')



_CREATECOSTREQUEST = DESCRIPTOR.message_types_by_name['CreateCostRequest']
_COSTREQUEST = DESCRIPTOR.message_types_by_name['CostRequest']
_GETCOSTREQUEST = DESCRIPTOR.message_types_by_name['GetCostRequest']
_COSTQUERY = DESCRIPTOR.message_types_by_name['CostQuery']
_COSTINFO = DESCRIPTOR.message_types_by_name['CostInfo']
_COSTSINFO = DESCRIPTOR.message_types_by_name['CostsInfo']
_COSTANALYZEQUERY = DESCRIPTOR.message_types_by_name['CostAnalyzeQuery']
_COSTSTATQUERY = DESCRIPTOR.message_types_by_name['CostStatQuery']
_COSTANALYZEQUERY_GRANULARITY = _COSTANALYZEQUERY.enum_types_by_name['Granularity']
CreateCostRequest = _reflection.GeneratedProtocolMessageType('CreateCostRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATECOSTREQUEST,
  '__module__' : 'spaceone.api.cost_analysis.v1.cost_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.CreateCostRequest)
  })
_sym_db.RegisterMessage(CreateCostRequest)

CostRequest = _reflection.GeneratedProtocolMessageType('CostRequest', (_message.Message,), {
  'DESCRIPTOR' : _COSTREQUEST,
  '__module__' : 'spaceone.api.cost_analysis.v1.cost_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.CostRequest)
  })
_sym_db.RegisterMessage(CostRequest)

GetCostRequest = _reflection.GeneratedProtocolMessageType('GetCostRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCOSTREQUEST,
  '__module__' : 'spaceone.api.cost_analysis.v1.cost_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.GetCostRequest)
  })
_sym_db.RegisterMessage(GetCostRequest)

CostQuery = _reflection.GeneratedProtocolMessageType('CostQuery', (_message.Message,), {
  'DESCRIPTOR' : _COSTQUERY,
  '__module__' : 'spaceone.api.cost_analysis.v1.cost_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.CostQuery)
  })
_sym_db.RegisterMessage(CostQuery)

CostInfo = _reflection.GeneratedProtocolMessageType('CostInfo', (_message.Message,), {
  'DESCRIPTOR' : _COSTINFO,
  '__module__' : 'spaceone.api.cost_analysis.v1.cost_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.CostInfo)
  })
_sym_db.RegisterMessage(CostInfo)

CostsInfo = _reflection.GeneratedProtocolMessageType('CostsInfo', (_message.Message,), {
  'DESCRIPTOR' : _COSTSINFO,
  '__module__' : 'spaceone.api.cost_analysis.v1.cost_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.CostsInfo)
  })
_sym_db.RegisterMessage(CostsInfo)

CostAnalyzeQuery = _reflection.GeneratedProtocolMessageType('CostAnalyzeQuery', (_message.Message,), {
  'DESCRIPTOR' : _COSTANALYZEQUERY,
  '__module__' : 'spaceone.api.cost_analysis.v1.cost_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.CostAnalyzeQuery)
  })
_sym_db.RegisterMessage(CostAnalyzeQuery)

CostStatQuery = _reflection.GeneratedProtocolMessageType('CostStatQuery', (_message.Message,), {
  'DESCRIPTOR' : _COSTSTATQUERY,
  '__module__' : 'spaceone.api.cost_analysis.v1.cost_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.CostStatQuery)
  })
_sym_db.RegisterMessage(CostStatQuery)

_COST = DESCRIPTOR.services_by_name['Cost']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _COST.methods_by_name['create']._options = None
  _COST.methods_by_name['create']._serialized_options = b'\202\323\344\223\002\031\"\027/cost-analysis/v1/costs'
  _COST.methods_by_name['delete']._options = None
  _COST.methods_by_name['delete']._serialized_options = b'\202\323\344\223\002\"* /cost-analysis/v1/cost/{cost_id}'
  _COST.methods_by_name['get']._options = None
  _COST.methods_by_name['get']._serialized_options = b'\202\323\344\223\002\"\022 /cost-analysis/v1/cost/{cost_id}'
  _COST.methods_by_name['list']._options = None
  _COST.methods_by_name['list']._serialized_options = b'\202\323\344\223\002;\022\027/cost-analysis/v1/costsZ \"\036/cost-analysis/v1/costs/search'
  _COST.methods_by_name['analyze']._options = None
  _COST.methods_by_name['analyze']._serialized_options = b'\202\323\344\223\002!\"\037/cost-analysis/v1/costs/analyze'
  _COST.methods_by_name['stat']._options = None
  _COST.methods_by_name['stat']._serialized_options = b'\202\323\344\223\002\036\"\034/cost-analysis/v1/costs/stat'
  _CREATECOSTREQUEST._serialized_start=199
  _CREATECOSTREQUEST._serialized_end=662
  _COSTREQUEST._serialized_start=664
  _COSTREQUEST._serialized_end=713
  _GETCOSTREQUEST._serialized_start=715
  _GETCOSTREQUEST._serialized_end=781
  _COSTQUERY._serialized_start=784
  _COSTQUERY._serialized_end=1147
  _COSTINFO._serialized_start=1150
  _COSTINFO._serialized_end=1661
  _COSTSINFO._serialized_start=1663
  _COSTSINFO._serialized_end=1753
  _COSTANALYZEQUERY._serialized_start=1756
  _COSTANALYZEQUERY._serialized_end=2203
  _COSTANALYZEQUERY_GRANULARITY._serialized_start=2122
  _COSTANALYZEQUERY_GRANULARITY._serialized_end=2203
  _COSTSTATQUERY._serialized_start=2205
  _COSTSTATQUERY._serialized_end=2293
  _COST._serialized_start=2296
  _COST._serialized_end=3098
# @@protoc_insertion_point(module_scope)
