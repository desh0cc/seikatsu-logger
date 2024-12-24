import flet as ft, json, os
from utils import get_time_based_color, todaysDate, load_config, lang_load
from libs.components.NavigationComp import BackToHome

def note_page(page: ft.Page) -> ft.View:
    back = BackToHome(lang_load("note_page_title"), page)

    config = load_config()
    folder_path = config.get("folder_path")

    def load_text():
        try:
            with open(f"{folder_path}/notes/{todaysDate}.json", "r", encoding="utf-8") as f:
                text = json.load(f)
                return text["note"]
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return ""

    def save_note():
        try:
            if not os.path.exists(f"{folder_path}/notes/"):
                os.makedirs(f"{folder_path}/notes/")

            with open(f"{folder_path}/notes/{todaysDate}.json", "w", encoding="utf-8") as f:
                json.dump({"note": text_field.value}, f, ensure_ascii=False, indent=4)
                page.open(ft.SnackBar(ft.Text(lang_load("note_page_save_success"), color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN))

        except Exception as e:
            print(e)
        
    def delete_note():
        try:
            text_field.value = ""
            os.remove(f"{folder_path}/notes/{todaysDate}.json")
            page.update()
            page.open(ft.SnackBar(ft.Text(lang_load("note_page_delete_success"), color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_ACCENT))
        except FileNotFoundError:
            text_field.value = ""
            page.update()
            page.open(ft.SnackBar(ft.Text(lang_load("note_page_delete_error")), bgcolor=ft.Colors.RED_ACCENT))


    text_field = ft.TextField(
        value=load_text(),
        multiline=True,
        expand=True,
        min_lines=20,
        cursor_color=get_time_based_color(),
        border_color=ft.Colors.with_opacity(0.0, color=ft.Colors.GREY_800),
        hint_text=lang_load("note_page_note_write"),
    )

    return ft.View(
        route="/note",
        controls=[
            back.add(),
            ft.Container(
                ft.Row(
                    [
                        ft.Container(
                            ft.Text(
                                lang_load(f"note_page_subtitle", date=todaysDate),
                                size=16,
                                color=ft.Colors.WHITE
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(left=23)
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    ft.IconButton(
                                        icon=ft.Icons.SAVE_ROUNDED,
                                        icon_color=get_time_based_color(),
                                        on_click=lambda _: save_note(),
                                        tooltip=lang_load("note_page_save_tooltip")
                                    ),
                                    alignment=ft.alignment.center,
                                ),
                                ft.Container(
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_ROUNDED,
                                        icon_color=ft.Colors.RED,
                                        on_click=lambda _: delete_note(),
                                        tooltip=lang_load("note_page_delete_tooltip")
                                    ),
                                    alignment=ft.alignment.center,
                                    padding=ft.padding.only(left=-5, right=15)
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                bgcolor=ft.Colors.with_opacity(0.4, "#333333"),
                height=45,
                border_radius=7,
                padding=ft.padding.only(left=-10,right=-10),
            ),

            ft.Column(
                controls=[
                    ft.Container(
                        text_field,
                        bgcolor=ft.Colors.with_opacity(0.4, "#222222"),
                        border_radius=7
                    ),
                ],
                scroll=ft.ScrollMode.ALWAYS,
                expand=True, 
                height=300,
            )
        ]
    )