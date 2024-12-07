import flet as ft, time
from threading import Thread

class TypewriterText:
    def __init__(self, size: int, weight: ft.FontWeight, page: ft.Page):
        self.text = ft.Text(
            size=size,
            weight=weight,
            font_family="Helvetica"
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