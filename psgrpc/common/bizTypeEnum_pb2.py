# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bizTypeEnum.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='bizTypeEnum.proto',
  package='common',
  syntax='proto3',
  serialized_options=b'\n\036com.megvii.lbg.wes.grpc.commonZDgit-pd.megvii-inc.com/slg-service/frworkstation/internal/grpc/common',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11\x62izTypeEnum.proto\x12\x06\x63ommon*!\n\x0b\x42izTypeEnum\x12\x12\n\x0e\x42izTypeUNKNOWN\x10\x00\x42\x66\n\x1e\x63om.megvii.lbg.wes.grpc.commonZDgit-pd.megvii-inc.com/slg-service/frworkstation/internal/grpc/commonb\x06proto3'
)

_BIZTYPEENUM = _descriptor.EnumDescriptor(
  name='BizTypeEnum',
  full_name='common.BizTypeEnum',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BizTypeUNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=29,
  serialized_end=62,
)
_sym_db.RegisterEnumDescriptor(_BIZTYPEENUM)

BizTypeEnum = enum_type_wrapper.EnumTypeWrapper(_BIZTYPEENUM)
BizTypeUNKNOWN = 0


DESCRIPTOR.enum_types_by_name['BizTypeEnum'] = _BIZTYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
