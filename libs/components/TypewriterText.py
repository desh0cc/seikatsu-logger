import flet as ft, time

from threading import Thread
from utils import lang_load

class TypewriterText:
    def __init__(self, size: int, weight: ft.FontWeight, page: ft.Page, font_name=None):
        self.text = ft.Text(
            size=size,
            weight=weight,
            font_family=font_name
        )
        self.page = page
        self.animation_thread = None

    def start_animation(self, text):
        def animate():
            full_text = f"{text}"
            self.text.value = ""
            
            for char in full_text:
                self.text.value += char
                self.page.update(self.text)
                time.sleep(0.05)

        if self.animation_thread and self.animation_thread.is_alive():
            return

        self.animation_thread = Thread(target=animate)
        self.animation_thread.start()

    def set_text(self, text):
        self.text.value = text
        self.page.update(self.text)

    def animate_thinking(self, base_text=lang_load("chat_page_ai_thinking"), delay=0.5):
        def thinking_animation():
            dots = ""
            while True:
                # Animate the dots
                for i in range(4):
                    self.text.value = f"{base_text}{'.' * i}"
                    self.page.update(self.text)
                    time.sleep(delay)  # Adjust the speed of dot animation
                time.sleep(delay)  # Pause before starting over

        if self.animation_thread and self.animation_thread.is_alive():
            return  # Prevent starting a new animation if one is already running

        self.animation_thread = Thread(target=thinking_animation)
        self.animation_thread.start()