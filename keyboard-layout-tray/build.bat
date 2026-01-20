@echo off
REM Build script for Keyboard Layout Tray

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building executable...
pyinstaller --onefile --windowed --icon=NONE --name=KeyboardLayoutTray keyboard_layout_tray.py

echo.
echo Build complete! Executable is in dist/KeyboardLayoutTray.exe
pause
