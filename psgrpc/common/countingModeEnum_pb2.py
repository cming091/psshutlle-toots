# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: countingModeEnum.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='countingModeEnum.proto',
  package='common',
  syntax='proto3',
  serialized_options=b'\n\036com.megvii.lbg.wes.grpc.commonZDgit-pd.megvii-inc.com/slg-service/frworkstation/internal/grpc/common',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16\x63ountingModeEnum.proto\x12\x06\x63ommon*S\n\x10\x43ountingModeEnum\x12\x17\n\x13\x43ountingModeUNKNOWN\x10\x00\x12\x12\n\x0e\x43ountingMode_1\x10\x01\x12\x12\n\x0e\x43ountingMode_2\x10\x02\x42\x66\n\x1e\x63om.megvii.lbg.wes.grpc.commonZDgit-pd.megvii-inc.com/slg-service/frworkstation/internal/grpc/commonb\x06proto3'
)

_COUNTINGMODEENUM = _descriptor.EnumDescriptor(
  name='CountingModeEnum',
  full_name='common.CountingModeEnum',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CountingModeUNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CountingMode_1', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CountingMode_2', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=34,
  serialized_end=117,
)
_sym_db.RegisterEnumDescriptor(_COUNTINGMODEENUM)

CountingModeEnum = enum_type_wrapper.EnumTypeWrapper(_COUNTINGMODEENUM)
CountingModeUNKNOWN = 0
CountingMode_1 = 1
CountingMode_2 = 2


DESCRIPTOR.enum_types_by_name['CountingModeEnum'] = _COUNTINGMODEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)