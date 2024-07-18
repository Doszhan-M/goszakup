from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SignByEdsStart(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    def __init__(self, type: _Optional[str] = ...) -> None: ...

class SignByEdsResult(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class EdsManagerStatusCheck(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class EdsManagerStatus(_message.Message):
    __slots__ = ("busy",)
    BUSY_FIELD_NUMBER: _ClassVar[int]
    busy: _wrappers_pb2.BoolValue
    def __init__(self, busy: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...) -> None: ...
