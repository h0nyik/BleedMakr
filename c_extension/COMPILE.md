# Kompilace C modulu pro detekci okrajů

## 🛠️ Požadavky

### Základní požadavky:
- **Python 3.8+**
- **numpy** (`pip install numpy`)
- **setuptools** (`pip install setuptools`)
- **C kompilátor**

### C kompilátory podle platformy:

#### Windows:
- **Visual Studio Build Tools** nebo **Visual Studio Community**
- **MinGW-w64** (alternativa)

#### macOS:
- **Xcode Command Line Tools** (`xcode-select --install`)
- **Clang** (součást Xcode)

#### Linux:
- **GCC** (`sudo apt-get install build-essential` na Ubuntu/Debian)
- **GCC** (`sudo yum groupinstall "Development Tools"` na CentOS/RHEL)

## 🔧 Kompilace

### 1. Přechod do složky C modulu
```bash
cd c_extension
```

### 2. Kompilace modulu
```bash
python setup_edge_detection.py build_ext --inplace
```

### 3. Ověření kompilace
```bash
python test_c_module.py
```

## 🐛 Řešení problémů

### Chyba "numpy/arrayobject.h not found"
```bash
pip install numpy
```

### Chyba "compiler not found" (Windows)
```bash
# Instalace Visual Studio Build Tools
# Nebo použití MinGW
python setup_edge_detection.py build_ext --inplace --compiler=mingw32
```

### Chyba "math.h not found" (macOS)
```bash
# Instalace Xcode Command Line Tools
xcode-select --install
```

### Chyba "gcc not found" (Linux)
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install build-essential

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
```

## 📊 Optimalizace kompilace

### Pro maximální výkon:
```bash
# Linux/macOS
CFLAGS="-O3 -march=native -ffast-math" python setup_edge_detection.py build_ext --inplace

# Windows (Visual Studio)
python setup_edge_detection.py build_ext --inplace --compiler=msvc
```

### Pro debug:
```bash
CFLAGS="-g -O0" python setup_edge_detection.py build_ext --inplace
```

## 🔍 Testování kompilace

### Základní test:
```bash
python test_c_module.py
```

### Benchmark test:
```bash
python benchmark.py
```

### Ruční test:
```python
python -c "
from edge_detection_wrapper import EdgeDetectionWrapper
wrapper = EdgeDetectionWrapper()
print('✅ C modul načten úspěšně')
"
```

## 📁 Výstupní soubory

Po úspěšné kompilaci se vytvoří:
- `edge_detection.*.so` (Linux/macOS)
- `edge_detection.*.pyd` (Windows)
- `build/` složka s dočasnými soubory

## 🔄 Aktualizace modulu

Při změnách v C kódu:
```bash
# Vyčištění starých souborů
python setup_edge_detection.py clean --all

# Nová kompilace
python setup_edge_detection.py build_ext --inplace
```

## 🌐 Cross-compilace

### Pro ARM64 (Apple Silicon):
```bash
ARCHFLAGS="-arch arm64" python setup_edge_detection.py build_ext --inplace
```

### Pro různé platformy:
```bash
# Linux x86_64
python setup_edge_detection.py build_ext --inplace --plat-name=linux-x86_64

# macOS x86_64
python setup_edge_detection.py build_ext --inplace --plat-name=macosx-x86_64
```

## 📋 Kontrolní seznam

- [ ] C kompilátor nainstalován
- [ ] numpy nainstalován
- [ ] setuptools nainstalován
- [ ] Kompilace proběhla bez chyb
- [ ] Test prošel úspěšně
- [ ] Benchmark ukazuje očekávané zrychlení

## 🆘 Podpora

Při problémech:
1. Zkontrolujte verzi Python a numpy
2. Ověřte instalaci C kompilátoru
3. Spusťte test s debug informacemi
4. Zkontrolujte logy kompilace 