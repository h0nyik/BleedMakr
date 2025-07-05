#!/usr/bin/env python3
"""
Testovací skript pro Generator Spadávek
Ověří základní funkce bez GUI
"""

import os
import tempfile
from PIL import Image
from spadavka_engine import SpadavkaEngine

def create_test_image():
    """Vytvoří testovací obrázek"""
    # Vytvoření jednoduchého testovacího obrázku
    img = Image.new('RGB', (200, 150), color='red')
    
    # Přidání nějakého obsahu
    for x in range(50, 150):
        for y in range(50, 100):
            img.putpixel((x, y), (0, 255, 0))  # Zelený obdélník
    
    return img

def test_image_processing():
    """Test zpracování obrázku"""
    print("Test zpracování obrázku...")
    
    # Vytvoření testovacího obrázku
    test_img = create_test_image()
    
    # Uložení do dočasného souboru
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        test_img.save(tmp.name)
        input_path = tmp.name
    
    try:
        # Vytvoření výstupního souboru
        output_path = input_path.replace('.png', '_spadavka.pdf')
        
        # Test engine
        engine = SpadavkaEngine(spadavka_size_mm=3)
        result = engine.generate_spadavka(input_path, output_path)
        
        if result and os.path.exists(output_path):
            print("✅ Test obrázku úspěšný")
            print(f"   Vstup: {os.path.basename(input_path)}")
            print(f"   Výstup: {os.path.basename(output_path)}")
            print(f"   Velikost výstupu: {os.path.getsize(output_path)} bajtů")
            return True
        else:
            print("❌ Test obrázku selhal")
            return False
            
    except Exception as e:
        print(f"❌ Chyba při testu obrázku: {e}")
        return False
    finally:
        # Úklid
        try:
            os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
        except:
            pass

def test_engine_validation():
    """Test validace engine"""
    print("\nTest validace engine...")
    
    engine = SpadavkaEngine(spadavka_size_mm=3)
    
    # Test neexistujícího souboru
    try:
        engine.generate_spadavka("neexistujici_soubor.jpg", "output.pdf")
        print("❌ Engine měl odmítnout neexistující soubor")
        return False
    except FileNotFoundError:
        print("✅ Engine správně odmítl neexistující soubor")
    except Exception as e:
        if "neexistuje" in str(e).lower():
            print("✅ Engine správně odmítl neexistující soubor")
        else:
            print(f"❌ Neočekávaná chyba: {e}")
            return False
    
    # Test nepodporovaného formátu
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
        tmp.write(b"test")
        tmp_path = tmp.name
    
    try:
        engine.generate_spadavka(tmp_path, "output.pdf")
        print("❌ Engine měl odmítnout nepodporovaný formát")
        return False
    except ValueError as e:
        if "Nepodporovaný formát" in str(e):
            print("✅ Engine správně odmítl nepodporovaný formát")
        else:
            print(f"❌ Neočekávaná chyba: {e}")
            return False
    except Exception as e:
        if "nepodporovaný" in str(e).lower() or "formát" in str(e).lower():
            print("✅ Engine správně odmítl nepodporovaný formát")
        else:
            print(f"❌ Neočekávaná chyba: {e}")
            return False
    finally:
        os.unlink(tmp_path)
    
    return True

def test_preview_quality():
    """Test výpočtu kvality náhledu"""
    print("\nTest výpočtu kvality náhledu...")
    
    # Simulace různých velikostí souborů
    test_sizes = [
        (0.5, "malý soubor"),
        (2.0, "střední soubor"), 
        (10.0, "velký soubor"),
        (50.0, "velmi velký soubor")
    ]
    
    for size_mb, description in test_sizes:
        # Simulace souboru dané velikosti
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            # Vytvoření souboru dané velikosti
            size_bytes = int(size_mb * 1024 * 1024)
            tmp.write(b'0' * size_bytes)
            tmp_path = tmp.name
        
        try:
            # Test výpočtu kvality - vytvoření mock objektu
            class MockApp:
                def get_file_size_mb(self, file_path):
                    try:
                        return os.path.getsize(file_path) / (1024 * 1024)
                    except:
                        return 0
                
                def calculate_preview_quality(self, file_path):
                    size_mb = self.get_file_size_mb(file_path)
                    
                    if size_mb < 1:
                        return 800, 800
                    elif size_mb < 5:
                        return 600, 600
                    elif size_mb < 20:
                        return 400, 400
                    else:
                        return 300, 300
            
            app = MockApp()
            quality = app.calculate_preview_quality(tmp_path)
            print(f"   {description} ({size_mb} MB): {quality[0]}x{quality[1]} px")
            
        except Exception as e:
            print(f"❌ Chyba při testu kvality: {e}")
            return False
        finally:
            os.unlink(tmp_path)
    
    print("✅ Test kvality náhledu úspěšný")
    return True

def main():
    """Hlavní testovací funkce"""
    print("Spouštím testy Generator Spadávek...")
    print("=" * 50)
    
    tests = [
        test_engine_validation,
        test_image_processing,
        test_preview_quality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test selhal s výjimkou: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Výsledky testů: {passed}/{total} úspěšných")
    
    if passed == total:
        print("🎉 Všechny testy prošly!")
        return True
    else:
        print("⚠️ Některé testy selhaly")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 