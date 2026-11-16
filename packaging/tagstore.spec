# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for the windowed TagStore build.

Equivalent to:

    pyinstaller --onedir --noconsole --name TagStore --noupx ^
        --add-data "tagstore/static;tagstore/static" ^
        --collect-submodules uvicorn run_tagstore.py

Paths are relative to the repo root so the spec can live in packaging/.
"""

import os

from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.win32.versioninfo import (
    FixedFileInfo,
    StringFileInfo,
    StringStruct,
    StringTable,
    VarFileInfo,
    VarStruct,
    VSVersionInfo,
)

root = os.path.dirname(os.path.dirname(os.path.abspath(SPEC)))

version_info = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(0, 1, 0, 0),
        prodvers=(0, 1, 0, 0),
        mask=0x3F,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0),
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    "040904B0",
                    [
                        StringStruct("CompanyName", "TagStore"),
                        StringStruct("FileDescription", "TagStore"),
                        StringStruct("FileVersion", "0.1.0.0"),
                        StringStruct("InternalName", "TagStore"),
                        StringStruct("OriginalFilename", "TagStore.exe"),
                        StringStruct("ProductName", "TagStore"),
                        StringStruct("ProductVersion", "0.1.0"),
                    ],
                )
            ]
        ),
        VarFileInfo([VarStruct("Translation", [1033, 1200])]),
    ],
)

hidden = collect_submodules("uvicorn")
hidden += [
    "webview",
    "send2trash",
    "tkinter",
    "tkinter.filedialog",
]

a = Analysis(
    [os.path.join(root, "run_tagstore.py")],
    pathex=[root],
    binaries=[],
    datas=[(os.path.join(root, "tagstore", "static"), os.path.join("tagstore", "static"))],
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["rich"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="TagStore",
    icon=os.path.join(root, "packaging", "tagstore.ico"),
    version=version_info,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="TagStore",
)
