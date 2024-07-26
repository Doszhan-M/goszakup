from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EdsManagerStatusCheck(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SignByEdsStart(_message.Message):
    __slots__ = ("eds_path", "eds_pass")
    EDS_PATH_FIELD_NUMBER: _ClassVar[int]
    EDS_PASS_FIELD_NUMBER: _ClassVar[int]
    eds_path: str
    eds_pass: str
    def __init__(self, eds_path: _Optional[str] = ..., eds_pass: _Optional[str] = ...) -> None: ...

class RestartParams(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class EdsManagerStatus(_message.Message):
    __slots__ = ("busy",)
    BUSY_FIELD_NUMBER: _ClassVar[int]
    busy: _wrappers_pb2.BoolValue
    def __init__(self, busy: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...) -> None: ...

class SignByEdsResult(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _wrappers_pb2.BoolValue
    def __init__(self, result: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...) -> None: ...

class RestartResult(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _wrappers_pb2.BoolValue
    def __init__(self, result: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...) -> None: ...
