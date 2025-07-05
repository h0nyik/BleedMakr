#!/usr/bin/env python3
"""
Build script pro vytvoření .exe release BleedMakr
Optimalizováno pro minimální velikost a rychlé spuštění
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Spustí příkaz a zobrazí výstup"""
    print(f"\n🔧 {description}")
    print(f"   Příkaz: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"   ✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Chyba: {e}")
        if e.stdout:
            print(f"   Stdout: {e.stdout}")
        if e.stderr:
            print(f"   Stderr: {e.stderr}")
        return False

def create_spec_file():
    """Vytvoří optimalizovaný .spec soubor pro PyInstaller"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Explicitní seznam modulů pro optimalizaci
hidden_imports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.scrolledtext',
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'PIL.ImageOps',
    'fitz',
    'numpy',
    'io',
    'threading',
    'queue',
    'os',
    'sys',
    'pathlib',
    'shutil',
    'subprocess'
]

# Vynechání nepotřebných modulů
excludes = [
    'matplotlib',
    'scipy',
    'pandas',
    'jupyter',
    'IPython',
    'notebook',
    'sphinx',
    'pytest',
    'setuptools',
    'pip',
    'wheel',
    'distutils',
    'email',
    'http',
    'urllib3',
    'requests',
    'xml',
    'html',
    'sqlite3',
    'csv',
    'json',
    'pickle',
    'unittest',
    'doctest',
    'pydoc',
    'multiprocessing',
    'concurrent',
    'asyncio',
    'socket',
    'ssl',
    'hashlib',
    'hmac',
    'base64',
    'uuid',
    'datetime',
    'calendar',
    'locale',
    'gettext',
    'argparse',
    'configparser',
    'logging',
    'warnings',
    'traceback',
    'pdb',
    'profile',
    'cProfile',
    'timeit',
    'gc',
    'weakref',
    'copy',
    'pickle',
    'shelve',
    'dbm',
    'gzip',
    'bz2',
    'lzma',
    'zipfile',
    'tarfile',
    'ftplib',
    'poplib',
    'imaplib',
    'smtplib',
    'telnetlib',
    'socketserver',
    'wsgiref',
    'msilib',
    'msvcrt',
    'winsound',
    'winreg'
]

a = Analysis(
    ['spadavka_generator.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('LICENSE', '.'),
        ('version.txt', '.')
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Optimalizace - odstranění nepotřebných souborů
def remove_unnecessary_files(a):
    """Odstraní nepotřebné soubory z analýzy"""
    # Filtrace binárních souborů
    a.binaries = [x for x in a.binaries if not any(
        exclude in x[0].lower() for exclude in [
            'api-ms-win', 'ucrtbase', 'msvcp', 'vcruntime',
            'concrt', 'mfc', 'atl', 'msvcr', 'vcomp'
        ]
    )]
    
    # Filtrace pure modulů
    a.pure = [x for x in a.pure if not any(
        exclude in x[0].lower() for exclude in [
            'test', 'tests', 'testing', 'unittest',
            'doctest', 'pydoc', 'distutils', 'setuptools',
            'pip', 'wheel', 'pkg_resources'
        ]
    )]
    
    return a

a = remove_unnecessary_files(a)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BleedMakr',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Komprese UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI aplikace
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None
)
'''
    
    with open('BleedMakr.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Vytvořen optimalizovaný .spec soubor")

def create_version_info():
    """Vytvoří version info soubor pro Windows exe"""
    version_info = '''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(0, 0, 1, 0),
    prodvers=(0, 0, 1, 0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'BleedMakr'),
        StringStruct(u'FileDescription', u'Profesionální generátor spadávek'),
        StringStruct(u'FileVersion', u'0.0.1'),
        StringStruct(u'InternalName', u'BleedMakr'),
        StringStruct(u'LegalCopyright', u'© 2025 BleedMakr. AGPL-3.0 License'),
        StringStruct(u'OriginalFilename', u'BleedMakr.exe'),
        StringStruct(u'ProductName', u'BleedMakr'),
        StringStruct(u'ProductVersion', u'0.0.1')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print("✅ Vytvořen version info soubor")

def install_dependencies():
    """Nainstaluje PyInstaller a další závislosti"""
    print("🔧 Instalace PyInstaller a UPX...")
    
    # Instalace PyInstaller
    if not run_command("pip install pyinstaller", "Instalace PyInstaller"):
        return False
    
    # Kontrola UPX (pro kompresi)
    if not shutil.which('upx'):
        print("⚠️  UPX není nainstalován - .exe bude větší")
        print("   Můžete stáhnout z: https://upx.github.io/")
    else:
        print("✅ UPX je k dispozici pro kompresi")
    
    return True

def build_exe():
    """Sestaví .exe soubor"""
    print("\n🚀 Sestavování .exe souboru...")
    
    # Vyčištění předchozích buildů
    for dir_name in ['build', 'dist', '__pycache__']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Vyčištěno: {dir_name}")
    
    # Sestavení
    cmd = "pyinstaller --clean --noconfirm BleedMakr.spec"
    if not run_command(cmd, "Sestavování pomocí PyInstaller"):
        return False
    
    # Kontrola výsledku
    exe_path = Path("dist/BleedMakr.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Úspěšně vytvořen: {exe_path}")
        print(f"   Velikost: {size_mb:.1f} MB")
        return True
    else:
        print("❌ .exe soubor nebyl vytvořen")
        return False

def create_release_package():
    """Vytvoří balíček pro release"""
    print("\n📦 Vytváření release balíčku...")
    
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    
    release_dir.mkdir()
    
    # Kopírování souborů
    files_to_copy = [
        ("dist/BleedMakr.exe", "BleedMakr.exe"),
        ("README.md", "README.md"),
        ("LICENSE", "LICENSE"),
        ("version.txt", "version.txt")
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, release_dir / dst)
            print(f"   Zkopírováno: {src} -> {dst}")
    
    # Vytvoření ZIP archivu
    zip_name = "BleedMakr-v0.0.1-Windows-x64"
    shutil.make_archive(zip_name, 'zip', release_dir)
    print(f"✅ Vytvořen release balíček: {zip_name}.zip")
    
    return f"{zip_name}.zip"

def main():
    """Hlavní funkce build procesu"""
    print("🎨 BleedMakr - Build .exe release")
    print("=" * 50)
    
    # Kontrola Python verze
    if sys.version_info < (3, 8):
        print("❌ Vyžaduje Python 3.8+")
        return False
    
    print(f"✅ Python {sys.version}")
    
    # Instalace závislostí
    if not install_dependencies():
        return False
    
    # Vytvoření konfiguračních souborů
    create_spec_file()
    create_version_info()
    
    # Sestavení .exe
    if not build_exe():
        return False
    
    # Vytvoření release balíčku
    zip_file = create_release_package()
    
    print("\n🎉 Build dokončen úspěšně!")
    print(f"   .exe soubor: dist/BleedMakr.exe")
    print(f"   Release balíček: {zip_file}")
    print("\nNyní můžete nahrát na GitHub jako release.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 