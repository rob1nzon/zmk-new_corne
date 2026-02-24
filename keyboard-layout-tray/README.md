# Keyboard Layout Tray / Индикатор раскладки клавиатуры

Простое приложение для Windows, которое показывает текущую раскладку клавиатуры в системном трее и визуализацию раскладки клавиш при клике на иконку.

A simple Windows application that displays the current keyboard layout in the system tray and shows keyboard layout visualization on click.

## Возможности / Features

- **Отображение в трее** - иконка с текущей раскладкой (EN, RU, и т.д.)
- **Автоматическое обновление** - следит за сменой раскладки в реальном времени
- **Визуализация раскладки** - показывает полную схему клавиатуры при клике на иконку
- **Минимальное потребление ресурсов** - работает в фоновом режиме

## Использование готового exe / Using the pre-built exe

1. Скачайте `KeyboardLayoutTray.exe` из релизов
2. Запустите exe файл
3. Приложение появится в системном трее
4. Кликните на иконку, чтобы увидеть визуализацию раскладки клавиатуры
5. Для выхода - правый клик на иконке → "Выход"

## Сборка из исходников / Building from source

### Требования / Requirements

- Python 3.8 или выше
- Windows OS
- GTK+ для Windows (требуется для cairosvg)

### Установка GTK+ для Windows

Для работы cairosvg необходимо установить GTK+:

1. Скачайте GTK+ для Windows: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
2. Установите GTK+ Runtime Environment

### Шаги сборки / Build Steps

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
pyinstaller --onefile --windowed --add-data "../keymap-drawer/eyelash_corne.svg;keymap-drawer" --name=KeyboardLayoutTray keyboard_layout_tray.py
```

## Запуск без сборки / Running without building

```bash
pip install -r requirements.txt
python keyboard_layout_tray.py
```

**Примечание:** При запуске из исходников, SVG файл должен находиться в `../keymap-drawer/eyelash_corne.svg` относительно скрипта.

## Поддерживаемые раскладки / Supported layouts

- EN - English
- RU - Russian
- UA - Ukrainian
- DE - German
- FR - French
- IT - Italian
- ES - Spanish
- PL - Polish

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

## Использование / Usage

- **Левый клик** на иконке в трее - показать визуализацию раскладки клавиатуры
- **Правый клик** на иконке - открыть меню (Показать раскладку / Выход)
- **Наведение мышки** - показывает текущую раскладку в подсказке
- **Клик на окне с визуализацией** - закрыть окно
- **Уход курсора из окна** - автоматическое закрытие через 1 секунду

## Технические детали / Technical Details

Приложение использует:
- Windows API для определения текущей раскладки клавиатуры
- pystray для создания иконки в системном трее
- tkinter для отображения всплывающего окна
- cairosvg для рендеринга SVG в PNG
- Pillow для работы с изображениями

## Лицензия / License

MIT License
