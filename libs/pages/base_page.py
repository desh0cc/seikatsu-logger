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
        navigation_bar = ft.Container(
            ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(
                        icon=ft.icons.CREATE, label="Write"
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.icons.RECORD_VOICE_OVER, label="Record"
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.icons.EDIT, label="Edit"
                    ),
                ],
                on_change=self.on_navigation_change,
            ),
            alignment=ft.alignment.bottom_center,
            padding=ft.padding.only(left=-20,right=-20)
        )

        navigation_bar_container = ft.Container(
            content=navigation_bar,
            alignment=ft.alignment.bottom_center,
            padding=ft.padding.only(left=-20, right=-20, bottom=-15),
            expand=True,
        )

        self.content_container = ft.Container(content=self.current_content)

        return ft.Column(
            [self.content_container, navigation_bar_container],
            expand=True
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