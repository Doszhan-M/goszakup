# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eds.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\teds.proto\x12\x03\x65\x64s\x1a\x1egoogle/protobuf/wrappers.proto\"\x17\n\x15\x45\x64sManagerStatusCheck\"4\n\x0eSignByEdsStart\x12\x10\n\x08\x65\x64s_path\x18\x01 \x01(\t\x12\x10\n\x08\x65\x64s_pass\x18\x02 \x01(\t\"\x0f\n\rRestartParams\"<\n\x10\x45\x64sManagerStatus\x12(\n\x04\x62usy\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\"=\n\x0fSignByEdsResult\x12*\n\x06result\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\";\n\rRestartResult\x12*\n\x06result\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.BoolValue2\xc9\x01\n\nEdsService\x12\x41\n\nSendStatus\x12\x1a.eds.EdsManagerStatusCheck\x1a\x15.eds.EdsManagerStatus0\x01\x12=\n\x10\x45xecuteSignByEds\x12\x13.eds.SignByEdsStart\x1a\x14.eds.SignByEdsResult\x12\x39\n\x0fRestartNCALayer\x12\x12.eds.RestartParams\x1a\x12.eds.RestartResultb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eds_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EDSMANAGERSTATUSCHECK']._serialized_start=50
  _globals['_EDSMANAGERSTATUSCHECK']._serialized_end=73
  _globals['_SIGNBYEDSSTART']._serialized_start=75
  _globals['_SIGNBYEDSSTART']._serialized_end=127
  _globals['_RESTARTPARAMS']._serialized_start=129
  _globals['_RESTARTPARAMS']._serialized_end=144
  _globals['_EDSMANAGERSTATUS']._serialized_start=146
  _globals['_EDSMANAGERSTATUS']._serialized_end=206
  _globals['_SIGNBYEDSRESULT']._serialized_start=208
  _globals['_SIGNBYEDSRESULT']._serialized_end=269
  _globals['_RESTARTRESULT']._serialized_start=271
  _globals['_RESTARTRESULT']._serialized_end=330
  _globals['_EDSSERVICE']._serialized_start=333
  _globals['_EDSSERVICE']._serialized_end=534
# @@protoc_insertion_point(module_scope)
