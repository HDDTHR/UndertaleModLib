import typing
from typing import Any

from System import IDisposable

T = Any


class FileMode(typing.SupportsInt):
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...

    # Values:
    CreateNew: "FileMode"  # 1
    Create: "FileMode"  # 2
    Open: "FileMode"  # 3
    OpenOrCreate: "FileMode"  # 4
    Truncate: "FileMode"  # 5
    Append: "FileMode"  # 6


class FileAccess(typing.SupportsInt):
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...

    # Values:
    Read: "FileAccess"  # 1
    Write: "FileAccess"  # 2
    ReadWrite: "FileAccess"  # 3


class FileShare(typing.SupportsInt):
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...

    # Values:
    None_: "FileShare"  # 0 (System.IO.FileShare.None)
    Read: "FileShare"  # 1
    Write: "FileShare"  # 2
    ReadWrite: "FileShare"  # 3
    Delete: "FileShare"  # 4
    Inheritable: "FileShare"  # 16


class SeekOrigin(typing.SupportsInt):
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...

    # Values:
    Begin: "SeekOrigin"  # 0
    Current: "SeekOrigin"  # 1
    End: "SeekOrigin"  # 2


class Stream(IDisposable):
    CanRead: bool
    CanSeek: bool
    CanWrite: bool
    Length: int
    Position: int

    def Close(self) -> None: ...
    def CopyTo(self, destination: Stream) -> None: ...
    def Dispose(self) -> None: ...
    def Flush(self) -> None: ...
    def Read(self, buffer: Any, offset: int, count: int) -> int: ...
    def Seek(self, offset: int, origin: SeekOrigin) -> int: ...
    def Write(self, buffer: Any, offset: int, count: int) -> None: ...


class MemoryStream(Stream):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, buffer: Any) -> None: ...


class FileStream(Stream):
    @typing.overload
    def __init__(self, path: str, mode: FileMode, access: FileAccess) -> None: ...
    @typing.overload
    def __init__(self, path: str, mode: FileMode, access: FileAccess, share: FileShare) -> None: ...


class TextReader(IDisposable):
    def Peek(self) -> int: ...
    def Read(self) -> int: ...
    def ReadLine(self) -> str | None: ...
    def ReadToEnd(self) -> str: ...


class TextWriter(IDisposable):
    def Write(self, value: Any) -> None: ...
    def WriteLine(self, value: Any = ...) -> None: ...


class BinaryWriter(IDisposable):
    def Write(self, value: Any) -> None: ...


class FileInfo:
    Name: str
    Length: int
    FullName: str

    def Exists(self) -> bool: ...


class UnmanagedMemoryStream(Stream):
    pass
