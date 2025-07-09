#!/usr/bin/env python3
"""
Příklad integrace C modulu detekce okrajů s hlavní BleedMakr aplikací
"""

import os
import sys

# Přidání cesty k modulu
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from edge_detection_wrapper import EdgeDetectionWrapper
    C_MODULE_AVAILABLE = True
    print("✅ C modul detekce okrajů je k dispozici")
except ImportError as e:
    C_MODULE_AVAILABLE = False
    print(f"⚠️ C modul není k dispozici: {e}")
    print("   Použije se Python implementace")

class SpadavkaEngineWithC:
    """
    Ukázka integrace C modulu do SpadavkaEngine
    """
    
    def __init__(self, spadavka_size_mm=3, inner_bleed_mm=2, extra_crop_px=2):
        self.spadavka_size_mm = spadavka_size_mm
        self.inner_bleed_mm = inner_bleed_mm
        self.spadavka_size_px = int(spadavka_size_mm * 11.811)
        self.inner_bleed_px = int(inner_bleed_mm * 11.811)
        self.extra_crop_px = extra_crop_px
        
        # Inicializace C modulu
        if C_MODULE_AVAILABLE:
            self.edge_detector = EdgeDetectionWrapper()
            self.use_c_detection = True
            print("🚀 C modul detekce okrajů aktivován")
        else:
            self.use_c_detection = False
            print("🐍 Používá se Python implementace detekce okrajů")
    
    def detect_white_borders(self, img, tolerance=10):
        """
        Detekuje bílé okraje s použitím C modulu nebo Python fallback
        """
        if self.use_c_detection:
            try:
                # Použití C implementace
                result = self.edge_detector.detect_white_borders(
                    img, tolerance, self.extra_crop_px
                )
                left, top, right, bottom, area_reduction = result
                
                print(f"[C_MODULE] Detekce okrajů dokončena")
                print(f"[C_MODULE] Snížení plochy: {area_reduction:.1f}%")
                
                return left, top, right, bottom
                
            except Exception as e:
                print(f"[C_MODULE] Chyba: {e}")
                print("[C_MODULE] Fallback na Python implementaci")
                return self._detect_white_borders_python(img, tolerance)
        else:
            # Použití Python implementace
            return self._detect_white_borders_python(img, tolerance)
    
    def _detect_white_borders_python(self, img, tolerance=10):
        """
        Původní Python implementace detekce okrajů
        """
        import numpy as np
        
        width, height = img.size
        img_array = np.array(img)
        
        print(f"[PYTHON] Detekce okrajů: {width}x{height} pixelů")
        
        # Zjednodušená Python implementace pro ukázku
        if img.mode == 'RGBA':
            alpha_channel = img_array[:, :, 3]
            rgb_channels = img_array[:, :, :3]
            
            # Detekce horního okraje
            top_border = 0
            for y in range(min(height, 100)):
                if not all(alpha_channel[y, :] < tolerance):
                    row_rgb = rgb_channels[y, :]
                    avg_brightness = np.mean(row_rgb)
                    if avg_brightness < 245:
                        top_border = y
                        break
            
            # Detekce spodního okraje
            bottom_border = height
            for y in range(height - 1, max(height - 100, 0), -1):
                if not all(alpha_channel[y, :] < tolerance):
                    row_rgb = rgb_channels[y, :]
                    avg_brightness = np.mean(row_rgb)
                    if avg_brightness < 245:
                        bottom_border = y + 1
                        break
            
            # Detekce levého okraje
            left_border = 0
            for x in range(min(width, 100)):
                if not all(alpha_channel[:, x] < tolerance):
                    col_rgb = rgb_channels[:, x]
                    avg_brightness = np.mean(col_rgb)
                    if avg_brightness < 245:
                        left_border = x
                        break
            
            # Detekce pravého okraje
            right_border = width
            for x in range(width - 1, max(width - 100, 0), -1):
                if not all(alpha_channel[:, x] < tolerance):
                    col_rgb = rgb_channels[:, x]
                    avg_brightness = np.mean(col_rgb)
                    if avg_brightness < 245:
                        right_border = x + 1
                        break
        else:
            # RGB implementace
            top_border = 0
            for y in range(min(height, 100)):
                row = img_array[y, :]
                avg_brightness = np.mean(row)
                if avg_brightness < 245:
                    top_border = y
                    break
            
            bottom_border = height
            for y in range(height - 1, max(height - 100, 0), -1):
                row = img_array[y, :]
                avg_brightness = np.mean(row)
                if avg_brightness < 245:
                    bottom_border = y + 1
                    break
            
            left_border = 0
            for x in range(min(width, 100)):
                col = img_array[:, x]
                avg_brightness = np.mean(col)
                if avg_brightness < 245:
                    left_border = x
                    break
            
            right_border = width
            for x in range(width - 1, max(width - 100, 0), -1):
                col = img_array[:, x]
                avg_brightness = np.mean(col)
                if avg_brightness < 245:
                    right_border = x + 1
                    break
        
        # Aplikace extra ořezu
        left_border = min(max(0, left_border + self.extra_crop_px), width)
        top_border = min(max(0, top_border + self.extra_crop_px), height)
        right_border = max(min(width, right_border - self.extra_crop_px), left_border+1)
        bottom_border = max(min(height, bottom_border - self.extra_crop_px), top_border+1)
        
        print(f"[PYTHON] Detekce okrajů dokončena")
        return left_border, top_border, right_border, bottom_border

def test_integration():
    """Test integrace C modulu"""
    print("🧪 Test integrace C modulu s BleedMakr")
    print("=" * 50)
    
    # Vytvoření testovacího obrázku
    from PIL import Image, ImageDraw
    
    # Testovací obrázek s bílými okraji
    img = Image.new('RGB', (300, 300), 'white')
    draw = ImageDraw.Draw(img)
    draw.rectangle([30, 30, 270, 270], fill='red')
    
    # Vytvoření engine s C podporou
    engine = SpadavkaEngineWithC(spadavka_size_mm=3, extra_crop_px=2)
    
    # Test detekce okrajů
    print(f"\n📏 Test obrázku: {img.size}")
    print(f"🔧 Používá se: {'C modul' if engine.use_c_detection else 'Python implementace'}")
    
    # Měření času
    import time
    start_time = time.time()
    
    left, top, right, bottom = engine.detect_white_borders(img, tolerance=10)
    
    end_time = time.time()
    processing_time = (end_time - start_time) * 1000
    
    print(f"\n📊 Výsledky:")
    print(f"  Okraje: left={left}, top={top}, right={right}, bottom={bottom}")
    print(f"  Oříznuté rozměry: {right-left} x {bottom-top}")
    print(f"  Čas zpracování: {processing_time:.2f} ms")
    
    # Test s RGBA obrázkem
    print(f"\n🎨 Test RGBA obrázku:")
    img_rgba = Image.new('RGBA', (300, 300), (255, 255, 255, 0))
    draw_rgba = ImageDraw.Draw(img_rgba)
    draw_rgba.rectangle([30, 30, 270, 270], fill=(255, 0, 0, 255))
    
    start_time = time.time()
    left_rgba, top_rgba, right_rgba, bottom_rgba = engine.detect_white_borders(img_rgba, tolerance=10)
    end_time = time.time()
    processing_time_rgba = (end_time - start_time) * 1000
    
    print(f"  Okraje RGBA: left={left_rgba}, top={top_rgba}, right={right_rgba}, bottom={bottom_rgba}")
    print(f"  Čas zpracování RGBA: {processing_time_rgba:.2f} ms")

def show_integration_instructions():
    """Zobrazí instrukce pro integraci"""
    print("\n📋 Instrukce pro integraci do hlavní aplikace:")
    print("=" * 60)
    
    print("""
1. Zkopírujte soubory z c_extension/ do hlavní aplikace:
   - edge_detection_wrapper.py
   - edge_detection.c (pokud chcete upravit C kód)
   - setup_edge_detection.py

2. Upravte spadavka_engine.py:
   ```python
   # Na začátku souboru
   try:
       from edge_detection_wrapper import EdgeDetectionWrapper
       edge_detector = EdgeDetectionWrapper()
       use_c_detection = True
   except ImportError:
       use_c_detection = False
   
   # V __init__ metodě
   self.use_c_detection = use_c_detection
   if use_c_detection:
       self.edge_detector = edge_detector
   
   # V _detect_white_borders metodě
   if self.use_c_detection:
       try:
           result = self.edge_detector.detect_white_borders(
               img, tolerance, self.extra_crop_px
           )
           return result[:4]  # Vrátí pouze left, top, right, bottom
       except Exception as e:
           print(f"C modul chyba: {e}, použití Python implementace")
           # Pokračuj s původní Python implementací
   ```

3. Kompilujte C modul:
   ```bash
   cd c_extension
   python setup_edge_detection.py build_ext --inplace
   ```

4. Otestujte integraci:
   ```bash
   python integration_example.py
   ```
    """)

if __name__ == "__main__":
    test_integration()
    show_integration_instructions() 