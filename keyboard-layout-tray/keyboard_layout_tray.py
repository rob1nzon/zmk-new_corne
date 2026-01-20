#!/usr/bin/env python3
"""
Keyboard Layout Tray - показывает текущую раскладку клавиатуры в системном трее Windows
и отображает визуализацию клавиатуры при наведении мышки
"""
import ctypes
import threading
import time
import os
import sys
from ctypes import wintypes
from PIL import Image, ImageDraw, ImageFont
import pystray
import tkinter as tk
from tkinter import Toplevel, Canvas
from PIL import ImageTk
import cairosvg
from io import BytesIO

# Путь к SVG файлу с раскладкой клавиатуры
def get_resource_path(relative_path):
    """Получить абсолютный путь к ресурсу (работает и для .exe)"""
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # В режиме разработки
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

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
}


class KeyboardLayoutTray:
    def __init__(self):
        self.current_layout = ""
        self.icon = None
        self.running = True
        self.popup_window = None
        self.root = None
        self.hide_timer = None
        
        # Инициализировать tkinter в главном потоке
        self.root = tk.Tk()
        self.root.withdraw()  # Скрыть главное окно
        
    def get_keyboard_layout(self):
        """Получить текущую раскладку клавиатуры через Windows API"""
        try:
            user32 = ctypes.WinDLL('user32', use_last_error=True)
            foreground_window = user32.GetForegroundWindow()
            thread_id = user32.GetWindowThreadProcessId(foreground_window, None)
            layout_id = user32.GetKeyboardLayout(thread_id)
            langid = layout_id & 0xFFFF
            
            layout_name = LAYOUT_NAMES.get(langid, f"{langid:04X}")
            return layout_name
        except Exception as e:
            print(f"Error getting keyboard layout: {e}")
            return "??"
    
    def create_icon_image(self, text):
        """Создать изображение для иконки в трее с текстом раскладки"""
        size = 64
        image = Image.new('RGB', (size, size), color='#2C3E50')
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype("segoeui.ttf", 32)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 32)
            except:
                font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        draw.text((x, y), text, fill='#ECF0F1', font=font)
        
        return image
    
    def load_svg_as_image(self, svg_path, scale=0.6):
        """Загрузить SVG файл и конвертировать в изображение PIL"""
        try:
            if not os.path.exists(svg_path):
                print(f"SVG file not found: {svg_path}")
                return None
            
            # Конвертировать SVG в PNG используя cairosvg
            # Масштабировать до удобного размера
            png_data = cairosvg.svg2png(url=svg_path, scale=scale)
            image = Image.open(BytesIO(png_data))
            return image
        except Exception as e:
            print(f"Error loading SVG {svg_path}: {e}")
            return None
    
    def show_layout_popup(self):
        """Показать всплывающее окно с визуализацией раскладки клавиатуры"""
        # Отменить таймер скрытия если он существует
        if self.hide_timer:
            self.root.after_cancel(self.hide_timer)
            self.hide_timer = None
        
        # Если окно уже показано, не создавать новое
        if self.popup_window is not None:
            try:
                self.popup_window.lift()  # Поднять на передний план
                return
            except:
                pass
        
        # Путь к SVG файлу раскладки клавиатуры
        svg_path = get_resource_path("keymap-drawer/eyelash_corne.svg")
        image = self.load_svg_as_image(svg_path)
        
        if image is None:
            print("Не удалось загрузить изображение раскладки клавиатуры")
            return
        
        # Создать всплывающее окно
        self.popup_window = Toplevel(self.root)
        self.popup_window.title("Раскладка клавиатуры")
        self.popup_window.overrideredirect(True)  # Убрать рамку окна
        self.popup_window.attributes('-topmost', True)  # Поверх всех окон
        self.popup_window.configure(bg='white')
        
        # Конвертировать PIL Image в PhotoImage
        photo = ImageTk.PhotoImage(image)
        
        # Создать Canvas для отображения изображения
        canvas = Canvas(self.popup_window, width=image.width, height=image.height, 
                       bg='white', highlightthickness=0)
        canvas.pack()
        canvas.create_image(0, 0, anchor='nw', image=photo)
        canvas.image = photo  # Сохранить ссылку
        
        # Получить размер экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Получить позицию курсора
        x = self.root.winfo_pointerx() + 20
        y = self.root.winfo_pointery() + 20
        
        # Проверить, чтобы окно не выходило за пределы экрана
        if x + image.width > screen_width:
            x = screen_width - image.width - 10
        if y + image.height > screen_height:
            y = screen_height - image.height - 10
        
        # Позиционировать окно
        self.popup_window.geometry(f"{image.width}x{image.height}+{x}+{y}")
        
        # Закрыть окно при клике
        self.popup_window.bind("<Button-1>", lambda e: self.hide_layout_popup())
        
        # Скрыть окно при уходе курсора (с небольшой задержкой)
        self.popup_window.bind("<Leave>", lambda e: self.schedule_hide_popup())
        self.popup_window.bind("<Enter>", lambda e: self.cancel_hide_popup())
    
    def schedule_hide_popup(self):
        """Запланировать скрытие всплывающего окна через 1 секунду"""
        if self.hide_timer:
            self.root.after_cancel(self.hide_timer)
        self.hide_timer = self.root.after(1000, self.hide_layout_popup)
    
    def cancel_hide_popup(self):
        """Отменить запланированное скрытие окна"""
        if self.hide_timer:
            self.root.after_cancel(self.hide_timer)
            self.hide_timer = None
    
    def hide_layout_popup(self):
        """Скрыть всплывающее окно"""
        if self.hide_timer:
            self.root.after_cancel(self.hide_timer)
            self.hide_timer = None
        
        if self.popup_window is not None:
            try:
                self.popup_window.destroy()
            except:
                pass
            self.popup_window = None
    
    def update_icon(self):
        """Обновить иконку с текущей раскладкой"""
        layout_name = self.get_keyboard_layout()
        if layout_name != self.current_layout:
            self.current_layout = layout_name
            if self.icon:
                self.icon.icon = self.create_icon_image(layout_name)
                self.icon.title = f"Раскладка: {layout_name}\nКликните для отображения схемы"
    
    def monitor_layout(self):
        """Мониторить изменения раскладки в фоновом потоке"""
        while self.running:
            try:
                self.update_icon()
                time.sleep(0.5)
            except Exception as e:
                print(f"Error in monitor thread: {e}")
                time.sleep(1)
    
    def on_click(self, icon, item):
        """Обработчик клика на иконку"""
        self.root.after(0, self.show_layout_popup)
    
    def on_quit(self, icon, item):
        """Обработчик выхода из приложения"""
        self.running = False
        self.hide_layout_popup()
        icon.stop()
        self.root.quit()
    
    def run(self):
        """Запустить приложение в трее"""
        self.current_layout = self.get_keyboard_layout()
        
        # Создать меню для трея
        menu = pystray.Menu(
            pystray.MenuItem("Показать раскладку", self.on_click, default=True),
            pystray.MenuItem("Выход", self.on_quit)
        )
        
        # Создать иконку в трее
        self.icon = pystray.Icon(
            "keyboard_layout",
            self.create_icon_image(self.current_layout),
            f"Раскладка: {self.current_layout}\nКликните для отображения схемы",
            menu
        )
        
        # Добавить обработчик клика по иконке
        self.icon.on_left_click = lambda icon, item: self.on_click(icon, item)
        
        # Запустить поток мониторинга раскладки
        monitor_thread = threading.Thread(target=self.monitor_layout, daemon=True)
        monitor_thread.start()
        
        # Запустить иконку в отдельном потоке
        icon_thread = threading.Thread(target=self.icon.run, daemon=True)
        icon_thread.start()
        
        # Запустить главный цикл tkinter
        self.root.mainloop()


if __name__ == "__main__":
    app = KeyboardLayoutTray()
    app.run()
