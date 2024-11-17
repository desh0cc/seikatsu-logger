import flet as ft
from libs.components.Back import BackToHome

def todo_page(page: ft.Page):
    from utils import get_time_based_color

    navigator = BackToHome("ToDo", page)

    return ft.View(
        route="/todo",
        controls=[
            navigator.add()

        ])