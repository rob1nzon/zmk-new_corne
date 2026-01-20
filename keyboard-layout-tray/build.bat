@echo off
REM Build script for Keyboard Layout Tray

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building executable...
pyinstaller --onefile --windowed --add-data "../keymap-drawer/eyelash_corne.svg;keymap-drawer" --name=KeyboardLayoutTray keyboard_layout_tray.py

echo.
echo Build complete! Executable is in dist/KeyboardLayoutTray.exe
echo.
echo NOTE: This executable requires GTK+ Runtime to be installed on the target system
echo You can download it from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
pause
