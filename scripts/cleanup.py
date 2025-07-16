#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cleanup script for BleedMakr build artifacts
Removes temporary files and build artifacts
"""

import os
import shutil
import glob
from pathlib import Path

def cleanup_build_artifacts():
    """Odstraní build artifacts a dočasné soubory"""
    print("🧹 Úklid build artifacts...")
    
    # Seznam souborů a složek k odstranění
    cleanup_items = [
        # PyInstaller artifacts
        "build/",
        "dist/",
        "BleedMakr.spec",
        "version_info.txt",
        
        # Dočasné soubory
        "temp_sign_*.ps1",
        "*.log",
        "*.tmp",
        
        # Testovací soubory
        "test_*.exe",
        "test_*.app",
        "test_*.bin",
        
        # Cache soubory
        "__pycache__/",
        "*.pyc",
        "*.pyo",
        
        # IDE soubory
        ".vscode/",
        ".idea/",
        "*.swp",
        "*.swo",
        
        # Backup soubory
        "*.bak",
        "*.backup",
        "*~"
    ]
    
    removed_count = 0
    
    for item in cleanup_items:
        if os.path.exists(item):
            try:
                if os.path.isfile(item):
                    os.remove(item)
                    print(f"   ✅ Odstraněn soubor: {item}")
                    removed_count += 1
                elif os.path.isdir(item):
                    shutil.rmtree(item)
                    print(f"   ✅ Odstraněna složka: {item}")
                    removed_count += 1
            except Exception as e:
                print(f"   ❌ Chyba při odstraňování {item}: {e}")
        
        # Pro glob patterny
        if "*" in item:
            for matched_item in glob.glob(item):
                try:
                    if os.path.isfile(matched_item):
                        os.remove(matched_item)
                        print(f"   ✅ Odstraněn soubor: {matched_item}")
                        removed_count += 1
                    elif os.path.isdir(matched_item):
                        shutil.rmtree(matched_item)
                        print(f"   ✅ Odstraněna složka: {matched_item}")
                        removed_count += 1
                except Exception as e:
                    print(f"   ❌ Chyba při odstraňování {matched_item}: {e}")
    
    return removed_count

def cleanup_icon_artifacts():
    """Odstraní dočasné ikony, ale zachová finální ikony"""
    print("\n🎨 Úklid dočasných ikon...")
    
    # Zachovat finální ikony
    keep_icons = [
        "icon.ico",
        "icon.icns", 
        "icon.png"
    ]
    
    # Odstranit dočasné ikony v assets
    temp_icon_dirs = [
        "assets/icons/windows/",
        "assets/icons/macos/",
        "assets/icons/linux/"
    ]
    
    removed_count = 0
    
    for icon_dir in temp_icon_dirs:
        if os.path.exists(icon_dir):
            try:
                shutil.rmtree(icon_dir)
                print(f"   ✅ Odstraněna složka: {icon_dir}")
                removed_count += 1
            except Exception as e:
                print(f"   ❌ Chyba při odstraňování {icon_dir}: {e}")
    
    # Zachovat finální ikony
    for icon in keep_icons:
        if os.path.exists(icon):
            print(f"   📁 Zachována ikona: {icon}")
    
    return removed_count

def cleanup_assets_structure():
    """Vyčistí assets strukturu"""
    print("\n📁 Úklid assets struktury...")
    
    # Odstranit prázdné složky
    empty_dirs = [
        "assets/icons/",
        "assets/"
    ]
    
    removed_count = 0
    
    for dir_path in empty_dirs:
        if os.path.exists(dir_path):
            try:
                # Kontrola, zda je složka prázdná
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    print(f"   ✅ Odstraněna prázdná složka: {dir_path}")
                    removed_count += 1
            except Exception as e:
                print(f"   ❌ Chyba při odstraňování {dir_path}: {e}")
    
    return removed_count

def verify_final_state():
    """Ověří finální stav po úklidu"""
    print("\n🔍 Ověření finálního stavu...")
    
    # Kontrola finálních ikon
    final_icons = [
        "icon.ico",
        "icon.icns",
        "icon.png"
    ]
    
    for icon in final_icons:
        if os.path.exists(icon):
            size = os.path.getsize(icon)
            print(f"   ✅ {icon} ({size:,} bytes)")
        else:
            print(f"   ❌ {icon} - CHYBÍ")
    
    # Kontrola, že build artifacts jsou odstraněny
    build_artifacts = [
        "build/",
        "dist/",
        "BleedMakr.spec"
    ]
    
    for artifact in build_artifacts:
        if os.path.exists(artifact):
            print(f"   ⚠️  {artifact} - stále existuje")
        else:
            print(f"   ✅ {artifact} - odstraněn")

def main():
    """Hlavní funkce pro úklid"""
    print("🧹 BleedMakr - Úklid projektu")
    print("=" * 40)
    
    # Úklid build artifacts
    build_removed = cleanup_build_artifacts()
    
    # Úklid dočasných ikon
    icon_removed = cleanup_icon_artifacts()
    
    # Úklid assets struktury
    assets_removed = cleanup_assets_structure()
    
    # Ověření finálního stavu
    verify_final_state()
    
    print("\n" + "=" * 40)
    print("📋 Shrnutí úklidu:")
    print(f"   - Build artifacts: {build_removed}")
    print(f"   - Dočasné ikony: {icon_removed}")
    print(f"   - Prázdné složky: {assets_removed}")
    print(f"   - Celkem odstraněno: {build_removed + icon_removed + assets_removed}")
    
    print("\n✅ Úklid dokončen!")
    print("💡 Finální ikony jsou zachovány pro build")

if __name__ == "__main__":
    main() 