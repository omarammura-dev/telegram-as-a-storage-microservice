# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: telegram-as-storage.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'telegram-as-storage.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19telegram-as-storage.proto\x12\x07storage\"7\n\x11UploadFileRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x10\n\x08\x66ileData\x18\x02 \x01(\t\"$\n\x12UploadFileResponse\x12\x0e\n\x06\x66ileId\x18\x01 \x01(\t\"2\n\x0eGetFileRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0e\n\x06\x66ileId\x18\x02 \x01(\t\"#\n\x11\x44\x65leteFileRequest\x12\x0e\n\x06\x66ileId\x18\x01 \x01(\t\"\x1f\n\x0fGetFileResponse\x12\x0c\n\x04\x66ile\x18\x01 \x01(\t\" \n\x12\x44\x65leteFileResponse\x12\n\n\x02ok\x18\x01 \x01(\x08\x32\xd5\x01\n\x07Storage\x12\x45\n\nUploadFile\x12\x1a.storage.UploadFileRequest\x1a\x1b.storage.UploadFileResponse\x12<\n\x07GetFile\x12\x17.storage.GetFileRequest\x1a\x18.storage.GetFileResponse\x12\x45\n\nDeleteFile\x12\x1a.storage.DeleteFileRequest\x1a\x1b.storage.DeleteFileResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'telegram_as_storage_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_UPLOADFILEREQUEST']._serialized_start=38
  _globals['_UPLOADFILEREQUEST']._serialized_end=93
  _globals['_UPLOADFILERESPONSE']._serialized_start=95
  _globals['_UPLOADFILERESPONSE']._serialized_end=131
  _globals['_GETFILEREQUEST']._serialized_start=133
  _globals['_GETFILEREQUEST']._serialized_end=183
  _globals['_DELETEFILEREQUEST']._serialized_start=185
  _globals['_DELETEFILEREQUEST']._serialized_end=220
  _globals['_GETFILERESPONSE']._serialized_start=222
  _globals['_GETFILERESPONSE']._serialized_end=253
  _globals['_DELETEFILERESPONSE']._serialized_start=255
  _globals['_DELETEFILERESPONSE']._serialized_end=287
  _globals['_STORAGE']._serialized_start=290
  _globals['_STORAGE']._serialized_end=503
# @@protoc_insertion_point(module_scope)
