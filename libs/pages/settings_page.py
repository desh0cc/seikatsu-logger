import flet as ft, json
from libs.components.Back import BackToHome

def settings_page(page: ft.Page) -> ft.View:
    from utils import get_time_based_color, theme_switch
    def save_cfg(e: ft.FilePickerResultEvent):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {"folder_path": None}

        config["folder_path"] = str(f"{e.path}\\")

        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

        page.open(ft.SnackBar(content=ft.Text("Шлях до папки успішно збережено в config.json"),bgcolor=get_time_based_color()))

    file_picker = ft.FilePicker(on_result=save_cfg)
    page.overlay.append(file_picker)

    navigator = BackToHome("Налаштування", page)

    return ft.View(
        route="/settings",
        controls=[
            navigator.add(),
            ft.Container(
                content=ft.Text("Про додаток", size=20,),
                alignment=ft.alignment.center
            ),

            ft.Container(
                ft.Container(
                    content=ft.Text("Версія 1.0"),
                    alignment=ft.alignment.center,
                    bgcolor=get_time_based_color(),
                    border_radius=20,
                    width=90,
                    height=25
                ),
                alignment=ft.alignment.center
            ),

            ft.Container(
                ft.Image(src="assets/icon.png", width=64, height=64),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=10)
            ),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            ft.IconButton(
                                content=ft.Image(src="assets/icons/github.png", color=get_time_based_color(), width=32, height=32),
                                url="https://github.com/desh0cc",
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            ft.IconButton(
                                content=ft.Image(src="assets/icons/telegram.png", color=get_time_based_color(), width=32, height=32),
                                url="https://t.me/+9Olu761hIZ4zYTJi",
                            ),
                            alignment=ft.alignment.center
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER 
                )
            ),

            ft.Container(
                content=ft.Text(
                    value="Вибрати тему",
                    size=20,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=10)
            ),

            ft.Container(
                content=ft.MenuBar(
                    expand=True,
                    controls=[
                        ft.SubmenuButton(
                            content=ft.Text("Вибрати тему"),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text("SYSTEM"),
                                    on_click=lambda e: theme_switch(e, page)
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("DARK"),
                                    on_click=lambda e: theme_switch(e, page)
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("LIGHT"),
                                    on_click=lambda e: theme_switch(e, page)
                                ),
                            ],
                            style=ft.ButtonStyle(color=get_time_based_color())
                        )
                    ]
                ),
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Text(
                    value="Вибрати шлях до логів",
                    size=20
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=10)
            ),
            ft.Container(
                ft.ElevatedButton(
                    icon=ft.Icon(ft.icons.DRIVE_FOLDER_UPLOAD), color=get_time_based_color(),
                    text="Вибрати теку",
                    on_click=lambda _: file_picker.get_directory_path("Вибрати теку для логів")
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=5)
            )]
        )