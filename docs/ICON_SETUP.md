# Nastavení ikon pro BleedMakr

## Přehled

BleedMakr používá vlastní ikony pro všechny platformy:
- **Windows**: `icon.ico`
- **macOS**: `icon.icns`
- **Linux**: `icon.png`

## Automatické vytvoření ikon

### Požadavky
- **ImageMagick** nainstalovaný na `C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\`
- **Zdrojová ikona** `BleedMakr.png` v root složce projektu

### Rychlé nastavení
```bash
# Umístěte BleedMakr.png do root složky projektu
# Spusťte automatické vytvoření ikon
python scripts/setup_bleedmakr_icons.py
```

### Co skript udělá
1. **Zkontroluje** dostupnost ImageMagick a zdrojové ikony
2. **Vytvoří** různé velikosti ikon pro všechny platformy
3. **Zkonvertuje** PNG do ICO a ICNS formátů
4. **Umístí** ikony do správných složek pro build

## Struktura ikon

### Root složka (pro build)
```
BleedMakr/
├── icon.ico          # Windows ikona
├── icon.icns         # macOS ikona
└── icon.png          # Linux ikona
```

### Assets složka (zdroje)
```
BleedMakr/
├── assets/
│   └── icons/
│       ├── windows/
│       │   ├── icon_16.png
│       │   ├── icon_32.png
│       │   ├── icon_48.png
│       │   └── icon_256.png
│       ├── macos/
│       │   ├── icon_16.png
│       │   ├── icon_32.png
│       │   ├── icon_128.png
│       │   ├── icon_256.png
│       │   └── icon_512.png
│       └── linux/
│           ├── icon_16.png
│           ├── icon_32.png
│           ├── icon_48.png
│           ├── icon_64.png
│           ├── icon_128.png
│           └── icon_256.png
```

## Velikosti ikon

### Windows (.ico)
- 16x16 pixelů
- 32x32 pixelů
- 48x48 pixelů
- 256x256 pixelů

### macOS (.icns)
- 16x16 pixelů
- 32x32 pixelů
- 128x128 pixelů
- 256x256 pixelů
- 512x512 pixelů

### Linux (.png)
- 16x16 pixelů
- 32x32 pixelů
- 48x48 pixelů
- 64x64 pixelů
- 128x128 pixelů
- 256x256 pixelů

## Použití v build skriptech

Build skripty automaticky detekují a použijí ikony:

```python
# Windows
icon_setting = "'icon.ico' if os.path.exists('icon.ico') else None"

# macOS
icon_setting = "'icon.icns' if os.path.exists('icon.icns') else None"

# Linux
icon_setting = "'icon.png' if os.path.exists('icon.png') else None"
```

## Aktualizace ikon

### Změna zdrojové ikony
1. Nahraďte `BleedMakr.png` novou ikonou
2. Spusťte: `python scripts/setup_bleedmakr_icons.py`
3. Všechny platformové ikony se automaticky aktualizují

### Ruční vytvoření
```bash
# Vytvoření pouze testovacích ikon
python scripts/generate_icons.py

# Vytvoření z vlastního SVG
python scripts/generate_icons.py path/to/icon.svg
```

## Řešení problémů

### ImageMagick nenalezen
```
❌ ImageMagick nenalezen: C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe
```
**Řešení**: 
- Nainstalujte ImageMagick z [imagemagick.org](https://imagemagick.org/)
- Nebo upravte cestu v `scripts/setup_bleedmakr_icons.py`

### Zdrojová ikona nenalezena
```
❌ BleedMakr.png nenalezen
```
**Řešení**: Umístěte `BleedMakr.png` do root složky projektu

### Chyba při konverzi
```
❌ Chyba při vytváření ICO/ICNS
```
**Řešení**: 
- Zkontrolujte, že ImageMagick je správně nainstalován
- Zkontrolujte, že zdrojová ikona je validní PNG
- Zkuste spustit ImageMagick přímo z příkazové řádky

## Nástroje pro správu ikon

### `scripts/setup_bleedmakr_icons.py`
- Automatické vytvoření všech ikon z `BleedMakr.png`
- Používá ImageMagick pro konverzi
- Vytvoří všechny potřebné velikosti

### `scripts/generate_icons.py`
- Vytvoření testovacích ikon
- Podpora pro konverzi z SVG
- Fallback řešení bez ImageMagick

### `scripts/manage_icons.py`
- Kontrola dostupnosti ikon
- Validace formátů
- Správa ikon v projektu

## Build s ikonami

Po vytvoření ikon můžete spustit build:

```bash
# Windows build
python scripts/build_exe.py

# macOS build (na macOS)
python scripts/build_exe.py

# Linux build (na Linux)
python scripts/build_exe.py
```

Build skripty automaticky detekují a použijí správné ikony pro každou platformu.

## Poznámky

- **Kvalita ikon**: Používejte vysoké rozlišení (minimálně 256x256) pro zdrojovou ikonu
- **Průhlednost**: PNG ikony podporují průhlednost
- **Formáty**: ICO a ICNS jsou proprietární formáty, PNG je univerzální
- **Velikosti**: Všechny velikosti jsou vytvořeny automaticky z jednoho zdroje 