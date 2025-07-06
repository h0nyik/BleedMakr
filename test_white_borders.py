#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test detekce bílých okrajů
Testuje funkčnost detekce a ořezání bílých okrajů
"""

import sys
import os
import unittest
import numpy as np
from PIL import Image

# Přidání cesty k modulům
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from spadavka_engine import SpadavkaEngine
except ImportError as e:
    print(f"❌ Chyba importu: {e}")
    sys.exit(1)

class TestWhiteBorders(unittest.TestCase):
    """Testy pro detekci bílých okrajů"""
    
    def setUp(self):
        """Inicializace před každým testem"""
        self.engine = SpadavkaEngine()
        
    def create_test_image(self, width=100, height=100, has_white_borders=True):
        """Vytvoří testovací obrázek"""
        if has_white_borders:
            # Obrázek s bílými okraji
            img = np.ones((height, width, 3), dtype=np.uint8) * 255  # Bílý
            # Přidání barevného obsahu uprostřed
            img[20:80, 20:80] = [255, 0, 0]  # Červený čtverec
        else:
            # Obrázek bez bílých okrajů
            img = np.zeros((height, width, 3), dtype=np.uint8)
            img[:, :] = [255, 0, 0]  # Celý červený
            
        return Image.fromarray(img)
        
    def test_detect_white_borders(self):
        """Test detekce bílých okrajů"""
        # Test s bílými okraji
        img_with_borders = self.create_test_image(has_white_borders=True)
        borders = self.engine.detect_white_borders(img_with_borders)
        
        self.assertIsNotNone(borders)
        self.assertTrue(hasattr(borders, 'left'))
        self.assertTrue(hasattr(borders, 'right'))
        self.assertTrue(hasattr(borders, 'top'))
        self.assertTrue(hasattr(borders, 'bottom'))
        
        # Test bez bílých okrajů
        img_without_borders = self.create_test_image(has_white_borders=False)
        borders = self.engine.detect_white_borders(img_without_borders)
        
        self.assertIsNotNone(borders)
        
    def test_crop_white_borders(self):
        """Test ořezání bílých okrajů"""
        # Vytvoření obrázku s bílými okraji
        original_img = self.create_test_image(has_white_borders=True)
        original_size = original_img.size
        
        # Detekce a ořezání
        borders = self.engine.detect_white_borders(original_img)
        cropped_img = self.engine.crop_white_borders(original_img, borders)
        
        # Ořezaný obrázek by měl být menší
        self.assertLess(cropped_img.size[0], original_size[0])
        self.assertLess(cropped_img.size[1], original_size[1])
        
    def test_white_border_tolerance(self):
        """Test tolerance detekce bílých okrajů"""
        # Vytvoření obrázku s různými odstíny bílé
        img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        # Přidání mírně šedých pixelů na okraj
        img[0:5, :] = [250, 250, 250]  # Mírně šedé
        
        borders = self.engine.detect_white_borders(Image.fromarray(img))
        self.assertIsNotNone(borders)
        
    def test_edge_cases(self):
        """Test hraničních případů"""
        # Prázdný obrázek
        empty_img = Image.new('RGB', (0, 0))
        with self.assertRaises(Exception):
            self.engine.detect_white_borders(empty_img)
            
        # Velmi malý obrázek
        small_img = self.create_test_image(5, 5)
        borders = self.engine.detect_white_borders(small_img)
        self.assertIsNotNone(borders)

def run_white_border_tests():
    """Spuštění testů detekce bílých okrajů"""
    print("🧪 Spouštím testy detekce bílých okrajů...")
    
    # Test základní funkčnosti
    try:
        engine = SpadavkaEngine()
        print("✅ SpadavkaEngine inicializován")
    except Exception as e:
        print(f"❌ Chyba inicializace engine: {e}")
        return False
        
    # Test vytvoření testovacích obrázků
    try:
        test_img = np.ones((50, 50, 3), dtype=np.uint8) * 255
        pil_img = Image.fromarray(test_img)
        print("✅ Testovací obrázek vytvořen")
    except Exception as e:
        print(f"❌ Chyba vytvoření testovacího obrázku: {e}")
        return False
        
    # Test detekce bílých okrajů
    try:
        borders = engine.detect_white_borders(pil_img)
        print("✅ Detekce bílých okrajů funkční")
    except Exception as e:
        print(f"❌ Chyba detekce bílých okrajů: {e}")
        return False
        
    print("✅ Všechny testy detekce bílých okrajů prošly!")
    return True

if __name__ == "__main__":
    # Spuštění základních testů
    success = run_white_border_tests()
    
    # Spuštění unit testů
    if success:
        print("\n🧪 Spouštím unit testy...")
        unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n✅ Testování detekce bílých okrajů dokončeno!") 