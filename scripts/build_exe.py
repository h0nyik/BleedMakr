#!/usr/bin/env python3
"""
Build script pro vytvoreni univerzalniho release BleedMakr
Podporuje Windows, macOS a Linux
Optimalizovano pro minimalni velikost a rychle spusteni
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def get_platform_info():
    """Vrati informace o platforme pro build"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        return "Windows", "exe", "BleedMakr.exe"
    elif system == "darwin":  # macOS
        return "macOS", "app", "BleedMakr"
    elif system == "linux":
        return "Linux", "bin", "BleedMakr"
    else:
        return "Unknown", "bin", "BleedMakr"

def run_command(cmd, description):
    """Spusti prikaz a zobrazi vystup"""
    print(f"\n[BUILD] {description}")
    print(f"   Prikaz: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"   [OK] {result.stdout.strip()}")
        if result.stderr:
            print(f"   [WARNING] {result.stderr.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   [ERROR] Chyba: {e}")
        print(f"   Exit code: {e.returncode}")
        if e.stdout:
            print(f"   Stdout: {e.stdout}")
        if e.stderr:
            print(f"   Stderr: {e.stderr}")
        return False

def create_spec_file():
    """Vytvori optimalizovany .spec soubor pro PyInstaller"""
    platform_name, platform_ext, exe_name = get_platform_info()
    
    # Určení správné cesty k hlavnímu souboru
    main_file = 'src/spadavka_generator.py'
    if not os.path.exists(main_file):
        main_file = '../src/spadavka_generator.py'
    
    # Dynamické určení cest k datovým souborům
    data_files = []
    
    # Testování různých možných cest
    possible_paths = [
        ('docs/README.md', '.'),
        ('LICENSE', '.'),
        ('version.txt', '.')
    ]
    
    for src_path, dst_path in possible_paths:
        if os.path.exists(src_path):
            data_files.append((src_path, dst_path))
        elif os.path.exists(f'../{src_path}'):
            data_files.append((f'../{src_path}', dst_path))
        else:
            print(f"[WARNING] Soubor {src_path} nenalezen - vynechavam z buildu")
    
    # Kontrola hlavního souboru
    if not os.path.exists(main_file):
        print(f"[ERROR] Hlavni soubor {main_file} nenalezen")
        return False
    
    print(f"[INFO] Platforma: {platform_name}")
    print(f"[INFO] Nalezene datove soubory: {data_files}")
    
    # Platform-specific nastaveni
    if platform_name == "Windows":
        console_setting = "False"  # GUI aplikace
        icon_setting = "'icon.ico' if os.path.exists('icon.ico') else None"
    elif platform_name == "macOS":
        console_setting = "False"  # GUI aplikace
        icon_setting = "'icon.icns' if os.path.exists('icon.icns') else None"
    else:  # Linux
        console_setting = "False"  # GUI aplikace
        icon_setting = "None"
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Explicitni seznam modulu pro optimalizaci
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
    'subprocess',
    'zipfile',  # Potřebné pro práci s ZIP soubory
    'json',     # Potřebné pro práci s JSON
    'logging',  # Potřebné pro logování
    'warnings', # Potřebné pro warnings
    'traceback' # Potřebné pro error handling
]

# Vynechani nepotrebnych modulu
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
    'unittest',
    'doctest',
    'pydoc',
    'test',
    'tests'
]

a = Analysis(
    ['{main_file}'],
    pathex=['src', '../src'],
    binaries=[],
    datas={data_files},
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Optimalizace - odstraneni nepotrebnych souboru
def remove_unnecessary_files(a):
    """Odstrani nepotrebne soubory z analyzy"""
    # Filtrace binarnich souboru
    a.binaries = [x for x in a.binaries if not any(
        exclude in x[0].lower() for exclude in [
            'api-ms-win', 'ucrtbase', 'msvcp', 'vcruntime',
            'concrt', 'mfc', 'atl', 'msvcr', 'vcomp'
        ]
    )]
    
    # Filtrace pure modulu
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

# Detekce GitHub Actions pro vypnuti UPX
use_upx = os.getenv('GITHUB_ACTIONS') != 'true'

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
    strip=True,  # Optimalizace velikosti .exe
    upx=use_upx,  # Vypnout UPX na GitHub Actions
    upx_exclude=[],
    runtime_tmpdir=None,
    console={console_setting},  # GUI aplikace
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon={icon_setting},
    version='version_info.txt' if os.path.exists('version_info.txt') else None
)
'''
    
    with open('BleedMakr.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"OK: Vytvoren optimalizovany .spec soubor pro {platform_name}")

def create_version_info():
    """Vytvori version info soubor pro Windows exe"""
    # Nacteni verze z version.txt
    version = "0.0.1"  # vychozi hodnota
    version_files = ["version.txt", "../version.txt"]
    
    for version_file in version_files:
        if os.path.exists(version_file):
            try:
                with open(version_file, 'r', encoding='utf-8') as f:
                    version = f.read().strip()
                print(f"   Nactena verze pro version info: {version}")
                break
            except Exception as e:
                print(f"   Chyba cteni {version_file}: {e}")
    
    # Rozdeleni verze na cisla
    version_parts = version.split('.')
    major = int(version_parts[0]) if len(version_parts) > 0 else 0
    minor = int(version_parts[1]) if len(version_parts) > 1 else 0
    patch = int(version_parts[2]) if len(version_parts) > 2 else 0
    
    version_info = f'''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=({major}, {minor}, {patch}, 0),
    prodvers=({major}, {minor}, {patch}, 0),
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
        StringStruct(u'FileDescription', u'Profesionalni generator spadavky'),
        StringStruct(u'FileVersion', u'{version}'),
        StringStruct(u'InternalName', u'BleedMakr'),
        StringStruct(u'LegalCopyright', u'© 2025 BleedMakr. AGPL-3.0 License'),
        StringStruct(u'OriginalFilename', u'BleedMakr.exe'),
        StringStruct(u'ProductName', u'BleedMakr'),
        StringStruct(u'ProductVersion', u'{version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print("OK: Vytvoren version info soubor")

def install_dependencies():
    """Nainstaluje PyInstaller a dalsi zavislosti"""
    print("Instalace PyInstaller a UPX...")
    
    # Instalace PyInstaller
    if not run_command("pip install pyinstaller", "Instalace PyInstaller"):
        return False
    
    # Kontrola UPX (pro kompresi)
    if not shutil.which('upx'):
        print("INFO: UPX neni nainstalovan - .exe bude vetsi")
        print("   Muzete stahnout z: https://upx.github.io/")
    else:
        print("OK: UPX je k dispozici pro kompresi")
    
    return True

def build_exe():
    """Sestavi .exe soubor"""
    print("\nSestavovani aplikace...")
    
    platform_name, platform_ext, exe_name = get_platform_info()
    
    # Vycisleni predchozich buildu
    for dir_name in ['build', 'dist', '__pycache__']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Vycisleno: {dir_name}")
    
    # Kontrola .spec souboru
    if not os.path.exists('BleedMakr.spec'):
        print("CHYBA: BleedMakr.spec neexistuje")
        return False
    
    # Sestaveni
    cmd = "pyinstaller --clean --noconfirm BleedMakr.spec"
    if not run_command(cmd, f"Sestavovani pomoci PyInstaller pro {platform_name}"):
        print("CHYBA: PyInstaller selhal")
        # Diagnostika
        if os.path.exists('build'):
            print("   Obsah build/:")
            for item in os.listdir('build'):
                print(f"     {item}")
        return False
    
    # Kontrola vysledku
    exe_path = Path(f"dist/{exe_name}")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"OK: Uspechne vytvoren: {exe_path}")
        print(f"   Velikost: {size_mb:.1f} MB")
        return True
    else:
        print(f"CHYBA: {exe_name} nebyl vytvoren")
        
        # Diagnostika
        print("   Diagnostika:")
        if os.path.exists('dist'):
            print("     Obsah dist/:")
            for item in os.listdir('dist'):
                print(f"       {item}")
        else:
            print("     Adresar dist/ neexistuje")
        
        if os.path.exists('build'):
            print("     Obsah build/:")
            for item in os.listdir('build'):
                print(f"       {item}")
        else:
            print("     Adresar build/ neexistuje")
        
        return False

def create_release_package():
    """Vytvori balicek pro release"""
    print("\nVytvareni release balicku...")
    
    platform_name, platform_ext, exe_name = get_platform_info()
    
    # Nacteni verze z version.txt
    version = "0.0.1"  # vychozi hodnota
    version_files = ["version.txt", "../version.txt"]
    
    for version_file in version_files:
        if os.path.exists(version_file):
            try:
                with open(version_file, 'r', encoding='utf-8') as f:
                    version = f.read().strip()
                print(f"   Nactena verze: {version}")
                break
            except Exception as e:
                print(f"   Chyba cteni {version_file}: {e}")
    
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    
    release_dir.mkdir()
    
    # Kopirovani souboru podle platformy
    files_to_copy = [
        (f"dist/{exe_name}", exe_name),
        ("docs/README.md", "README.md"),
        ("LICENSE", "LICENSE"),
        ("version.txt", "version.txt")
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, release_dir / dst)
            print(f"   Zkopirovano: {src} -> {dst}")
        elif os.path.exists(f"../{src}"):
            shutil.copy2(f"../{src}", release_dir / dst)
            print(f"   Zkopirovano: ../{src} -> {dst}")
    
    # Vytvoreni ZIP archivu s platform-specific nazvem
    zip_name = f"BleedMakr-v{version}-{platform_name}-x64"
    shutil.make_archive(zip_name, 'zip', release_dir)
    print(f"OK: Vytvoren release balicek: {zip_name}.zip")
    
    return f"{zip_name}.zip"

def main():
    """Hlavni funkce build procesu"""
    platform_name, platform_ext, exe_name = get_platform_info()
    
    print(f"BleedMakr - Build {platform_name} release")
    print("=" * 50)
    
    # Kontrola Python verze
    if sys.version_info < (3, 8):
        print("CHYBA: Vyzdauje Python 3.8+")
        return False
    
    print(f"OK: Python {sys.version}")
    print(f"OK: Platforma: {platform_name}")
    
    # Kontrola, zda jsme ve správné složce
    src_path = '../src/spadavka_generator.py'
    if not os.path.exists(src_path):
        # Zkusíme alternativní cestu pro GitHub Actions
        src_path = 'src/spadavka_generator.py'
        if not os.path.exists(src_path):
            print("CHYBA: SpadavkaGenerator.py nenalezen")
            print("   Aktualni cesta:", os.getcwd())
            print("   Hledane cesty: ../src/spadavka_generator.py, src/spadavka_generator.py")
            return False
    
    # Instalace zavislosti
    if not install_dependencies():
        return False
    
    # Vytvoreni konfiguracnich souboru
    create_spec_file()
    create_version_info()
    
    # Sestaveni aplikace
    if not build_exe():
        return False
    
    # Vytvoreni release balicku
    zip_file = create_release_package()
    
    print(f"\nBuild dokoncen uspesne pro {platform_name}!")
    print(f"   Aplikace: dist/{exe_name}")
    print(f"   Release balicek: {zip_file}")
    print(f"\nNyni muzete nahrat na GitHub jako release pro {platform_name}.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 