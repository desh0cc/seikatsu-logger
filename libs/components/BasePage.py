import flet as ft

from libs.pages.write_page import write_page
from libs.pages.record_page import record_page
from libs.pages.edit_page import edit_page

from utils import get_time_based_color

class BasePage:
    def __init__(self, page):
        self.page = page
        self.current_content = write_page(page)

    def build(self):
        def on_navigation_change(e):
            if e.control.selected_index == 0:
                self.current_content = write_page(self.page)
            elif e.control.selected_index == 1:
                self.current_content = record_page(self.page)
            elif e.control.selected_index == 2:
                self.current_content = edit_page(self.page)

            self.content_container.content = self.current_content
            self.page.update()

        navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.ADD, label="Додати"),
                ft.NavigationBarDestination(icon=ft.icons.PLAY_ARROW_ROUNDED, label="Записати"),
                ft.NavigationBarDestination(icon=ft.icons.EDIT, label="Редагувати"),
            ],
            on_change=on_navigation_change,
            indicator_color=get_time_based_color(),
        )

        self.content_container = ft.Container(
            content=self.current_content,
            expand=True,
        )

        return ft.Column(
            controls=[
                self.content_container,
                ft.Container(
                    content=navigation_bar,
                    alignment=ft.alignment.bottom_center,
                    padding=ft.padding.only(left=-20,right=-20,bottom=-10)
                ),
            ],
        )