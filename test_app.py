#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Základní testovací skript pro BleedMakr
Testuje základní funkčnost aplikace
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Přidání cesty k modulům
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from spadavka_engine import SpadavkaEngine
    from spadavka_generator import BleedMakrApp
except ImportError as e:
    print(f"[ERROR] Chyba importu: {e}")
    sys.exit(1)

class TestBleedMakrApp(unittest.TestCase):
    """Testy pro hlavní aplikaci"""
    
    def setUp(self):
        """Inicializace před každým testem"""
        self.engine = SpadavkaEngine()
        
    def test_engine_initialization(self):
        """Test inicializace engine"""
        self.assertIsNotNone(self.engine)
        self.assertTrue(hasattr(self.engine, 'process_image'))
        self.assertTrue(hasattr(self.engine, 'detect_white_borders'))
        
    def test_bleed_size_validation(self):
        """Test validace velikosti spadávky"""
        # Test pozitivních hodnot
        self.assertTrue(self.engine.validate_bleed_size(3))
        self.assertTrue(self.engine.validate_bleed_size(5))
        
        # Test negativních hodnot
        self.assertFalse(self.engine.validate_bleed_size(-1))
        self.assertFalse(self.engine.validate_bleed_size(0))
        
    def test_supported_formats(self):
        """Test podporovaných formátů"""
        supported = ['.pdf', '.eps', '.tiff', '.jpg', '.jpeg', '.png']
        for fmt in supported:
            self.assertTrue(self.engine.is_supported_format(f'test{fmt}'))
            
    def test_unsupported_formats(self):
        """Test nepodporovaných formátů"""
        unsupported = ['.txt', '.doc', '.xls', '.gif', '.bmp']
        for fmt in unsupported:
            self.assertFalse(self.engine.is_supported_format(f'test{fmt}'))

def run_basic_tests():
    """Spuštění základních testů"""
    print("Spoustim zakladni testy BleedMakr...")
    
    # Test importů
    try:
        import PIL
        print("OK: PIL/Pillow importovan")
    except ImportError:
        print("CHYBA: PIL/Pillow neni nainstalovan")
        return False
        
    try:
        import numpy
        print("OK: NumPy importovan")
    except ImportError:
        print("CHYBA: NumPy neni nainstalovan")
        return False
        
    try:
        import fitz  # PyMuPDF
        print("OK: PyMuPDF importovan")
    except ImportError:
        print("CHYBA: PyMuPDF neni nainstalovan")
        return False
        
    # Test engine
    try:
        engine = SpadavkaEngine()
        print("OK: SpadavkaEngine inicializovan")
    except Exception as e:
        print(f"CHYBA: Chyba inicializace engine: {e}")
        return False
        
    # Test podporovaných formátů
    supported_formats = ['.pdf', '.eps', '.tiff', '.jpg', '.jpeg', '.png']
    for fmt in supported_formats:
        if engine.is_supported_format(f'test{fmt}'):
            print(f"OK: Podporovan format: {fmt}")
        else:
            print(f"CHYBA: Nepodporovan format: {fmt}")
            return False
            
    print("OK: Vsechny zakladni testy prosly!")
    return True

if __name__ == "__main__":
    # Spuštění základních testů
    success = run_basic_tests()
    
    # Spuštění unit testů
    if success:
        print("\nSpoustim unit testy...")
        unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\nTestovani dokonceno!") 