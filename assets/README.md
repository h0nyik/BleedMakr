# Assets - Ikony a grafické soubory

Tato složka obsahuje ikony a grafické soubory pro BleedMakr aplikaci.

## Ikony pro různé platformy

### Windows (.ico)
- **icon.ico** - Hlavní ikona pro Windows aplikace
- **icon_16.ico** - 16x16 pixelů
- **icon_32.ico** - 32x32 pixelů  
- **icon_48.ico** - 48x48 pixelů
- **icon_256.ico** - 256x256 pixelů

### macOS (.icns)
- **icon.icns** - Hlavní ikona pro macOS aplikace
- **icon_16.icns** - 16x16 pixelů
- **icon_32.icns** - 32x32 pixelů
- **icon_128.icns** - 128x128 pixelů
- **icon_256.icns** - 256x256 pixelů
- **icon_512.icns** - 512x512 pixelů

### Linux (.png)
- **icon.png** - Hlavní ikona pro Linux aplikace
- **icon_16.png** - 16x16 pixelů
- **icon_32.png** - 32x32 pixelů
- **icon_48.png** - 48x48 pixelů
- **icon_64.png** - 64x64 pixelů
- **icon_128.png** - 128x128 pixelů
- **icon_256.png** - 256x256 pixelů

## Specifikace ikon

### Design
- **Téma**: Profesionální nástroj pro reklamní agentury
- **Styl**: Moderní, minimalistický
- **Barvy**: Modrá (#2c3e50) a bílá (#ffffff)
- **Symbol**: Spadávka/bleed symbol nebo písmeno "B"

### Technické požadavky
- **Formát**: PNG pro editaci, ICO/ICNS pro build
- **Průhlednost**: Podporována
- **Rozlišení**: Vektorové zdroje pro všechny velikosti
- **Kontrast**: Dobrá viditelnost na světlém i tmavém pozadí

## Použití v build skriptech

Build skripty automaticky detekují a použijí správné ikony:

- **Windows**: `icon.ico` v root složce
- **macOS**: `icon.icns` v root složce  
- **Linux**: `icon.png` v root složce

## Vytvoření ikon

### Z vektorového zdroje
1. Vytvořte vektorový soubor (SVG) s ikonou
2. Exportujte do různých velikostí
3. Konvertujte do požadovaných formátů

### Nástroje pro konverzi
- **ICO**: Online konvertory nebo ImageMagick
- **ICNS**: Icon Composer (macOS) nebo online nástroje
- **PNG**: Jakýkoliv grafický editor

## Umístění v projektu

```
BleedMakr/
├── assets/
│   ├── icons/
│   │   ├── windows/
│   │   ├── macos/
│   │   └── linux/
│   └── README.md
├── icon.ico          # Windows ikona (kopie z assets)
├── icon.icns         # macOS ikona (kopie z assets)
└── icon.png          # Linux ikona (kopie z assets)
``` 