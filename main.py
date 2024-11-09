import flet as ft
from utils import show_page

def main(page: ft.Page):
    page.title = "Simple Logging Unit (SLU)"
    
    page.window.height = 720
    page.window.width = 480

    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.SYSTEM

    show_page("home", page)

if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets"
    )