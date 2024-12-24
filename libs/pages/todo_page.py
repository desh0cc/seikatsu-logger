import flet as ft, asyncio
from libs.components.NavigationComp import BackToHome

def todo_page(page: ft.Page):
    from utils import get_time_based_color

    navigator = BackToHome("To-Do", page)

    todos = ft.Column(controls=[], width=350, height=200, horizontal_alignment=ft.CrossAxisAlignment.CENTER,scroll=ft.ScrollMode.ALWAYS)

    textik = ft.TextField(
                hint_text="Write something idk...",
                fill_color=ft.colors.WHITE,
                border_color=get_time_based_color(),
                border_radius=15,
                text_style=ft.TextStyle(
                    color=ft.colors.BLACK87,
                    weight=ft.FontWeight.W_600,
                    font_family="CaskaydiaCove"
                )
            )
    
    def make_todo():
        if textik.value.strip():
            todos.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(textik.value)
                    ]),
                    alignment=ft.alignment.center
                )
            )
            textik.value = ""
            page.update()

    tabs = ft.Tabs(
        tabs=[
            ft.Tab(text="Усі"),
            ft.Tab(text="Сьогодні"),
            ft.Tab(text="Щодня"),
            ft.Tab(text="До певного терміну"),
        ],
        selected_index=0,
        divider_color=ft.colors.with_opacity(0.0, "#FFFFFF"),
        indicator_color=get_time_based_color(),
        label_color=get_time_based_color(),
    )

    return ft.View(
        route="/todo",
        controls=[
            navigator.add(),
            
            ft.Container(
                content=ft.Column([
                    ft.Container(height=7),
                    ft.Container(
                        ft.Row([
                            tabs,
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor=ft.colors.with_opacity(0.4,ft.colors.BLACK),
                        height=60
                    ),
                    ft.Container(
                        content=todos,
                        expand=True,
                        width=float("inf")
                    ),
                    ft.Container(height=5)
                ]),
                bgcolor=ft.colors.with_opacity(0.4,"#333333"),
                border_radius=15,
                expand=True
            ),

            ft.Container(
                content=ft.Row([
                    ft.Container(
                        textik,
                        width=250,
                        alignment=ft.alignment.center_left,
                    ),

                    ft.Container(
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.ADJUST,
                                icon_color=get_time_based_color(),
                                bgcolor=ft.colors.with_opacity(0.4,ft.colors.BLACK),
                            ),
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                icon_color=get_time_based_color(),
                                bgcolor=ft.colors.with_opacity(0.4,ft.colors.BLACK),
                                on_click=lambda _: make_todo()
                            )
                        ]),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(left=30)
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
                ),
                border_radius=15,
                padding=ft.padding.only(top=0),
                height=95,
                alignment=ft.alignment.bottom_center,
                bgcolor=ft.colors.with_opacity(0.4,"#333333")
            )
        ])