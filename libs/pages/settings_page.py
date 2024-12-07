import flet as ft, json, os
from libs.components.NavigationComp import BackToHome

def settings_page(page: ft.Page) -> ft.View:
    from utils import get_time_based_color, theme_switch, load_config, lang_load

    config = load_config()

    def restart_app(page: ft.Page):
        page.views.clear()
        page.go("/")
        page.update()


    def language_load():
        try:
            current_file = os.path.abspath(__file__)
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
            lang_dir = os.path.join(base_dir, "lang")

            langs = [l for l in os.listdir(lang_dir) if os.path.isfile(os.path.join(lang_dir, l))]
            return [ft.dropdown.Option(l) for l in langs]
        except Exception as e:
            print(f"Помилка: {e}")
            return []

    def save_cfg(e: ft.FilePickerResultEvent):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {"folder_path": None}

        config["folder_path"] = str(f"{e.path}\\")
        
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

        page.open(ft.SnackBar(content=ft.Text(lang_load("settings_page_save_success")), bgcolor=get_time_based_color()))
        restart_app(page)

    def on_dropdown_change(e):
        picked_lang = e.control.value
        with open("config.json", "r") as f:
            config = json.load(f)
        config["language"] = picked_lang
        

        with open("config.json", "w", encoding="utf-8") as cfg:
            json.dump(config, cfg, indent=4)

        page.update()
        restart_app(page)

    file_picker = ft.FilePicker(on_result=save_cfg)
    page.overlay.append(file_picker)

    navigator = BackToHome(lang_load("settings_page_title"), page)

    return ft.View(
        route="/settings",
        controls=[
            navigator.add(),
            ft.Container(
                content=ft.Text(lang_load("settings_page_about_title"), size=20,),
                alignment=ft.alignment.center
            ),

            ft.Container(
                ft.Container(
                    content=ft.Text(lang_load("settings_page_version")),
                    alignment=ft.alignment.center,
                    bgcolor=get_time_based_color(),
                    border_radius=20,
                    width=90,
                    height=25
                ),
                alignment=ft.alignment.center
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
                    lang_load("settings_page_theme_title"),
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
                            content=ft.Text(lang_load("settings_page_theme_title")),
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
                    value=lang_load("settings_page_folder_title"),
                    size=20
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=10)
            ),
            ft.Container(
                ft.ElevatedButton(
                    icon=ft.Icon(ft.icons.DRIVE_FOLDER_UPLOAD), color=get_time_based_color(),
                    text=lang_load("settings_page_folder_button"),
                    on_click=lambda _: file_picker.get_directory_path(lang_load("settings_page_folder_dialog"))
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=5)
            ),
            
            ft.Column([
                ft.Container(
                    ft.Text(lang_load("settings_page_choose_lang"), size=20),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=10)
                ),
                ft.Container(
                    ft.Dropdown(
                        options=language_load(),
                        on_change=on_dropdown_change,
                        value=config.get("language"),
                        border_color=get_time_based_color(),
                        width=150,
                        border_radius=10,
                        hint_style=ft.TextStyle(
                            color=ft.colors.GREY_500,
                            size=14
                        ),
                        content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
                    ),
                    alignment=ft.alignment.center
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
        ]
    )
