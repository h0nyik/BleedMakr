import os
from PIL import Image, ImageOps
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import tempfile
import shutil
import time
import numpy as np
import io

class SpadavkaEngine:
    def __init__(self, spadavka_size_mm=3, inner_bleed_mm=2, extra_crop_px=2):
        self.spadavka_size_mm = spadavka_size_mm
        self.inner_bleed_mm = inner_bleed_mm
        self.spadavka_size_px = int(spadavka_size_mm * 11.811)  # Převod mm na px (300 DPI)
        self.inner_bleed_px = int(inner_bleed_mm * 11.811)
        self.extra_crop_px = extra_crop_px
        
    def is_supported_format(self, file_path):
        """Kontroluje, zda je formát souboru podporován"""
        supported_extensions = ['.pdf', '.eps', '.tiff', '.tif', '.jpg', '.jpeg', '.png']
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in supported_extensions
        
    def validate_bleed_size(self, size_mm):
        """Validuje velikost spadávky"""
        return 0 < size_mm <= 50  # Maximálně 50mm spadávka
        
    def detect_white_borders(self, img, tolerance=10):
        """Detekuje bílé okraje v obrázku - alias pro _detect_white_borders"""
        return self._detect_white_borders(img, tolerance)
        
    def generate_spadavka(self, input_path, output_path):
        """Generuje spadávku z vstupního souboru"""
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Soubor neexistuje: {input_path}")
            
        file_ext = os.path.splitext(input_path)[1].lower()
        
        try:
            if file_ext in ['.jpg', '.jpeg', '.png', '.tiff', '.tif']:
                return self._process_image(input_path, output_path)
            elif file_ext == '.pdf':
                return self._process_pdf(input_path, output_path)
            elif file_ext == '.eps':
                return self._process_eps(input_path, output_path)
            else:
                raise ValueError(f"Nepodporovaný formát: {file_ext}")
        except Exception as e:
            raise Exception(f"Chyba při zpracování {os.path.basename(input_path)}: {str(e)}")
    
    def _is_white_or_transparent(self, color, tolerance=10):
        """Kontroluje, zda je barva bílá nebo průhledná"""
        if len(color) == 4:  # RGBA
            r, g, b, a = color
            # Kontrola průhlednosti
            if a < tolerance:
                return True
            # Kontrola bílé barvy
            return r >= 255 - tolerance and g >= 255 - tolerance and b >= 255 - tolerance
        else:  # RGB
            r, g, b = color
            return r >= 255 - tolerance and g >= 255 - tolerance and b >= 255 - tolerance
    
    def _detect_white_borders(self, img, tolerance=10):
        """Detekuje světlé okraje a vrátí souřadnice ořezu až na čistou grafiku (žádná bílá na okraji)"""
        width, height = img.size
        img_array = np.array(img)
        
        # Debug informace
        print(f"[ANALYZE] Analýza obrázku: {width}x{height} pixelů")
        
        # Kontrola režimu obrázku
        if img.mode == 'RGBA':
            print(f"[COLOR] RGBA režim - kontrola průhlednosti a světlosti")
            # Pro RGBA kontrolujeme alpha kanál a světlost
            alpha_channel = img_array[:, :, 3]
            rgb_channels = img_array[:, :, :3]
            
            # Detekce horního okraje
            top_border = 0
            for y in range(min(height, 100)):
                # Kontrola průhlednosti
                if not all(alpha_channel[y, :] < tolerance):
                    # Kontrola světlosti (průměrná hodnota RGB)
                    row_rgb = rgb_channels[y, :]
                    avg_brightness = np.mean(row_rgb)
                    if avg_brightness < 245:  # Adaptivní práh pro světlost
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
            print(f"[COLOR] RGB režim - kontrola světlosti")
            # Pro RGB kontrolujeme světlost (průměrnou hodnotu RGB)
            # Detekce horního okraje
            top_border = 0
            for y in range(min(height, 100)):
                row = img_array[y, :]
                avg_brightness = np.mean(row)
                if avg_brightness < 245:  # Adaptivní práh pro světlost
                    top_border = y
                    break
            
            # Detekce spodního okraje
            bottom_border = height
            for y in range(height - 1, max(height - 100, 0), -1):
                row = img_array[y, :]
                avg_brightness = np.mean(row)
                if avg_brightness < 245:
                    bottom_border = y + 1
                    break
            
            # Detekce levého okraje
            left_border = 0
            for x in range(min(width, 100)):
                col = img_array[:, x]
                avg_brightness = np.mean(col)
                if avg_brightness < 245:
                    left_border = x
                    break
            
            # Detekce pravého okraje
            right_border = width
            for x in range(width - 1, max(width - 100, 0), -1):
                col = img_array[:, x]
                avg_brightness = np.mean(col)
                if avg_brightness < 245:
                    right_border = x + 1
                    break
        
        # Kontrola, zda byly detekovány nějaké okraje
        original_area = width * height
        cropped_area = (right_border - left_border) * (bottom_border - top_border)
        area_reduction = ((original_area - cropped_area) / original_area) * 100
        
        # Debug informace
        print(f"[OKRAJE] Detekované okraje: left={left_border}, top={top_border}, right={right_border}, bottom={bottom_border}")
        print(f"[OREZ] Ořezané rozměry: {right_border-left_border} x {bottom_border-top_border}")
        print(f"[STATS] Snížení plochy: {area_reduction:.1f}%")
        
        # Po detekci hran motivu ořízni ještě o extra_crop_px pixelů z každé strany (pokud to rozměry dovolí)
        left_border = min(max(0, left_border + self.extra_crop_px), width)
        top_border = min(max(0, top_border + self.extra_crop_px), height)
        right_border = max(min(width, right_border - self.extra_crop_px), left_border+1)
        bottom_border = max(min(height, bottom_border - self.extra_crop_px), top_border+1)
        return left_border, top_border, right_border, bottom_border
    
    def _detect_content_borders(self, img, tolerance=10):
        """Detekuje okraje obsahu na základě změny barvy"""
        width, height = img.size
        img_array = np.array(img)
        
        print(f"[DETEKCE] Detekce okrajů obsahu: {width}x{height} pixelů")
        
        # Konverze do RGB pokud je potřeba
        if img.mode == 'RGBA':
            # Vytvoření bílého pozadí pro průhledné oblasti
            background = Image.new('RGB', img.size, 'white')
            background.paste(img, mask=img.split()[-1])
            img_array = np.array(background)
        
        # Detekce horního okraje - hledáme první řádek s významným obsahem
        top_border = 0
        for y in range(min(height, 200)):  # Kontrola prvních 200 řádků
            row = img_array[y, :]
            # Vypočítáme standardní odchylku barvy v řádku
            std_dev = np.std(row)
            if std_dev > 20:  # Pokud je variabilita barvy vysoká, máme obsah
                top_border = y
                break
        
        # Detekce spodního okraje
        bottom_border = height
        for y in range(height - 1, max(height - 200, 0), -1):
            row = img_array[y, :]
            std_dev = np.std(row)
            if std_dev > 20:
                bottom_border = y + 1
                break
        
        # Detekce levého okraje
        left_border = 0
        for x in range(min(width, 200)):
            col = img_array[:, x]
            std_dev = np.std(col)
            if std_dev > 20:
                left_border = x
                break
        
        # Detekce pravého okraje
        right_border = width
        for x in range(width - 1, max(width - 200, 0), -1):
            col = img_array[:, x]
            std_dev = np.std(col)
            if std_dev > 20:
                right_border = x + 1
                break
        
        # Kontrola, zda byly detekovány nějaké okraje
        original_area = width * height
        cropped_area = (right_border - left_border) * (bottom_border - top_border)
        area_reduction = ((original_area - cropped_area) / original_area) * 100
        
        print(f"[OKRAJE] Detekované okraje obsahu: left={left_border}, top={top_border}, right={right_border}, bottom={bottom_border}")
        print(f"[OREZ] Ořezané rozměry: {right_border-left_border} x {bottom_border-top_border}")
        print(f"[STATS] Snížení plochy: {area_reduction:.1f}%")
        
        # Pokud se plocha snížila o méně než 1%, nepovažujeme to za významné ořezání
        if area_reduction < 1:
            print(f"[WARNING] Malé snížení plochy - použití původních rozměrů")
            return 0, 0, width, height
        
        print(f"[OK] Významné snížení plochy - aplikování ořezu")
        return left_border, top_border, right_border, bottom_border
    
    def _create_intelligent_spadavka(self, img, width, height, new_width, new_height, original_mode):
        # Detekce bílých okrajů
        left, top, right, bottom = self._detect_white_borders(img)
        needs_crop = (left > 0 or top > 0 or right < width or bottom < height)
        if needs_crop:
            cropped_img = img.crop((left, top, right, bottom))
            cropped_width, cropped_height = cropped_img.size
            new_cropped_width = cropped_width + (2 * self.spadavka_size_px)
            new_cropped_height = cropped_height + (2 * self.spadavka_size_px)
            # Transparentní pozadí pokud mód umožňuje, jinak bez barvy
            if 'A' in original_mode:
                new_img = Image.new(original_mode, (new_cropped_width, new_cropped_height), (0, 0, 0, 0))
            else:
                new_img = Image.new(original_mode, (new_cropped_width, new_cropped_height))
            # Vložení ořezané grafiky přesně na pozici spadávky
            new_img.paste(cropped_img, (self.spadavka_size_px, self.spadavka_size_px))
            # Okraje a rohy generovat vždy z cropped_img
            self._add_standard_mirrored_borders(cropped_img, new_img, cropped_width, cropped_height, new_cropped_width, new_cropped_height)
            print(f"[DEBUG] Ořez: left={left}, top={top}, right={right}, bottom={bottom}, offset={self.spadavka_size_px}")
            print(f"[DEBUG] Nový rozměr plátna: {new_cropped_width}x{new_cropped_height}, mód: {original_mode}")
            return new_img
        else:
            # Pokud není potřeba ořez, použij původní obrázek
            if 'A' in original_mode:
                new_img = Image.new(original_mode, (new_width, new_height), (0, 0, 0, 0))
            else:
                new_img = Image.new(original_mode, (new_width, new_height))
            new_img.paste(img, (self.spadavka_size_px, self.spadavka_size_px))
            self._add_standard_mirrored_borders(img, new_img, width, height, new_width, new_height)
            print(f"[DEBUG] Bez ořezu, offset={self.spadavka_size_px}, mód: {original_mode}")
            return new_img
    
    def _add_mirrored_borders(self, original_img, new_img, width, height, new_width, new_height):
        if self.spadavka_size_px <= 0:
            return
        border_quality = self._check_border_quality(original_img, width, height)
        if border_quality['has_content']:
            self._add_standard_mirrored_borders(original_img, new_img, width, height, new_width, new_height)
        else:
            self._add_alternative_borders(original_img, new_img, width, height, new_width, new_height)
    
    def _check_border_quality(self, img, width, height):
        """Kontroluje kvalitu okrajů pro zrcadlení"""
        # Kontrola horního okraje
        top_border = img.crop((0, 0, width, min(self.spadavka_size_px, height)))
        top_has_content = not self._is_border_white(top_border, width, min(self.spadavka_size_px, height))
        
        # Kontrola spodního okraje
        bottom_border = img.crop((0, max(0, height - self.spadavka_size_px), width, height))
        bottom_has_content = not self._is_border_white(bottom_border, width, min(self.spadavka_size_px, height))
        
        # Kontrola levého okraje
        left_border = img.crop((0, 0, min(self.spadavka_size_px, width), height))
        left_has_content = not self._is_border_white(left_border, min(self.spadavka_size_px, width), height)
        
        # Kontrola pravého okraje
        right_border = img.crop((max(0, width - self.spadavka_size_px), 0, width, height))
        right_has_content = not self._is_border_white(right_border, min(self.spadavka_size_px, width), height)
        
        return {
            'has_content': top_has_content or bottom_has_content or left_has_content or right_has_content,
            'top': top_has_content,
            'bottom': bottom_has_content,
            'left': left_has_content,
            'right': right_has_content
        }
    
    def _is_border_white(self, border_img, width, height, tolerance=10):
        """Kontroluje, zda je okraj bílý"""
        arr = np.array(border_img)
        avg = np.mean(arr[:, :, :3])
        return avg > 250 - tolerance
    
    def _add_standard_mirrored_borders(self, original_img, new_img, width, height, new_width, new_height):
        """Původní metoda - nyní používá perfektní napojení"""
        print(f"[NAPOJENI] Používám perfektní napojení barev...")
        self._add_perfect_mirrored_borders(original_img, new_img, width, height, new_width, new_height)
    
    def _add_perfect_mirrored_borders(self, original_img, new_img, width, height, new_width, new_height):
        """Přidá zrcadlené okraje s 100% přesným napojením barev"""
        # Horní spadávka - s přesným napojením
        for y in range(self.spadavka_size_px):
            source_y = self.spadavka_size_px - 1 - y  # Zrcadlení
            for x in range(width):
                source_pixel = original_img.getpixel((x, source_y))
                new_img.putpixel((x + self.spadavka_size_px, y), source_pixel)
        
        # Spodní spadávka - s přesným napojením
        for y in range(self.spadavka_size_px):
            source_y = height - 1 - y  # Zrcadlení od spodního okraje
            for x in range(width):
                source_pixel = original_img.getpixel((x, source_y))
                new_img.putpixel((x + self.spadavka_size_px, new_height - self.spadavka_size_px + y), source_pixel)
        
        # Levá spadávka - s přesným napojením (KLÍČOVÁ OPRAVA)
        for x in range(self.spadavka_size_px):
            source_x = self.spadavka_size_px - 1 - x  # Zrcadlení
            for y in range(height):
                source_pixel = original_img.getpixel((source_x, y))
                new_img.putpixel((x, y + self.spadavka_size_px), source_pixel)
        
        # Pravá spadávka - s přesným napojením
        for x in range(self.spadavka_size_px):
            source_x = width - 1 - x  # Zrcadlení od pravého okraje
            for y in range(height):
                source_pixel = original_img.getpixel((source_x, y))
                new_img.putpixel((new_width - self.spadavka_size_px + x, y + self.spadavka_size_px), source_pixel)
        
        # Rohové spadávky s přesným napojením
        self._add_perfect_corner_borders(original_img, new_img, width, height, new_width, new_height)
        
        # NOVÉ: Aplikace color matching pro 100% shodu
        new_img = self._apply_color_matching(new_img, original_img, self.spadavka_size_px)
        
        return new_img
    
    def _add_perfect_corner_borders(self, original_img, new_img, width, height, new_width, new_height):
        """Přidá rohové spadávky s 100% přesným napojením"""
        # Levý horní roh
        for y in range(self.spadavka_size_px):
            for x in range(self.spadavka_size_px):
                source_x = self.spadavka_size_px - 1 - x
                source_y = self.spadavka_size_px - 1 - y
                source_pixel = original_img.getpixel((source_x, source_y))
                new_img.putpixel((x, y), source_pixel)
        
        # Pravý horní roh
        for y in range(self.spadavka_size_px):
            for x in range(self.spadavka_size_px):
                source_x = width - 1 - x
                source_y = self.spadavka_size_px - 1 - y
                source_pixel = original_img.getpixel((source_x, source_y))
                new_img.putpixel((new_width - self.spadavka_size_px + x, y), source_pixel)
        
        # Levý spodní roh
        for y in range(self.spadavka_size_px):
            for x in range(self.spadavka_size_px):
                source_x = self.spadavka_size_px - 1 - x
                source_y = height - 1 - y
                source_pixel = original_img.getpixel((source_x, source_y))
                new_img.putpixel((x, new_height - self.spadavka_size_px + y), source_pixel)
        
        # Pravý spodní roh
        for y in range(self.spadavka_size_px):
            for x in range(self.spadavka_size_px):
                source_x = width - 1 - x
                source_y = height - 1 - y
                source_pixel = original_img.getpixel((source_x, source_y))
                new_img.putpixel((new_width - self.spadavka_size_px + x, new_height - self.spadavka_size_px + y), source_pixel)
    
    def _add_alternative_borders(self, original_img, new_img, width, height, new_width, new_height):
        """Přidá alternativní okraje pro soubory s bílými okraji"""
        # Najde nejbližší barevné pixely pro roztažení
        self._add_stretched_borders(original_img, new_img, width, height, new_width, new_height)
    
    def _add_stretched_borders(self, original_img, new_img, width, height, new_width, new_height):
        """Přidá roztažené okraje místo zrcadlení"""
        # Horní spadávka - roztažení horního řádku
        if height > 0:
            top_row = original_img.crop((0, 0, width, 1))
            top_stretched = top_row.resize((width, self.spadavka_size_px), Image.Resampling.NEAREST)
            new_img.paste(top_stretched, (self.spadavka_size_px, 0))
        
        # Spodní spadávka - roztažení spodního řádku
        if height > 0:
            bottom_row = original_img.crop((0, height - 1, width, height))
            bottom_stretched = bottom_row.resize((width, self.spadavka_size_px), Image.Resampling.NEAREST)
            new_img.paste(bottom_stretched, (self.spadavka_size_px, new_height - self.spadavka_size_px))
        
        # Levá spadávka - roztažení levého sloupce
        if width > 0:
            left_col = original_img.crop((0, 0, 1, height))
            left_stretched = left_col.resize((self.spadavka_size_px, height), Image.Resampling.NEAREST)
            new_img.paste(left_stretched, (0, self.spadavka_size_px))
        
        # Pravá spadávka - roztažení pravého sloupce
        if width > 0:
            right_col = original_img.crop((width - 1, 0, width, height))
            right_stretched = right_col.resize((self.spadavka_size_px, height), Image.Resampling.NEAREST)
            new_img.paste(right_stretched, (new_width - self.spadavka_size_px, self.spadavka_size_px))
        
        # Rohové spadávky
        self._add_corner_borders(original_img, new_img, width, height, new_width, new_height)
    
    def _add_corner_borders(self, original_img, new_img, width, height, new_width, new_height):
        # Levý horní roh
        top_left = original_img.crop((0, 0, self.spadavka_size_px, self.spadavka_size_px))
        top_left_mirror = ImageOps.mirror(ImageOps.flip(top_left))
        new_img.paste(top_left_mirror, (0, 0))
        # Pravý horní roh
        top_right = original_img.crop((width - self.spadavka_size_px, 0, width, self.spadavka_size_px))
        top_right_mirror = ImageOps.mirror(ImageOps.flip(top_right))
        new_img.paste(top_right_mirror, (new_width - self.spadavka_size_px, 0))
        # Levý spodní roh
        bottom_left = original_img.crop((0, height - self.spadavka_size_px, self.spadavka_size_px, height))
        bottom_left_mirror = ImageOps.mirror(ImageOps.flip(bottom_left))
        new_img.paste(bottom_left_mirror, (0, new_height - self.spadavka_size_px))
        # Pravý spodní roh
        bottom_right = original_img.crop((width - self.spadavka_size_px, height - self.spadavka_size_px, width, height))
        bottom_right_mirror = ImageOps.mirror(ImageOps.flip(bottom_right))
        new_img.paste(bottom_right_mirror, (new_width - self.spadavka_size_px, new_height - self.spadavka_size_px))
            
    def _process_image(self, input_path, output_path):
        """Zpracování obrázku s inteligentní detekcí okrajů"""
        try:
            # Načtení obrázku s optimalizací
            with Image.open(input_path) as img:
                original_mode = img.mode
                print(f"[DEBUG] Zdrojový barevný prostor: {original_mode}")
                # Konverze do RGB pouze pokud je potřeba pro výpočty, ale originální mód si pamatujeme
                work_img = img.convert('RGB') if img.mode not in ('RGB', 'L', 'CMYK', 'LAB') else img.copy()
                width, height = work_img.size
                if width < 10 or height < 10:
                    raise ValueError("Obrázek je příliš malý pro zpracování")
                new_width = width + (2 * self.spadavka_size_px)
                new_height = height + (2 * self.spadavka_size_px)
                if new_width * new_height > 100000000:
                    raise ValueError("Obrázek je příliš velký pro zpracování")
                new_img = self._create_intelligent_spadavka(work_img, width, height, new_width, new_height, original_mode)
                # Pokud je původní mód jiný než RGB, převedeme zpět
                if new_img.mode != original_mode:
                    try:
                        new_img = new_img.convert(original_mode)
                    except Exception as e:
                        print(f"[DEBUG] Nelze převést zpět do původního módu {original_mode}: {e}")
                print(f"[DEBUG] Výsledný barevný prostor: {new_img.mode}")
                new_img.save(output_path, 'PDF', resolution=300.0, optimize=True)
                return True, "Obrázek zpracován, inteligentní detekce okrajů"
        except Exception as e:
            raise Exception(f"Chyba při zpracování obrázku: {str(e)}")
            
    def _process_pdf(self, input_path, output_path):
        """Zpracování PDF: bitmapová spadávka pouze v okrajích, vždy až po ořezu na grafiku"""
        try:
            import fitz
            from PIL import Image, ImageOps
            import io

            # Otevření PDF
            doc = fitz.open(input_path)
            if doc.page_count == 0:
                doc.close()
                raise ValueError("PDF neobsahuje žádné stránky")
            page = doc[0]
            rect = page.rect
            original_width, original_height = rect.width, rect.height

            spadavka_points = self.spadavka_size_mm * 2.83465  # mm na body
            
            # 1. Vytvoření bitmapy stránky
            dpi = 300
            scale_factor = dpi / 72
            matrix = fitz.Matrix(scale_factor, scale_factor)
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            spadavka_px = int(spadavka_points * scale_factor)
            
            print(f"[DIAGNOSTIKA] Původní PDF: {original_width:.1f}x{original_height:.1f} bodů")
            print(f"[DIAGNOSTIKA] Bitmapa: {img.size[0]}x{img.size[1]} px")
            print(f"[DIAGNOSTIKA] Scale factor: {scale_factor:.3f}")
            print(f"[DIAGNOSTIKA] Spadávka: {spadavka_points:.1f} bodů = {spadavka_px} px")
            
            # 2. Ořez bitmapy až na grafiku (žádná bílá na okraji)
            left, top, right, bottom = self._detect_white_borders(img, tolerance=15)
            
            # Kontrola zda je ořez smysluplný (minimálně 10 pixelů na každé straně)
            min_crop = 10
            if left < min_crop and top < min_crop and (img.size[0] - right) < min_crop and (img.size[1] - bottom) < min_crop:
                print(f"[DIAGNOSTIKA] Detekovaný ořez je příliš malý - použiji původní rozměry")
                left, top, right, bottom = 0, 0, img.size[0], img.size[1]
            
            cropped_img = img.crop((left, top, right, bottom))
            cropped_width, cropped_height = cropped_img.size
            
            print(f"[DIAGNOSTIKA] Ořez: left={left}, top={top}, right={right}, bottom={bottom}")
            print(f"[DIAGNOSTIKA] Ořezané rozměry: {cropped_width}x{cropped_height} px")
            
            # Převod ořezaných rozměrů na body
            cropped_width_points = cropped_width / scale_factor
            cropped_height_points = cropped_height / scale_factor
            
            print(f"[DIAGNOSTIKA] Ořezané rozměry: {cropped_width_points:.1f}x{cropped_height_points:.1f} bodů")
            
            # Nové rozměry PDF stránky musí odpovídat ořezané bitmapě + spadávka
            new_width = cropped_width_points + 2 * spadavka_points
            new_height = cropped_height_points + 2 * spadavka_points
            
            print(f"[DIAGNOSTIKA] Nové rozměry stránky: {new_width:.1f}x{new_height:.1f} bodů")

            # 3. Vytvoření spadávky z ořezané bitmapy
            new_img = self._create_raster_bleed(cropped_img, spadavka_px, already_cropped=True)
            
            print(f"[DIAGNOSTIKA] Spadávka vytvořena: {new_img.size[0]}x{new_img.size[1]} px")

            # --- OŘÍZNUTÍ bitmapy pouze na okraje, BEZ SOFT FADE ---
            presah_mm = 2
            presah_px = int(presah_mm * 11.811 * scale_factor)

            bleed = spadavka_px
            w, h = new_img.size

            result_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))

            # Horní pruh
            top_strip = new_img.crop((0, 0, w, bleed + presah_px))
            result_img.paste(top_strip, (0, 0))
            # Dolní pruh
            bottom_strip = new_img.crop((0, h - bleed - presah_px, w, h))
            result_img.paste(bottom_strip, (0, h - bleed - presah_px))
            # Levý pruh
            left_strip = new_img.crop((0, bleed + presah_px, bleed + presah_px, h - bleed - presah_px))
            result_img.paste(left_strip, (0, bleed + presah_px))
            # Pravý pruh
            right_strip = new_img.crop((w - bleed - presah_px, bleed + presah_px, w, h - bleed - presah_px))
            result_img.paste(right_strip, (w - bleed - presah_px, bleed + presah_px))

            # 4. Vložení bitmapové spadávky do PDF
            new_doc = fitz.open()
            new_page = new_doc.new_page(width=new_width, height=new_height)

            img_bytes = io.BytesIO()
            result_img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            new_page.insert_image(
                fitz.Rect(0, 0, new_width, new_height),
                stream=img_bytes.getvalue()
            )

            # 5. Překrytí středem původní vektorové stránky
            # OPRAVA: Pozice a clip region v bodech (ne pixelech!)
            crop_offset_x_points = left / scale_factor  # Převod na body
            crop_offset_y_points = top / scale_factor   # Převod na body
            
            print(f"[DIAGNOSTIKA] Crop offset: {crop_offset_x_points:.1f}, {crop_offset_y_points:.1f} bodů")
            
            # Pozice vektorové části na nové stránce
            vector_x = spadavka_points
            vector_y = spadavka_points
            vector_width = cropped_width_points
            vector_height = cropped_height_points
            
            print(f"[DIAGNOSTIKA] Vektorová pozice: x={vector_x:.1f}, y={vector_y:.1f}")
            print(f"[DIAGNOSTIKA] Vektorová velikost: {vector_width:.1f}x{vector_height:.1f} bodů")
            
            # Clip region - oblast z původní stránky
            clip_x = crop_offset_x_points
            clip_y = crop_offset_y_points
            clip_width = cropped_width_points
            clip_height = cropped_height_points
            
            print(f"[DIAGNOSTIKA] Clip region: x={clip_x:.1f}, y={clip_y:.1f}")
            print(f"[DIAGNOSTIKA] Clip velikost: {clip_width:.1f}x{clip_height:.1f} bodů")
            
            new_page.show_pdf_page(
                fitz.Rect(
                    vector_x, 
                    vector_y, 
                    vector_x + vector_width, 
                    vector_y + vector_height
                ),
                doc, 0,
                clip=fitz.Rect(
                    clip_x,
                    clip_y, 
                    clip_x + clip_width,
                    clip_y + clip_height
                )
            )
            
            # 6. KONTROLA NAPOJENÍ PIXELŮ
            print(f"[KONTROLA NAPOJENI] Ověřuji shodu pixelů na hranicích...")
            
            try:
                # Vytvoření kontrolní bitmapy pro porovnání
                control_matrix = fitz.Matrix(scale_factor, scale_factor)
                control_pix = new_page.get_pixmap(matrix=control_matrix, alpha=False)
                control_img = Image.open(io.BytesIO(control_pix.tobytes("png")))
                
                # Kontrola napojení na hranicích spadávky
                self._check_bleed_alignment(control_img, spadavka_px)
            except Exception as e:
                print(f"[WARNING] [KONTROLA NAPOJENÍ] Chyba při kontrole napojení: {e}")
                print(f"[FALLBACK] [KONTROLA NAPOJENÍ] Pokračujem bez kontroly napojení...")

            new_doc.save(output_path, garbage=4, deflate=True)
            new_doc.close()
            doc.close()
            return True, "Vektor zachován, bitmapová spadávka pouze v okrajích (s diagnostikou)"
        except Exception as e:
            raise Exception(f"Chyba při zpracování PDF: {str(e)}")
    
    def _check_bleed_alignment(self, img, spadavka_px):
        """Kontrola napojení spadávky na grafiku"""
        try:
            width, height = img.size
            
            # Bezpečnostní kontrola rozměrů
            if width <= spadavka_px * 2 or height <= spadavka_px * 2:
                print(f"[WARNING] [NAPOJENÍ] Obrázek příliš malý pro kontrolu napojení")
                return
            
            print(f"[NAPOJENI] Kontroluji obrázek {width}x{height} px, spadávka {spadavka_px} px")
            
            # Kontrola horní hranice - bezpečněji
            differences_found = 0
            for x in range(spadavka_px, min(width - spadavka_px, spadavka_px + 500), 50):  # Omezit rozsah
                try:
                    pixel_above = img.getpixel((x, spadavka_px - 1))  # Pixel ve spadávce
                    pixel_below = img.getpixel((x, spadavka_px))      # Pixel v grafice
                    
                    # Porovnání s tolerancí pro malé rozdíly
                    if abs(pixel_above[0] - pixel_below[0]) > 2 or \
                       abs(pixel_above[1] - pixel_below[1]) > 2 or \
                       abs(pixel_above[2] - pixel_below[2]) > 2:
                        differences_found += 1
                        if differences_found <= 3:  # Zobrazit jen první 3 rozdíly
                            print(f"[WARNING] [NAPOJENÍ] Rozdíl na horní hranici x={x}: {pixel_above} vs {pixel_below}")
                except Exception as e:
                    print(f"[WARNING] [NAPOJENÍ] Chyba při čtení pixelu na pozici x={x}: {e}")
                    break
            
            if differences_found == 0:
                print(f"[OK] [NAPOJENÍ] Horní hranice - OK")
            else:
                print(f"[WARNING] [NAPOJENÍ] Horní hranice - nalezeno {differences_found} rozdílů")
            
            # Kontrola levé hranice - bezpečněji
            differences_found = 0
            for y in range(spadavka_px, min(height - spadavka_px, spadavka_px + 500), 50):  # Omezit rozsah
                try:
                    pixel_left = img.getpixel((spadavka_px - 1, y))   # Pixel ve spadávce
                    pixel_right = img.getpixel((spadavka_px, y))      # Pixel v grafice
                    
                    # Porovnání s tolerancí pro malé rozdíly
                    if abs(pixel_left[0] - pixel_right[0]) > 2 or \
                       abs(pixel_left[1] - pixel_right[1]) > 2 or \
                       abs(pixel_left[2] - pixel_right[2]) > 2:
                        differences_found += 1
                        if differences_found <= 3:  # Zobrazit jen první 3 rozdíly
                            print(f"[WARNING] [NAPOJENÍ] Rozdíl na levé hranici y={y}: {pixel_left} vs {pixel_right}")
                except Exception as e:
                    print(f"[WARNING] [NAPOJENÍ] Chyba při čtení pixelu na pozici y={y}: {e}")
                    break
                    
            if differences_found == 0:
                print(f"[OK] [NAPOJENÍ] Levá hranice - OK")
            else:
                print(f"[WARNING] [NAPOJENÍ] Levá hranice - nalezeno {differences_found} rozdílů")
                
        except Exception as e:
            print(f"[WARNING] [NAPOJENÍ] Chyba při kontrole: {e}")
    
    def _add_vector_bleed(self, original_page, new_page, width, height, spadavka_points):
        """Přidá vektorovou spadávku pomocí zrcadlení vektorových objektů"""
        try:
            # Získání všech vektorových objektů ze stránky
            drawings = original_page.get_drawings()
            
            if not drawings:
                print("[WARNING] Žádné vektorové objekty nenalezeny - použití rastrové spadávky")
                self._add_raster_bleed_fallback(original_page, new_page, width, height, spadavka_points)
                return
            
            print(f"[VECTOR] Nalezeno {len(drawings)} vektorových objektů")
            
            # Přidání zrcadlených objektů pro spadávku
            self._mirror_vector_objects(drawings, new_page, width, height, spadavka_points)
            
        except Exception as e:
            print(f"[WARNING] Chyba při vektorovém zpracování: {e}")
            print("[FALLBACK] Použití rastrové spadávky jako zálohy")
            self._add_raster_bleed_fallback(original_page, new_page, width, height, spadavka_points)
    
    def _mirror_vector_objects(self, drawings, new_page, width, height, spadavka_points):
        """Zrcadlí vektorové objekty pro vytvoření spadávky"""
        # Horní spadávka
        for drawing in drawings:
            if drawing['rect'].y0 < spadavka_points:  # Objekt v horní části
                mirrored_drawing = self._mirror_drawing(drawing, 'horizontal', spadavka_points)
                new_page.insert_draw_annot(mirrored_drawing)
        
        # Spodní spadávka
        for drawing in drawings:
            if drawing['rect'].y1 > height - spadavka_points:  # Objekt ve spodní části
                mirrored_drawing = self._mirror_drawing(drawing, 'horizontal', spadavka_points)
                new_page.insert_draw_annot(mirrored_drawing)
        
        # Levá spadávka
        for drawing in drawings:
            if drawing['rect'].x0 < spadavka_points:  # Objekt v levé části
                mirrored_drawing = self._mirror_drawing(drawing, 'vertical', spadavka_points)
                new_page.insert_draw_annot(mirrored_drawing)
        
        # Pravá spadávka
        for drawing in drawings:
            if drawing['rect'].x1 > width - spadavka_points:  # Objekt v pravé části
                mirrored_drawing = self._mirror_drawing(drawing, 'vertical', spadavka_points)
                new_page.insert_draw_annot(mirrored_drawing)
    
    def _mirror_drawing(self, drawing, direction, spadavka_points):
        """Zrcadlí vektorový objekt"""
        mirrored = drawing.copy()
        rect = drawing['rect']
        
        if direction == 'horizontal':
            # Zrcadlení horizontálně
            mirrored['rect'] = fitz.Rect(
                rect.x0, 
                spadavka_points - (rect.y1 - rect.y0), 
                rect.x1, 
                spadavka_points
            )
        else:  # vertical
            # Zrcadlení vertikálně
            mirrored['rect'] = fitz.Rect(
                spadavka_points - (rect.x1 - rect.x0), 
                rect.y0, 
                spadavka_points, 
                rect.y1
            )
        
        return mirrored
    
    def _add_raster_bleed_fallback(self, original_page, new_page, width, height, spadavka_points):
        """Zálohní rastrová spadávka pro PDF bez vektorových objektů"""
        try:
            # Vytvoření rastrového náhledu s vysokým rozlišením
            matrix = fitz.Matrix(2, 2)  # 2x zvětšení pro kvalitu
            pix = original_page.get_pixmap(matrix=matrix, alpha=False)
            
            # Konverze na PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            # Vytvoření spadávky z rastru - převod na int
            spadavka_px = int(spadavka_points * 2)  # *2 kvůli zvětšení, převod na int
            new_img = self._create_raster_bleed(img, spadavka_px, already_cropped=False)
            
            # Vložení zpět do PDF
            img_bytes = io.BytesIO()
            new_img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            new_page.insert_image(new_page.rect, stream=img_bytes.getvalue())
            
        except Exception as e:
            print(f"[ERROR] Chyba při rastrové spadávce: {e}")
            # Pokud selže i rastrová spadávka, pokračujeme bez ní
    
    def _process_eps(self, input_path, output_path):
        """Zpracování EPS s optimalizací"""
        try:
            # Kontrola Ghostscript
            import subprocess
            import shutil
            
            gs_path = shutil.which('gswin64c')
            if not gs_path:
                gs_path = shutil.which('gs')
            if not gs_path:
                raise ValueError("Ghostscript není nainstalován nebo není v PATH")
            
            # Vytvoření dočasného PDF
            temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
            temp_pdf.close()
            
            try:
                # Konverze EPS na PDF s optimalizací
                result = subprocess.run([
                    gs_path,
                    '-sDEVICE=pdfwrite',
                    '-dNOPAUSE',
                    '-dBATCH',
                    '-dSAFER',
                    '-dPDFSETTINGS=/printer',  # Optimalizace pro tisk
                    '-dCompatibilityLevel=1.4',
                    f'-sOutputFile={temp_pdf.name}',
                    input_path
                ], check=True, capture_output=True, timeout=60)
                
                # Zpracování jako PDF
                result, info = self._process_pdf(temp_pdf.name, output_path)
                
                return result, f"EPS konvertován: {info}"
                
            finally:
                # Úklid
                try:
                    os.unlink(temp_pdf.name)
                except:
                    pass
                    
        except subprocess.TimeoutExpired:
            raise Exception("Konverze EPS trvala příliš dlouho (timeout 60s)")
        except Exception as e:
            raise Exception(f"Chyba při zpracování EPS: {str(e)}")
    
    def _create_raster_bleed(self, img, spadavka_size_px, already_cropped=False):
        """Vytvoří rastrovou spadávku: generuje okraje a rohy z kraje motivu. Preferuje mirror/flip, fallback stretch."""
        if already_cropped:
            # Obrázek je už ořezaný, použij ho přímo
            cropped_img = img
            cropped_width, cropped_height = cropped_img.size
        else:
            # Ořez až na grafiku pouze pokud není už ořezaný
            width, height = img.size
            left, top, right, bottom = self._detect_white_borders(img, tolerance=5)
            cropped_img = img.crop((left, top, right, bottom))
            cropped_width, cropped_height = cropped_img.size
        
        new_width = cropped_width + (2 * spadavka_size_px)
        new_height = cropped_height + (2 * spadavka_size_px)
        new_img = Image.new('RGB', (new_width, new_height), 'white')
        new_img.paste(cropped_img, (spadavka_size_px, spadavka_size_px))

        # --- Okraje ---
        # Horní okraj (prefer mirror, fallback stretch)
        top_row = cropped_img.crop((0, 0, cropped_width, spadavka_size_px))
        if self._is_border_white(top_row, cropped_width, spadavka_size_px, tolerance=5):
            # fallback: stretch první barevné řady
            first_row = cropped_img.crop((0, 0, cropped_width, 1)).resize((cropped_width, spadavka_size_px))
            new_img.paste(first_row, (spadavka_size_px, 0))
        else:
            top_flip = ImageOps.flip(top_row)
            new_img.paste(top_flip, (spadavka_size_px, 0))

        # Spodní okraj
        bottom_row = cropped_img.crop((0, cropped_height - spadavka_size_px, cropped_width, cropped_height))
        if self._is_border_white(bottom_row, cropped_width, spadavka_size_px, tolerance=5):
            last_row = cropped_img.crop((0, cropped_height - 1, cropped_width, cropped_height)).resize((cropped_width, spadavka_size_px))
            new_img.paste(last_row, (spadavka_size_px, new_height - spadavka_size_px))
        else:
            bottom_flip = ImageOps.flip(bottom_row)
            new_img.paste(bottom_flip, (spadavka_size_px, new_height - spadavka_size_px))

        # Levý okraj
        left_col = cropped_img.crop((0, 0, spadavka_size_px, cropped_height))
        if self._is_border_white(left_col, spadavka_size_px, cropped_height, tolerance=5):
            first_col = cropped_img.crop((0, 0, 1, cropped_height)).resize((spadavka_size_px, cropped_height))
            new_img.paste(first_col, (0, spadavka_size_px))
        else:
            left_mirror = ImageOps.mirror(left_col)
            new_img.paste(left_mirror, (0, spadavka_size_px))

        # Pravý okraj
        right_col = cropped_img.crop((cropped_width - spadavka_size_px, 0, cropped_width, cropped_height))
        if self._is_border_white(right_col, spadavka_size_px, cropped_height, tolerance=5):
            last_col = cropped_img.crop((cropped_width - 1, 0, cropped_width, cropped_height)).resize((spadavka_size_px, cropped_height))
            new_img.paste(last_col, (new_width - spadavka_size_px, spadavka_size_px))
        else:
            right_mirror = ImageOps.mirror(right_col)
            new_img.paste(right_mirror, (new_width - spadavka_size_px, spadavka_size_px))

        # --- Rohy ---
        # Levý horní roh
        corner = cropped_img.crop((0, 0, spadavka_size_px, spadavka_size_px))
        if self._is_border_white(corner, spadavka_size_px, spadavka_size_px, tolerance=5):
            pixel = cropped_img.getpixel((0, 0))
            corner_img = Image.new('RGB', (spadavka_size_px, spadavka_size_px), pixel)
        else:
            corner_img = ImageOps.mirror(ImageOps.flip(corner))
        new_img.paste(corner_img, (0, 0))

        # Pravý horní roh
        corner = cropped_img.crop((cropped_width - spadavka_size_px, 0, cropped_width, spadavka_size_px))
        if self._is_border_white(corner, spadavka_size_px, spadavka_size_px, tolerance=5):
            pixel = cropped_img.getpixel((cropped_width - 1, 0))
            corner_img = Image.new('RGB', (spadavka_size_px, spadavka_size_px), pixel)
        else:
            corner_img = ImageOps.mirror(ImageOps.flip(corner))
        new_img.paste(corner_img, (new_width - spadavka_size_px, 0))

        # Levý dolní roh
        corner = cropped_img.crop((0, cropped_height - spadavka_size_px, spadavka_size_px, cropped_height))
        if self._is_border_white(corner, spadavka_size_px, spadavka_size_px, tolerance=5):
            pixel = cropped_img.getpixel((0, cropped_height - 1))
            corner_img = Image.new('RGB', (spadavka_size_px, spadavka_size_px), pixel)
        else:
            corner_img = ImageOps.mirror(ImageOps.flip(corner))
        new_img.paste(corner_img, (0, new_height - spadavka_size_px))

        # Pravý dolní roh
        corner = cropped_img.crop((cropped_width - spadavka_size_px, cropped_height - spadavka_size_px, cropped_width, cropped_height))
        if self._is_border_white(corner, spadavka_size_px, spadavka_size_px, tolerance=5):
            pixel = cropped_img.getpixel((cropped_width - 1, cropped_height - 1))
            corner_img = Image.new('RGB', (spadavka_size_px, spadavka_size_px), pixel)
        else:
            corner_img = ImageOps.mirror(ImageOps.flip(corner))
        new_img.paste(corner_img, (new_width - spadavka_size_px, new_height - spadavka_size_px))

        return new_img

    def _get_background_color(self, mode):
        if mode == 'RGB':
            return (255, 255, 255)
        elif mode == 'L':
            return 255
        elif mode == 'CMYK':
            return (0, 0, 0, 0)
        elif mode == 'LAB':
            return (100, 0, 0)
        else:
            return 255

    def _apply_color_matching(self, spadavka_img, original_img, spadavka_px):
        """Aplikuje color matching pro 100% shodu barev na hranicích"""
        try:
            width, height = spadavka_img.size
            
            # Korekce levé hranice
            for y in range(spadavka_px, height - spadavka_px):
                # Referenční pixel z grafiky (první pixel grafiky)
                ref_pixel = original_img.getpixel((0, y - spadavka_px))
                # Současný pixel ve spadávce (poslední pixel spadávky)
                current_pixel = spadavka_img.getpixel((spadavka_px - 1, y))
                
                # Pokud se liší, použij referenční pixel
                if ref_pixel != current_pixel:
                    spadavka_img.putpixel((spadavka_px - 1, y), ref_pixel)
            
            # Korekce horní hranice
            for x in range(spadavka_px, width - spadavka_px):
                # Referenční pixel z grafiky (první řádek grafiky)
                ref_pixel = original_img.getpixel((x - spadavka_px, 0))
                # Současný pixel ve spadávce (poslední řádek spadávky)
                current_pixel = spadavka_img.getpixel((x, spadavka_px - 1))
                
                # Pokud se liší, použij referenční pixel
                if ref_pixel != current_pixel:
                    spadavka_img.putpixel((x, spadavka_px - 1), ref_pixel)
            
            # Korekce pravé hranice
            for y in range(spadavka_px, height - spadavka_px):
                # Referenční pixel z grafiky (poslední pixel grafiky)
                ref_pixel = original_img.getpixel((original_img.size[0] - 1, y - spadavka_px))
                # Současný pixel ve spadávce (první pixel pravé spadávky)
                current_pixel = spadavka_img.getpixel((width - spadavka_px, y))
                
                # Pokud se liší, použij referenční pixel
                if ref_pixel != current_pixel:
                    spadavka_img.putpixel((width - spadavka_px, y), ref_pixel)
            
            # Korekce spodní hranice
            for x in range(spadavka_px, width - spadavka_px):
                # Referenční pixel z grafiky (poslední řádek grafiky)
                ref_pixel = original_img.getpixel((x - spadavka_px, original_img.size[1] - 1))
                # Současný pixel ve spadávce (první řádek spodní spadávky)
                current_pixel = spadavka_img.getpixel((x, height - spadavka_px))
                
                # Pokud se liší, použij referenční pixel
                if ref_pixel != current_pixel:
                    spadavka_img.putpixel((x, height - spadavka_px), ref_pixel)
            
            print(f"[COLOR MATCHING] Aplikována korekce barev na hranicích")
            return spadavka_img
            
        except Exception as e:
            print(f"[WARNING] [COLOR MATCHING] Chyba při color matching: {e}")
            return spadavka_img 