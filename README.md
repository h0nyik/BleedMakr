# BleedMakr 🎨

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-AGPL%203.0-green.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![Status](https://img.shields.io/badge/Status-Pre%20Alpha-orange.svg)](https://github.com/h0nyik/BleedMakr)
[![Version](https://img.shields.io/badge/Version-0.0.1-blue.svg)](https://github.com/h0nyik/BleedMakr/releases)

**Profesionální generátor spadávek pro reklamní agentury**

BleedMakr je nástroj pro automatické generování spadávek (bleed) pro tiskové PDF, obrázky a EPS soubory. Zachovává vektorovou kvalitu středu a generuje bitmapové okraje s plynulým napojením. Ideální pro přípravu tiskových dat bez ručního zásahu.

## 🚀 Funkce

- ✅ **Automatická detekce a generování spadávky**
- ✅ **Zachování vektorového středu PDF**
- ✅ **Inteligentní bitmapové okraje** s plynulým přechodem (soft fade)
- ✅ **Podpora formátů**: PDF, EPS, TIFF, JPG, PNG
- ✅ **Moderní GUI** včetně náhledu a logu operací
- ✅ **Inteligentní detekce bílých okrajů** - automatické ořezání
- ✅ **Adaptivní zrcadlení** - roztažení místo zrcadlení pro bílé okraje
- ✅ **Batch zpracování** více souborů
- ✅ **Export do PDF** s vysokým rozlišením (300 DPI)

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
python spadavka_generator.py
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

### Metody zpracování
1. **Standardní spadávka** - zrcadlení okrajů
2. **Ořezaná spadávka** - ořezání bílých okrajů + zrcadlení
3. **Roztažená spadávka** - roztažení nejbližších pixelů místo zrcadlení

## 🔧 Technické detaily

### Zpracování spadávek
- **Obrázky**: Inteligentní detekce okrajů + zrcadlení/roztažení
- **PDF**: Konverze na obrázek a zpracování
- **EPS**: Konverze na PDF pomocí Ghostscript

### Detekce okrajů
- **Tolerance**: 10 pixelů pro bílou barvu
- **Algoritmus**: Analýza řádků a sloupců pomocí numpy
- **Automatické ořezání**: Odstranění bílých okrajů před zpracováním

### Rozlišení
- **Výstupní PDF**: 300 DPI
- **Zachování kvality** původních souborů
- **Dynamická kvalita náhledu** podle velikosti

### Podporované formáty
- **Vstup**: PDF, EPS, TIFF, JPG, JPEG, PNG
- **Výstup**: PDF (vždy)

## 📁 Struktura projektu

```
BleedMakr/
├── spadavka_generator.py    # Hlavní aplikace s GUI
├── spadavka_engine.py       # Engine pro zpracování s detekcí okrajů
├── spadavka_engine_zaloha.py # Záloha engine
├── requirements.txt         # Python závislosti
├── test_app.py             # Testovací skript
├── test_white_borders.py   # Test detekce okrajů
├── test_pdf_bleed.py       # Test PDF spadávek
├── test_vector_pdf.py      # Test vektorových PDF
├── spustit.bat             # Spouštěcí skript pro Windows
├── LICENSE                 # AGPL-3.0 licence
└── README.md               # Tato dokumentace
```

## 🎯 Použití v reklamní agentuře

Aplikace je optimalizována pro:
- **Tiskové materiály**: Letáky, brožury, plakáty
- **Digitální tisk**: Velkoformátové tisky
- **Profesionální výstup**: PDF pro tiskárny
- **Batch zpracování**: Hromadné zpracování souborů
- **Automatické ořezání**: Odstranění bílých okrajů z importovaných souborů

## 🧪 Testování

Spusťte testy pro ověření funkcí:
```bash
python test_app.py              # Základní testy
python test_white_borders.py    # Test detekce okrajů
python test_pdf_bleed.py        # Test PDF spadávek
python test_vector_pdf.py       # Test vektorových PDF
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
- Zkontrolujte dostatek RAM
- Inteligentní detekce okrajů může zpomalit zpracování

### Bílé okraje se stále zrcadlí
- Zkontrolujte toleranci detekce (výchozí: 10 pixelů)
- Zkontrolujte log pro informace o použité metodě

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

**BleedMakr** - Profesionální řešení pro generování spadávek v reklamních agenturách 🎨 