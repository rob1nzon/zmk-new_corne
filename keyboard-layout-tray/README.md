# Keyboard Layout Tray / Индикатор раскладки клавиатуры

Простое приложение для Windows, которое показывает текущую раскладку клавиатуры в системном трее.

A simple Windows application that displays the current keyboard layout in the system tray.

## Возможности / Features

- **Отображение в трее** - иконка с текущей раскладкой (EN, RU, и т.д.)
- **Подсказка при наведении** - при наведении мышки показывает полное название раскладки
- **Автоматическое обновление** - следит за сменой раскладки в реальном времени
- **Минимальное потребление ресурсов** - работает в фоновом режиме

## Использование готового exe / Using the pre-built exe

1. Скачайте `KeyboardLayoutTray.exe` из релизов
2. Запустите exe файл
3. Приложение появится в системном трее
4. Наведите мышку на иконку, чтобы увидеть текущую раскладку
5. Для выхода - правый клик на иконке → "Выход"

## Сборка из исходников / Building from source

### Требования / Requirements

- Python 3.8 или выше
- Windows OS

### Шаги / Steps

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите скрипт сборки:
```bash
build.bat
```

3. Готовый exe файл будет в папке `dist/KeyboardLayoutTray.exe`

### Альтернативный метод сборки / Alternative build method

```bash
pip install -r requirements.txt
pyinstaller --onefile --windowed --name=KeyboardLayoutTray keyboard_layout_tray.py
```

## Запуск без сборки / Running without building

```bash
pip install -r requirements.txt
python keyboard_layout_tray.py
```

## Поддерживаемые раскладки / Supported layouts

- EN - English
- RU - Russian
- UA - Ukrainian
- DE - German
- FR - French
- IT - Italian
- ES - Spanish
- PL - Polish
- PT - Portuguese
- TR - Turkish
- CN - Chinese (Simplified)
- TW - Chinese (Traditional)
- JP - Japanese
- KR - Korean

Другие раскладки будут показываться в виде их LCID кода.
Other layouts will be displayed as their LCID code.

## Автозагрузка / Auto-start

Чтобы приложение запускалось при старте Windows:

1. Нажмите `Win + R`
2. Введите `shell:startup`
3. Скопируйте `KeyboardLayoutTray.exe` в открывшуюся папку

To start the application automatically with Windows:

1. Press `Win + R`
2. Type `shell:startup`
3. Copy `KeyboardLayoutTray.exe` to the opened folder

## Лицензия / License

MIT License
