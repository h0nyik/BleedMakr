#!/usr/bin/env python3
"""
Python wrapper pro C modul detekce okrajů
Poskytuje kompatibilní rozhraní s původní Python implementací
"""

import numpy as np
from PIL import Image
import os
import sys

# Přidání cesty k C modulu
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    import edge_detection
    C_MODULE_AVAILABLE = True
    print("[C_MODULE] C modul pro detekci okrajů je k dispozici")
except ImportError as e:
    C_MODULE_AVAILABLE = False
    print(f"[C_MODULE] C modul není k dispozici: {e}")
    print("[C_MODULE] Použije se Python implementace")

class EdgeDetectionWrapper:
    """Wrapper pro detekci okrajů s fallback na Python implementaci"""
    
    def __init__(self):
        self.use_c_module = C_MODULE_AVAILABLE
        
    def detect_white_borders(self, img, tolerance=10, extra_crop=2):
        """
        Detekuje bílé okraje v obrázku
        
        Args:
            img: PIL Image objekt
            tolerance: Tolerance pro bílou barvu (0-255)
            extra_crop: Extra ořez v pixelech
            
        Returns:
            tuple: (left, top, right, bottom, area_reduction)
        """
        if not self.use_c_module:
            return self._detect_white_borders_python(img, tolerance, extra_crop)
        
        try:
            return self._detect_white_borders_c(img, tolerance, extra_crop)
        except Exception as e:
            print(f"[C_MODULE] Chyba v C modulu: {e}")
            print("[C_MODULE] Fallback na Python implementaci")
            return self._detect_white_borders_python(img, tolerance, extra_crop)
    
    def _detect_white_borders_c(self, img, tolerance=10, extra_crop=2):
        """C implementace detekce okrajů"""
        width, height = img.size
        
        # Konverze na numpy array
        img_array = np.array(img)
        
        # Kontrola formátu
        if len(img_array.shape) != 3:
            raise ValueError("Očekáván 3D array (height, width, channels)")
        
        channels = img_array.shape[2]
        if channels not in [3, 4]:
            raise ValueError("Očekáván RGB (3) nebo RGBA (4) formát")
        
        # Volání C funkce
        result = edge_detection.detect_white_borders(img_array, tolerance, extra_crop)
        
        # Výpis debug informací
        left, top, right, bottom, area_reduction = result
        print(f"[C_MODULE] Detekovane okraje: left={left}, top={top}, right={right}, bottom={bottom}")
        print(f"[C_MODULE] Orizane rozmery: {right-left} x {bottom-top}")
        print(f"[C_MODULE] Snizeni plochy: {area_reduction:.1f}%")
        
        return result
    
    def _detect_white_borders_python(self, img, tolerance=10, extra_crop=2):
        """Python fallback implementace"""
        width, height = img.size
        img_array = np.array(img)
        
        print(f"[PYTHON] Analyza obrazku: {width}x{height} pixelu")
        
        # Kontrola režimu obrázku
        if img.mode == 'RGBA':
            print(f"[PYTHON] RGBA rezim - kontrola pruhlednosti a svetlosti")
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
            print(f"[PYTHON] RGB rezim - kontrola svetlosti")
            # Pro RGB kontrolujeme světlost
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
        
        # Výpočet snížení plochy
        original_area = width * height
        cropped_area = (right_border - left_border) * (bottom_border - top_border)
        area_reduction = ((original_area - cropped_area) / original_area) * 100
        
        print(f"[PYTHON] Detekovane okraje: left={left_border}, top={top_border}, right={right_border}, bottom={bottom_border}")
        print(f"[PYTHON] Orizane rozmery: {right_border-left_border} x {bottom_border-top_border}")
        print(f"[PYTHON] Snizeni plochy: {area_reduction:.1f}%")
        
        # Aplikace extra ořezu
        left_border = min(max(0, left_border + extra_crop), width)
        top_border = min(max(0, top_border + extra_crop), height)
        right_border = max(min(width, right_border - extra_crop), left_border+1)
        bottom_border = max(min(height, bottom_border - extra_crop), top_border+1)
        
        return left_border, top_border, right_border, bottom_border, area_reduction

# Testovací funkce
def test_edge_detection():
    """Test detekce okrajů"""
    print("=== Test detekce okrajů ===")
    
    # Vytvoření testovacího obrázku s bílými okraji
    from PIL import Image, ImageDraw
    
    # Vytvoření obrázku 200x200 s bílými okraji a barevným středem
    img = Image.new('RGB', (200, 200), 'white')
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 180, 180], fill='red')
    
    # Test wrapper
    wrapper = EdgeDetectionWrapper()
    result = wrapper.detect_white_borders(img, tolerance=10, extra_crop=2)
    
    print(f"Výsledek: {result}")
    
    # Test s RGBA obrázkem
    img_rgba = Image.new('RGBA', (200, 200), (255, 255, 255, 0))
    draw_rgba = ImageDraw.Draw(img_rgba)
    draw_rgba.rectangle([20, 20, 180, 180], fill=(255, 0, 0, 255))
    
    result_rgba = wrapper.detect_white_borders(img_rgba, tolerance=10, extra_crop=2)
    print(f"Výsledek RGBA: {result_rgba}")

if __name__ == "__main__":
    test_edge_detection() 