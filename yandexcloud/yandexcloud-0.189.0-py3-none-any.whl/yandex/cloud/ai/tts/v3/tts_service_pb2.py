# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/ai/tts/v3/tts_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from yandex.cloud.ai.tts.v3 import tts_pb2 as yandex_dot_cloud_dot_ai_dot_tts_dot_v3_dot_tts__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yandex/cloud/ai/tts/v3/tts_service.proto',
  package='speechkit.tts.v3',
  syntax='proto3',
  serialized_options=b'\n\032yandex.cloud.api.ai.tts.v3Z>github.com/yandex-cloud/go-genproto/yandex/cloud/ai/tts/v3;tts',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n(yandex/cloud/ai/tts/v3/tts_service.proto\x12\x10speechkit.tts.v3\x1a yandex/cloud/ai/tts/v3/tts.proto2\x82\x01\n\x0bSynthesizer\x12s\n\x12UtteranceSynthesis\x12+.speechkit.tts.v3.UtteranceSynthesisRequest\x1a,.speechkit.tts.v3.UtteranceSynthesisResponse\"\x00\x30\x01\x42\\\n\x1ayandex.cloud.api.ai.tts.v3Z>github.com/yandex-cloud/go-genproto/yandex/cloud/ai/tts/v3;ttsb\x06proto3'
  ,
  dependencies=[yandex_dot_cloud_dot_ai_dot_tts_dot_v3_dot_tts__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_SYNTHESIZER = _descriptor.ServiceDescriptor(
  name='Synthesizer',
  full_name='speechkit.tts.v3.Synthesizer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=97,
  serialized_end=227,
  methods=[
  _descriptor.MethodDescriptor(
    name='UtteranceSynthesis',
    full_name='speechkit.tts.v3.Synthesizer.UtteranceSynthesis',
    index=0,
    containing_service=None,
    input_type=yandex_dot_cloud_dot_ai_dot_tts_dot_v3_dot_tts__pb2._UTTERANCESYNTHESISREQUEST,
    output_type=yandex_dot_cloud_dot_ai_dot_tts_dot_v3_dot_tts__pb2._UTTERANCESYNTHESISRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SYNTHESIZER)

DESCRIPTOR.services_by_name['Synthesizer'] = _SYNTHESIZER

# @@protoc_insertion_point(module_scope)
