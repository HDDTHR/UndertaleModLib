"""Runtime loading of UndertaleModLib into the Python process via pythonnet."""

import os
import shutil
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from UndertaleModLib import UndertaleData

_REQUIRED_ASSEMBLIES = (
    "UndertaleModLib.dll",
    "Underanalyzer.dll",
    "Magick.NET.Core.dll",
    "Magick.NET-Q8-AnyCPU.dll",
)
_LIB_DIR = Path(__file__).resolve().parent / "_lib"

_initialized = False
_assembly_resolve_handler: Any = None


def _require_bundled_files() -> None:
    for name in _REQUIRED_ASSEMBLIES:
        path = _LIB_DIR / name
        if not path.is_file():
            raise FileNotFoundError(
                f"{path} not found; install a built wheel or populate _lib via CI"
            )


def _preload_native_libraries() -> None:
    """Preload bundled native libraries so P/Invokes (e.g. Magick.Native) resolve."""
    import ctypes

    if sys.platform == "win32":
        loader, suffixes = ctypes.WinDLL, (".dll",)
    else:
        loader, suffixes = ctypes.CDLL, (".so", ".dylib")
    for path in sorted(_LIB_DIR.glob("runtimes/*/native/*")):
        if path.suffix.lower() not in suffixes:
            continue
        try:
            loader(str(path))
        except OSError:
            pass


def _initialize() -> None:
    """Initialize the .NET runtime and load UndertaleModLib plus its dependencies."""
    global _initialized, _assembly_resolve_handler
    if _initialized:
        return
    _require_bundled_files()
    _preload_native_libraries()
    os.environ.setdefault("DOTNET_ROLL_FORWARD", "LatestMajor")
    os.environ.setdefault("PYTHONNET_RUNTIME", "coreclr")
    dotnet = shutil.which("dotnet")
    if dotnet:
        dotnet_root = Path(dotnet).resolve().parent
        if (dotnet_root / "host" / "fxr").is_dir():
            os.environ.setdefault("DOTNET_ROOT", str(dotnet_root))
    if "clr" in sys.modules:
        _verify_coreclr_active()
    else:
        from pythonnet import load

        load("coreclr")

    import clr
    from System import AppDomain, ResolveEventHandler
    from System.Reflection import Assembly

    def resolve_assembly(_sender: object, args: Any) -> Any:
        name = str(args.Name).split(",")[0]
        candidate = _LIB_DIR / f"{name}.dll"
        return Assembly.LoadFrom(str(candidate)) if candidate.is_file() else None

    _assembly_resolve_handler = ResolveEventHandler(resolve_assembly)
    AppDomain.CurrentDomain.add_AssemblyResolve(_assembly_resolve_handler)
    for dll in sorted(_LIB_DIR.glob("*.dll")):
        clr.AddReference(str(dll))
    _initialized = True


def _verify_coreclr_active() -> None:
    """Fail fast if a bare ``import clr`` auto-selected an incompatible runtime."""
    try:
        from System import Environment

        major = int(str(Environment.Version).split(".")[0])
    except Exception as exc:
        raise RuntimeError(_CLR_ORDER_MESSAGE) from exc
    if major < 10:
        raise RuntimeError(_CLR_ORDER_MESSAGE)


_CLR_ORDER_MESSAGE = (
    "The Python module 'clr' was imported before undertale_mod_lib, so pythonnet "
    "auto-selected a runtime that cannot run UndertaleModLib (.NET 10 required). "
    "Import undertale_mod_lib (or call load_data) before 'import clr', and "
    "uninstall mono if present so auto-detection cannot pick it."
)


def typings_path() -> Path:
    """Return the directory containing the bundled .NET stub packages."""
    return Path(__file__).resolve().parent / "typings"


def load_data(path: str | Path) -> "UndertaleData":
    """Load a GameMaker data file (e.g. ``data.win``) as an ``UndertaleData``."""
    _initialize()
    from System.IO import FileAccess, FileMode, FileStream
    from UndertaleModLib import UndertaleReader

    stream = FileStream(str(path), FileMode.Open, FileAccess.Read)
    try:
        return UndertaleReader(stream).ReadUndertaleData()
    finally:
        stream.Dispose()
