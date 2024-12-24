import flet as ft, json, os, subprocess
from libs.components.NavigationComp import BackToHome

def settings_page(page: ft.Page) -> ft.View:
    from utils import get_time_based_color, load_config, lang_load

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
        
    def fetch_models():
        try:
            result = subprocess.run(['ollama', 'list'], stdout=subprocess.PIPE)
            models = result.stdout.decode('utf-8').splitlines()
            models = [ft.dropdown.Option(line.split()[0]) for line in models[1:]]
            return models
        except Exception as e:
            print(e)
            return []

    def save_cfg(note_path=None, model=None, lang=None):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {"folder_path": None}

        if note_path:
            config["folder_path"] = str(f"{note_path.path}\\")
        if model:
            config["model"] = model
        if lang:
            config["language"] = lang
        
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

        page.open(ft.SnackBar(content=ft.Text(lang_load("settings_page_save_success")), bgcolor=get_time_based_color()))
        restart_app(page)

    def on_lang_change(e):
        lang = e.control.value
        save_cfg(lang=lang)

    def on_model_change(e):
        model = e.control.value
        save_cfg(model=model)

    def on_hover(e):
        e.control.content = (
            ft.Image(src="assets/icons/open-file.svg", width=24,height=24,color=get_time_based_color()) if
            e.data == "true" 
            else ft.Icon(ft.Icons.FOLDER_ROUNDED,color=get_time_based_color())
        )
        page.update()

    file_picker = ft.FilePicker(on_result=save_cfg)
    page.overlay.append(file_picker)

    navigator = BackToHome(lang_load("settings_page_title"), page)

    return ft.View(
        route="/settings",
        controls=[
            navigator.add(),
            

            ft.Container(
                ft.Column([
                    ft.Container(
                        ft.Image(src="icon.png",width=72,height=72),
                        alignment=ft.alignment.center
                    ),

                    ft.Container(
                        ft.Text(
                                lang_load("settings_page_about_title"), 
                                size=20,
                                font_family="CaskaydiaCove",
                                weight=ft.FontWeight.W_600
                            ),
                        alignment=ft.alignment.center
                    ),

                    ft.Row([
                        ft.Container(
                            ft.Row([
                                ft.IconButton(content=ft.Image(src="icons/github.png"),url="https://github.com/desh0cc/seikatsu-logger",width=32,height=32),
                                ft.IconButton(content=ft.Image(src="icons/telegram.png"),url="https://t.me/+9Olu761hIZ4zYTJi",width=32,height=32)
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            alignment=ft.alignment.center,
                            bgcolor=get_time_based_color(),
                            border_radius=15,
                            width=120,
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ]),
            ),
            
            ft.Container(
                ft.Column([
                    ft.Container(
                        ft.Row([
                            ft.Container(
                                ft.Text(lang_load("settings_page_version")),
                                expand=1,
                                alignment=ft.alignment.center_left,
                                padding=ft.padding.only(left=10, top=5)
                            ),
                            ft.Container(
                                ft.Text("1.0.0"),
                                expand=1,
                                alignment=ft.alignment.center_right,
                                padding=ft.padding.only(right=10, top=5)
                            )
                        ])
                    ),
                    ft.Container(
                        ft.Row([
                            ft.Container(
                                ft.Text(lang_load("settings_page_developer")),
                                expand=1,
                                alignment=ft.alignment.center_left,
                                padding=ft.padding.only(left=10)
                            ),
                            ft.Container(
                                ft.Text("desh0cc"),
                                expand=1,
                                alignment=ft.alignment.center_right,
                                padding=ft.padding.only(right=10)
                            )
                        ]),
                        padding=ft.padding.only(top=-5,bottom=7)
                    )
                ]),
                bgcolor=ft.Colors.with_opacity(0.4, color="#333333"),
                border_radius=15,
            ),

            ft.Container(ft.Text(lang_load("settings_page_configuration"), size=20,font_family="CaskaydiaCove",weight=ft.FontWeight.W_600),alignment=ft.alignment.center,padding=ft.padding.only(top=7)),

            ft.Container(
                ft.Column([
                    ft.Container(
                        ft.Row([
                            ft.Container(
                                ft.Text(lang_load("settings_page_language")),
                                padding=ft.padding.only(left=10,top=5)
                            ),
                            ft.Container(
                                ft.Dropdown(
                                    value=config.get("language"),
                                    options=language_load(),
                                    on_change=on_lang_change,
                                    text_size=15,
                                    height=30,
                                    width=90,
                                    bgcolor=None,
                                    border=None,
                                    border_color=ft.Colors.with_opacity(0.0, "#FFFFFF"),
                                    fill_color=ft.Colors.with_opacity(0.0, "#FFFFFF"),
                                    focused_bgcolor=ft.Colors.with_opacity(0.0, "#FFFFFF"),
                                    content_padding=ft.padding.symmetric(horizontal=0),
                                    alignment=ft.alignment.center,
                                ),
                                expand=1,
                                alignment=ft.alignment.center_right,
                                padding=ft.padding.only(top=5,right=10)
                            )
                        ]),
                    ),
                    ft.Container(
                        ft.Row([
                            ft.Container(
                                ft.Text(lang_load("settings_page_model")),
                                padding=ft.padding.only(left=10,top=5)
                            ),
                            ft.Container(
                                ft.Dropdown(
                                    value=config.get("model"),
                                    options=fetch_models(),
                                    on_change=on_model_change,
                                    text_size=15,
                                    height=30,
                                    width=90,
                                    bgcolor=None,
                                    border=None,
                                    border_color=ft.Colors.with_opacity(0.0, "#FFFFFF"),
                                    fill_color=ft.Colors.with_opacity(0.0, "#FFFFFF"),
                                    focused_bgcolor=ft.Colors.with_opacity(0.0, "#FFFFFF"),
                                    content_padding=ft.padding.symmetric(horizontal=0),
                                    alignment=ft.alignment.center,
                                ),
                                padding=ft.padding.only(top=5,right=10)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=ft.padding.only(top=-15)
                    ),
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                ft.Text(lang_load("settings_page_note_path")),
                                alignment=ft.alignment.center_left,
                                padding=ft.padding.only(left=10)
                            ),
                            ft.Container(
                                ft.Row([
                                    ft.Container(
                                        ft.Text(
                                            config.get("folder_path"),
                                            color=ft.Colors.BLACK,
                                            max_lines=1,
                                            overflow=ft.TextOverflow.ELLIPSIS
                                        ),
                                        width=200,
                                        bgcolor=ft.Colors.with_opacity(0.85, "#FFFFFF"),
                                        border_radius=15,
                                        padding=ft.padding.all(5)
                                    ),
                                    ft.ElevatedButton(
                                        content=ft.Icon(ft.Icons.FOLDER_ROUNDED, color=get_time_based_color()),
                                        on_hover=on_hover,
                                        on_click=lambda _: file_picker.get_directory_path(lang_load("settings_page_folder_dialog"))
                                    ),
                                ], alignment=ft.MainAxisAlignment.END), 
                                expand=1,
                                alignment=ft.alignment.center_right,
                                padding=ft.padding.only(right=10)
                            )
                        ]),
                        padding=ft.padding.only(top=-15)
                    )
                ]),
                bgcolor=ft.Colors.with_opacity(0.4, "#333333"),
                border_radius=15
            ),


        ]
    )
