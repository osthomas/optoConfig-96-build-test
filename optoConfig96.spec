# -*- mode: python ; coding: utf-8 -*-

# To build: pyinstaller optoConfig96.spec

import sys
import subprocess
from optoConfig96.version import __version__

name = f"optoConfig96"

from PyInstaller.utils.hooks import copy_metadata, collect_submodules

# Resource files
datas = [("optoConfig96/resources/", "optoConfig96/resources")]
# Traits and friends utilize entry points to load the relevant toolkit,
# (dist-info, formerly egg-info), these need to be included explicitly.
datas += copy_metadata("traitsui") + copy_metadata("pyface")


# Due to the dynamic nature of toolkit loading by pyface, these are not
# included automatically
hiddenimports = [
    "traitsui.toolkits",
    "traitsui.qt4",
    "pyface.toolkits",
    "pyface.ui.qt4"
]
hiddenimports += collect_submodules('pyface.ui.qt4')
hiddenimports += collect_submodules('traitsui.qt4')

block_cipher = None


a = Analysis(
    ['optoConfig96/__main__.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    )
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=f"{name}-{__version__}",  # avoid name conflict with optoConfig96/resources dir
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
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
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=name
)

# NOTE:
# As of 2023-02-04, pyinstaller 5.7.0, the call to `codesign` fails due to
# subcomponents in PyQt5/qml/QtQml. Several unneeded QT components are included
# by pyinstaller, of which this is one. Removing this gets rid of the error,
# but the pop up preventing launch of the app after download remains. Thus,
# removing these unneeded components is not worth the hassle.
app = BUNDLE(
    coll,
    name = name + ".app",
    icon = "optoConfig96/resources/oc96.icns"
)
