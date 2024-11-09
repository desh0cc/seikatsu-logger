# navigation.py

import flet as ft
from libs.pages.note_page import WritePage
from libs.pages.edit_page import EditPage
from libs.pages.record_page import RecordPage

def create_navigation_bar(page: ft.Page):
    def on_nav_change(e):
        selected_index = e.control.selected_index
        page.controls.clear()
        if selected_index == 0:
            page.controls.append(WritePage(page, on_nav_change).build())
        elif selected_index == 1:
            page.controls.append(RecordPage(page, on_nav_change).build())
        elif selected_index == 2:
            page.controls.append(EditPage(page, on_nav_change).build())
          # Re-add the navigation bar at the bottom
        page.update()

    nav_bar = ft.Container(ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationDestination(icon=ft.icons.EDIT, label="Edit"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings")
        ], 
        on_change=on_nav_change
        ),
        alignment=ft.alignment.bottom_center,
        padding=ft.padding.only(left=-20,right=-20)
    )
    return nav_bar
