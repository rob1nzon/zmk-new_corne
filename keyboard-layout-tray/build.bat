@echo off
REM Build script for Keyboard Layout Tray

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist KeyboardLayoutTray.spec del KeyboardLayoutTray.spec

echo.
echo Building executable...
pyinstaller --onefile ^
    --windowed ^
    --add-data "../keymap-drawer/eyelash_corne.svg;keymap-drawer" ^
    --name=KeyboardLayoutTray ^
    --hidden-import=pkg_resources.extern ^
    --collect-all setuptools ^
    --noupx ^
    keyboard_layout_tray.py

echo.
if exist dist\KeyboardLayoutTray.exe (
    echo Build complete! Executable is in dist/KeyboardLayoutTray.exe
    echo.
    echo NOTE: This executable requires GTK+ Runtime to be installed on the target system
    echo You can download it from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
) else (
    echo Build failed! Please check the error messages above.
)
echo.
pause
