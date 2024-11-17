import flet as ft
from libs.components.TypewriterText import TypewriterText

def home_page(page: ft.Page) -> ft.View:
    from utils import get_time_based_color, todaysDate

    typewriter = TypewriterText(page)
    typewriter.start_animation("Привіт чим допомогти?")

    time_color = get_time_based_color()

    time_reactiveBg = ft.Container(
        width=page.window.width,
        height=300,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[time_color, ft.colors.TRANSPARENT],
            stops=[0.0, 0.7]
        ),
        opacity=0.4,
        left=0,  
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

    GIF = ft.Image(
            src="assets/icons/animegirly.gif",  
            width=64, 
            height=64,
            fit=ft.ImageFit.CONTAIN  
        )

    return ft.View(
        route = "/",
        controls=[
            ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.SETTINGS,icon_color=ft.colors.WHITE,
                    on_click=lambda e: page.go("/settings"),
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
                    # Перший ряд кнопок
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

                    # Другий ряд кнопок
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.ElevatedButton(
                                    height=100,
                                    width=100,
                                    content=ft.Image(src="assets/icons/copy-writing.png", color=get_time_based_color(), width=32, height=32),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                    on_click=lambda e: page.go("/write")
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
                                    on_click=lambda e: page.go("/analyze"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER 
                        ),
                        padding=ft.padding.only(top=10)
                    ),

                    # Третій ряд кнопок
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
                                    on_click=lambda _: page.go("/todo")
                                ),
                                ft.ElevatedButton(
                                    height=100,
                                    width=100,
                                    content=ft.Image(src="assets/icons/folder.png", color=get_time_based_color(), width=32, height=32),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                    on_click=lambda e: e
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER  # Центрирование второй строки кнопок
                        ),
                        padding=ft.padding.only(top=10)
                    ),
                ]),
                alignment=ft.alignment.center
            )
        ]
    )