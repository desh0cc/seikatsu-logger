import flet as ft, json, os, time
from datetime import datetime
from threading import Thread
todaysDate = datetime.today().strftime("%Y-%m-%d")

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "folder_path": None  
}

def save_config(config_data):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config_data, file, indent=4)

def load_config():
    try:
        if not os.path.exists(CONFIG_FILE):
            save_config(DEFAULT_CONFIG)
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return DEFAULT_CONFIG
    


class TypewriterText:
    def __init__(self, page: ft.Page):
        self.text = ft.Text(
            size=25,
            weight=ft.FontWeight.BOLD,
            font_family="Helvetica"
        )
        self.page = page
        self.animation_thread = None

    def start_animation(self):
        def animate():
            full_text = "Привіт, чим допомогти?"
            self.text.value = ""
            
            for char in full_text:
                self.text.value += char
                self.page.update(self.text)
                time.sleep(0.05)

        # Stop previous animation if running
        if self.animation_thread and self.animation_thread.is_alive():
            return

        self.animation_thread = Thread(target=animate)
        self.animation_thread.start()
    
def main(page: ft.Page):
    page.title = "Simple Logging Unit (SLU)"
    page.window.height = 720
    page.window.width = 480
    page.window.resizable = False

    page.theme_mode = ft.ThemeMode.SYSTEM

    selected_folder_path = load_config()

    def theme_switch(e):
        selected_theme = e.control.content.value  
        if selected_theme == "SYSTEM":
            page.theme_mode = ft.ThemeMode.SYSTEM
        elif selected_theme == "DARK":
            page.theme_mode = ft.ThemeMode.DARK
        elif selected_theme == "LIGHT":
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()  



    def show_page(page_name):
        page.controls.clear()  

        if page_name == "home":
            page.add(home())
        elif page_name == "write_page":
            page.add(write_page())
        elif page_name == "record_page":
            page.add(record_page())
        elif page_name == "settings_page":
            page.add(settings_page())

        
        page.update()

    gif = ft.Image(
        src="src/icons/animegirly.gif",  
        width=64, 
        height=64,
        fit=ft.ImageFit.CONTAIN  
    )



    def home():
        typewriter = TypewriterText(page)
        typewriter.start_animation()

        return ft.Container(
            content=ft.Column([
                ft.Container(
                content=ft.IconButton(icon=ft.icons.SETTINGS,
                                        on_click=lambda e: show_page("settings_page")
                                        ),
                alignment=ft.alignment.top_right,
                padding=ft.padding.only(right=10)
                ),
                ft.Container(
                    content=gif,
                    alignment=ft.alignment.top_center
                ),

                ft.Container(content=typewriter.text,
                alignment=ft.alignment.center, padding=ft.padding.only(top=20)),
                ft.Container(ft.Text(
                    f"Сьогодні {todaysDate}",
                    size=10,
                    font_family="Helvetica",
                    color=ft.colors.BLUE_GREY_200), 
                    padding=ft.padding.only(top=-5), 
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton(
                            height=100,
                            width=210,
                            content=ft.Icon(ft.icons.TEXT_FIELDS),  
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=lambda e: show_page("write_page")
                        ),
                        ft.ElevatedButton(
                            height=100,
                            width=100,
                            content=ft.Image(src="src/icons/magic-wand-auto-fix-button.png", color=ft.colors.BLUE_200, width=32, height=32), 
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=lambda e: show_page("record_page")
                        )
                    ]),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=60, left=60, right=60)
                ),

                # Первый ряд кнопок
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton(
                            height=100,
                            width=100,
                            content=ft.Image(src="src/icons/copy-writing.png", color=ft.colors.BLUE_200, width=32, height=32),  
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=lambda e: show_page("write_page")
                        ),
                        ft.ElevatedButton(
                            height=100,
                            width=100,
                            content=ft.Image(src="src/icons/button.png", color=ft.colors.BLUE_200, width=32, height=32), 
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                        ),
                        ft.ElevatedButton(
                            height=100,
                            width=100,
                            content=ft.Image(src="src/icons/chart.png", color=ft.colors.BLUE_200, width=32, height=32),  
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                        )
                    ]),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=10, left=60, right=60)
                ),


                # Второй ряд кнопок
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton(
                            height=100,
                            width=100,
                            content=ft.Image(src="src/icons/neuron.png", color=ft.colors.BLUE_200, width=32, height=32),  
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                        ),
                        ft.ElevatedButton(
                            height=100,
                            width=100,
                            content=ft.Image(src="src/icons/folder.png", color=ft.colors.BLUE_200, width=32, height=32), 
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                        ),
                        ft.ElevatedButton(
                            height=100,
                            width=100,
                            content=ft.Icon(ft.icons.EXIT_TO_APP),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=lambda e: quit(ft.app)
                        )
                    ]),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=10, left=60, right=60)
                )
            ])
        )
    def write_page():
        def handle_change(e):
            page.add(ft.Text(f"Date changed: {e.control.value.strftime('%Y-%m-%d')}"))

        def handle_dismissal(e):
            page.add(ft.Text(f"DatePicker dismissed"))

        return ft.Column([
            ft.Container(
                content=ft.IconButton(icon=ft.icons.ARROW_BACK,
                                        on_click=lambda e: show_page("home")
                                        ),
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(left=10)
            ),
            ft.Container(
                content=ft.Text(
                    "Змінити лог",
                    color=ft.colors.BLUE_200,
                    font_family="Helvetica",
                    size=20
                ),
                alignment=ft.alignment.top_center,
                padding=ft.padding.only(top=-45)
            ),

            ft.Container(
                content=ft.Text(
                    value="Виберіть Дату:",
                    size=20
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=10)
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    "Вибрати дату",
                    icon=ft.icons.CALENDAR_MONTH,
                    on_click=lambda e: page.open(
                        ft.DatePicker(
                            on_change=handle_change,
                            on_dismiss=handle_dismissal,
                        )
                    ),
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only()
            )
        ])

    def record_page():
        return ft.Column([
            ft.Container(
                content=ft.IconButton(icon=ft.icons.ARROW_BACK,
                                        on_click=lambda e: show_page("home")
                                        ),
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(left=10)
            ),

        ])
    
    def settings_page():
        def save_cfg(e: ft.FilePickerResultEvent):
            try:
                with open("config.json", "r") as f:
                    config = json.load(f)
            except FileNotFoundError:
                config = {"folder_path": None}

            # Оновлюємо значення folder_path
            config["folder_path"] = e.path

            # Записуємо оновлений конфіг у файл
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)

            # Додаємо повідомлення про успішне збереження (опціонально)
            print("Шлях до папки успішно збережено в config.json")


        file_picker = ft.FilePicker(on_result=save_cfg)
        page.overlay.append(file_picker)


        return ft.Column([
            ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: show_page("home")
                ),
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(left=10),
            ),

            ft.Container(
                content=ft.Text(
                    "Налаштування",
                    color=ft.colors.BLUE_200,
                    font_family="Helvetica",
                    size=20
                ),
                alignment=ft.alignment.top_center,
                padding=ft.padding.only(top=-45)
            ),

            ft.Container(
                content=ft.Text(
                    value="Вибрати тему",
                    size=20
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
                                    on_click=theme_switch
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("DARK"),
                                    on_click=theme_switch
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("LIGHT"),
                                    on_click=theme_switch
                                ),
                            ],
                            style=ft.ButtonStyle(color=ft.colors.BLUE_300)
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
                    icon=ft.Icon(ft.icons.DRIVE_FOLDER_UPLOAD),
                    text="Вибрати теку",
                    on_click=lambda _: file_picker.get_directory_path("Вибрати теку для логів")
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=5)
            )
          
        ])

    show_page("home")

ft.app(main)
