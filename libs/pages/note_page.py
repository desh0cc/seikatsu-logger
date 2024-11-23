import flet as ft, json, os
from utils import get_time_based_color, todaysDate, load_config
from libs.components.Back import BackToHome

def note_page(page: ft.Page) -> ft.View:
    back = BackToHome("Зробити запис", page)

    deleted = None

    config = load_config()
    folder_path = config.get("folder_path")

    def on_field_change(e):
        nonlocal deleted
        text.data = e.control.value

        if deleted:
            e.control.value = load_text()
            page.update()
            deleted = False

        page.update()

    def save_note(text):
        try:
            if not os.path.exists(f"{folder_path}/notes/"):
                os.makedirs(f"{folder_path}/notes/")

            with open(f"{folder_path}/notes/{todaysDate}.json", "w", encoding="utf-8") as f:
                json.dump({"note": text}, f, ensure_ascii=False, indent=4)
                page.open(ft.SnackBar(ft.Text("Успішно записано", color=ft.colors.WHITE), bgcolor=ft.colors.GREEN))

        except Exception as e:
            print(e)

    def load_text():
        try:
            with open(f"{folder_path}/notes/{todaysDate}.json", "r", encoding="utf-8") as f:
                text = json.load(f)
                return text["note"]
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return ""
        
    def delete_note():
        nonlocal deleted
        try:
            os.remove(f"{folder_path}/notes/{todaysDate}.json")
            text.data = ""
            deleted = True
            page.update()
            page.open(ft.SnackBar(ft.Text("Нотатку видалено", color=ft.colors.WHITE), bgcolor=ft.colors.RED_ACCENT))
        except FileNotFoundError:
            page.open(ft.SnackBar(ft.Text("Помилка при видаленні нотатки"), bgcolor=ft.colors.RED_ACCENT))

    text = ft.Text("")

    return ft.View(
        route="/note",
        controls=[
            back.add(),
            ft.Container(
                ft.Row(
                    [
                        ft.Container(
                            ft.Text(
                                f"Запис за {todaysDate}",
                                size=16,
                                font_family="Helvetica",
                                color=ft.colors.WHITE
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(left=23)
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    ft.IconButton(
                                        icon=ft.icons.SAVE,
                                        icon_color=get_time_based_color(),
                                        on_click=lambda _: save_note(text.data),
                                        tooltip="Зберегти нотатку"
                                    ),
                                    alignment=ft.alignment.center,
                                ),
                                ft.Container(
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        icon_color=ft.colors.RED,
                                        on_click=lambda _: delete_note(),
                                        tooltip="Видалити нотатку"
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
                bgcolor=ft.colors.with_opacity(0.4, "#333333"),
                height=45,
                border_radius=7,
                padding=ft.padding.only(left=-10,right=-10),
            ),

            ft.Column(
                controls=[
                    ft.Container(
                        ft.TextField(
                            value=load_text(),
                            multiline=True,
                            expand=True,
                            min_lines=20,
                            on_change=on_field_change,
                            border_color=ft.colors.with_opacity(0.0, color=ft.colors.GREY_800),
                            hint_text="Введіть текст нотатки...",
                        ),
                        bgcolor=ft.colors.with_opacity(0.4, "#222222"),
                        border_radius=7
                    ),
                ],
                scroll=ft.ScrollMode.ALWAYS,
                expand=True, 
                height=300,
            ),
            text
        ]
    )