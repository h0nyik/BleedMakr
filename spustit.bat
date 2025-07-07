@echo off
echo ========================================
echo           BleedMakr - Spusteni
echo ========================================
echo.

REM Kontrola existence Pythonu
python --version >nul 2>&1
if errorlevel 1 (
    echo CHYBA: Python neni nainstalovan nebo neni v PATH!
    echo Stahnete Python z https://www.python.org/downloads/
    echo Ujistete se, ze je Python pridan do PATH.
    pause
    exit /b 1
)

REM Kontrola existence requirements.txt
if not exist "requirements.txt" (
    echo CHYBA: Soubor requirements.txt nebyl nalezen!
    pause
    exit /b 1
)

REM Instalace závislostí
echo Instaluji zavislosti...
pip install -r requirements.txt
if errorlevel 1 (
    echo VAROVANI: Nepodarilo se nainstalovat vsechny zavislosti!
    echo Pokracuji bez instalace...
)

REM Spuštění aplikace
echo.
echo Spoustim BleedMakr...
echo.
python src/spadavka_generator.py

REM Kontrola chyby při spuštění
if errorlevel 1 (
    echo.
    echo CHYBA: Aplikace se nepodarilo spustit!
    echo Zkontrolujte, zda jsou vsechny zavislosti nainstalovane.
    pause
    exit /b 1
)

echo.
echo Aplikace byla ukoncena.
pause 