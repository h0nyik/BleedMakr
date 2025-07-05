@echo off
echo 🎨 BleedMakr - Rychlé sestavení .exe
echo =====================================

echo 🔧 Instalace PyInstaller...
pip install pyinstaller

echo 🚀 Sestavování .exe souboru...
pyinstaller --onefile --windowed --name="BleedMakr" --add-data="README.md;." --add-data="LICENSE;." --add-data="version.txt;." --exclude-module=matplotlib --exclude-module=scipy --exclude-module=pandas --exclude-module=jupyter --exclude-module=IPython --exclude-module=notebook --exclude-module=sphinx --exclude-module=pytest --exclude-module=setuptools --exclude-module=pip --exclude-module=wheel --exclude-module=distutils spadavka_generator.py

if exist "dist\BleedMakr.exe" (
    echo ✅ Úspěšně vytvořen BleedMakr.exe
    for %%A in ("dist\BleedMakr.exe") do echo    Velikost: %%~zA bytes
    echo 📦 Soubor je připraven v složce dist\
) else (
    echo ❌ Chyba při vytváření .exe souboru
    pause
    exit /b 1
)

echo.
echo 🎉 Build dokončen!
echo    Soubor: dist\BleedMakr.exe
echo.
pause 