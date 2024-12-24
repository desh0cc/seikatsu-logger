import flet as ft, json, platform, os, subprocess
from libs.components.TypewriterText import TypewriterText

def home_page(page: ft.Page) -> ft.View:
    from utils import get_time_based_color, todaysDate, lang_load, load_config

    config = load_config()
    folder_path = config.get("folder_path")

    typewriter = TypewriterText(25, ft.FontWeight.BOLD, page, "CaskaydiaCove")
    typewriter.start_animation(lang_load("home_page_title"))

    time_color = get_time_based_color()

    time_reactiveBg = ft.Container(
        width=page.window.width,
        height=300,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[time_color, ft.Colors.TRANSPARENT],
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
    
    def get_note_text():
        try:
            with open(f"{folder_path}/notes/{todaysDate}.json", "r", encoding="utf-8") as f:
                text = json.load(f)

                if len(text["note"]) <= 5:
                    return lang_load("home_page_note_desc")
                else:
                    return text["note"]
        except (FileNotFoundError, json.decoder.JSONDecodeError, TypeError):
            return lang_load("home_page_note_desc")
        
    def open_folder(path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Linux":
            subprocess.Popen(["xdg-open", path])
        else:
            raise NotImplementedError("Uknown system")

    return ft.View(
        route = "/",
        controls=[
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.SETTINGS,icon_color=ft.Colors.WHITE,
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
                    lang_load(f"home_page_date", date=todaysDate),
                    size=13,
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
                                            ft.Text(lang_load("home_page_note_title"),color=get_time_based_color(), weight=ft.FontWeight.BOLD),
                                            alignment=ft.alignment.top_left,
                                            padding=ft.padding.only(top=15,left=10)
                                        ),
                                        ft.Container(
                                            ft.Text(get_note_text(), color=ft.Colors.WHITE70, max_lines=2, overflow="ellipsis"),
                                            alignment=ft.alignment.center_left,
                                            padding=ft.padding.only(left=10,top=-7),
                                        )
                                    ]),
                                    on_click=lambda _: page.go("/note"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                ),
                                ft.ElevatedButton(
                                    height=100,
                                    width=100,
                                    content=ft.Image(src="assets/icons/chat.png", color=get_time_based_color(), width=32, height=32),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                    on_click=lambda _: page.go("/chat")
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
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
                                    content=ft.Image(src="icons/copy-writing.png", color=get_time_based_color(), width=32, height=32),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                    on_click=lambda e: page.go("/write")
                                ),
                                ft.ElevatedButton(
                                    height=100,
                                    width=100,
                                    content=ft.Image(src="icons/calendar.png", color=get_time_based_color(), width=32, height=32),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                    on_click=lambda e: e
                                ),
                                ft.ElevatedButton(
                                    height=100,
                                    width=100,
                                    content=ft.Image(src="icons/chart.png", color=get_time_based_color(), width=32, height=32),
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
                                    content=ft.Image(src="icons/neuron.png", color=get_time_based_color(), width=32, height=32),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                                ),
                                ft.ElevatedButton(
                                    height=100,
                                    width=100,
                                    content=ft.Image(src="icons/checklist.png", color=get_time_based_color(), width=32, height=32),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                    on_click=lambda _: page.go("/todo")
                                ),
                                ft.ElevatedButton(
                                    height=100,
                                    width=100,
                                    content=ft.Image(src="icons/folder.png", color=get_time_based_color(), width=32, height=32),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                    on_click=lambda e: open_folder(folder_path)
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