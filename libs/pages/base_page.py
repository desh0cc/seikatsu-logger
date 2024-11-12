import flet as ft
from libs.pages.write_page import WritePage
from libs.pages.record_page import RecordPage
from libs.pages.edit_page import EditPage

class BasePage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.current_content = WritePage(page)

    def build(self):
        from utils import get_time_based_color

        navigation_bar = ft.Container(
            ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(
                        icon=ft.icons.ADD, label="Додати"
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.icons.PLAY_ARROW_ROUNDED, label="Записати"
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.icons.EDIT_DOCUMENT, label="Редагувати"
                    ),
                ],
                on_change=self.on_navigation_change,
                indicator_color=get_time_based_color()
            ),
            alignment=ft.alignment.bottom_center,
            padding=ft.padding.only(left=-20,right=-20, top=590)
        )

        self.content_container = ft.Container(content=self.current_content)

        return ft.Stack(
            [navigation_bar, self.content_container],
        )

    def on_navigation_change(self, e):

        if e.control.selected_index == 0:
            self.current_content = WritePage(self.page)
        elif e.control.selected_index == 1:
            self.current_content = RecordPage(self.page)
        elif e.control.selected_index == 2:
            self.current_content = EditPage(self.page)


        self.content_container.content = self.current_content
        self.update()