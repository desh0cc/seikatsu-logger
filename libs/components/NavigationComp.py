import flet as ft

class BackToHome():
    def __init__(self, title, page: ft.Page):
        self.title = title
        self.page = page

    def add(self):
        from utils import get_time_based_color

        return ft.Container(
            content=ft.Column([
                # Back button
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color=get_time_based_color(),
                        on_click=lambda e: self.page.go("/"),
                    ),
                    alignment=ft.alignment.top_left,
                    padding=ft.padding.only(left=5),
                ),
                # Title
                ft.Container(
                    content=ft.Text(
                        f"{self.title}",
                        color=get_time_based_color(),
                        weight=ft.FontWeight.BOLD,
                        size=20
                    ),
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(top=-45)
                ),
            ])
        )