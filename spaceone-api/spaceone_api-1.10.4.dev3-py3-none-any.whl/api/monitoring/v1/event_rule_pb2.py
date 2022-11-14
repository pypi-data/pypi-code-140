# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/monitoring/v1/event_rule.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+spaceone/api/monitoring/v1/event_rule.proto\x12\x1aspaceone.api.monitoring.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"B\n\x12\x45ventRuleCondition\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x10\n\x08operator\x18\x03 \x01(\t\"F\n\x18\x45ventRuleActionResponder\x12\x15\n\rresource_type\x18\x01 \x01(\t\x12\x13\n\x0bresource_id\x18\x02 \x01(\t\"+\n\tMatchRule\x12\x0e\n\x06source\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\"\xdd\x02\n\x10\x45ventRuleActions\x12\x17\n\x0f\x63hange_assignee\x18\x01 \x01(\t\x12\x16\n\x0e\x63hange_urgency\x18\x02 \x01(\t\x12\x16\n\x0e\x63hange_project\x18\x03 \x01(\t\x12\x1e\n\x16\x61\x64\x64_project_dependency\x18\x04 \x03(\t\x12K\n\radd_responder\x18\x05 \x03(\x0b\x32\x34.spaceone.api.monitoring.v1.EventRuleActionResponder\x12\x44\n\x15match_service_account\x18\x06 \x01(\x0b\x32%.spaceone.api.monitoring.v1.MatchRule\x12\x34\n\x13\x61\x64\x64_additional_info\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x17\n\x0fno_notification\x18\x08 \x01(\x08\"+\n\x10\x45ventRuleOptions\x12\x17\n\x0fstop_processing\x18\x01 \x01(\x08\"\xd2\x03\n\x16\x43reateEventRuleRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x42\n\nconditions\x18\x02 \x03(\x0b\x32..spaceone.api.monitoring.v1.EventRuleCondition\x12^\n\x11\x63onditions_policy\x18\x03 \x01(\x0e\x32\x43.spaceone.api.monitoring.v1.CreateEventRuleRequest.ConditionsPolicy\x12=\n\x07\x61\x63tions\x18\x04 \x01(\x0b\x32,.spaceone.api.monitoring.v1.EventRuleActions\x12=\n\x07options\x18\x05 \x01(\x0b\x32,.spaceone.api.monitoring.v1.EventRuleOptions\x12\x12\n\nproject_id\x18\x06 \x01(\t\x12%\n\x04tags\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x0b \x01(\t\":\n\x10\x43onditionsPolicy\x12\x08\n\x04NONE\x10\x00\x12\x07\n\x03\x41LL\x10\x01\x12\x07\n\x03\x41NY\x10\x02\x12\n\n\x06\x41LWAYS\x10\x03\"\xd5\x03\n\x16UpdateEventRuleRequest\x12\x15\n\revent_rule_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x42\n\nconditions\x18\x03 \x03(\x0b\x32..spaceone.api.monitoring.v1.EventRuleCondition\x12^\n\x11\x63onditions_policy\x18\x04 \x01(\x0e\x32\x43.spaceone.api.monitoring.v1.UpdateEventRuleRequest.ConditionsPolicy\x12=\n\x07\x61\x63tions\x18\x05 \x01(\x0b\x32,.spaceone.api.monitoring.v1.EventRuleActions\x12=\n\x07options\x18\x06 \x01(\x0b\x32,.spaceone.api.monitoring.v1.EventRuleOptions\x12%\n\x04tags\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x0b \x01(\t\":\n\x10\x43onditionsPolicy\x12\x08\n\x04NONE\x10\x00\x12\x07\n\x03\x41LL\x10\x01\x12\x07\n\x03\x41NY\x10\x02\x12\n\n\x06\x41LWAYS\x10\x03\"V\n\x1b\x43hangeEventRuleOrderRequest\x12\x15\n\revent_rule_id\x18\x01 \x01(\t\x12\r\n\x05order\x18\x02 \x01(\x05\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"<\n\x10\x45ventRuleRequest\x12\x15\n\revent_rule_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"M\n\x13GetEventRuleRequest\x12\x15\n\revent_rule_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"\x8d\x02\n\x0e\x45ventRuleQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x15\n\revent_rule_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12H\n\x05scope\x18\x04 \x01(\x0e\x32\x39.spaceone.api.monitoring.v1.EventRuleQuery.EventRuleScope\x12\x12\n\nproject_id\x18\x05 \x01(\t\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"9\n\x0e\x45ventRuleScope\x12\x0e\n\nSCOPE_NONE\x10\x00\x12\n\n\x06GLOBAL\x10\x01\x12\x0b\n\x07PROJECT\x10\x02\"\xfe\x04\n\rEventRuleInfo\x12\x15\n\revent_rule_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05order\x18\x03 \x01(\x05\x12\x42\n\nconditions\x18\x04 \x03(\x0b\x32..spaceone.api.monitoring.v1.EventRuleCondition\x12U\n\x11\x63onditions_policy\x18\x05 \x01(\x0e\x32:.spaceone.api.monitoring.v1.EventRuleInfo.ConditionsPolicy\x12=\n\x07\x61\x63tions\x18\x06 \x01(\x0b\x32,.spaceone.api.monitoring.v1.EventRuleActions\x12=\n\x07options\x18\x07 \x01(\x0b\x32,.spaceone.api.monitoring.v1.EventRuleOptions\x12G\n\x05scope\x18\x08 \x01(\x0e\x32\x38.spaceone.api.monitoring.v1.EventRuleInfo.EventRuleScope\x12\x12\n\nproject_id\x18\t \x01(\t\x12%\n\x04tags\x18\n \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x0b \x01(\t\x12\x12\n\ncreated_at\x18\x15 \x01(\t\"9\n\x0e\x45ventRuleScope\x12\x0e\n\nSCOPE_NONE\x10\x00\x12\n\n\x06GLOBAL\x10\x01\x12\x0b\n\x07PROJECT\x10\x02\":\n\x10\x43onditionsPolicy\x12\x08\n\x04NONE\x10\x00\x12\x07\n\x03\x41LL\x10\x01\x12\x07\n\x03\x41NY\x10\x02\x12\n\n\x06\x41LWAYS\x10\x03\"a\n\x0e\x45ventRulesInfo\x12:\n\x07results\x18\x01 \x03(\x0b\x32).spaceone.api.monitoring.v1.EventRuleInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"]\n\x12\x45ventRuleStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\xa3\x08\n\tEventRule\x12\x8b\x01\n\x06\x63reate\x12\x32.spaceone.api.monitoring.v1.CreateEventRuleRequest\x1a).spaceone.api.monitoring.v1.EventRuleInfo\"\"\x82\xd3\xe4\x93\x02\x1c\"\x1a/monitoring/v1/event-rules\x12\x9a\x01\n\x06update\x12\x32.spaceone.api.monitoring.v1.UpdateEventRuleRequest\x1a).spaceone.api.monitoring.v1.EventRuleInfo\"1\x82\xd3\xe4\x93\x02+\x1a)/monitoring/v1/event-rule/{event_rule_id}\x12\xab\x01\n\x0c\x63hange_order\x12\x37.spaceone.api.monitoring.v1.ChangeEventRuleOrderRequest\x1a).spaceone.api.monitoring.v1.EventRuleInfo\"7\x82\xd3\xe4\x93\x02\x31\x1a//monitoring/v1/event-rule/{event_rule_id}/order\x12\x81\x01\n\x06\x64\x65lete\x12,.spaceone.api.monitoring.v1.EventRuleRequest\x1a\x16.google.protobuf.Empty\"1\x82\xd3\xe4\x93\x02+*)/monitoring/v1/event-rule/{event_rule_id}\x12\x94\x01\n\x03get\x12/.spaceone.api.monitoring.v1.GetEventRuleRequest\x1a).spaceone.api.monitoring.v1.EventRuleInfo\"1\x82\xd3\xe4\x93\x02+\x12)/monitoring/v1/event-rule/{event_rule_id}\x12\xa7\x01\n\x04list\x12*.spaceone.api.monitoring.v1.EventRuleQuery\x1a*.spaceone.api.monitoring.v1.EventRulesInfo\"G\x82\xd3\xe4\x93\x02\x41\x12\x1a/monitoring/v1/event-rulesZ#\"!/monitoring/v1/event-rules/search\x12x\n\x04stat\x12..spaceone.api.monitoring.v1.EventRuleStatQuery\x1a\x17.google.protobuf.Struct\"\'\x82\xd3\xe4\x93\x02!\"\x1f/monitoring/v1/event-rules/statb\x06proto3')



_EVENTRULECONDITION = DESCRIPTOR.message_types_by_name['EventRuleCondition']
_EVENTRULEACTIONRESPONDER = DESCRIPTOR.message_types_by_name['EventRuleActionResponder']
_MATCHRULE = DESCRIPTOR.message_types_by_name['MatchRule']
_EVENTRULEACTIONS = DESCRIPTOR.message_types_by_name['EventRuleActions']
_EVENTRULEOPTIONS = DESCRIPTOR.message_types_by_name['EventRuleOptions']
_CREATEEVENTRULEREQUEST = DESCRIPTOR.message_types_by_name['CreateEventRuleRequest']
_UPDATEEVENTRULEREQUEST = DESCRIPTOR.message_types_by_name['UpdateEventRuleRequest']
_CHANGEEVENTRULEORDERREQUEST = DESCRIPTOR.message_types_by_name['ChangeEventRuleOrderRequest']
_EVENTRULEREQUEST = DESCRIPTOR.message_types_by_name['EventRuleRequest']
_GETEVENTRULEREQUEST = DESCRIPTOR.message_types_by_name['GetEventRuleRequest']
_EVENTRULEQUERY = DESCRIPTOR.message_types_by_name['EventRuleQuery']
_EVENTRULEINFO = DESCRIPTOR.message_types_by_name['EventRuleInfo']
_EVENTRULESINFO = DESCRIPTOR.message_types_by_name['EventRulesInfo']
_EVENTRULESTATQUERY = DESCRIPTOR.message_types_by_name['EventRuleStatQuery']
_CREATEEVENTRULEREQUEST_CONDITIONSPOLICY = _CREATEEVENTRULEREQUEST.enum_types_by_name['ConditionsPolicy']
_UPDATEEVENTRULEREQUEST_CONDITIONSPOLICY = _UPDATEEVENTRULEREQUEST.enum_types_by_name['ConditionsPolicy']
_EVENTRULEQUERY_EVENTRULESCOPE = _EVENTRULEQUERY.enum_types_by_name['EventRuleScope']
_EVENTRULEINFO_EVENTRULESCOPE = _EVENTRULEINFO.enum_types_by_name['EventRuleScope']
_EVENTRULEINFO_CONDITIONSPOLICY = _EVENTRULEINFO.enum_types_by_name['ConditionsPolicy']
EventRuleCondition = _reflection.GeneratedProtocolMessageType('EventRuleCondition', (_message.Message,), {
  'DESCRIPTOR' : _EVENTRULECONDITION,
  '__module__' : 'spaceone.api.monitoring.v1.event_rule_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.EventRuleCondition)
  })
_sym_db.RegisterMessage(EventRuleCondition)

EventRuleActionResponder = _reflection.GeneratedProtocolMessageType('EventRuleActionResponder', (_message.Message,), {
  'DESCRIPTOR' : _EVENTRULEACTIONRESPONDER,
  '__module__' : 'spaceone.api.monitoring.v1.event_rule_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.EventRuleActionResponder)
  })
_sym_db.RegisterMessage(EventRuleActionResponder)

MatchRule = _reflection.GeneratedProtocolMessageType('MatchRule', (_message.Message,), {
  'DESCRIPTOR' : _MATCHRULE,
  '__module__' : 'spaceone.api.monitoring.v1.event_rule_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.MatchRule)
  })
_sym_db.RegisterMessage(MatchRule)

EventRuleActions = _reflection.GeneratedProtocolMessageType('EventRuleActions', (_message.Message,), {
  'DESCRIPTOR' : _EVENTRULEACTIONS,
  '__module__' : 'spaceone.api.monitoring.v1.event_rule_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.EventRuleActions)
  })
_sym_db.RegisterMessage(EventRuleActions)

EventRuleOptions = _reflection.GeneratedProtocolMessageType('EventRuleOptions', (_message.Message,), {
  'DESCRIPTOR' : _EVENTRULEOPTIONS,
  '__module__' : 'spaceone.api.monitoring.v1.event_rule_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.EventRuleOptions)
  })
_sym_db.RegisterMessage(EventRuleOptions)

CreateEventRuleRequest = _reflection.GeneratedProtocolMessageType('CreateEventRuleRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEEVENTRULEREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.event_rule_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.CreateEventRuleRequest)
  })
_sym_db.RegisterMessage(CreateEventRuleRequest)

UpdateEventRuleRequest = _reflection.GeneratedProtocolMessageType('UpdateEventRuleRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEEVENTRULEREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.event_rule_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.UpdateEventRuleRequest)
  })
_sym_db.RegisterMessage(UpdateEventRuleRequest)

ChangeEventRuleOrderRequest = _reflection.GeneratedProtocolMessageType('ChangeEventRuleOrderRequest', (_message.Message,), {
  'DESCRIPTOR' : _CHANGEEVENTRULEORDERREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.event_rule_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.ChangeEventRuleOrderRequest)
  })
_sym_db.RegisterMessage(ChangeEventRuleOrderRequest)

EventRuleRequest = _reflection.GeneratedProtocolMessageType('EventRuleRequest', (_message.Message,), {
  'DESCRIPTOR' : _EVENTRULEREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.event_rule_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.EventRuleRequest)
  })
_sym_db.RegisterMessage(EventRuleRequest)

GetEventRuleRequest = _reflection.GeneratedProtocolMessageType('GetEventRuleRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETEVENTRULEREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.event_rule_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.GetEventRuleRequest)
  })
_sym_db.RegisterMessage(GetEventRuleRequest)

EventRuleQuery = _reflection.GeneratedProtocolMessageType('EventRuleQuery', (_message.Message,), {
  'DESCRIPTOR' : _EVENTRULEQUERY,
  '__module__' : 'spaceone.api.monitoring.v1.event_rule_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.EventRuleQuery)
  })
_sym_db.RegisterMessage(EventRuleQuery)

EventRuleInfo = _reflection.GeneratedProtocolMessageType('EventRuleInfo', (_message.Message,), {
  'DESCRIPTOR' : _EVENTRULEINFO,
  '__module__' : 'spaceone.api.monitoring.v1.event_rule_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.EventRuleInfo)
  })
_sym_db.RegisterMessage(EventRuleInfo)

EventRulesInfo = _reflection.GeneratedProtocolMessageType('EventRulesInfo', (_message.Message,), {
  'DESCRIPTOR' : _EVENTRULESINFO,
  '__module__' : 'spaceone.api.monitoring.v1.event_rule_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.EventRulesInfo)
  })
_sym_db.RegisterMessage(EventRulesInfo)

EventRuleStatQuery = _reflection.GeneratedProtocolMessageType('EventRuleStatQuery', (_message.Message,), {
  'DESCRIPTOR' : _EVENTRULESTATQUERY,
  '__module__' : 'spaceone.api.monitoring.v1.event_rule_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.EventRuleStatQuery)
  })
_sym_db.RegisterMessage(EventRuleStatQuery)

_EVENTRULE = DESCRIPTOR.services_by_name['EventRule']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EVENTRULE.methods_by_name['create']._options = None
  _EVENTRULE.methods_by_name['create']._serialized_options = b'\202\323\344\223\002\034\"\032/monitoring/v1/event-rules'
  _EVENTRULE.methods_by_name['update']._options = None
  _EVENTRULE.methods_by_name['update']._serialized_options = b'\202\323\344\223\002+\032)/monitoring/v1/event-rule/{event_rule_id}'
  _EVENTRULE.methods_by_name['change_order']._options = None
  _EVENTRULE.methods_by_name['change_order']._serialized_options = b'\202\323\344\223\0021\032//monitoring/v1/event-rule/{event_rule_id}/order'
  _EVENTRULE.methods_by_name['delete']._options = None
  _EVENTRULE.methods_by_name['delete']._serialized_options = b'\202\323\344\223\002+*)/monitoring/v1/event-rule/{event_rule_id}'
  _EVENTRULE.methods_by_name['get']._options = None
  _EVENTRULE.methods_by_name['get']._serialized_options = b'\202\323\344\223\002+\022)/monitoring/v1/event-rule/{event_rule_id}'
  _EVENTRULE.methods_by_name['list']._options = None
  _EVENTRULE.methods_by_name['list']._serialized_options = b'\202\323\344\223\002A\022\032/monitoring/v1/event-rulesZ#\"!/monitoring/v1/event-rules/search'
  _EVENTRULE.methods_by_name['stat']._options = None
  _EVENTRULE.methods_by_name['stat']._serialized_options = b'\202\323\344\223\002!\"\037/monitoring/v1/event-rules/stat'
  _EVENTRULECONDITION._serialized_start=198
  _EVENTRULECONDITION._serialized_end=264
  _EVENTRULEACTIONRESPONDER._serialized_start=266
  _EVENTRULEACTIONRESPONDER._serialized_end=336
  _MATCHRULE._serialized_start=338
  _MATCHRULE._serialized_end=381
  _EVENTRULEACTIONS._serialized_start=384
  _EVENTRULEACTIONS._serialized_end=733
  _EVENTRULEOPTIONS._serialized_start=735
  _EVENTRULEOPTIONS._serialized_end=778
  _CREATEEVENTRULEREQUEST._serialized_start=781
  _CREATEEVENTRULEREQUEST._serialized_end=1247
  _CREATEEVENTRULEREQUEST_CONDITIONSPOLICY._serialized_start=1189
  _CREATEEVENTRULEREQUEST_CONDITIONSPOLICY._serialized_end=1247
  _UPDATEEVENTRULEREQUEST._serialized_start=1250
  _UPDATEEVENTRULEREQUEST._serialized_end=1719
  _UPDATEEVENTRULEREQUEST_CONDITIONSPOLICY._serialized_start=1189
  _UPDATEEVENTRULEREQUEST_CONDITIONSPOLICY._serialized_end=1247
  _CHANGEEVENTRULEORDERREQUEST._serialized_start=1721
  _CHANGEEVENTRULEORDERREQUEST._serialized_end=1807
  _EVENTRULEREQUEST._serialized_start=1809
  _EVENTRULEREQUEST._serialized_end=1869
  _GETEVENTRULEREQUEST._serialized_start=1871
  _GETEVENTRULEREQUEST._serialized_end=1948
  _EVENTRULEQUERY._serialized_start=1951
  _EVENTRULEQUERY._serialized_end=2220
  _EVENTRULEQUERY_EVENTRULESCOPE._serialized_start=2163
  _EVENTRULEQUERY_EVENTRULESCOPE._serialized_end=2220
  _EVENTRULEINFO._serialized_start=2223
  _EVENTRULEINFO._serialized_end=2861
  _EVENTRULEINFO_EVENTRULESCOPE._serialized_start=2163
  _EVENTRULEINFO_EVENTRULESCOPE._serialized_end=2220
  _EVENTRULEINFO_CONDITIONSPOLICY._serialized_start=1189
  _EVENTRULEINFO_CONDITIONSPOLICY._serialized_end=1247
  _EVENTRULESINFO._serialized_start=2863
  _EVENTRULESINFO._serialized_end=2960
  _EVENTRULESTATQUERY._serialized_start=2962
  _EVENTRULESTATQUERY._serialized_end=3055
  _EVENTRULE._serialized_start=3058
  _EVENTRULE._serialized_end=4117
# @@protoc_insertion_point(module_scope)
