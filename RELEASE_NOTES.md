# BleedMakr v0.0.1 - První Release

## Profesionální generátor spadávek pro reklamní agentury

### ✨ Hlavní funkce:

- [OK] **Perfektní napojení spadávky** - Color matching algoritmus pro 100% shodu barev
- [OK] **Zachování vektorové kvality** - PDF střed zůstává vektorový
- [OK] **Inteligentní detekce okrajů** - Automatické ořezání bílých okrajů
- [OK] **Moderní GUI** - Drag&drop podpora, náhledy, progress bar
- [OK] **Podpora formátů**: PDF, EPS, PNG, JPG, TIFF
- [OK] **Batch zpracování** - Více souborů najednou
- [OK] **Export do PDF** - Vysoké rozlišení (300 DPI)
- [OK] **Diagnostika** - Detailní log operací a kontrola napojení

### 🔧 Technické vylepšení:

- **Pixel-perfect napojení** - Eliminace interpolace při zrcadlení
- **Bezpečnostní kontroly** - Validace rozměrů a pozic
- **Optimalizovaná detekce** - Inteligentní rozpoznání bílých okrajů
- **Color matching** - Automatická korekce barev na hranicích
- **Diagnostické nástroje** - Kompletní trasování zpracování

### 📋 Požadavky:

- **Windows 10/11** (64-bit)
- **Minimálně 4GB RAM**
- **500MB volného místa**
- **Ghostscript** (pro EPS soubory) - volitelné

### 🚀 Instalace:

#### Varianta A: Spustitelný soubor (.exe)
1. Stáhněte `BleedMakr-v0.0.1-Windows-x64.zip`
2. Rozbalte do libovolné složky
3. Spusťte `BleedMakr.exe`

#### Varianta B: Python zdrojový kód
1. Klonujte repository: `git clone https://github.com/h0nyik/BleedMakr.git`
2. Nainstalujte závislosti: `pip install -r requirements.txt`
3. Spusťte: `python spadavka_generator.py`

### 🔧 Použití:

1. **Přidání souborů** - Přetáhněte soubory do aplikace nebo klikněte "Přidat soubory"
2. **Nastavení spadávky** - Zadejte velikost spadávky v mm (výchozí: 3 mm)
3. **Výstupní složka** - Vyberte, kam uložit zpracované soubory
4. **Generování** - Klikněte "Generovat spadávky" a sledujte progress

### 🎯 Použití v reklamní agentuře:

- **Tiskové materiály** - Letáky, brožury, plakáty
- **Digitální tisk** - Velkoformátové tisky
- **Profesionální výstup** - PDF pro tiskárny
- **Automatizace** - Batch zpracování projektů

### 🐛 Známé problémy:

- Velmi malé soubory (< 50x50 px) mohou způsobit problémy
- EPS soubory vyžadují Ghostscript pro správné zpracování
- Velmi složité PDF s transparentnostmi mohou mít drobné odchylky

### 📈 Plánované vylepšení (budoucí verze):

- [ ] Podpora CMYK barevného prostoru
- [ ] Automatická detekce ořezových značek
- [ ] Podpora AI a SVG formátů
- [ ] Batch export do různých formátů
- [ ] Pokročilé nastavení diagnostiky

### 🤝 Přispívání:

Projekt je open source pod AGPL-3.0 licencí. Příspěvky jsou vítány!

1. Fork repository
2. Vytvořte feature branch
3. Commit změny
4. Push a otevřete Pull Request

### 📞 Podpora:

- **GitHub Issues**: [Nahlášení problémů](https://github.com/h0nyik/BleedMakr/issues)
- **Dokumentace**: [README.md](https://github.com/h0nyik/BleedMakr/blob/master/README.md)
- **Licence**: [AGPL-3.0](https://github.com/h0nyik/BleedMakr/blob/master/LICENSE)

---

**BleedMakr v0.0.1** - První stabilní verze pro produkční použití! 🎉 