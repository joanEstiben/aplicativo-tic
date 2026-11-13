@echo off
echo === Compilando AplicativoTIC con PyInstaller ===
cd cliente.tic
pyinstaller --noconfirm --onedir --windowed --name AplicativoTIC main.py
cd ..

echo === Moviendo dist al directorio raiz ===
if exist dist rmdir /s /q dist
move cliente.tic\dist .

echo === Generando instalador con Inno Setup ===
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup.iss

echo === Listo! El instalador esta en: Output\InstaladorTIC.exe ===
pause
