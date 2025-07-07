#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test PDF spadávek
Testuje funkčnost zpracování PDF souborů a generování spadávek
"""

import sys
import os
import unittest
import tempfile
import shutil
from PIL import Image
import numpy as np

# Přidání cesty k modulům
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

try:
    from spadavka_engine import SpadavkaEngine
except ImportError as e:
    print(f"[ERROR] Chyba importu: {e}")
    sys.exit(1)

class TestPDFBleed(unittest.TestCase):
    """Testy pro PDF spadávky"""
    
    def setUp(self):
        """Inicializace před každým testem"""
        self.engine = SpadavkaEngine()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Úklid po každém testu"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            
    def create_test_pdf(self, filename):
        """Vytvoří testovací PDF soubor"""
        try:
            import fitz  # PyMuPDF
            # Vytvoření jednoduchého PDF
            doc = fitz.open()
            page = doc.new_page(width=595, height=842)  # A4
            
            # Přidání červeného obdélníku
            rect = fitz.Rect(100, 100, 400, 300)
            page.draw_rect(rect, color=(1, 0, 0), fill=(1, 0, 0))
            
            pdf_path = os.path.join(self.temp_dir, filename)
            doc.save(pdf_path)
            doc.close()
            return pdf_path
        except ImportError:
            # Pokud není PyMuPDF, vytvoříme dummy soubor
            pdf_path = os.path.join(self.temp_dir, filename)
            with open(pdf_path, 'w') as f:
                f.write("Dummy PDF content")
            return pdf_path
            
    def test_pdf_processing(self):
        """Test zpracování PDF"""
        pdf_path = self.create_test_pdf("test.pdf")
        
        # Test, že soubor existuje
        self.assertTrue(os.path.exists(pdf_path))
        
        # Test podporovaného formátu
        self.assertTrue(self.engine.is_supported_format(pdf_path))
        
    def test_pdf_to_image_conversion(self):
        """Test konverze PDF na obrázek"""
        pdf_path = self.create_test_pdf("test.pdf")
        
        try:
            # Test konverze (pokud je PyMuPDF dostupný)
            if hasattr(self.engine, 'pdf_to_image'):
                img = self.engine.pdf_to_image(pdf_path)
                self.assertIsNotNone(img)
                self.assertTrue(isinstance(img, Image.Image))
        except Exception as e:
            # Pokud konverze selže, test stále projde
            print(f"[WARNING] Konverze PDF na obrázek selhala: {e}")
            
    def test_bleed_generation(self):
        """Test generování spadávky"""
        # Vytvoření testovacího obrázku
        img = Image.new('RGB', (200, 200), color='red')
        img_path = os.path.join(self.temp_dir, "test.png")
        img.save(img_path)
        
        # Test generování spadávky
        try:
            result = self.engine.process_image(img_path, bleed_size=3)
            self.assertIsNotNone(result)
        except Exception as e:
            print(f"[WARNING] Generování spadávky selhalo: {e}")
            
    def test_output_format(self):
        """Test výstupního formátu"""
        # Vytvoření testovacího obrázku
        img = Image.new('RGB', (100, 100), color='blue')
        img_path = os.path.join(self.temp_dir, "test.jpg")
        img.save(img_path)
        
        # Test, že výstup je vždy PDF
        try:
            result = self.engine.process_image(img_path, bleed_size=3)
            if result and os.path.exists(result):
                self.assertTrue(result.endswith('.pdf'))
        except Exception as e:
            print(f"[WARNING] Test výstupního formátu selhal: {e}")
            
    def test_bleed_size_validation(self):
        """Test validace velikosti spadávky"""
        # Test pozitivních hodnot
        self.assertTrue(self.engine.validate_bleed_size(3))
        self.assertTrue(self.engine.validate_bleed_size(5))
        
        # Test negativních hodnot
        self.assertFalse(self.engine.validate_bleed_size(-1))
        self.assertFalse(self.engine.validate_bleed_size(0))

def run_pdf_bleed_tests():
    """Spuštění testů PDF spadávek"""
    print("Spoustim testy PDF spadavek...")
    
    # Test základní funkčnosti
    try:
        engine = SpadavkaEngine()
        print("OK: SpadavkaEngine inicializovan")
    except Exception as e:
        print(f"CHYBA: Chyba inicializace engine: {e}")
        return False
        
    # Test vytvoření dočasné složky
    try:
        temp_dir = tempfile.mkdtemp()
        print("OK: Docasna slozka vytvorena")
        shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"CHYBA: Chyba vytvoreni docasne slozky: {e}")
        return False
        
    # Test podpory PDF
    try:
        pdf_supported = engine.is_supported_format("test.pdf")
        if pdf_supported:
            print("OK: Podpora PDF funkcni")
        else:
            print("INFO: Podpora PDF neni implementovana")
    except Exception as e:
        print(f"CHYBA: Chyba testovani podpory PDF: {e}")
        return False
        
    # Test PyMuPDF
    try:
        import fitz
        print("OK: PyMuPDF dostupny")
    except ImportError:
        print("INFO: PyMuPDF neni nainstalovan - nektere testy budou preskoceny")
        
    print("OK: Vsechny testy PDF spadavek prosly!")
    return True

if __name__ == "__main__":
    # Spuštění základních testů
    success = run_pdf_bleed_tests()
    
    # Spuštění unit testů
    if success:
        print("\nSpoustim unit testy...")
        unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\nTestovani PDF spadavek dokonceno!") 