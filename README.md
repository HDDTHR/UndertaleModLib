# Undertale Mod Lib

> https://github.com/UnderminersTeam/UndertaleModTool

## Requirements

- Python 3.13+
- [.NET runtime](https://dotnet.microsoft.com/download/dotnet/10.0) 10 or newer

## Install

```sh
uv add "undertale-mod-lib @ https://github.com/HDDTHR/UndertaleModLib/releases/download/<tag>/undertale_mod_lib-<version>-py3-none-any.whl"
```

## Usage

`undertale_mod_lib` must be imported **before** `clr` (and before any `from System... import`),
so it can initialize pythonnet with the correct .NET runtime. Everything under `UndertaleModLib`
is exposed through the CLR bridge, and `typings/` ships inside the package so editors get
autocomplete out of the box:

```python
import undertale_mod_lib as uml

data = uml.UndertaleModLib.UndertaleData.CreateNew()

from Underanalyzer.Decompiler import GlobalFunctions
```
