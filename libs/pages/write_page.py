import flet as ft, json, os
from datetime import datetime

def write_page(page: ft.Page):
    from utils import get_time_based_color, load_config, lang_load
    from libs.components.NavigationComp import BackToHome

    config = load_config()
    folder_path = config.get("folder_path")

    def handle_date_change(e):
        selected_date.value = f"{e.control.value.strftime('%Y-%m-%d')}"
        selected_date.data = e.control.value
        page.update()

    def handle_activity_change(e):
        activity_input.data = e.control.value
        page.update()

    def handle_start_time_change(e):
        start_time.value = f"{e.control.value.strftime('%H:%M:%S')}"
        start_time.data = e.control.value
        page.update()

    def handle_end_time_change(e):
        end_time.value = f"{e.control.value.strftime('%H:%M:%S')}"
        end_time.data = e.control.value
        page.update()

    def save_activity():
        try:
            if not all([selected_date.data, start_time.data, end_time.data, activity_input.data]):
                page.open(
                    ft.SnackBar(content=ft.Text(lang_load("write_page_error_message")), bgcolor=ft.Colors.ERROR)
                )
                return

            file_date = selected_date.data.strftime('%Y-%m-%d')
            
            start_datetime = datetime.combine(selected_date.data, start_time.data)
            end_datetime = datetime.combine(selected_date.data, end_time.data)
            duration = end_datetime - start_datetime
            file_path = os.path.join(folder_path, "logs", f"{file_date}.json")

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            data = {}
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except json.decoder.JSONDecodeError:
                    data = {}

            data[activity_input.data] = {
                "start_time": start_time.data.strftime('%H:%M:%S'),
                "end_time": end_time.data.strftime('%H:%M:%S'),
                "duration": str(duration)
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            page.open(
                ft.SnackBar(content=ft.Text(lang_load("write_page_success_message")), bgcolor=ft.Colors.GREEN)
            )

            activity_input.value = ""
            selected_date.value = ""
            start_time.value = ""
            end_time.value = ""
            selected_date.data = None
            start_time.data = None
            end_time.data = None
            page.update()

        except FileNotFoundError:
            page.open(
                ft.SnackBar(content=ft.Text(f"Error"), bgcolor=ft.Colors.ERROR)
            )

    selected_date = ft.Text("")
    start_time = ft.Text("")
    end_time = ft.Text("")
    activity_input = ft.Text("")

    navigator = BackToHome(lang_load("write_page_title"), page)

    content = ft.Column([
            navigator.add(),

            # Секція вибору дати
            ft.Container(
                content=ft.Column([
                    ft.Container(ft.Text(lang_load("write_page_calendar_title"), size=16),alignment=ft.alignment.center),
                    ft.Container(ft.ElevatedButton(
                        text=lang_load("write_page_button_calendar"), color=get_time_based_color(),
                        icon=ft.Icons.CALENDAR_MONTH,
                        icon_color=get_time_based_color(),
                        on_click=lambda e: page.open(
                            ft.DatePicker(
                                on_change=handle_date_change,
                            )
                        ),
                    ),alignment=ft.alignment.center),
                    selected_date
                ])
            ),

            # Секція вибору активності
            ft.Container(
                content=ft.Column([
                    ft.Container(ft.Text(lang_load("write_page_activity_title"), size=16), alignment=ft.alignment.center),
                    ft.Container(ft.TextField(
                        width=200,
                        text_align=ft.TextAlign.LEFT,
                        label=lang_load("write_page_activity_input_label"),
                        color=ft.Colors.WHITE,
                        border_color=get_time_based_color(),
                        label_style=ft.TextStyle(color=get_time_based_color()),
                        on_change=handle_activity_change
                    ), alignment=ft.alignment.center),
                    activity_input
                ])
            ),

            # Секція вибору часу
            ft.Container(
                content=ft.Column([
                    ft.Container(ft.Text(lang_load("write_page_start_time_title"), size=16), alignment=ft.alignment.center),
                    ft.Container(ft.ElevatedButton(
                        text=lang_load("write_page_time_button"),color=get_time_based_color(),
                        icon=ft.Icons.ACCESS_TIME,
                        icon_color=get_time_based_color(),
                        on_click=lambda e: page.open(
                            ft.TimePicker(
                                on_change=handle_start_time_change,
                            )
                        ),
                    ),alignment=ft.alignment.center),
                    start_time,
                ]),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=20)
            ),

            ft.Container(
                content=ft.Column([
                    ft.Container(ft.Text(lang_load("write_page_start_time_title"), size=16), alignment=ft.alignment.center),
                    ft.Container(ft.ElevatedButton(
                        text=lang_load("write_page_time_button"),color=get_time_based_color(),
                        icon=ft.Icons.ACCESS_TIME,
                        icon_color=get_time_based_color(),
                        on_click=lambda e: page.open(
                            ft.TimePicker(
                                on_change=handle_end_time_change,
                            )
                        ),
                    ),alignment=ft.alignment.center),
                    end_time,
                ])
            ),

            ft.Container(
                content=ft.ElevatedButton(text=lang_load("write_page_save_button"),color=get_time_based_color(),on_click=lambda _: save_activity()),
                alignment=ft.alignment.center
            )
        ]
    )
    return ft.Column([content], expand=True)