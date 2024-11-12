import flet as ft

class EditPage(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page



    def build(self):
        from utils import get_time_based_color, show_page, load_files

        content = ft.Column([
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
                    "Редагувати лог",
                    color=get_time_based_color(),
                    font_family="Helvetica",
                    weight=ft.FontWeight.BOLD,
                    size=20
                ),
                alignment=ft.alignment.top_center,
                padding=ft.padding.only(top=-45)
            ),

            ft.Container(
                ft.Dropdown(
                    options=[
                        ft.SubmenuButton(ft.Text("Nothing"))
                    ]
                )
            ),

            ft.Container(
                ft.Dropdown(
                    options=[
                        ft.SubmenuButton(ft.Text("Nothing"))
                    ]
                )
            ),

            # Секція вибору активності
                ft.Container(
                    content=ft.Column([
                        ft.Container(ft.Text("Назва активності:", size=16), alignment=ft.alignment.center),
                        ft.Container(ft.TextField(
                            width=200,
                            text_align=ft.TextAlign.LEFT,
                            label="Активність",
                            hint_text="Введіть назву активності",
                            color=ft.colors.WHITE,
                            border_color=get_time_based_color(),
                            label_style=ft.TextStyle(color=get_time_based_color()),
                        ), alignment=ft.alignment.center),
                        
                    ])
                ),

                # Секція вибору часу
                ft.Container(
                    content=ft.Column([
                        ft.Container(ft.Text("Вкажіть новий час початку:", size=16), alignment=ft.alignment.center),
                        ft.Container(ft.ElevatedButton(
                            text="Вибрати час",color=get_time_based_color(),
                            icon=ft.icons.ACCESS_TIME,
                            icon_color=get_time_based_color(),
                            on_click=lambda e: self.page.open(
                                ft.TimePicker(
                                )
                            ),
                        ),alignment=ft.alignment.center),
                        
                    ]),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=20)
                ),

                ft.Container(
                    content=ft.Column([
                        ft.Container(ft.Text("Вкажіть новий час закінчення:", size=16), alignment=ft.alignment.center),
                        ft.Container(ft.ElevatedButton(
                            text="Вибрати час",color=get_time_based_color(),
                            icon=ft.icons.ACCESS_TIME,
                            icon_color=get_time_based_color(),
                            on_click=lambda e: self.page.open(
                                ft.TimePicker(
                                )
                            ),
                        ),alignment=ft.alignment.center),
                        
                    ])
                ),

                ft.Container(
                    content=ft.ElevatedButton(text="Редагувати",color=get_time_based_color()),
                    alignment=ft.alignment.center
                )
        ])
        return ft.Column([content], expand=True)