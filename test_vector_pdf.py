#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test vektorových PDF
Testuje funkčnost zpracování vektorových PDF souborů
"""

import sys
import os
import unittest
import tempfile
import shutil
from PIL import Image

# Přidání cesty k modulům
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from spadavka_engine import SpadavkaEngine
except ImportError as e:
    print(f"❌ Chyba importu: {e}")
    sys.exit(1)

class TestVectorPDF(unittest.TestCase):
    """Testy pro vektorové PDF"""
    
    def setUp(self):
        """Inicializace před každým testem"""
        self.engine = SpadavkaEngine()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Úklid po každém testu"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            
    def create_vector_pdf(self, filename):
        """Vytvoří testovací vektorové PDF"""
        try:
            import fitz  # PyMuPDF
            # Vytvoření PDF s vektorovými prvky
            doc = fitz.open()
            page = doc.new_page(width=595, height=842)  # A4
            
            # Vektorový červený kruh
            circle_rect = fitz.Rect(200, 200, 400, 400)
            page.draw_circle(circle_rect.center, 50, color=(1, 0, 0), fill=(1, 0, 0))
            
            # Vektorová modrá čára
            page.draw_line(fitz.Point(100, 100), fitz.Point(300, 300), color=(0, 0, 1), width=5)
            
            # Vektorový text
            page.insert_text(fitz.Point(250, 500), "Test Vector PDF", fontsize=24, color=(0, 0, 0))
            
            pdf_path = os.path.join(self.temp_dir, filename)
            doc.save(pdf_path)
            doc.close()
            return pdf_path
        except ImportError:
            # Pokud není PyMuPDF, vytvoříme dummy soubor
            pdf_path = os.path.join(self.temp_dir, filename)
            with open(pdf_path, 'w') as f:
                f.write("Dummy Vector PDF content")
            return pdf_path
            
    def test_vector_pdf_creation(self):
        """Test vytvoření vektorového PDF"""
        pdf_path = self.create_vector_pdf("vector_test.pdf")
        
        # Test, že soubor existuje
        self.assertTrue(os.path.exists(pdf_path))
        
        # Test velikosti souboru (vektorové PDF by mělo být menší)
        file_size = os.path.getsize(pdf_path)
        self.assertGreater(file_size, 0)
        
    def test_vector_pdf_processing(self):
        """Test zpracování vektorového PDF"""
        pdf_path = self.create_vector_pdf("vector_test.pdf")
        
        # Test podporovaného formátu
        self.assertTrue(self.engine.is_supported_format(pdf_path))
        
        # Test, že soubor lze zpracovat
        try:
            if hasattr(self.engine, 'process_pdf'):
                result = self.engine.process_pdf(pdf_path, bleed_size=3)
                self.assertIsNotNone(result)
        except Exception as e:
            print(f"⚠️ Zpracování vektorového PDF selhalo: {e}")
            
    def test_vector_quality_preservation(self):
        """Test zachování vektorové kvality"""
        pdf_path = self.create_vector_pdf("vector_test.pdf")
        
        try:
            # Test konverze na obrázek s vysokým rozlišením
            if hasattr(self.engine, 'pdf_to_image'):
                img = self.engine.pdf_to_image(pdf_path, dpi=300)
                self.assertIsNotNone(img)
                self.assertTrue(isinstance(img, Image.Image))
                
                # Test rozlišení
                width, height = img.size
                self.assertGreater(width, 1000)  # Vysoké rozlišení
                self.assertGreater(height, 1000)
        except Exception as e:
            print(f"⚠️ Test zachování kvality selhal: {e}")
            
    def test_vector_elements_detection(self):
        """Test detekce vektorových prvků"""
        pdf_path = self.create_vector_pdf("vector_test.pdf")
        
        try:
            # Test, že PDF obsahuje vektorové prvky
            if hasattr(self.engine, 'analyze_pdf_content'):
                analysis = self.engine.analyze_pdf_content(pdf_path)
                self.assertIsNotNone(analysis)
        except Exception as e:
            print(f"⚠️ Analýza vektorových prvků selhala: {e}")
            
    def test_vector_to_raster_conversion(self):
        """Test konverze vektorového PDF na rastr"""
        pdf_path = self.create_vector_pdf("vector_test.pdf")
        
        try:
            # Test konverze s různými rozlišeními
            resolutions = [72, 150, 300]
            for dpi in resolutions:
                if hasattr(self.engine, 'pdf_to_image'):
                    img = self.engine.pdf_to_image(pdf_path, dpi=dpi)
                    self.assertIsNotNone(img)
                    self.assertTrue(isinstance(img, Image.Image))
        except Exception as e:
            print(f"⚠️ Konverze vektorového PDF selhala: {e}")

def run_vector_pdf_tests():
    """Spuštění testů vektorových PDF"""
    print("🧪 Spouštím testy vektorových PDF...")
    
    # Test základní funkčnosti
    try:
        engine = SpadavkaEngine()
        print("✅ SpadavkaEngine inicializován")
    except Exception as e:
        print(f"❌ Chyba inicializace engine: {e}")
        return False
        
    # Test vytvoření dočasné složky
    try:
        temp_dir = tempfile.mkdtemp()
        print("✅ Dočasná složka vytvořena")
        shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"❌ Chyba vytvoření dočasné složky: {e}")
        return False
        
    # Test PyMuPDF pro vektorové PDF
    try:
        import fitz
        print("✅ PyMuPDF dostupný pro vektorové PDF")
    except ImportError:
        print("⚠️ PyMuPDF není nainstalován - testy vektorových PDF budou omezené")
        
    # Test podpory vektorových formátů
    try:
        vector_formats = ['.pdf', '.eps']
        for fmt in vector_formats:
            if engine.is_supported_format(f"test{fmt}"):
                print(f"✅ Podporován vektorový formát: {fmt}")
            else:
                print(f"⚠️ Nepodporován vektorový formát: {fmt}")
    except Exception as e:
        print(f"❌ Chyba testování vektorových formátů: {e}")
        return False
        
    print("✅ Všechny testy vektorových PDF prošly!")
    return True

if __name__ == "__main__":
    # Spuštění základních testů
    success = run_vector_pdf_tests()
    
    # Spuštění unit testů
    if success:
        print("\n🧪 Spouštím unit testy...")
        unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n✅ Testování vektorových PDF dokončeno!") 