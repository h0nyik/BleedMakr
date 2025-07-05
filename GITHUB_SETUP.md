# Instrukce pro nahrání na GitHub

## 1. Vytvoření repository na GitHub

1. Jděte na [GitHub.com](https://github.com) a přihlaste se
2. Klikněte na zelené tlačítko "New" nebo "+" → "New repository"
3. Nastavte:
   - **Repository name**: `BleedMakr`
   - **Description**: `Profesionální generátor spadávek pro reklamní agentury`
   - **Visibility**: `Public`
   - **NEZAŠKRTÁVEJTE** "Add a README file" (už máme)
   - **NEZAŠKRTÁVEJTE** "Add .gitignore" (už máme)
   - **NEZAŠKRTÁVEJTE** "Choose a license" (už máme)

4. Klikněte "Create repository"

## 2. Inicializace Git v lokálním projektu

Otevřete PowerShell nebo Command Prompt ve složce projektu a spusťte:

```bash
# Inicializace Git repository
git init

# Přidání všech souborů
git add .

# První commit
git commit -m "Initial commit: BleedMakr - Profesionální generátor spadávek"

# Přidání remote repository (nahraďte YOUR_USERNAME vaším GitHub uživatelským jménem)
git remote add origin https://github.com/YOUR_USERNAME/BleedMakr.git

# Push na GitHub
git branch -M main
git push -u origin main
```

## 3. Aktualizace README.md

Po vytvoření repository nezapomeňte upravit v `README.md`:

1. Nahraďte `yourusername` vaším skutečným GitHub uživatelským jménem
2. Aktualizujte odkazy na Issues a další GitHub funkce

## 4. Nastavení GitHub Pages (volitelné)

Pro vytvoření webové stránky projektu:

1. Jděte do Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: "main" → "/ (root)"
4. Save

## 5. Přidání Topics (štítků)

V hlavní stránce repository klikněte na "About" a přidejte topics:
- `python`
- `pdf`
- `bleed`
- `print`
- `graphics`
- `gui`
- `tkinter`
- `advertising`

## 6. Vytvoření Release (volitelné)

Pro první verzi:

1. Jděte do "Releases" → "Create a new release"
2. Tag: `v1.0.0`
3. Title: `BleedMakr v1.0.0 - Initial Release`
4. Description: Popis funkcí a změn
5. Publish release

## 7. Nastavení Issues a Projects

1. **Issues**: Povolte pro hlášení chyb a požadavků
2. **Projects**: Vytvořte board pro sledování úkolů
3. **Wiki**: Povolte pro detailní dokumentaci

## 8. Přidání Collaborators (volitelné)

Pokud chcete spolupracovat s dalšími vývojáři:
1. Settings → Collaborators → "Add people"
2. Přidejte GitHub uživatelská jména

## 9. Nastavení Branch Protection (doporučeno)

1. Settings → Branches → "Add rule"
2. Branch name pattern: `main`
3. Zaškrtněte:
   - Require pull request reviews
   - Require status checks to pass
   - Include administrators

## 10. Automatické akce (volitelné)

Vytvořte `.github/workflows/ci.yml` pro automatické testování:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python test_app.py
        python test_white_borders.py
```

## Hotovo! 🎉

Váš projekt je nyní na GitHubu a připraven pro spolupráci s komunitou.

### Užitečné odkazy:
- **Repository**: `https://github.com/YOUR_USERNAME/BleedMakr`
- **Issues**: `https://github.com/YOUR_USERNAME/BleedMakr/issues`
- **Releases**: `https://github.com/YOUR_USERNAME/BleedMakr/releases`

### Další kroky:
1. Sdílejte odkaz na repository
2. Přidejte projekt do portfolia
3. Sledujte Issues a Pull Requests
4. Pravidelně aktualizujte dokumentaci 