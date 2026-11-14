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

root = os.path.dirname(os.path.dirname(os.path.abspath(SPEC)))

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
