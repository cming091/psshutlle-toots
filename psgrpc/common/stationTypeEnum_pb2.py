# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: stationTypeEnum.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='stationTypeEnum.proto',
  package='common',
  syntax='proto3',
  serialized_options=b'\n\036com.megvii.lbg.wes.grpc.commonZDgit-pd.megvii-inc.com/slg-service/frworkstation/internal/grpc/common',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x15stationTypeEnum.proto\x12\x06\x63ommon*\x82\x01\n\x0fStationTypeEnum\x12\x16\n\x12StationTypeUnknown\x10\x00\x12\x14\n\x10StationTypeHuman\x10\x01\x12\x12\n\x0eStationTypeARM\x10\x02\x12\x15\n\x11StationTypeDevice\x10\x03\x12\x16\n\x12StationTypeVirtual\x10\x63\x42\x66\n\x1e\x63om.megvii.lbg.wes.grpc.commonZDgit-pd.megvii-inc.com/slg-service/frworkstation/internal/grpc/commonb\x06proto3'
)

_STATIONTYPEENUM = _descriptor.EnumDescriptor(
  name='StationTypeEnum',
  full_name='common.StationTypeEnum',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='StationTypeUnknown', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='StationTypeHuman', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='StationTypeARM', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='StationTypeDevice', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='StationTypeVirtual', index=4, number=99,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=34,
  serialized_end=164,
)
_sym_db.RegisterEnumDescriptor(_STATIONTYPEENUM)

StationTypeEnum = enum_type_wrapper.EnumTypeWrapper(_STATIONTYPEENUM)
StationTypeUnknown = 0
StationTypeHuman = 1
StationTypeARM = 2
StationTypeDevice = 3
StationTypeVirtual = 99


DESCRIPTOR.enum_types_by_name['StationTypeEnum'] = _STATIONTYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
