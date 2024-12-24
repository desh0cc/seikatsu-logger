import flet as ft, asyncio, time, datetime

from ollama import chat

from libs.components.NavigationComp import BackToHome
from libs.components.TypewriterText import TypewriterText

from utils import get_time_based_color, load_config

def chat_page(page: ft.Page) -> ft.View:
    navigator = BackToHome("Чат", page)

    message_cont = ft.Column(controls=[], expand=True, scroll=ft.ScrollMode.ALWAYS)

    exact_moment = datetime.datetime.now().strftime("%H:%M")

    config = load_config()

    textik = ft.TextField(
        value="",
        hint_text="Type your message...",
        text_style=ft.TextStyle(
            color=ft.Colors.BLACK
        ),
        border_radius=20,
        icon=ft.Icons.TEXT_FIELDS,
        border=ft.BorderSide(width=7),
        focused_border_width=2,
        border_width=2,
        cursor_color=get_time_based_color(),
        fill_color=ft.Colors.WHITE,
        border_color=get_time_based_color(),
        max_lines=5,
        multiline=True
    )

    async def send_message():
        user_message = textik.value.strip()
        max_width = 300 if len(user_message) > 30 else None
        if user_message:
            animated_container = ft.Container(
                content=ft.Column([
                    ft.Container(
                        ft.Text(
                            user_message,
                            color=ft.Colors.WHITE,
                            size=15,
                            no_wrap=False
                        ),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        ft.Text(
                            exact_moment,
                            color=ft.Colors.with_opacity(0.4, "#FFFFFF"),
                        ),
                        alignment=ft.alignment.bottom_right,
                        expand=1
                    )
                ]),
                bgcolor=ft.Colors.GREY_800,
                border_radius=15,
                width=max_width,
                padding=10,
                opacity=0,
                offset=ft.Offset(0, 0.2),
                animate_opacity=ft.animation.Animation(300, curve=ft.AnimationCurve.EASE_IN_OUT),
                animate_offset=ft.animation.Animation(300, curve=ft.AnimationCurve.EASE_IN_OUT)
            )
            
            message_cont.controls.append(
                ft.Row(
                    controls=[animated_container],
                    alignment=ft.MainAxisAlignment.END
                )
            )
            page.update()

            await asyncio.sleep(0.05)

            animated_container.opacity = 1
            animated_container.offset = ft.Offset(0, 0)

            textik.value = ""

            fetch_response(user_message)

            page.update()
        else:
            page.open(ft.SnackBar(ft.Text("Будь ласка напишіть щось!"), bgcolor=ft.Colors.RED_600))


    def fetch_response(user_message):
        stream = chat(
            model=config.get("model"),
            messages=[{'role': 'user', 'content': user_message}],
            stream=True
        )

        response_text = TypewriterText(15, ft.FontWeight.NORMAL, page)

        response_text.animate_thinking()

        response_container = ft.Container(
            content=response_text.text,
            bgcolor=get_time_based_color(),
            width=None,
            border_radius=15,
            padding=10,
            opacity=0,
            offset=ft.Offset(0, 0.2),
            animate_opacity=ft.animation.Animation(300, curve=ft.AnimationCurve.EASE_IN_OUT),
            animate_offset=ft.animation.Animation(300, curve=ft.AnimationCurve.EASE_IN_OUT)
        )

        message_cont.controls.append(
            ft.Row(
                controls=[response_container],
                alignment=ft.MainAxisAlignment.START
            )
        )
        
        page.update()

        time.sleep(0.5)

        response_container.opacity = 1
        response_container.offset = ft.Offset(0, 0)

        page.update()

        full_message = ""
        for chunk in stream:
            full_message += chunk['message']['content']

        response_container.width = 300 if len(full_message) > 30 else None

        full_msg_text = TypewriterText(size=15, weight=ft.FontWeight.NORMAL, page=page)
        response_container.content = full_msg_text.text

        full_msg_text.start_animation(full_message)

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
                            icon=ft.Icons.ARROW_UPWARD_ROUNDED,
                            icon_color=ft.Colors.WHITE,
                            splash_radius=15,
                            bgcolor=get_time_based_color(),
                            on_click=lambda _: asyncio.run(send_message())
                        ),
                        padding=ft.padding.only(left=10)
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.with_opacity(0.4, "#333333"),
                border_radius=15,
                height=70,
                padding=ft.padding.only(left=-20,right=-20),
                clip_behavior=ft.ClipBehavior.NONE,
                shape=ft.BoxShape.RECTANGLE 
            )
        ]
    )