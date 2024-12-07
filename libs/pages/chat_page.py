import flet as ft, time
from ollama import chat
from libs.components.NavigationComp import BackToHome
from libs.components.TypewriterText import TypewriterText
from utils import get_time_based_color

def chat_page(page: ft.Page) -> ft.View:
    navigator = BackToHome("Чат з ШІ", page)

    message_cont = ft.Column(controls=[], expand=True, scroll=ft.ScrollMode.ALWAYS)

    textik = ft.TextField(
        value="",
        hint_text="Type your message...",
        text_style=ft.TextStyle(
            font_family="Helvetica",
            color=ft.colors.BLACK
        ),
        border_radius=20,
        cursor_color=get_time_based_color(),
        fill_color=ft.colors.WHITE,
        border_color=get_time_based_color()
    )

    def send_message():
        user_message = textik.value.strip()
        if user_message:
            message_cont.controls.append(
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                user_message, 
                                color=ft.colors.WHITE,
                                size=15
                            ),
                            bgcolor=ft.colors.GREY_800,
                            width=200,
                            border_radius=15,
                            padding=10,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            )
            textik.value = ""
            page.update()

            fetch_response(user_message)
        else:
            page.open(ft.SnackBar(ft.Text("Будь ласка напишіть щось!"), bgcolor=ft.colors.RED_600))

    def fetch_response(user_message):
        stream = chat(
            model="llama3:latest",
            messages=[{'role': 'user', 'content': user_message}],
            stream=True
        )

        response_text = TypewriterText(15, ft.FontWeight.NORMAL, page)
        
        response_container = ft.Container(
            content=response_text.text,
            bgcolor=get_time_based_color(),
            width=300,
            border_radius=15,
            padding=10,
        )
        message_cont.controls.append(
            ft.Row(
                controls=[response_container],
                alignment=ft.MainAxisAlignment.START
            )
        )
        page.update()

        full_message = ""
        for chunk in stream:
            full_message += chunk['message']['content']

        response_text.start_animation(full_message)

    return ft.View(
        route="/chat",
        controls=[
            navigator.add(),
            ft.Container(
                content=ft.Column([ft.Container(height=5),message_cont, ft.Container(height=5)]),
                width=float('inf'),
                border_radius=15,
                expand=True,
            ),
            ft.Container(
                content=ft.Row([
                    textik,
                    ft.Container(
                        ft.IconButton(
                            icon=ft.icons.SEND, 
                            on_click=lambda _: send_message()
                        ),
                        padding=ft.padding.only(left=10)
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.colors.with_opacity(0.4, ft.colors.BLACK),
                border_radius=15,
                height=70
            )
        ]
    )
