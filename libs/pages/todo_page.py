import flet as ft

class TodoPage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        
    def build(self):
        from utils import get_time_based_color, show_page

        return(ft.Column([
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color=get_time_based_color(),
                        on_click=lambda e: show_page("home", self.page)
                    ),
                    alignment=ft.alignment.top_left,
                    padding=ft.padding.only(left=10),
                ),
                ft.Container(
                    content=ft.Text(
                        "To-Do",
                        color=get_time_based_color(),
                        font_family="Helvetica",
                        weight=ft.FontWeight.BOLD,
                        size=20
                    ),
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(top=-45)
                ),

            ])
        )
