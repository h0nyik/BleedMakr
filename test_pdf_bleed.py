#!/usr/bin/env python3
"""
Testovací skript pro ověření zpracování PDF s průhlednými okraji
"""

import os
import tempfile
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from spadavka_engine import SpadavkaEngine

def create_test_pdf_with_transparent_borders():
    """Vytvoří testovací PDF s průhlednými okraji"""
    # Vytvoření dočasného PDF
    temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    temp_pdf.close()
    
    # Vytvoření PDF s průhlednými okraji
    c = canvas.Canvas(temp_pdf.name, pagesize=A4)
    width, height = A4
    
    # Vykreslení červeného obdélníku uprostřed (s průhlednými okraji)
    margin = 50
    c.setFillColorRGB(1, 0, 0)  # Červená
    c.rect(margin, margin, width - 2*margin, height - 2*margin, fill=1)
    
    # Přidání textu
    c.setFillColorRGB(1, 1, 1)  # Bílá
    c.setFont("Helvetica", 24)
    c.drawString(width/2 - 50, height/2, "TEST PDF")
    
    c.save()
    return temp_pdf.name

def create_test_pdf_without_borders():
    """Vytvoří testovací PDF bez průhledných okrajů"""
    # Vytvoření dočasného PDF
    temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    temp_pdf.close()
    
    # Vytvoření PDF bez průhledných okrajů
    c = canvas.Canvas(temp_pdf.name, pagesize=A4)
    width, height = A4
    
    # Vykreslení modrého pozadí přes celou stránku
    c.setFillColorRGB(0, 0, 1)  # Modrá
    c.rect(0, 0, width, height, fill=1)
    
    # Přidání červeného kruhu
    c.setFillColorRGB(1, 0, 0)  # Červená
    c.circle(width/2, height/2, 100, fill=1)
    
    c.save()
    return temp_pdf.name

def create_test_pdf_with_light_borders():
    """Vytvoří testovací PDF se světlými okraji (šedými)"""
    # Vytvoření dočasného PDF
    temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    temp_pdf.close()
    
    # Vytvoření PDF se světlými okraji
    c = canvas.Canvas(temp_pdf.name, pagesize=A4)
    width, height = A4
    
    # Vykreslení světle šedého pozadí (simulace světlých okrajů)
    c.setFillColorRGB(0.95, 0.95, 0.95)  # Světle šedá
    c.rect(0, 0, width, height, fill=1)
    
    # Vykreslení červeného obdélníku uprostřed
    margin = 100
    c.setFillColorRGB(1, 0, 0)  # Červená
    c.rect(margin, margin, width - 2*margin, height - 2*margin, fill=1)
    
    # Přidání textu
    c.setFillColorRGB(1, 1, 1)  # Bílá
    c.setFont("Helvetica", 24)
    c.drawString(width/2 - 50, height/2, "TEST PDF")
    
    c.save()
    return temp_pdf.name

def create_test_pdf_with_white_borders():
    """Vytvoří testovací PDF s bílými okraji"""
    # Vytvoření dočasného PDF
    temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    temp_pdf.close()
    
    # Vytvoření PDF s bílými okraji
    c = canvas.Canvas(temp_pdf.name, pagesize=A4)
    width, height = A4
    
    # Vykreslení bílého pozadí
    c.setFillColorRGB(1, 1, 1)  # Bílá
    c.rect(0, 0, width, height, fill=1)
    
    # Vykreslení modrého obdélníku uprostřed
    margin = 150
    c.setFillColorRGB(0, 0, 1)  # Modrá
    c.rect(margin, margin, width - 2*margin, height - 2*margin, fill=1)
    
    # Přidání textu
    c.setFillColorRGB(1, 1, 1)  # Bílá
    c.setFont("Helvetica", 24)
    c.drawString(width/2 - 50, height/2, "TEST PDF")
    
    c.save()
    return temp_pdf.name

def test_pdf_processing():
    """Test zpracování PDF"""
    print("🧪 Test zpracování PDF...")
    
    engine = SpadavkaEngine(spadavka_size_mm=3)
    
    # Test 1: PDF s průhlednými okraji
    print("\n📄 Test 1: PDF s průhlednými okraji")
    pdf_with_borders = create_test_pdf_with_transparent_borders()
    
    try:
        output_path = pdf_with_borders.replace('.pdf', '_spadavka.pdf')
        result, info = engine.generate_spadavka(pdf_with_borders, output_path)
        
        print(f"   ✅ Výsledek: {result}")
        print(f"   📋 Metoda: {info}")
        print(f"   📁 Výstup: {os.path.basename(output_path)}")
        print(f"   📏 Velikost: {os.path.getsize(output_path)} bajtů")
        
    except Exception as e:
        print(f"   ❌ Chyba: {e}")
    finally:
        os.unlink(pdf_with_borders)
        if os.path.exists(output_path):
            os.unlink(output_path)
    
    # Test 2: PDF se světlými okraji
    print("\n📄 Test 2: PDF se světlými okraji")
    pdf_with_light_borders = create_test_pdf_with_light_borders()
    
    try:
        output_path = pdf_with_light_borders.replace('.pdf', '_spadavka.pdf')
        result, info = engine.generate_spadavka(pdf_with_light_borders, output_path)
        
        print(f"   ✅ Výsledek: {result}")
        print(f"   📋 Metoda: {info}")
        print(f"   📁 Výstup: {os.path.basename(output_path)}")
        print(f"   📏 Velikost: {os.path.getsize(output_path)} bajtů")
        
    except Exception as e:
        print(f"   ❌ Chyba: {e}")
    finally:
        os.unlink(pdf_with_light_borders)
        if os.path.exists(output_path):
            os.unlink(output_path)
    
    # Test 3: PDF s bílými okraji
    print("\n📄 Test 3: PDF s bílými okraji")
    pdf_with_white_borders = create_test_pdf_with_white_borders()
    
    try:
        output_path = pdf_with_white_borders.replace('.pdf', '_spadavka.pdf')
        result, info = engine.generate_spadavka(pdf_with_white_borders, output_path)
        
        print(f"   ✅ Výsledek: {result}")
        print(f"   📋 Metoda: {info}")
        print(f"   📁 Výstup: {os.path.basename(output_path)}")
        print(f"   📏 Velikost: {os.path.getsize(output_path)} bajtů")
        
    except Exception as e:
        print(f"   ❌ Chyba: {e}")
    finally:
        os.unlink(pdf_with_white_borders)
        if os.path.exists(output_path):
            os.unlink(output_path)
    
    # Test 4: PDF bez průhledných okrajů
    print("\n📄 Test 4: PDF bez průhledných okrajů")
    pdf_without_borders = create_test_pdf_without_borders()
    
    try:
        output_path = pdf_without_borders.replace('.pdf', '_spadavka.pdf')
        result, info = engine.generate_spadavka(pdf_without_borders, output_path)
        
        print(f"   ✅ Výsledek: {result}")
        print(f"   📋 Metoda: {info}")
        print(f"   📁 Výstup: {os.path.basename(output_path)}")
        print(f"   📏 Velikost: {os.path.getsize(output_path)} bajtů")
        
    except Exception as e:
        print(f"   ❌ Chyba: {e}")
    finally:
        os.unlink(pdf_without_borders)
        if os.path.exists(output_path):
            os.unlink(output_path)

def test_pdf_conversion():
    """Test konverze PDF na obrázek"""
    print("\n🔄 Test konverze PDF na obrázek...")
    
    # Vytvoření testovacího PDF
    pdf_path = create_test_pdf_with_transparent_borders()
    
    try:
        import fitz
        import io
        
        # Otevření PDF
        doc = fitz.open(pdf_path)
        page = doc[0]
        
        # Konverze na obrázek s vysokým rozlišením
        dpi = 300
        scale_factor = dpi / 72
        matrix = fitz.Matrix(scale_factor, scale_factor)
        pix = page.get_pixmap(matrix=matrix, alpha=True)
        
        # Konverze na PIL Image
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        print(f"   📐 Původní PDF rozměry: {page.rect.width} x {page.rect.height} bodů")
        print(f"   🖼️ Konvertovaný obrázek: {img.size} pixelů")
        print(f"   🎨 Režim obrázku: {img.mode}")
        
        # Kontrola průhlednosti
        if img.mode == 'RGBA':
            alpha = img.split()[-1]
            transparent_pixels = sum(1 for pixel in alpha.getdata() if pixel < 128)
            total_pixels = img.size[0] * img.size[1]
            transparency_percent = (transparent_pixels / total_pixels) * 100
            print(f"   🔍 Průhledné pixely: {transparent_pixels}/{total_pixels} ({transparency_percent:.1f}%)")
        
        doc.close()
        
    except Exception as e:
        print(f"   ❌ Chyba při konverzi: {e}")
    finally:
        os.unlink(pdf_path)

def main():
    """Hlavní testovací funkce"""
    print("Test nové funkcionality zpracování PDF")
    print("=" * 60)
    
    test_pdf_conversion()
    test_pdf_processing()
    
    print("\n" + "=" * 60)
    print("🎉 Testy dokončeny!")

if __name__ == "__main__":
    main() 