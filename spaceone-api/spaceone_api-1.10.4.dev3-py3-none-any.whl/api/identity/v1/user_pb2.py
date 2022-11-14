# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/identity/v1/user.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#spaceone/api/identity/v1/user.proto\x12\x18spaceone.api.identity.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"\xa0\x02\n\x11\x43reateUserRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\r\n\x05\x65mail\x18\x04 \x01(\t\x12\x35\n\tuser_type\x18\x05 \x01(\x0e\x32\".spaceone.api.identity.v1.UserType\x12\x36\n\x07\x62\x61\x63kend\x18\x06 \x01(\x0e\x32%.spaceone.api.identity.v1.UserBackend\x12\x10\n\x08language\x18\x07 \x01(\t\x12\x10\n\x08timezone\x18\x08 \x01(\t\x12%\n\x04tags\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\n \x01(\t\"\xb1\x01\n\x11UpdateUserRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\r\n\x05\x65mail\x18\x04 \x01(\t\x12\x10\n\x08language\x18\x07 \x01(\t\x12\x10\n\x08timezone\x18\x08 \x01(\t\x12%\n\x04tags\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\n \x01(\t\"~\n\x19SetRequiredActionsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12=\n\x07\x61\x63tions\x18\x02 \x03(\x0e\x32,.spaceone.api.identity.v1.UserRequiredAction\x12\x11\n\tdomain_id\x18\x03 \x01(\t\"1\n\x0bUserRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"B\n\x0eGetUserRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"\xf6\x01\n\tUserQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\r\n\x05state\x18\x04 \x01(\t\x12\r\n\x05\x65mail\x18\x05 \x01(\t\x12\x35\n\tuser_type\x18\x06 \x01(\x0e\x32\".spaceone.api.identity.v1.UserType\x12\x36\n\x07\x62\x61\x63kend\x18\x07 \x01(\x0e\x32%.spaceone.api.identity.v1.UserBackend\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"\xef\x03\n\x08UserInfo\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x37\n\x05state\x18\x03 \x01(\x0e\x32(.spaceone.api.identity.v1.UserInfo.State\x12\r\n\x05\x65mail\x18\x04 \x01(\t\x12\x35\n\tuser_type\x18\x05 \x01(\x0e\x32\".spaceone.api.identity.v1.UserType\x12\x36\n\x07\x62\x61\x63kend\x18\x06 \x01(\x0e\x32%.spaceone.api.identity.v1.UserBackend\x12\x10\n\x08language\x18\x07 \x01(\t\x12\x10\n\x08timezone\x18\x08 \x01(\t\x12\x46\n\x10required_actions\x18\t \x03(\x0e\x32,.spaceone.api.identity.v1.UserRequiredAction\x12%\n\x04tags\x18\n \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x18\n\x10last_accessed_at\x18\x0b \x01(\t\x12\x12\n\ncreated_at\x18\x0c \x01(\t\x12\x11\n\tdomain_id\x18\r \x01(\t\"9\n\x05State\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x0c\n\x08\x44ISABLED\x10\x02\x12\x0b\n\x07PENDING\x10\x03\"U\n\tUsersInfo\x12\x33\n\x07results\x18\x01 \x03(\x0b\x32\".spaceone.api.identity.v1.UserInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"X\n\rUserStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"F\n\x0e\x46indUserSearch\x12\x11\n\x07user_id\x18\x01 \x01(\tH\x00\x12\x11\n\x07keyword\x18\x02 \x01(\tH\x00\x42\x0e\n\x0csearch_alias\"\\\n\rFindUserQuery\x12\x38\n\x06search\x18\x01 \x01(\x0b\x32(.spaceone.api.identity.v1.FindUserSearch\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"c\n\x0c\x46indUserInfo\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12%\n\x04tags\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\"]\n\rFindUsersInfo\x12\x37\n\x07results\x18\x01 \x03(\x0b\x32&.spaceone.api.identity.v1.FindUserInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05*8\n\x0bUserBackend\x12\x10\n\x0cNONE_BACKEND\x10\x00\x12\t\n\x05LOCAL\x10\x01\x12\x0c\n\x08\x45XTERNAL\x10\x02*6\n\x08UserType\x12\x12\n\x0eNONE_USER_TYPE\x10\x00\x12\x08\n\x04USER\x10\x01\x12\x0c\n\x08\x41PI_USER\x10\x02*)\n\x12UserRequiredAction\x12\x13\n\x0fUPDATE_PASSWORD\x10\x00\x32\xe1\n\n\x04User\x12u\n\x06\x63reate\x12+.spaceone.api.identity.v1.CreateUserRequest\x1a\".spaceone.api.identity.v1.UserInfo\"\x1a\x82\xd3\xe4\x93\x02\x14\"\x12/identity/v1/users\x12u\n\x06update\x12+.spaceone.api.identity.v1.UpdateUserRequest\x1a\".spaceone.api.identity.v1.UserInfo\"\x1a\x82\xd3\xe4\x93\x02\x14\x1a\x12/identity/v1/users\x12\xa0\x01\n\x14set_required_actions\x12\x33.spaceone.api.identity.v1.SetRequiredActionsRequest\x1a\".spaceone.api.identity.v1.UserInfo\"/\x82\xd3\xe4\x93\x02)\"\'/identity/v1/users/set-required-actions\x12\x7f\n\x06\x65nable\x12%.spaceone.api.identity.v1.UserRequest\x1a\".spaceone.api.identity.v1.UserInfo\"*\x82\xd3\xe4\x93\x02$\x1a\"/identity/v1/user/{user_id}/enable\x12\x81\x01\n\x07\x64isable\x12%.spaceone.api.identity.v1.UserRequest\x1a\".spaceone.api.identity.v1.UserInfo\"+\x82\xd3\xe4\x93\x02%\x1a#/identity/v1/user/{user_id}/disable\x12\x63\n\x06\x64\x65lete\x12%.spaceone.api.identity.v1.UserRequest\x1a\x16.google.protobuf.Empty\"\x1a\x82\xd3\xe4\x93\x02\x14*\x12/identity/v1/users\x12x\n\x03get\x12(.spaceone.api.identity.v1.GetUserRequest\x1a\".spaceone.api.identity.v1.UserInfo\"#\x82\xd3\xe4\x93\x02\x1d\x12\x1b/identity/v1/user/{user_id}\x12\x89\x01\n\x04list\x12#.spaceone.api.identity.v1.UserQuery\x1a#.spaceone.api.identity.v1.UsersInfo\"7\x82\xd3\xe4\x93\x02\x31\x12\x12/identity/v1/usersZ\x1b\"\x19/identity/v1/users/search\x12i\n\x04stat\x12\'.spaceone.api.identity.v1.UserStatQuery\x1a\x17.google.protobuf.Struct\"\x1f\x82\xd3\xe4\x93\x02\x19\"\x17/identity/v1/users/stat\x12y\n\x04\x66ind\x12\'.spaceone.api.identity.v1.FindUserQuery\x1a\'.spaceone.api.identity.v1.FindUsersInfo\"\x1f\x82\xd3\xe4\x93\x02\x19\"\x17/identity/v1/users/find\x12r\n\x04sync\x12%.spaceone.api.identity.v1.UserRequest\x1a\".spaceone.api.identity.v1.UserInfo\"\x1f\x82\xd3\xe4\x93\x02\x19\"\x17/identity/v1/users/syncb\x06proto3')

_USERBACKEND = DESCRIPTOR.enum_types_by_name['UserBackend']
UserBackend = enum_type_wrapper.EnumTypeWrapper(_USERBACKEND)
_USERTYPE = DESCRIPTOR.enum_types_by_name['UserType']
UserType = enum_type_wrapper.EnumTypeWrapper(_USERTYPE)
_USERREQUIREDACTION = DESCRIPTOR.enum_types_by_name['UserRequiredAction']
UserRequiredAction = enum_type_wrapper.EnumTypeWrapper(_USERREQUIREDACTION)
NONE_BACKEND = 0
LOCAL = 1
EXTERNAL = 2
NONE_USER_TYPE = 0
USER = 1
API_USER = 2
UPDATE_PASSWORD = 0


_CREATEUSERREQUEST = DESCRIPTOR.message_types_by_name['CreateUserRequest']
_UPDATEUSERREQUEST = DESCRIPTOR.message_types_by_name['UpdateUserRequest']
_SETREQUIREDACTIONSREQUEST = DESCRIPTOR.message_types_by_name['SetRequiredActionsRequest']
_USERREQUEST = DESCRIPTOR.message_types_by_name['UserRequest']
_GETUSERREQUEST = DESCRIPTOR.message_types_by_name['GetUserRequest']
_USERQUERY = DESCRIPTOR.message_types_by_name['UserQuery']
_USERINFO = DESCRIPTOR.message_types_by_name['UserInfo']
_USERSINFO = DESCRIPTOR.message_types_by_name['UsersInfo']
_USERSTATQUERY = DESCRIPTOR.message_types_by_name['UserStatQuery']
_FINDUSERSEARCH = DESCRIPTOR.message_types_by_name['FindUserSearch']
_FINDUSERQUERY = DESCRIPTOR.message_types_by_name['FindUserQuery']
_FINDUSERINFO = DESCRIPTOR.message_types_by_name['FindUserInfo']
_FINDUSERSINFO = DESCRIPTOR.message_types_by_name['FindUsersInfo']
_USERINFO_STATE = _USERINFO.enum_types_by_name['State']
CreateUserRequest = _reflection.GeneratedProtocolMessageType('CreateUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEUSERREQUEST,
  '__module__' : 'spaceone.api.identity.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.v1.CreateUserRequest)
  })
_sym_db.RegisterMessage(CreateUserRequest)

UpdateUserRequest = _reflection.GeneratedProtocolMessageType('UpdateUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEUSERREQUEST,
  '__module__' : 'spaceone.api.identity.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.v1.UpdateUserRequest)
  })
_sym_db.RegisterMessage(UpdateUserRequest)

SetRequiredActionsRequest = _reflection.GeneratedProtocolMessageType('SetRequiredActionsRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETREQUIREDACTIONSREQUEST,
  '__module__' : 'spaceone.api.identity.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.v1.SetRequiredActionsRequest)
  })
_sym_db.RegisterMessage(SetRequiredActionsRequest)

UserRequest = _reflection.GeneratedProtocolMessageType('UserRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERREQUEST,
  '__module__' : 'spaceone.api.identity.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.v1.UserRequest)
  })
_sym_db.RegisterMessage(UserRequest)

GetUserRequest = _reflection.GeneratedProtocolMessageType('GetUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERREQUEST,
  '__module__' : 'spaceone.api.identity.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.v1.GetUserRequest)
  })
_sym_db.RegisterMessage(GetUserRequest)

UserQuery = _reflection.GeneratedProtocolMessageType('UserQuery', (_message.Message,), {
  'DESCRIPTOR' : _USERQUERY,
  '__module__' : 'spaceone.api.identity.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.v1.UserQuery)
  })
_sym_db.RegisterMessage(UserQuery)

UserInfo = _reflection.GeneratedProtocolMessageType('UserInfo', (_message.Message,), {
  'DESCRIPTOR' : _USERINFO,
  '__module__' : 'spaceone.api.identity.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.v1.UserInfo)
  })
_sym_db.RegisterMessage(UserInfo)

UsersInfo = _reflection.GeneratedProtocolMessageType('UsersInfo', (_message.Message,), {
  'DESCRIPTOR' : _USERSINFO,
  '__module__' : 'spaceone.api.identity.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.v1.UsersInfo)
  })
_sym_db.RegisterMessage(UsersInfo)

UserStatQuery = _reflection.GeneratedProtocolMessageType('UserStatQuery', (_message.Message,), {
  'DESCRIPTOR' : _USERSTATQUERY,
  '__module__' : 'spaceone.api.identity.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.v1.UserStatQuery)
  })
_sym_db.RegisterMessage(UserStatQuery)

FindUserSearch = _reflection.GeneratedProtocolMessageType('FindUserSearch', (_message.Message,), {
  'DESCRIPTOR' : _FINDUSERSEARCH,
  '__module__' : 'spaceone.api.identity.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.v1.FindUserSearch)
  })
_sym_db.RegisterMessage(FindUserSearch)

FindUserQuery = _reflection.GeneratedProtocolMessageType('FindUserQuery', (_message.Message,), {
  'DESCRIPTOR' : _FINDUSERQUERY,
  '__module__' : 'spaceone.api.identity.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.v1.FindUserQuery)
  })
_sym_db.RegisterMessage(FindUserQuery)

FindUserInfo = _reflection.GeneratedProtocolMessageType('FindUserInfo', (_message.Message,), {
  'DESCRIPTOR' : _FINDUSERINFO,
  '__module__' : 'spaceone.api.identity.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.v1.FindUserInfo)
  })
_sym_db.RegisterMessage(FindUserInfo)

FindUsersInfo = _reflection.GeneratedProtocolMessageType('FindUsersInfo', (_message.Message,), {
  'DESCRIPTOR' : _FINDUSERSINFO,
  '__module__' : 'spaceone.api.identity.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.identity.v1.FindUsersInfo)
  })
_sym_db.RegisterMessage(FindUsersInfo)

_USER = DESCRIPTOR.services_by_name['User']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USER.methods_by_name['create']._options = None
  _USER.methods_by_name['create']._serialized_options = b'\202\323\344\223\002\024\"\022/identity/v1/users'
  _USER.methods_by_name['update']._options = None
  _USER.methods_by_name['update']._serialized_options = b'\202\323\344\223\002\024\032\022/identity/v1/users'
  _USER.methods_by_name['set_required_actions']._options = None
  _USER.methods_by_name['set_required_actions']._serialized_options = b'\202\323\344\223\002)\"\'/identity/v1/users/set-required-actions'
  _USER.methods_by_name['enable']._options = None
  _USER.methods_by_name['enable']._serialized_options = b'\202\323\344\223\002$\032\"/identity/v1/user/{user_id}/enable'
  _USER.methods_by_name['disable']._options = None
  _USER.methods_by_name['disable']._serialized_options = b'\202\323\344\223\002%\032#/identity/v1/user/{user_id}/disable'
  _USER.methods_by_name['delete']._options = None
  _USER.methods_by_name['delete']._serialized_options = b'\202\323\344\223\002\024*\022/identity/v1/users'
  _USER.methods_by_name['get']._options = None
  _USER.methods_by_name['get']._serialized_options = b'\202\323\344\223\002\035\022\033/identity/v1/user/{user_id}'
  _USER.methods_by_name['list']._options = None
  _USER.methods_by_name['list']._serialized_options = b'\202\323\344\223\0021\022\022/identity/v1/usersZ\033\"\031/identity/v1/users/search'
  _USER.methods_by_name['stat']._options = None
  _USER.methods_by_name['stat']._serialized_options = b'\202\323\344\223\002\031\"\027/identity/v1/users/stat'
  _USER.methods_by_name['find']._options = None
  _USER.methods_by_name['find']._serialized_options = b'\202\323\344\223\002\031\"\027/identity/v1/users/find'
  _USER.methods_by_name['sync']._options = None
  _USER.methods_by_name['sync']._serialized_options = b'\202\323\344\223\002\031\"\027/identity/v1/users/sync'
  _USERBACKEND._serialized_start=2192
  _USERBACKEND._serialized_end=2248
  _USERTYPE._serialized_start=2250
  _USERTYPE._serialized_end=2304
  _USERREQUIREDACTION._serialized_start=2306
  _USERREQUIREDACTION._serialized_end=2347
  _CREATEUSERREQUEST._serialized_start=189
  _CREATEUSERREQUEST._serialized_end=477
  _UPDATEUSERREQUEST._serialized_start=480
  _UPDATEUSERREQUEST._serialized_end=657
  _SETREQUIREDACTIONSREQUEST._serialized_start=659
  _SETREQUIREDACTIONSREQUEST._serialized_end=785
  _USERREQUEST._serialized_start=787
  _USERREQUEST._serialized_end=836
  _GETUSERREQUEST._serialized_start=838
  _GETUSERREQUEST._serialized_end=904
  _USERQUERY._serialized_start=907
  _USERQUERY._serialized_end=1153
  _USERINFO._serialized_start=1156
  _USERINFO._serialized_end=1651
  _USERINFO_STATE._serialized_start=1594
  _USERINFO_STATE._serialized_end=1651
  _USERSINFO._serialized_start=1653
  _USERSINFO._serialized_end=1738
  _USERSTATQUERY._serialized_start=1740
  _USERSTATQUERY._serialized_end=1828
  _FINDUSERSEARCH._serialized_start=1830
  _FINDUSERSEARCH._serialized_end=1900
  _FINDUSERQUERY._serialized_start=1902
  _FINDUSERQUERY._serialized_end=1994
  _FINDUSERINFO._serialized_start=1996
  _FINDUSERINFO._serialized_end=2095
  _FINDUSERSINFO._serialized_start=2097
  _FINDUSERSINFO._serialized_end=2190
  _USER._serialized_start=2350
  _USER._serialized_end=3727
# @@protoc_insertion_point(module_scope)
