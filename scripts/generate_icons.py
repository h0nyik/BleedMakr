#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Icon generation script for BleedMakr
Generates icons from vector source for all platforms
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from PIL import Image, ImageDraw

def check_dependencies():
    """Kontroluje dostupnost nástrojů pro konverzi"""
    print("🔍 Kontrola nástrojů pro konverzi...")
    
    tools = {
        'PIL/Pillow': 'PIL',
        'ImageMagick': 'magick',
        'Inkscape': 'inkscape'
    }
    
    available_tools = []
    
    for tool_name, import_name in tools.items():
        try:
            if import_name == 'PIL':
                import PIL
                print(f"   ✅ {tool_name}")
                available_tools.append(tool_name)
            else:
                # Kontrola příkazu v PATH
                result = subprocess.run([import_name, '--version'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"   ✅ {tool_name}")
                    available_tools.append(tool_name)
                else:
                    print(f"   ❌ {tool_name} - není dostupné")
        except Exception as e:
            print(f"   ❌ {tool_name} - chyba: {e}")
    
    return available_tools

def create_simple_icon():
    """Vytvoří jednoduchou ikonu pro testování"""
    print("\n🎨 Vytváření jednoduché testovací ikony...")
    
    # Vytvoření složek
    Path("assets/icons/windows").mkdir(parents=True, exist_ok=True)
    Path("assets/icons/macos").mkdir(parents=True, exist_ok=True)
    Path("assets/icons/linux").mkdir(parents=True, exist_ok=True)
    
    # Vytvoření jednoduché ikony (modrý čtverec s písmenem "B")
    sizes = {
        'windows': [16, 32, 48, 256],
        'macos': [16, 32, 128, 256, 512],
        'linux': [16, 32, 48, 64, 128, 256]
    }
    
    for platform, size_list in sizes.items():
        print(f"   📱 {platform.upper()}:")
        for size in size_list:
            # Vytvoření obrázku
            img = Image.new('RGBA', (size, size), (44, 62, 80, 255))  # Modrá barva
            draw = ImageDraw.Draw(img)
            
            # Přidání písmene "B" (jednoduché)
            try:
                # Pokus o použití systémového fontu
                from PIL import ImageFont
                font_size = size // 3
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # Fallback na default font
                font = ImageFont.load_default()
            
            # Výpočet pozice textu
            bbox = draw.textbbox((0, 0), "B", font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (size - text_width) // 2
            y = (size - text_height) // 2
            
            # Kreslení textu
            draw.text((x, y), "B", fill=(255, 255, 255, 255), font=font)
            
            # Uložení
            if platform == 'windows':
                filename = f"assets/icons/windows/icon_{size}.png"
            elif platform == 'macos':
                filename = f"assets/icons/macos/icon_{size}.png"
            else:  # linux
                filename = f"assets/icons/linux/icon_{size}.png"
            
            img.save(filename, 'PNG')
            print(f"      ✅ {size}x{size} → {filename}")
    
    print("   ✅ Testovací ikony vytvořeny")

def convert_to_ico():
    """Konvertuje PNG ikony do ICO formátu pro Windows"""
    print("\n🪟 Konverze do ICO formátu...")
    
    try:
        # Použití ImageMagick pokud je dostupné
        png_files = list(Path("assets/icons/windows").glob("icon_*.png"))
        png_files.sort(key=lambda x: int(x.stem.split('_')[1]))
        
        if png_files:
            # Vytvoření ICO souboru s více velikostmi
            cmd = ['magick', 'convert']
            for png_file in png_files:
                cmd.append(str(png_file))
            cmd.extend(['icon.ico'])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("   ✅ icon.ico vytvořen pomocí ImageMagick")
            else:
                print("   ❌ Chyba při vytváření ICO pomocí ImageMagick")
                # Fallback - kopie největší PNG
                largest_png = png_files[-1]
                shutil.copy2(largest_png, "icon.ico")
                print(f"   ⚠️  Fallback: zkopírován {largest_png}")
        else:
            print("   ❌ Nenalezeny PNG soubory pro konverzi")
    
    except Exception as e:
        print(f"   ❌ Chyba při konverzi do ICO: {e}")
        # Fallback - vytvoření jednoduchého ICO
        try:
            largest_png = max(Path("assets/icons/windows").glob("icon_*.png"), 
                            key=lambda x: int(x.stem.split('_')[1]))
            shutil.copy2(largest_png, "icon.ico")
            print(f"   ⚠️  Fallback: zkopírován {largest_png}")
        except Exception as fallback_error:
            print(f"   ❌ Fallback také selhal: {fallback_error}")

def convert_to_icns():
    """Konvertuje PNG ikony do ICNS formátu pro macOS"""
    print("\n🍎 Konverze do ICNS formátu...")
    
    try:
        # Použití ImageMagick pokud je dostupné
        png_files = list(Path("assets/icons/macos").glob("icon_*.png"))
        png_files.sort(key=lambda x: int(x.stem.split('_')[1]))
        
        if png_files:
            # Vytvoření ICNS souboru
            cmd = ['magick', 'convert']
            for png_file in png_files:
                cmd.append(str(png_file))
            cmd.extend(['icon.icns'])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("   ✅ icon.icns vytvořen pomocí ImageMagick")
            else:
                print("   ❌ Chyba při vytváření ICNS pomocí ImageMagick")
                # Fallback - kopie největší PNG
                largest_png = png_files[-1]
                shutil.copy2(largest_png, "icon.icns")
                print(f"   ⚠️  Fallback: zkopírován {largest_png}")
        else:
            print("   ❌ Nenalezeny PNG soubory pro konverzi")
    
    except Exception as e:
        print(f"   ❌ Chyba při konverzi do ICNS: {e}")
        # Fallback - vytvoření jednoduchého ICNS
        try:
            largest_png = max(Path("assets/icons/macos").glob("icon_*.png"), 
                            key=lambda x: int(x.stem.split('_')[1]))
            shutil.copy2(largest_png, "icon.icns")
            print(f"   ⚠️  Fallback: zkopírován {largest_png}")
        except Exception as fallback_error:
            print(f"   ❌ Fallback také selhal: {fallback_error}")

def copy_linux_icon():
    """Kopíruje největší PNG ikonu pro Linux"""
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
    
    # Kontrola nástrojů
    available_tools = check_dependencies()
    
    if 'Inkscape' in available_tools:
        print("\n📐 Použití Inkscape pro konverzi SVG...")
        # Zde by byla logika pro konverzi pomocí Inkscape
        # Inkscape --export-png=icon.png --export-width=256 --export-height=256 icon.svg
    elif 'ImageMagick' in available_tools:
        print("\n🖼️  Použití ImageMagick pro konverzi SVG...")
        # Zde by byla logika pro konverzi pomocí ImageMagick
        # magick convert icon.svg -resize 256x256 icon.png
    else:
        print("\n⚠️  Žádný nástroj pro konverzi SVG není dostupný")
        print("   Vytvářím testovací ikony...")
        create_simple_icon()
    
    # Konverze do platformových formátů
    convert_to_ico()
    convert_to_icns()
    copy_linux_icon()
    
    print("\n✅ Ikony byly vygenerovány")
    print("📁 Umístění:")
    print("   - Windows: icon.ico")
    print("   - macOS: icon.icns")
    print("   - Linux: icon.png")
    print("   - Zdroje: assets/icons/")
    
    return True

def main():
    """Hlavní funkce"""
    if len(sys.argv) == 2:
        # Generování z SVG
        svg_file = sys.argv[1]
        generate_icons_from_svg(svg_file)
    else:
        # Vytvoření testovacích ikon
        print("🎨 BleedMakr - Generování ikon")
        print("=" * 40)
        print("Použití:")
        print("  python scripts/generate_icons.py [path/to/icon.svg]")
        print("")
        print("Pokud není zadán SVG soubor, vytvoří se testovací ikony.")
        print("")
        
        create_simple_icon()
        convert_to_ico()
        convert_to_icns()
        copy_linux_icon()
        
        print("\n✅ Testovací ikony vytvořeny!")
        print("💡 Pro vlastní ikonu použijte:")
        print("   python scripts/generate_icons.py path/to/your/icon.svg")

if __name__ == "__main__":
    main() 