import flet as ft
from libs.components.TypewriterText import TypewriterText

class HomePage(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

    def build(self):
        from utils import get_time_based_color, GIF, todaysDate, show_page
        typewriter = TypewriterText(self.page)
        typewriter.start_animation("Привіт чим допомогти?")

        time_color = get_time_based_color()

        time_reactiveBg = ft.Container(
            width=self.page.window.width,  # Використовуємо повну ширину вікна
            height=300,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[time_color, ft.colors.TRANSPARENT],
                stops=[0.0, 0.7]
            ),
            opacity=0.4,
            left=0,  #
            right=0,
            top=0,
            margin=None,
            padding=None,
        )

        typewriter_text = ft.Container(
            content=typewriter.text,
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=120)
        )

        return(ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.SETTINGS,icon_color=ft.colors.WHITE,
                        on_click=lambda e: show_page("settings_page", self.page),
                    ),
                    alignment=ft.alignment.top_right,
                    padding=ft.padding.only(right=10)
                ),

                ft.Container(
                    content=GIF,
                    alignment=ft.alignment.top_center
                ),

                ft.Container(
                    content=ft.Stack([
                        time_reactiveBg,
                        typewriter_text,
                    ]),
                    height=100, 
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=-150, right=-20, left=-20),
                    margin=ft.margin.only(top=-20),
                ),

                ft.Container(
                    ft.Text(
                        f"Сьогодні {todaysDate}",
                        size=13,
                        font_family="Helvetica",
                        weight=ft.FontWeight.W_600,
                        color=get_time_based_color()
                    ),
                    padding=ft.padding.only(top=-100),
                    alignment=ft.alignment.center,
                ),
                
                ft.Container(
                    ft.Column([
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.ElevatedButton(
                                        height=100,
                                        width=210,
                                        content=ft.Column([
                                            ft.Container(
                                                ft.Text("Останній запис",color=get_time_based_color()),
                                                alignment=ft.alignment.top_left,
                                                padding=ft.padding.only(top=15,left=-10)
                                            ),
                                            ft.Container(
                                                ft.Text("Сьогодні ви написали не занадто багато.", color=ft.colors.WHITE70),
                                                alignment=ft.alignment.center_left,
                                                padding=ft.padding.only(left=-10,top=-7),
                                            )
                                        ]),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                    ),
                                    ft.ElevatedButton(
                                        height=100,
                                        width=100,
                                        content=ft.Image(src="assets/icons/chat.png", color=get_time_based_color(), width=32, height=32),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER  # Центрирование первой строки
                            ),
                            padding=ft.padding.only(top=32)
                        ),

                        # First row of buttons
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.ElevatedButton(
                                        height=100,
                                        width=100,
                                        content=ft.Image(src="assets/icons/copy-writing.png", color=get_time_based_color(), width=32, height=32),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                        on_click=lambda e: show_page("base_page", self.page)
                                    ),
                                    ft.ElevatedButton(
                                        height=100,
                                        width=100,
                                        content=ft.Image(src="assets/icons/calendar.png", color=get_time_based_color(), width=32, height=32),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                        on_click=lambda e: e
                                    ),
                                    ft.ElevatedButton(
                                        height=100,
                                        width=100,
                                        content=ft.Image(src="assets/icons/chart.png", color=get_time_based_color(), width=32, height=32),
                                        on_click=lambda e: show_page("chart_page", self.page),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER 
                            ),
                            padding=ft.padding.only(top=10)
                        ),

                        # Second row of buttons
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.ElevatedButton(
                                        height=100,
                                        width=100,
                                        content=ft.Image(src="assets/icons/neuron.png", color=get_time_based_color(), width=32, height=32),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                                    ),
                                    ft.ElevatedButton(
                                        height=100,
                                        width=100,
                                        content=ft.Image(src="assets/icons/checklist.png", color=get_time_based_color(), width=32, height=32),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                        on_click=lambda _: show_page("todo_page", self.page)
                                    ),
                                    ft.ElevatedButton(
                                        height=100,
                                        width=100,
                                        content=ft.Image(src="assets/icons/folder.png", color=get_time_based_color(), width=32, height=32),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                        on_click=lambda e: quit(ft.app)
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER  # Центрирование второй строки кнопок
                            ),
                            padding=ft.padding.only(top=10)
                        ),
                    ]),
                    alignment=ft.alignment.center
                )
            ]),
            padding=ft.padding.all(0), 
            margin=ft.margin.all(0)
        ))