# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: token.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0btoken.proto\x12\x0c\x62\x61tchx.token\x1a\x0c\x63ommon.proto\"Z\n\x0f\x41\x64\x64TokenRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0c\n\x04host\x18\x02 \x01(\t\x12\r\n\x05token\x18\x03 \x01(\t\x12\x15\n\rts_expiration\x18\x04 \x01(\x03\"\x12\n\x10\x41\x64\x64TokenResponse2l\n\x0cTokenService\x12N\n\x08\x41\x64\x64Token\x12\x1d.batchx.token.AddTokenRequest\x1a\x1e.batchx.token.AddTokenResponse\"\x03\x90\x02\x02\x1a\x0c\x82\x97\"\x02\x08\n\x82\x97\"\x02\x10\x02\x42\x1d\n\x0fio.batchx.protoB\nTokenProtob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'token_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017io.batchx.protoB\nTokenProto'
  _TOKENSERVICE._options = None
  _TOKENSERVICE._serialized_options = b'\202\227\"\002\010\n\202\227\"\002\020\002'
  _TOKENSERVICE.methods_by_name['AddToken']._options = None
  _TOKENSERVICE.methods_by_name['AddToken']._serialized_options = b'\220\002\002'
  _ADDTOKENREQUEST._serialized_start=43
  _ADDTOKENREQUEST._serialized_end=133
  _ADDTOKENRESPONSE._serialized_start=135
  _ADDTOKENRESPONSE._serialized_end=153
  _TOKENSERVICE._serialized_start=155
  _TOKENSERVICE._serialized_end=263
# @@protoc_insertion_point(module_scope)
