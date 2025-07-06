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
    print(f"❌ Chyba importu: {e}")
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
    print("🧪 Spouštím základní testy BleedMakr...")
    
    # Test importů
    try:
        import PIL
        print("✅ PIL/Pillow importován")
    except ImportError:
        print("❌ PIL/Pillow není nainstalován")
        return False
        
    try:
        import numpy
        print("✅ NumPy importován")
    except ImportError:
        print("❌ NumPy není nainstalován")
        return False
        
    try:
        import fitz  # PyMuPDF
        print("✅ PyMuPDF importován")
    except ImportError:
        print("❌ PyMuPDF není nainstalován")
        return False
        
    # Test engine
    try:
        engine = SpadavkaEngine()
        print("✅ SpadavkaEngine inicializován")
    except Exception as e:
        print(f"❌ Chyba inicializace engine: {e}")
        return False
        
    # Test podporovaných formátů
    supported_formats = ['.pdf', '.eps', '.tiff', '.jpg', '.jpeg', '.png']
    for fmt in supported_formats:
        if engine.is_supported_format(f'test{fmt}'):
            print(f"✅ Podporován formát: {fmt}")
        else:
            print(f"❌ Nepodporován formát: {fmt}")
            return False
            
    print("✅ Všechny základní testy prošly!")
    return True

if __name__ == "__main__":
    # Spuštění základních testů
    success = run_basic_tests()
    
    # Spuštění unit testů
    if success:
        print("\n🧪 Spouštím unit testy...")
        unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n✅ Testování dokončeno!") 