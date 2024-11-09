import flet as ft

class EditPage():
    def __init__(self, page: ft.Page, on_nav_change):
        super().__init__()
        self.page = page
        self.on_nav_change = on_nav_change

    def build(self):
        from libs.components.navigation import create_navigation_bar
        content = ft.Container(
            ft.Text("rooomu")
        )
        return ft.Column([content, create_navigation_bar(self.page)], expand=True)