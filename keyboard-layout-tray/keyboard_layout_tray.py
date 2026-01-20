#!/usr/bin/env python3
"""
Keyboard Layout Tray - показывает текущую раскладку клавиатуры в системном трее Windows
"""
import ctypes
import threading
import time
from ctypes import wintypes
from PIL import Image, ImageDraw, ImageFont
import pystray

# Windows API constants
LOCALE_SNAME = 0x0000005c
LOCALE_NAME_MAX_LENGTH = 85

# Словарь раскладок (LCID -> короткое название)
LAYOUT_NAMES = {
    0x0409: "EN",  # English (US)
    0x0809: "EN",  # English (UK)
    0x0419: "RU",  # Russian
    0x0422: "UA",  # Ukrainian
    0x0407: "DE",  # German
    0x040c: "FR",  # French
    0x0410: "IT",  # Italian
    0x040a: "ES",  # Spanish
    0x0415: "PL",  # Polish
    0x0416: "PT",  # Portuguese (Brazil)
    0x041f: "TR",  # Turkish
    0x0804: "CN",  # Chinese (Simplified)
    0x0404: "TW",  # Chinese (Traditional)
    0x0411: "JP",  # Japanese
    0x0412: "KR",  # Korean
}


class KeyboardLayoutTray:
    def __init__(self):
        self.current_layout = ""
        self.icon = None
        self.running = True
        
    def get_keyboard_layout(self):
        """Получить текущую раскладку клавиатуры через Windows API"""
        try:
            # Получить дескриптор активного окна
            user32 = ctypes.WinDLL('user32', use_last_error=True)
            
            # Получить ID потока переднего окна
            foreground_window = user32.GetForegroundWindow()
            thread_id = user32.GetWindowThreadProcessId(foreground_window, None)
            
            # Получить раскладку клавиатуры для этого потока
            layout_id = user32.GetKeyboardLayout(thread_id)
            
            # Извлечь LANGID (младшие 16 бит)
            langid = layout_id & 0xFFFF
            
            # Получить короткое название из словаря или использовать hex
            layout_name = LAYOUT_NAMES.get(langid, f"{langid:04X}")
            
            return layout_name
        except Exception as e:
            print(f"Error getting keyboard layout: {e}")
            return "??"
    
    def create_icon_image(self, text):
        """Создать изображение для иконки в трее с текстом раскладки"""
        # Создать изображение 64x64
        size = 64
        image = Image.new('RGB', (size, size), color='#2C3E50')
        draw = ImageDraw.Draw(image)
        
        # Попробовать загрузить шрифт
        try:
            # Использовать системный шрифт Windows
            font = ImageFont.truetype("segoeui.ttf", 32)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 32)
            except:
                font = ImageFont.load_default()
        
        # Получить размер текста для центрирования
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Нарисовать текст в центре
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        draw.text((x, y), text, fill='#ECF0F1', font=font)
        
        return image
    
    def update_icon(self):
        """Обновить иконку с текущей раскладкой"""
        layout = self.get_keyboard_layout()
        if layout != self.current_layout:
            self.current_layout = layout
            if self.icon:
                # Обновить иконку и подсказку
                self.icon.icon = self.create_icon_image(layout)
                self.icon.title = f"Раскладка: {layout}"
    
    def monitor_layout(self):
        """Мониторить изменения раскладки в фоновом потоке"""
        while self.running:
            try:
                self.update_icon()
                time.sleep(0.5)  # Проверять каждые 500мс
            except Exception as e:
                print(f"Error in monitor thread: {e}")
                time.sleep(1)
    
    def on_quit(self, icon, item):
        """Обработчик выхода из приложения"""
        self.running = False
        icon.stop()
    
    def run(self):
        """Запустить приложение в трее"""
        # Получить начальную раскладку
        self.current_layout = self.get_keyboard_layout()
        
        # Создать меню для трея
        menu = pystray.Menu(
            pystray.MenuItem("Выход", self.on_quit)
        )
        
        # Создать иконку в трее
        self.icon = pystray.Icon(
            "keyboard_layout",
            self.create_icon_image(self.current_layout),
            f"Раскладка: {self.current_layout}",
            menu
        )
        
        # Запустить поток мониторинга раскладки
        monitor_thread = threading.Thread(target=self.monitor_layout, daemon=True)
        monitor_thread.start()
        
        # Запустить иконку в трее (блокирующий вызов)
        self.icon.run()


if __name__ == "__main__":
    app = KeyboardLayoutTray()
    app.run()
