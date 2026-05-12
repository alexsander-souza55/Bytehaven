import sys
from cx_Freeze import setup, Executable

build_options = {
    "packages": ["pygame", "sqlite3", "code"],
    "include_files": [
        ("asset/audio",   "asset/audio"),
        ("asset/sprites", "asset/sprites"),
    ],
    "excludes": ["tkinter", "unittest", "email", "html", "http", "xml",
                 "xmlrpc", "pydoc", "doctest", "difflib"],
    "zip_include_packages": ["code"],
}

exe = Executable(
    script="main.py",
    base="Win32GUI" if sys.platform == "win32" else None,
    target_name="Bytehaven",
)

setup(
    name="BYTEHAVEN",
    version="1.0",
    description="BYTEHAVEN — THE LOST CONTAINERS",
    options={"build_exe": build_options},
    executables=[exe],
)
