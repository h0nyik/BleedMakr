# BleedMakr - Instalace na macOS

## 🍎 Spuštění BleedMakr na macOS

### **Problém s aktuálními buildy**
GitHub Actions aktuálně vytváří macOS buildy, které **nejsou správně konfigurované pro spuštění**. Toto je známý problém, který bude opraven v příští verzi.

### **Řešení: Spuštění z Python zdrojového kódu**

#### **Krok 1: Stáhněte zdrojový kód**
```bash
git clone https://github.com/h0nyik/BleedMakr.git
cd BleedMakr
```

#### **Krok 2: Nainstalujte Python 3.8+**
Pokud nemáte Python nainstalovaný:
```bash
# Pomocí Homebrew (doporučeno)
brew install python

# Nebo stáhněte z python.org
# https://www.python.org/downloads/macos/
```

#### **Krok 3: Nainstalujte závislosti**
```bash
pip3 install -r requirements.txt
```

#### **Krok 4: Spusťte aplikaci**
```bash
python3 src/spadavka_generator.py
```

### **Automatický spouštěcí skript**

Vytvořil jsem spouštěcí skript `spustit_macos.sh`:

1. **Udělejte skript spustitelný:**
   ```bash
   chmod +x spustit_macos.sh
   ```

2. **Spusťte skript:**
   ```bash
   ./spustit_macos.sh
   ```

### **Řešení problémů**

#### **Chyba: "Python3 není nainstalovaný"**
```bash
# Instalace pomocí Homebrew
brew install python

# Nebo stáhněte z python.org
```

#### **Chyba: "PIL not found"**
```bash
pip3 install Pillow
```

#### **Chyba: "fitz not found"**
```bash
pip3 install pymupdf
```

#### **Chyba: "Ghostscript not found" (pro EPS soubory)**
```bash
# Instalace pomocí Homebrew
brew install ghostscript

# Nebo stáhněte z ghostscript.com
```

### **Požadavky pro macOS**

- **macOS 10.14+** (Mojave nebo novější)
- **Python 3.8+**
- **Minimálně 4GB RAM**
- **500MB volného místa**
- **Ghostscript** (pro EPS soubory)

### **Funkce na macOS**

✅ **Všechny funkce fungují stejně jako na Windows:**
- Automatická detekce a generování spadávek
- Zachování vektorového středu PDF
- Inteligentní bitmapové okraje
- Podpora formátů: PDF, EPS, TIFF, JPG, PNG
- Moderní GUI s drag&drop
- Inteligentní detekce bílých okrajů
- Batch zpracování více souborů
- Export do PDF s vysokým rozlišením (300 DPI)

### **Příští verze**

V příští verzi bude:
- ✅ Správný macOS .app bundle
- ✅ Automatické podepisování kódu
- ✅ Notarizace pro macOS Gatekeeper
- ✅ Drag&drop .app do Applications složky

### **Kontakt**

Pokud máte problémy s instalací nebo spuštěním:
- Otevřete [Issue na GitHubu](https://github.com/h0nyik/BleedMakr/issues)
- Popište váš macOS systém a chybové hlášky

---

**BleedMakr** - Profesionální řešení pro generování spadávek na macOS 