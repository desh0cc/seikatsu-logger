import flet as ft

from libs.components.BasePage import BasePage

from libs.pages.home_page import home_page
from libs.pages.settings_page import settings_page
from libs.pages.chart_page import chart_page
from libs.pages.todo_page import todo_page

def main(page: ft.Page):
    page.title = "Seikatsu"
    
    page.window.height = 720
    page.window.width = 480

    page.window.icon = "assets/icon.png"

    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.SYSTEM

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(home_page(page))
        if page.route == "/settings":
            page.views.append(settings_page(page))
        if page.route == "/write":
            base_page = BasePage(page)
            page.views.append(base_page.build())
        if page.route == "/analyze":
            page.views.append(chart_page(page))
        if page.route == "/todo":
            page.views.append(todo_page(page))

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets"
    )