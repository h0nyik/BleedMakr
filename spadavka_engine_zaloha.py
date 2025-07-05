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
        print(f"🔍 Analýza obrázku: {width}x{height} pixelů")
        
        # Kontrola režimu obrázku
        if img.mode == 'RGBA':
            print(f"🎨 RGBA režim - kontrola průhlednosti a světlosti")
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
            print(f"🎨 RGB režim - kontrola světlosti")
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
        print(f"📐 Detekované okraje: left={left_border}, top={top_border}, right={right_border}, bottom={bottom_border}")
        print(f"✂️ Ořezané rozměry: {right_border-left_border} x {bottom_border-top_border}")
        print(f"📊 Snížení plochy: {area_reduction:.1f}%")
        
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
        
        print(f"🔍 Detekce okrajů obsahu: {width}x{height} pixelů")
        
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
        
        print(f"📐 Detekované okraje obsahu: left={left_border}, top={top_border}, right={right_border}, bottom={bottom_border}")
        print(f"✂️ Ořezané rozměry: {right_border-left_border} x {bottom_border-top_border}")
        print(f"📊 Snížení plochy: {area_reduction:.1f}%")
        
        # Pokud se plocha snížila o méně než 1%, nepovažujeme to za významné ořezání
        if area_reduction < 1:
            print(f"⚠️ Malé snížení plochy - použití původních rozměrů")
            return 0, 0, width, height
        
        print(f"✅ Významné snížení plochy - aplikování ořezu")
        return left_border, top_border, right_border, bottom_border
    
    def _create_intelligent_spadavka(self, img, width, height, new_width, new_height):
        """Vytvoří inteligentní spadávku s detekcí bílých okrajů"""
        # Detekce bílých okrajů
        left, top, right, bottom = self._detect_white_borders(img)
        
        # Kontrola, zda je potřeba ořezat
        needs_crop = (left > 0 or top > 0 or right < width or bottom < height)
        
        if needs_crop:
            # Ořezání bílých okrajů
            cropped_img = img.crop((left, top, right, bottom))
            cropped_width, cropped_height = cropped_img.size
            
            # Přepočítání rozměrů pro spadávku
            new_cropped_width = cropped_width + (2 * self.spadavka_size_px)
            new_cropped_height = cropped_height + (2 * self.spadavka_size_px)
            
            new_img = Image.new('RGB', (new_cropped_width, new_cropped_height), 'white')
            
            # Vložení ořezaného obrázku do středu
            new_img.paste(cropped_img, (self.spadavka_size_px, self.spadavka_size_px))
            
            # Vytvoření spadávky z ořezaného obrázku
            self._add_mirrored_borders(cropped_img, new_img, cropped_width, cropped_height, 
                                     new_cropped_width, new_cropped_height)
            
            return new_img, f"Ořezány bílé okraje: {left},{top},{right},{bottom}"
        else:
            # Standardní spadávka bez ořezu
            new_img = Image.new('RGB', (new_width, new_height), 'white')
            new_img.paste(img, (self.spadavka_size_px, self.spadavka_size_px))
            self._add_mirrored_borders(img, new_img, width, height, new_width, new_height)
            return new_img, "Standardní spadávka"
    
    def _add_mirrored_borders(self, original_img, new_img, width, height, new_width, new_height):
        """Přidá zrcadlené okraje pro spadávku s kontrolou kvality"""
        if self.spadavka_size_px <= 0:
            return
        
        # Kontrola kvality okrajů před zrcadlením
        border_quality = self._check_border_quality(original_img, width, height)
        
        if border_quality['has_content']:
            # Standardní zrcadlení
            self._add_standard_mirrored_borders(original_img, new_img, width, height, new_width, new_height)
        else:
            # Alternativní metody pro prázdné okraje
            self._add_alternative_borders(original_img, new_img, width, height, new_width, new_height)
    
    def _check_border_quality(self, img, width, height):
        """Kontroluje kvalitu okrajů pro zrcadlení"""
        # Kontrola horního okraje
        top_border = img.crop((0, 0, width, min(self.spadavka_size_px, height)))
        top_has_content = not self._is_border_white(top_border)
        
        # Kontrola spodního okraje
        bottom_border = img.crop((0, max(0, height - self.spadavka_size_px), width, height))
        bottom_has_content = not self._is_border_white(bottom_border)
        
        # Kontrola levého okraje
        left_border = img.crop((0, 0, min(self.spadavka_size_px, width), height))
        left_has_content = not self._is_border_white(left_border)
        
        # Kontrola pravého okraje
        right_border = img.crop((max(0, width - self.spadavka_size_px), 0, width, height))
        right_has_content = not self._is_border_white(right_border)
        
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
        """Přidá standardní zrcadlené okraje"""
        # Horní spadávka
        top_mirror = ImageOps.mirror(original_img.crop((0, 0, width, self.spadavka_size_px)))
        new_img.paste(top_mirror, (self.spadavka_size_px, 0))
        
        # Spodní spadávka
        bottom_mirror = ImageOps.mirror(original_img.crop((0, height - self.spadavka_size_px, width, height)))
        new_img.paste(bottom_mirror, (self.spadavka_size_px, new_height - self.spadavka_size_px))
        
        # Levá spadávka
        left_mirror = ImageOps.mirror(original_img.crop((0, 0, self.spadavka_size_px, height)))
        new_img.paste(left_mirror, (0, self.spadavka_size_px))
        
        # Pravá spadávka
        right_mirror = ImageOps.mirror(original_img.crop((width - self.spadavka_size_px, 0, width, height)))
        new_img.paste(right_mirror, (new_width - self.spadavka_size_px, self.spadavka_size_px))
        
        # Rohové spadávky
        self._add_corner_borders(original_img, new_img, width, height, new_width, new_height)
    
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
        """Přidá rohové spadávky"""
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
                # Konverze do RGB pokud je potřeba
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Získání rozměrů
                width, height = img.size
                
                # Kontrola minimální velikosti
                if width < 10 or height < 10:
                    raise ValueError("Obrázek je příliš malý pro zpracování")
                
                # Vytvoření nového obrázku se spadávkou
                new_width = width + (2 * self.spadavka_size_px)
                new_height = height + (2 * self.spadavka_size_px)
                
                # Optimalizace pro velké obrázky
                if new_width * new_height > 100000000:  # 100MP
                    raise ValueError("Obrázek je příliš velký pro zpracování")
                
                # Inteligentní vytvoření spadávky
                new_img, processing_info = self._create_intelligent_spadavka(img, width, height, new_width, new_height)
                
                # Uložení s optimalizací
                new_img.save(output_path, 'PDF', resolution=300.0, optimize=True)
                
                # Vrácení informace o zpracování
                return True, processing_info
                
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
            width, height = rect.width, rect.height

            spadavka_points = self.spadavka_size_mm * 2.83465  # mm na body
            new_width = width + 2 * spadavka_points
            new_height = height + 2 * spadavka_points

            # 1. Vytvoření bitmapy stránky
            dpi = 300
            scale_factor = dpi / 72
            matrix = fitz.Matrix(scale_factor, scale_factor)
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            spadavka_px = int(spadavka_points * scale_factor)
            img_bleed = self._create_raster_bleed(img, spadavka_px)

            # 2. Ořez bitmapy až na grafiku (žádná bílá na okraji)
            left, top, right, bottom = self._detect_white_borders(img, tolerance=5)
            cropped_img = img.crop((left, top, right, bottom))
            cropped_width, cropped_height = cropped_img.size

            # 3. Vytvoření spadávky z této bitmapy
            new_img = self._create_raster_bleed(cropped_img, spadavka_px)

            # 4. Vložení bitmapové spadávky do PDF
            new_doc = fitz.open()
            new_page = new_doc.new_page(width=new_width, height=new_height)

            img_bytes = io.BytesIO()
            new_img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            new_page.insert_image(
                fitz.Rect(0, 0, new_width, new_height),
                stream=img_bytes.getvalue()
            )

            # 5. Překrytí středem původní vektorové stránky
            new_page.show_pdf_page(
                fitz.Rect(spadavka_points, spadavka_points, spadavka_points + width, spadavka_points + height),
                doc, 0
            )

            new_doc.save(output_path, garbage=4, deflate=True)
            new_doc.close()
            doc.close()
            return True, "Vektor zachován, bitmapová spadávka pouze v okrajích"
        except Exception as e:
            raise Exception(f"Chyba při zpracování PDF: {str(e)}")
    
    def _add_vector_bleed(self, original_page, new_page, width, height, spadavka_points):
        """Přidá vektorovou spadávku pomocí zrcadlení vektorových objektů"""
        try:
            # Získání všech vektorových objektů ze stránky
            drawings = original_page.get_drawings()
            
            if not drawings:
                print("⚠️ Žádné vektorové objekty nenalezeny - použití rastrové spadávky")
                self._add_raster_bleed_fallback(original_page, new_page, width, height, spadavka_points)
                return
            
            print(f"🎨 Nalezeno {len(drawings)} vektorových objektů")
            
            # Přidání zrcadlených objektů pro spadávku
            self._mirror_vector_objects(drawings, new_page, width, height, spadavka_points)
            
        except Exception as e:
            print(f"⚠️ Chyba při vektorovém zpracování: {e}")
            print("🔄 Použití rastrové spadávky jako zálohy")
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
            new_img = self._create_raster_bleed(img, spadavka_px)
            
            # Vložení zpět do PDF
            img_bytes = io.BytesIO()
            new_img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            new_page.insert_image(new_page.rect, stream=img_bytes.getvalue())
            
        except Exception as e:
            print(f"❌ Chyba při rastrové spadávce: {e}")
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
    
    def _create_raster_bleed(self, img, spadavka_size_px):
        """Vytvoří rastrovou spadávku: po ořezu na grafiku generuje okraje a rohy z kraje motivu. Preferuje mirror/flip, fallback stretch."""
        width, height = img.size
        # 1. Ořez až na grafiku
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