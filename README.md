# BleedMakr

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-AGPL%203.0-green.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![Status](https://img.shields.io/badge/Status-Pre%20Alpha-orange.svg)](https://github.com/h0nyik/BleedMakr)
[![Version](https://img.shields.io/badge/version-0.0.1-blue)](https://github.com/h0nyik/BleedMakr/releases)

**Profesionální generátor spadávek pro reklamní agentury**

BleedMakr je nástroj pro automatické generování spadávek (bleed) pro tiskové PDF, obrázky a EPS soubory. Zachovává vektorovou kvalitu středu a generuje bitmapové okraje s plynulým napojením. Ideální pro přípravu tiskových dat bez ručního zásahu.

## 🚀 Funkce

- [OK] **Automatická detekce a generování spadávky**
- [OK] **Zachování vektorového středu PDF** - střed zůstává vektorový, pouze okraje bitmapové
- [OK] **Inteligentní bitmapové okraje** s plynulým napojením na grafiku
- [OK] **Podpora formátů**: PDF, EPS, TIFF, JPG, PNG
- [OK] **Moderní GUI** s drag&drop, náhledy a detailním logem operací
- [OK] **Inteligentní detekce bílých okrajů** - automatické ořezání až na grafiku
- [OK] **Adaptivní zrcadlení** - roztažení místo zrcadlení pro bílé okraje
- [OK] **Batch zpracování** více souborů s progress barem
- [OK] **Export do PDF** s vysokým rozlišením (300 DPI)
- [OK] **Bezlimitní zpracování** - odstranění limitu velikosti obrázků pro tiskové aplikace
- [OK] **Automatická diagnostika** - detailní informace o zpracování každého souboru
- [OK] **Kontrola napojení** - automatická kontrola shody pixelů na hranicích spadávky
- [OK] **Adaptivní DPI** - automatické snížení rozlišení pro velmi velké PDF
- [OK] **Color matching** - automatická korekce barev na hranicích spadávky

## 📋 Požadavky

- **Python 3.8+**
- **Windows 10/11** (testováno)
- **Minimálně 4GB RAM**
- **500MB volného místa**
- **Ghostscript** (pro EPS soubory)

## 🛠️ Instalace

### 1. Klonování repository
```bash
git clone https://github.com/h0nyik/BleedMakr.git
cd BleedMakr
```

### 2. Instalace závislostí
```bash
pip install -r requirements.txt
```

### 3. Instalace Ghostscript (pro EPS soubory)
- Stáhněte z [ghostscript.com](https://ghostscript.com/)
- Pro Windows: `gswin64c.exe` musí být v PATH

## 🎯 Použití

### Spuštění aplikace
```bash
python src/spadavka_generator.py
```

### Postup práce
1. **Klikněte "Přidat soubory"** a vyberte grafické soubory
2. **Nastavte velikost spadávky** (výchozí: 3 mm)
3. **Vyberte výstupní složku**
4. **Klikněte "Generovat spadávky"**

### Výstup
- Všechny soubory budou zpracovány s příponou `_spadavka.pdf`
- Log operací zobrazuje průběh zpracování a použité metody
- Náhledy všech formátů v reálném čase

## 🧠 Inteligentní zpracování

### Detekce bílých okrajů
Aplikace automaticky detekuje bílé nebo průhledné okraje a:
- **Ořezává** bílé okraje před vytvořením spadávky
- **Používá roztažení** místo zrcadlení pro jednobarevné okraje
- **Loguje** informace o použité metodě zpracování
- **Kontroluje napojení** - automatická kontrola shody pixelů na hranicích

### Metody zpracování
1. **Standardní spadávka** - zrcadlení okrajů
2. **Ořezaná spadávka** - ořezání bílých okrajů + zrcadlení
3. **Roztažená spadávka** - roztažení nejbližších pixelů místo zrcadlení
4. **Adaptivní DPI** - automatické snížení rozlišení pro velké soubory

### Diagnostika a monitoring
- **Detailní log** každého zpracovaného souboru
- **Kontrola napojení** - automatická kontrola shody pixelů na hranicích spadávky
- **Informace o metodě** - zobrazení použité metody zpracování
- **Statistiky ořezu** - procento snížení plochy po ořezu

## 🔧 Technické detaily

### Zpracování spadávek
- **Obrázky**: Inteligentní detekce okrajů + zrcadlení/roztažení
- **PDF**: Konverze na obrázek a zpracování
- **EPS**: Konverze na PDF pomocí Ghostscript

### Detekce okrajů
- **Tolerance**: 10 pixelů pro bílou barvu
- **Algoritmus**: Analýza řádků a sloupců pomocí numpy
- **Automatické ořezání**: Odstranění bílých okrajů před zpracováním

### Rozlišení a výkon
- **Výstupní PDF**: 300 DPI (automaticky sníženo na 150 DPI pro velmi velké soubory)
- **Zachování kvality** původních souborů
- **Dynamická kvalita náhledu** podle velikosti
- **Bezlimitní zpracování** - odstranění Pillow limitu pro tiskové aplikace
- **Optimalizace paměti** - inteligentní zpracování velkých souborů

### Podporované formáty
- **Vstup**: PDF, EPS, TIFF, JPG, JPEG, PNG
- **Výstup**: PDF (vždy)

## 📁 Struktura projektu

```
BleedMakr/
├── src/
│   ├── spadavka_generator.py    # Hlavní aplikace s GUI
│   ├── spadavka_engine.py       # Engine pro zpracování s detekcí okrajů
│   └── thumbnail_utils.py       # Správa náhledů
├── tests/
│   ├── test_app.py             # Testovací skript
│   ├── test_white_borders.py   # Test detekce okrajů
│   ├── test_pdf_bleed.py       # Test PDF spadávek
│   └── test_vector_pdf.py      # Test vektorových PDF
├── scripts/
│   └── build_exe.py            # Build skript pro .exe
├── docs/
│   ├── README.md               # Detailní dokumentace
│   ├── RELEASE_NOTES.md        # Poznámky k vydání
│   └── CODE_SIGNING.md         # Dokumentace podpisu kódu
├── requirements.txt            # Python závislosti
├── version.txt                 # Verze aplikace
├── spustit.bat                 # Spouštěcí skript pro Windows
├── LICENSE                     # AGPL-3.0 licence
└── README.md                   # Tato dokumentace
```

## 🎯 Použití v reklamní agentuře

Aplikace je optimalizována pro:
- **Tiskové materiály**: Letáky, brožury, plakáty
- **Digitální tisk**: Velkoformátové tisky (až 2x3m)
- **Profesionální výstup**: PDF pro tiskárny s vysokým rozlišením
- **Batch zpracování**: Hromadné zpracování souborů s progress barem
- **Automatické ořezání**: Odstranění bílých okrajů z importovaných souborů
- **Velkoformátové tisky**: Podpora pro velmi velké PDF (až 1 miliarda pixelů)
- **Kontrola kvality**: Automatická kontrola napojení spadávky na grafiku

## 🧪 Testování

Spusťte testy pro ověření funkcí:
```bash
python tests/test_app.py              # Základní testy
python tests/test_white_borders.py    # Test detekce okrajů
python tests/test_pdf_bleed.py        # Test PDF spadávek
python tests/test_vector_pdf.py       # Test vektorových PDF
```

## 🛠️ Řešení problémů

### Chyba "Ghostscript not found"
- Nainstalujte Ghostscript z [ghostscript.com](https://ghostscript.com/)
- Přidejte do systémové PATH

### Chyba "PIL not found"
```bash
pip install Pillow
```

### Pomalé zpracování
- Velké soubory mohou trvat déle
- Zkontrolujte dostatek RAM (minimálně 4GB)
- Inteligentní detekce okrajů může zpomalit zpracování
- Velkoformátové PDF (>1 miliarda pixelů) se automaticky zpracují s nižším DPI

### Bílé okraje se stále zrcadlí
- Zkontrolujte toleranci detekce (výchozí: 10 pixelů)
- Zkontrolujte log pro informace o použité metodě
- Aplikace automaticky detekuje bílé okraje a ořezává je

### Chyba "Image size exceeds limit"
- ✅ **VYŘEŠENO** - Limit byl odstraněn pro tiskové aplikace
- Velké PDF se automaticky zpracují s nižším DPI
- Aplikace nyní podporuje až 1 miliardu pixelů

## 🤝 Přispívání

Příspěvky jsou vítány! Prosím:

1. Fork repository
2. Vytvořte feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit změny (`git commit -m 'Add some AmazingFeature'`)
4. Push do branch (`git push origin feature/AmazingFeature`)
5. Otevřete Pull Request

## 📞 Podpora

Pro technickou podporu:
- Otevřete [Issue](https://github.com/h0nyik/BleedMakr/issues) na GitHubu
- Kontaktujte vývojový tým

## 📄 Licence

Tento projekt je licencován pod **GNU Affero General Public License v3.0 (AGPL-3.0)** – maximálně restriktivní copyleft licence. Jakékoliv úpravy a nasazení musí být zveřejněny pod stejnou licencí.

Více v souboru [LICENSE](LICENSE).

## ⭐ Hvězdičky

Pokud vám tento projekt pomohl, dejte mu hvězdičku na GitHubu! ⭐

---

## 🆕 Nejnovější vylepšení (v0.0.1)

### ✅ Vyřešené problémy
- **Odstranění limitu velikosti obrázků** - Aplikace nyní zpracuje i velmi velké tiskové PDF
- **Automatická diagnostika** - Detailní informace o zpracování každého souboru
- **Kontrola napojení** - Automatická kontrola shody pixelů na hranicích spadávky
- **Adaptivní DPI** - Automatické snížení rozlišení pro velmi velké PDF (>1 miliarda pixelů)

### 🎯 Optimalizace pro tiskové aplikace
- **Bezlimitní zpracování** - Odstranění Pillow limitu pro tiskové aplikace
- **Velkoformátové tisky** - Podpora pro PDF až 2x3m s vysokým rozlišením
- **Inteligentní optimalizace** - Automatické snížení DPI pro velké soubory
- **Kontrola kvality** - Automatická kontrola napojení spadávky na grafiku

### 📊 Výkonnostní vylepšení
- **Optimalizace paměti** - Inteligentní zpracování velkých souborů
- **Adaptivní zpracování** - Automatické přizpůsobení podle velikosti souboru
- **Progress tracking** - Detailní sledování průběhu zpracování
- **Error handling** - Robustní zpracování chyb s detailními zprávami

**BleedMakr** - Profesionální řešení pro generování spadávek v reklamních agenturách 

<!-- Trigger build: testovací změna pro GitHub Actions --> 
