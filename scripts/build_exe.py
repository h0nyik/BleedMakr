#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for creating universal BleedMakr release
Supports Windows, macOS and Linux
Optimized for minimal size and fast startup
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

# UTF-8 encoding setup for Windows
if sys.platform.startswith('win'):
    import locale
    # Set UTF-8 for stdout and stderr
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    # Set locale for UTF-8
    try:
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
    except:
        pass

# --- Check for numpy folder in current directory ---
if os.path.isdir('numpy'):
    print('[ERROR] There is a numpy folder in the current directory! This will cause numpy import error.')
    print('  Delete or move the numpy folder outside the project or build directory and run build again.')
    sys.exit(1)
# --- end of check ---

def get_platform_info():
    """Returns platform information for build"""
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
    """Runs command and displays output"""
    print(f"\n[BUILD] {description}")
    print(f"   Command: {cmd}")
    
    try:
        # Set UTF-8 encoding for subprocess
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            env=env
        )
        if result.stdout:
            print(f"   [OK] {result.stdout.strip()}")
        if result.stderr:
            print(f"   [WARNING] {result.stderr.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   [ERROR] Error: {e}")
        print(f"   Exit code: {e.returncode}")
        if e.stdout:
            print(f"   Stdout: {e.stdout}")
        if e.stderr:
            print(f"   Stderr: {e.stderr}")
        return False

def create_spec_file():
    """Creates optimized .spec file for PyInstaller"""
    platform_name, platform_ext, exe_name = get_platform_info()
    
    # Determine correct path to main file
    main_file = 'src/spadavka_generator.py'
    if not os.path.exists(main_file):
        main_file = '../src/spadavka_generator.py'
    
    # Dynamic determination of data file paths
    data_files = []
    
    # Test various possible paths
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
            print(f"[WARNING] File {src_path} not found - skipping from build")
    
    # Check main file
    if not os.path.exists(main_file):
        print(f"[ERROR] Main file {main_file} not found")
        return False
    
    print(f"[INFO] Platform: {platform_name}")
    print(f"[INFO] Found data files: {data_files}")
    
    # Platform-specific settings
    if platform_name == "Windows":
        console_setting = "False"  # GUI application
        icon_setting = "'icon.ico' if os.path.exists('icon.ico') else None"
    elif platform_name == "macOS":
        console_setting = "False"  # GUI application
        icon_setting = "'icon.icns' if os.path.exists('icon.icns') else None"
    else:  # Linux
        console_setting = "False"  # GUI application
        icon_setting = "None"
    
    # Detect numpy binary files
    try:
        import numpy
        numpy_path = os.path.dirname(numpy.__file__)
        numpy_binaries = []
        
        # Add numpy._core DLL files
        core_path = os.path.join(numpy_path, '_core')
        if os.path.exists(core_path):
            for file in os.listdir(core_path):
                if file.endswith('.pyd') or file.endswith('.dll'):
                    numpy_binaries.append((os.path.join(core_path, file), 'numpy/_core'))
        
        # Add numpy.random DLL files
        random_path = os.path.join(numpy_path, 'random')
        if os.path.exists(random_path):
            for file in os.listdir(random_path):
                if file.endswith('.pyd') or file.endswith('.dll'):
                    numpy_binaries.append((os.path.join(random_path, file), 'numpy/random'))
        
        # Add numpy.fft DLL files
        fft_path = os.path.join(numpy_path, 'fft')
        if os.path.exists(fft_path):
            for file in os.listdir(fft_path):
                if file.endswith('.pyd') or file.endswith('.dll'):
                    numpy_binaries.append((os.path.join(fft_path, file), 'numpy/fft'))
        
        binaries_str = str(numpy_binaries)
        print(f"[NUMPY] Found {len(numpy_binaries)} numpy binary files")
        
    except Exception as e:
        print(f"[WARNING] Error detecting numpy binaries: {e}")
        binaries_str = "[]"
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Explicit list of modules for optimization
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
    'numpy.lib.format',
    'numpy._core',
    'numpy._core._multiarray_umath',
    'numpy._core.multiarray',
    'numpy._core.umath',
    'numpy.random',
    'numpy.random._pickle',
    'numpy.random._sfc64',
    'numpy.random._philox',
    'numpy.random._pcg64',
    'numpy.random._mt19937',
    'numpy.random.mtrand',
    'numpy.random.bit_generator',
    'numpy.random._generator',
    'numpy.random._bounded_integers',
    'numpy.random._common',
    'numpy.fft',
    'numpy.fft._pocketfft_umath',
    'io',
    'threading',
    'queue',
    'os',
    'sys',
    'pathlib',
    'shutil',
    'subprocess',
    'zipfile',  # Required for ZIP file operations
    'json',     # Required for JSON operations
    'logging',  # Required for logging
    'warnings', # Required for warnings
    'traceback' # Required for error handling
]

# Exclude unnecessary modules
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
    binaries={binaries_str},
    datas={data_files},
    hiddenimports=hidden_imports,
    hookspath=['.'],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='{exe_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('BleedMakr.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"OK: Created optimized .spec file for {platform_name}")
    return True

def create_version_info():
    """Creates version info file for Windows exe"""
    # Load version from version.txt
    version = "0.0.1"  # default value
    version_files = ["version.txt", "../version.txt"]
    
    for version_file in version_files:
        if os.path.exists(version_file):
            try:
                with open(version_file, 'r', encoding='utf-8') as f:
                    version = f.read().strip()
                print(f"   Loaded version: {version}")
                break
            except Exception as e:
                print(f"   Error reading {version_file}: {e}")
    
    # Create version info for Windows
    version_info = f'''# UTF-8
#
# Version info for Windows executable
#
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({version.replace(".", ",")}, 0),
    prodvers=({version.replace(".", ",")}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'BleedMakr Team'),
         StringStruct(u'FileDescription', u'BleedMakr - Generator Spadavek'),
         StringStruct(u'FileVersion', u'{version}'),
         StringStruct(u'InternalName', u'BleedMakr'),
         StringStruct(u'LegalCopyright', u'Copyright (c) 2025 BleedMakr Team'),
         StringStruct(u'OriginalFilename', u'BleedMakr.exe'),
         StringStruct(u'ProductName', u'BleedMakr'),
         StringStruct(u'ProductVersion', u'{version}')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print(f"OK: Created version info file")
    return True

def install_dependencies():
    """Installs required dependencies"""
    print("\nInstalling PyInstaller and UPX...")
    
    # Install PyInstaller
    if not run_command("pip install pyinstaller", "Installing PyInstaller"):
        return False
    
    # Check for UPX (optional) - with proper encoding
    try:
        upx_result = subprocess.run(['upx', '--version'], capture_output=True, text=True, encoding='utf-8')
        if upx_result.returncode == 0:
            print("INFO: UPX is installed - .exe will be smaller")
        else:
            print("INFO: UPX is not installed - .exe will be larger")
            print("   You can download from: https://upx.github.io/")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("INFO: UPX is not installed - .exe will be larger")
        print("   You can download from: https://upx.github.io/")
    
    return True

def run_pyinstaller():
    """Runs PyInstaller with optimized parameters"""
    print("\n[BUILD] Running PyInstaller...")
    
    # PyInstaller parameters - basic only, numpy is already in .spec
    cmd = [
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'BleedMakr.spec'
    ]
    
    try:
        # Set UTF-8 encoding for subprocess
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            cmd, 
            check=True, 
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            env=env
        )
        print(f"[BUILD] PyInstaller completed successfully")
        if result.stdout:
            print(f"   [INFO] {result.stdout.strip()}")
        if result.stderr:
            print(f"   [WARNING] {result.stderr.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] PyInstaller failed: {e}")
        if e.stdout:
            print(f"[ERROR] Stdout: {e.stdout}")
        if e.stderr:
            print(f"[ERROR] Stderr: {e.stderr}")
        return False

def sign_executable(exe_path):
    """Signs .exe file with digital certificate"""
    print("\n[SIGNING] Signing application...")
    
    try:
        # PowerShell commands for certificate creation and signing
        ps_commands = [
            # Create certificate (if doesn't exist)
            f'''$cert = Get-ChildItem -Path "Cert:\\CurrentUser\\My" | Where-Object {{$_.Subject -like "*BleedMakr*"}} | Select-Object -First 1
if (-not $cert) {{
    Write-Host "  Creating new certificate for signing..."
    $cert = New-SelfSignedCertificate -Subject "CN=BleedMakr, O=BleedMakr Team, C=CZ" -Type CodeSigningCert -CertStoreLocation "Cert:\\CurrentUser\\My" -NotAfter (Get-Date).AddYears(3)
    Write-Host "  Certificate created: $($cert.Thumbprint)"
}} else {{
    Write-Host "  Using existing certificate: $($cert.Thumbprint)"
}}''',
            
            # Sign application
            f'''$result = Set-AuthenticodeSignature -FilePath "{exe_path}" -Certificate $cert
if ($result.Status -eq "UnknownError" -or $result.Status -eq "Valid") {{
    Write-Host "  ✅ Application signed successfully"
    Write-Host "  Certificate: $($cert.Thumbprint)"
    exit 0
}} else {{
    Write-Host "  ⚠️ Signing with warning: $($result.StatusMessage)"
    exit 0
}}'''
        ]
        
        # Run PowerShell commands
        for i, ps_cmd in enumerate(ps_commands):
            print(f"  Step {i+1}: {'Creating certificate' if i == 0 else 'Signing application'}")
            
            # Create temporary PowerShell script
            temp_script = f"temp_sign_{i}.ps1"
            with open(temp_script, 'w', encoding='utf-8') as f:
                f.write(ps_cmd)
            
            try:
                # Run PowerShell script with UTF-8 encoding
                env = os.environ.copy()
                env['PYTHONIOENCODING'] = 'utf-8'
                
                result = subprocess.run([
                    'powershell', '-ExecutionPolicy', 'Bypass', '-File', temp_script
                ], capture_output=True, text=True, encoding='utf-8', env=env, check=True)
                
                if result.stdout:
                    print(f"    {result.stdout.strip()}")
                if result.stderr:
                    print(f"    [WARNING] {result.stderr.strip()}")
                    
            except subprocess.CalledProcessError as e:
                print(f"    [ERROR] PowerShell error: {e}")
                if e.stdout:
                    print(f"    Stdout: {e.stdout}")
                if e.stderr:
                    print(f"    Stderr: {e.stderr}")
                return False
            finally:
                # Delete temporary script
                if os.path.exists(temp_script):
                    os.remove(temp_script)
        
        print("  ✅ Signing completed")
        return True
        
    except Exception as e:
        print(f"  ❌ Error during signing: {e}")
        return False

def build_exe():
    """Builds .exe file"""
    print("\nBuilding application...")
    
    platform_name, platform_ext, exe_name = get_platform_info()
    
    # Cleanup
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   Cleaned: {folder}")
    
    # Create .spec file
    if not create_spec_file():
        return False
    
    # Build
    if not run_pyinstaller():
        print("ERROR: PyInstaller failed")
        return False
    
    # Check result
    exe_path = os.path.join('dist', exe_name)
    if not os.path.exists(exe_path):
        print("ERROR: .exe file was not created")
        return False
    
    # Sign application
    if platform.system().lower() == "windows":
        sign_executable(exe_path)
    
    # Print information
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"OK: Successfully created: {exe_path}")
    print(f"   Size: {size_mb:.1f} MB")
    
    # Print dist/ content
    print("   Content of dist/:")
    for item in os.listdir('dist'):
        print(f"     {item}")
    
    return True

def create_release_package():
    """Creates release package"""
    print("\nCreating release package...")
    
    platform_name, platform_ext, exe_name = get_platform_info()
    
    # Load version from version.txt
    version = "0.0.1"  # default value
    version_files = ["version.txt", "../version.txt"]
    
    for version_file in version_files:
        if os.path.exists(version_file):
            try:
                with open(version_file, 'r', encoding='utf-8') as f:
                    version = f.read().strip()
                print(f"   Loaded version: {version}")
                break
            except Exception as e:
                print(f"   Error reading {version_file}: {e}")
    
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    
    release_dir.mkdir()
    
    # Copy files according to platform
    files_to_copy = [
        (f"dist/{exe_name}", exe_name),
        ("docs/README.md", "README.md"),
        ("LICENSE", "LICENSE"),
        ("version.txt", "version.txt")
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, release_dir / dst)
            print(f"   Copied: {src} -> {dst}")
        elif os.path.exists(f"../{src}"):
            shutil.copy2(f"../{src}", release_dir / dst)
            print(f"   Copied: ../{src} -> {dst}")
    
    # Create ZIP archive with platform-specific name
    zip_name = f"BleedMakr-v{version}-{platform_name}-x64"
    shutil.make_archive(zip_name, 'zip', release_dir)
    print(f"OK: Created release package: {zip_name}.zip")
    
    return f"{zip_name}.zip"

def main():
    """Main build process function"""
    platform_name, platform_ext, exe_name = get_platform_info()
    
    print(f"BleedMakr - Build {platform_name} release")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Requires Python 3.8+")
        return False
    
    print(f"OK: Python {sys.version}")
    print(f"OK: Platform: {platform_name}")
    
    # Check if we're in the right folder
    src_path = '../src/spadavka_generator.py'
    if not os.path.exists(src_path):
        # Try alternative path for GitHub Actions
        src_path = 'src/spadavka_generator.py'
        if not os.path.exists(src_path):
            print("ERROR: SpadavkaGenerator.py not found")
            print("   Current path:", os.getcwd())
            print("   Searched paths: ../src/spadavka_generator.py, src/spadavka_generator.py")
            return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create configuration files
    create_version_info()
    
    # Build application
    if not build_exe():
        return False
    
    # Create release package
    zip_file = create_release_package()
    
    print(f"\nBuild completed successfully for {platform_name}!")
    print(f"   Application: dist/{exe_name}")
    print(f"   Release package: {zip_file}")
    print(f"\nYou can now upload to GitHub as release for {platform_name}.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 