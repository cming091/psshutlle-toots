# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tesDeviceStatusEnum.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tesDeviceStatusEnum.proto',
  package='common',
  syntax='proto3',
  serialized_options=b'\n\036com.megvii.lbg.wes.grpc.commonZDgit-pd.megvii-inc.com/slg-service/frworkstation/internal/grpc/common',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x19tesDeviceStatusEnum.proto\x12\x06\x63ommon*\x92\x01\n\x13TesDeviceStatusEnum\x12\x14\n\x10\x44\x65viceStatusTODO\x10\x00\x12\x1a\n\x16\x44\x65viceStatusPROCESSING\x10\x03\x12\x17\n\x13\x44\x65viceStatusSUCCESS\x10\x64\x12\x16\n\x12\x44\x65viceStatusFAILED\x10\x65\x12\x18\n\x14\x44\x65viceStatusCANCELED\x10\x66\x42\x66\n\x1e\x63om.megvii.lbg.wes.grpc.commonZDgit-pd.megvii-inc.com/slg-service/frworkstation/internal/grpc/commonb\x06proto3'
)

_TESDEVICESTATUSENUM = _descriptor.EnumDescriptor(
  name='TesDeviceStatusEnum',
  full_name='common.TesDeviceStatusEnum',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DeviceStatusTODO', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DeviceStatusPROCESSING', index=1, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DeviceStatusSUCCESS', index=2, number=100,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DeviceStatusFAILED', index=3, number=101,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DeviceStatusCANCELED', index=4, number=102,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=38,
  serialized_end=184,
)
_sym_db.RegisterEnumDescriptor(_TESDEVICESTATUSENUM)

TesDeviceStatusEnum = enum_type_wrapper.EnumTypeWrapper(_TESDEVICESTATUSENUM)
DeviceStatusTODO = 0
DeviceStatusPROCESSING = 3
DeviceStatusSUCCESS = 100
DeviceStatusFAILED = 101
DeviceStatusCANCELED = 102


DESCRIPTOR.enum_types_by_name['TesDeviceStatusEnum'] = _TESDEVICESTATUSENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)