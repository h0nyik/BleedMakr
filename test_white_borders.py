#!/usr/bin/env python3
"""
Testovací skript pro detekci bílých okrajů
"""

import os
import tempfile
from PIL import Image, ImageDraw
from spadavka_engine import SpadavkaEngine

def create_test_image_with_white_borders():
    """Vytvoří testovací obrázek s bílými okraji"""
    # Vytvoření obrázku 300x200 s bílými okraji
    img = Image.new('RGB', (300, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Vykreslení červeného obdélníku uprostřed (s bílými okraji)
    draw.rectangle([20, 15, 280, 185], fill='red', outline='blue', width=2)
    
    # Přidání textu
    draw.text((150, 100), "TEST", fill='white', anchor='mm')
    
    return img

def create_test_image_without_borders():
    """Vytvoří testovací obrázek bez bílých okrajů"""
    # Vytvoření obrázku 200x150 bez bílých okrajů
    img = Image.new('RGB', (200, 150), color='blue')
    draw = ImageDraw.Draw(img)
    
    # Vykreslení červeného kruhu
    draw.ellipse([50, 25, 150, 125], fill='red', outline='yellow', width=3)
    
    return img

def test_white_border_detection():
    """Test detekce bílých okrajů"""
    print("Test detekce bílých okrajů...")
    
    engine = SpadavkaEngine(spadavka_size_mm=3)
    
    # Test 1: Obrázek s bílými okraji
    print("\n📸 Test 1: Obrázek s bílými okraji")
    img_with_borders = create_test_image_with_white_borders()
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        img_with_borders.save(tmp.name)
        input_path = tmp.name
    
    try:
        output_path = input_path.replace('.png', '_spadavka.pdf')
        result, info = engine.generate_spadavka(input_path, output_path)
        
        print(f"   ✅ Výsledek: {result}")
        print(f"   📋 Metoda: {info}")
        print(f"   📁 Výstup: {os.path.basename(output_path)}")
        print(f"   📏 Velikost: {os.path.getsize(output_path)} bajtů")
        
    except Exception as e:
        print(f"   ❌ Chyba: {e}")
    finally:
        os.unlink(input_path)
        if os.path.exists(output_path):
            os.unlink(output_path)
    
    # Test 2: Obrázek bez bílých okrajů
    print("\n📸 Test 2: Obrázek bez bílých okrajů")
    img_without_borders = create_test_image_without_borders()
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        img_without_borders.save(tmp.name)
        input_path = tmp.name
    
    try:
        output_path = input_path.replace('.png', '_spadavka.pdf')
        result, info = engine.generate_spadavka(input_path, output_path)
        
        print(f"   ✅ Výsledek: {result}")
        print(f"   📋 Metoda: {info}")
        print(f"   📁 Výstup: {os.path.basename(output_path)}")
        print(f"   📏 Velikost: {os.path.getsize(output_path)} bajtů")
        
    except Exception as e:
        print(f"   ❌ Chyba: {e}")
    finally:
        os.unlink(input_path)
        if os.path.exists(output_path):
            os.unlink(output_path)

def test_border_detection_algorithm():
    """Test algoritmu detekce okrajů"""
    print("\n🔍 Test algoritmu detekce okrajů...")
    
    engine = SpadavkaEngine(spadavka_size_mm=3)
    
    # Vytvoření testovacího obrázku
    img = create_test_image_with_white_borders()
    
    # Test detekce bílých okrajů
    left, top, right, bottom = engine._detect_white_borders(img)
    
    print(f"   📐 Detekované okraje: left={left}, top={top}, right={right}, bottom={bottom}")
    print(f"   📏 Původní rozměry: {img.size}")
    print(f"   ✂️ Ořezané rozměry: {right-left} x {bottom-top}")
    
    # Kontrola, zda detekce dává smysl
    if left < right and top < bottom:
        print("   ✅ Detekce okrajů je logická")
    else:
        print("   ❌ Detekce okrajů je neplatná")

def main():
    """Hlavní testovací funkce"""
    print("Test inteligentní detekce bílých okrajů")
    print("=" * 60)
    
    test_border_detection_algorithm()
    test_white_border_detection()
    
    print("\n" + "=" * 60)
    print("🎉 Testy dokončeny!")

if __name__ == "__main__":
    main() 