"""Python access to UndertaleModLib through the .NET runtime (pythonnet).

Example:
    from undertale_mod_lib import load_data, UndertaleModLib

    data = load_data("data.win")
    for sprite in data.Sprites:
        print(sprite.Name)
"""

from undertale_mod_lib.wrapper import load_data, typings_path

__all__ = ["Underanalyzer", "UndertaleModLib", "load_data", "typings_path"]
__version__ = "0.1.0"

_CLR_NAMESPACES = ("UndertaleModLib", "Underanalyzer")


def __getattr__(name: str):
    if name in _CLR_NAMESPACES:
        import importlib

        from undertale_mod_lib import wrapper

        wrapper._initialize()
        return importlib.import_module(name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
