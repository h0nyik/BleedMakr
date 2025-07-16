#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for BleedMakr icons from BleedMakr.png
Uses ImageMagick to create all required icon formats
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# ImageMagick path
IMAGEMAGICK_PATH = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

def check_imagemagick():
    """Kontroluje dostupnost ImageMagick"""
    print("🔍 Kontrola ImageMagick...")
    
    if os.path.exists(IMAGEMAGICK_PATH):
        print(f"   ✅ ImageMagick nalezen: {IMAGEMAGICK_PATH}")
        return True
    else:
        print(f"   ❌ ImageMagick nenalezen: {IMAGEMAGICK_PATH}")
        return False

def check_source_icon():
    """Kontroluje dostupnost zdrojové ikony"""
    print("\n🔍 Kontrola zdrojové ikony...")
    
    source_icon = "BleedMakr.png"
    if os.path.exists(source_icon):
        size = os.path.getsize(source_icon)
        print(f"   ✅ {source_icon} nalezen ({size:,} bytes)")
        return True
    else:
        print(f"   ❌ {source_icon} nenalezen")
        return False

def create_icon_sizes():
    """Vytvoří různé velikosti ikon z BleedMakr.png"""
    print("\n📏 Vytváření různých velikostí ikon...")
    
    # Vytvoření složek
    Path("assets/icons/windows").mkdir(parents=True, exist_ok=True)
    Path("assets/icons/macos").mkdir(parents=True, exist_ok=True)
    Path("assets/icons/linux").mkdir(parents=True, exist_ok=True)
    
    # Velikosti pro různé platformy
    sizes = {
        'windows': [16, 32, 48, 256],
        'macos': [16, 32, 128, 256, 512],
        'linux': [16, 32, 48, 64, 128, 256]
    }
    
    for platform, size_list in sizes.items():
        print(f"   📱 {platform.upper()}:")
        for size in size_list:
            output_file = f"assets/icons/{platform}/icon_{size}.png"
            
            # ImageMagick příkaz pro změnu velikosti
            cmd = [
                IMAGEMAGICK_PATH,
                "convert",
                "BleedMakr.png",
                "-resize", f"{size}x{size}",
                "-background", "transparent",
                "-gravity", "center",
                "-extent", f"{size}x{size}",
                output_file
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"      ✅ {size}x{size} → {output_file}")
                else:
                    print(f"      ❌ Chyba při vytváření {size}x{size}")
            except Exception as e:
                print(f"      ❌ Chyba: {e}")

def create_ico_file():
    """Vytvoří ICO soubor pro Windows"""
    print("\n🪟 Vytváření ICO souboru pro Windows...")
    
    try:
        # Seznam PNG souborů pro Windows
        png_files = list(Path("assets/icons/windows").glob("icon_*.png"))
        png_files.sort(key=lambda x: int(x.stem.split('_')[1]))
        
        if png_files:
            # ImageMagick příkaz pro vytvoření ICO
            cmd = [IMAGEMAGICK_PATH, "convert"]
            for png_file in png_files:
                cmd.append(str(png_file))
            cmd.extend(["icon.ico"])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("   ✅ icon.ico vytvořen")
            else:
                print(f"   ❌ Chyba při vytváření ICO: {result.stderr}")
        else:
            print("   ❌ Nenalezeny PNG soubory pro Windows")
    
    except Exception as e:
        print(f"   ❌ Chyba při vytváření ICO: {e}")

def create_icns_file():
    """Vytvoří ICNS soubor pro macOS"""
    print("\n🍎 Vytváření ICNS souboru pro macOS...")
    
    try:
        # Seznam PNG souborů pro macOS
        png_files = list(Path("assets/icons/macos").glob("icon_*.png"))
        png_files.sort(key=lambda x: int(x.stem.split('_')[1]))
        
        if png_files:
            # ImageMagick příkaz pro vytvoření ICNS
            cmd = [IMAGEMAGICK_PATH, "convert"]
            for png_file in png_files:
                cmd.append(str(png_file))
            cmd.extend(["icon.icns"])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("   ✅ icon.icns vytvořen")
            else:
                print(f"   ❌ Chyba při vytváření ICNS: {result.stderr}")
        else:
            print("   ❌ Nenalezeny PNG soubory pro macOS")
    
    except Exception as e:
        print(f"   ❌ Chyba při vytváření ICNS: {e}")

def copy_linux_icon():
    """Zkopíruje největší PNG ikonu pro Linux"""
    print("\n🐧 Kopírování Linux ikony...")
    
    try:
        png_files = list(Path("assets/icons/linux").glob("icon_*.png"))
        if png_files:
            # Najít největší ikonu
            largest_png = max(png_files, key=lambda x: int(x.stem.split('_')[1]))
            shutil.copy2(largest_png, "icon.png")
            print(f"   ✅ Zkopírováno: {largest_png} → icon.png")
        else:
            print("   ❌ Nenalezeny PNG soubory pro Linux")
    
    except Exception as e:
        print(f"   ❌ Chyba při kopírování Linux ikony: {e}")

def verify_icons():
    """Ověří, že všechny ikony byly vytvořeny"""
    print("\n🔍 Ověření vytvořených ikon...")
    
    required_files = [
        "icon.ico",
        "icon.icns", 
        "icon.png"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ {file} ({size:,} bytes)")
        else:
            print(f"   ❌ {file} - CHYBÍ")

def main():
    """Hlavní funkce"""
    print("🎨 BleedMakr - Nastavení ikon")
    print("=" * 50)
    
    # Kontrola ImageMagick
    if not check_imagemagick():
        print("\n❌ ImageMagick není dostupný!")
        print("   Zkontrolujte cestu: C:\\Program Files\\ImageMagick-7.1.2-Q16-HDRI\\magick.exe")
        return False
    
    # Kontrola zdrojové ikony
    if not check_source_icon():
        print("\n❌ Zdrojová ikona BleedMakr.png není dostupná!")
        print("   Umístěte BleedMakr.png do root složky projektu")
        return False
    
    # Vytvoření různých velikostí
    create_icon_sizes()
    
    # Vytvoření platformových formátů
    create_ico_file()
    create_icns_file()
    copy_linux_icon()
    
    # Ověření
    verify_icons()
    
    print("\n" + "=" * 50)
    print("✅ Nastavení ikon dokončeno!")
    print("\n📋 Vytvořené soubory:")
    print("   - Windows: icon.ico")
    print("   - macOS: icon.icns")
    print("   - Linux: icon.png")
    print("   - Zdroje: assets/icons/")
    
    print("\n🚀 Nyní můžete spustit build s novými ikonami:")
    print("   python scripts/build_exe.py")
    
    return True

if __name__ == "__main__":
    main() 