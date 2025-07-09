import threading
from PIL import Image
import os

class ThumbnailManager:
    """
    Správa generování náhledů (thumbnails) – rychlý, progresivní, lazyload.
    Použití:
        manager = ThumbnailManager()
        fast_thumb = manager.get_fast_thumbnail(path)
        manager.get_quality_thumbnail_async(path, callback)
    """
    def __init__(self, fast_size=(64, 64), quality_size=(256, 256)):
        self.fast_size = fast_size
        self.quality_size = quality_size

    def get_fast_thumbnail(self, path):
        """Okamžitě vygeneruje malý, nekvalitní náhled (Pillow Image)."""
        img = Image.open(path)
        img = img.convert('RGB')
        img.thumbnail(self.fast_size, Image.BILINEAR)
        return img

    def get_quality_thumbnail_async(self, path, callback):
        """Na pozadí vygeneruje kvalitní náhled a zavolá callback(img)."""
        def worker():
            img = Image.open(path)
            img = img.convert('RGB')
            img.thumbnail(self.quality_size, Image.LANCZOS)
            callback(img)
        threading.Thread(target=worker, daemon=True).start()

# Lazyload: v GUI generuj náhled až při zobrazení (např. v on_scroll nebo při vstupu widgetu do viditelné oblasti)

# Příklad použití v GUI:
#
# from thumbnail_utils import ThumbnailManager
# manager = ThumbnailManager()
# fast_thumb = manager.get_fast_thumbnail('soubor.pdf')
# zobraz fast_thumb v GUI
#
# def update_gui_with_quality(img):
#     # aktualizuj widget s novým obrázkem
#     pass
# manager.get_quality_thumbnail_async('soubor.pdf', update_gui_with_quality) 