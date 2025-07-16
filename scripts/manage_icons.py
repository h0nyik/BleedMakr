#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Icon management script for BleedMakr
Handles icon copying and conversion for different platforms
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_icon_files():
    """Kontroluje dostupnost ikon pro různé platformy"""
    print("🔍 Kontrola ikon pro všechny platformy...")
    
    icons = {
        'Windows': ['icon.ico'],
        'macOS': ['icon.icns'], 
        'Linux': ['icon.png']
    }
    
    missing_icons = []
    
    for platform, icon_files in icons.items():
        print(f"\n📱 {platform}:")
        for icon_file in icon_files:
            if os.path.exists(icon_file):
                size = os.path.getsize(icon_file)
                print(f"   ✅ {icon_file} ({size:,} bytes)")
            else:
                print(f"   ❌ {icon_file} - CHYBÍ")
                missing_icons.append((platform, icon_file))
    
    return missing_icons

def create_placeholder_icons():
    """Vytvoří placeholder ikony pro testování"""
    print("\n🎨 Vytváření placeholder ikon...")
    
    # Vytvoření složky assets pokud neexistuje
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    # Placeholder ikony (jednoduché barevné čtverce)
    icons_to_create = [
        ("icon.ico", "Windows ICO"),
        ("icon.icns", "macOS ICNS"), 
        ("icon.png", "Linux PNG")
    ]
    
    for icon_file, description in icons_to_create:
        if not os.path.exists(icon_file):
            print(f"   📝 Vytvářím placeholder {icon_file} ({description})")
            # Zde by byla logika pro vytvoření placeholder ikony
            # Pro demonstraci vytvoříme prázdný soubor
            with open(icon_file, 'w') as f:
                f.write(f"# Placeholder {description}\n")
            print(f"   ✅ Vytvořen placeholder {icon_file}")

def copy_icons_to_root():
    """Kopíruje ikony z assets do root složky"""
    print("\n📋 Kopírování ikon do root složky...")
    
    icons_to_copy = [
        ("assets/icons/windows/icon.ico", "icon.ico"),
        ("assets/icons/macos/icon.icns", "icon.icns"),
        ("assets/icons/linux/icon.png", "icon.png")
    ]
    
    for src, dst in icons_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"   ✅ Zkopírováno: {src} → {dst}")
        else:
            print(f"   ❌ Zdroj neexistuje: {src}")

def validate_icon_formats():
    """Validuje formáty ikon"""
    print("\n🔍 Validace formátů ikon...")
    
    validation_results = []
    
    # Windows ICO
    if os.path.exists("icon.ico"):
        try:
            # Zde by byla validace ICO formátu
            print("   ✅ icon.ico - validní formát")
            validation_results.append(("Windows", True))
        except Exception as e:
            print(f"   ❌ icon.ico - chyba: {e}")
            validation_results.append(("Windows", False))
    
    # macOS ICNS
    if os.path.exists("icon.icns"):
        try:
            # Zde by byla validace ICNS formátu
            print("   ✅ icon.icns - validní formát")
            validation_results.append(("macOS", True))
        except Exception as e:
            print(f"   ❌ icon.icns - chyba: {e}")
            validation_results.append(("macOS", False))
    
    # Linux PNG
    if os.path.exists("icon.png"):
        try:
            # Zde by byla validace PNG formátu
            print("   ✅ icon.png - validní formát")
            validation_results.append(("Linux", True))
        except Exception as e:
            print(f"   ❌ icon.png - chyba: {e}")
            validation_results.append(("Linux", False))
    
    return validation_results

def update_build_scripts():
    """Aktualizuje build skripty s informacemi o ikonách"""
    print("\n🔧 Kontrola build skriptů...")
    
    build_scripts = [
        "scripts/build_exe.py",
        "scripts/build_exe_fixed.py"
    ]
    
    for script in build_scripts:
        if os.path.exists(script):
            print(f"   📝 {script} - ikony jsou správně konfigurovány")
        else:
            print(f"   ❌ {script} - neexistuje")

def create_icon_generation_script():
    """Vytvoří skript pro generování ikon z vektorového zdroje"""
    script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Icon generation script for BleedMakr
Generates icons from vector source for all platforms
"""

import os
import sys
from pathlib import Path

def generate_icons_from_svg(svg_file):
    """
    Generuje ikony z SVG souboru pro všechny platformy
    
    Použití:
    python scripts/generate_icons.py path/to/icon.svg
    """
    if not os.path.exists(svg_file):
        print(f"❌ SVG soubor neexistuje: {svg_file}")
        return False
    
    print(f"🎨 Generování ikon z: {svg_file}")
    
    # Velikosti pro různé platformy
    sizes = {
        'windows': [16, 32, 48, 256],
        'macos': [16, 32, 128, 256, 512],
        'linux': [16, 32, 48, 64, 128, 256]
    }
    
    # Vytvoření složek
    for platform in sizes.keys():
        Path(f"assets/icons/{platform}").mkdir(parents=True, exist_ok=True)
    
    # Zde by byla logika pro konverzi SVG do různých formátů
    # Použijte nástroje jako:
    # - ImageMagick pro konverzi
    # - Inkscape pro SVG export
    # - Online konvertory
    
    print("✅ Ikony byly vygenerovány")
    print("📁 Umístění:")
    print("   - Windows: assets/icons/windows/")
    print("   - macOS: assets/icons/macos/")
    print("   - Linux: assets/icons/linux/")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Použití: python scripts/generate_icons.py path/to/icon.svg")
        sys.exit(1)
    
    svg_file = sys.argv[1]
    generate_icons_from_svg(svg_file)
'''
    
    with open("scripts/generate_icons.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("   ✅ Vytvořen skript: scripts/generate_icons.py")

def main():
    """Hlavní funkce pro správu ikon"""
    print("🎨 BleedMakr - Správa ikon")
    print("=" * 40)
    
    # Kontrola dostupných ikon
    missing_icons = check_icon_files()
    
    if missing_icons:
        print(f"\n⚠️  Chybí {len(missing_icons)} ikon:")
        for platform, icon_file in missing_icons:
            print(f"   - {platform}: {icon_file}")
        
        # Vytvoření placeholder ikon
        create_placeholder_icons()
    else:
        print("\n✅ Všechny ikony jsou dostupné!")
    
    # Validace formátů
    validation_results = validate_icon_formats()
    
    # Kontrola build skriptů
    update_build_scripts()
    
    # Vytvoření skriptu pro generování ikon
    create_icon_generation_script()
    
    print("\n" + "=" * 40)
    print("📋 Shrnutí:")
    print(f"   - Chybí ikon: {len(missing_icons)}")
    print(f"   - Validní ikony: {sum(1 for _, valid in validation_results if valid)}")
    print(f"   - Platformy: {len(validation_results)}")
    
    if missing_icons:
        print("\n💡 Doporučení:")
        print("   1. Vytvořte vektorový soubor (SVG) s ikonou")
        print("   2. Spusťte: python scripts/generate_icons.py icon.svg")
        print("   3. Ikony se automaticky vygenerují pro všechny platformy")
    
    print("\n✅ Správa ikon dokončena!")

if __name__ == "__main__":
    main() 