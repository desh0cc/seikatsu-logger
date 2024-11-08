import flet as ft, json, os, time, asyncio
from datetime import datetime, timedelta
from threading import Thread

todaysDate = datetime.today().strftime("%Y-%m-%d")
record_duration = timedelta()

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "folder_path": "/logs",
    "color": "1",
    "AI": "",
    "prompt": ""
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

    config = load_config()
    folder_path = config.get("folder_path")

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
        elif page_name == "chart_page":
            page.add(chart_page())
        elif page_name == "settings_page":
            page.add(settings_page())

        
        page.update()

    gif = ft.Image(
        src="src/icons/animegirly.gif",  
        width=64, 
        height=64,
        fit=ft.ImageFit.CONTAIN  
    )

    def get_time_based_color():
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return "#7DAA6A"  
        elif 12 <= hour < 18:
            return "#D69465"   
        else:
            return "#907bd2"
        
        
    def home():
        typewriter = TypewriterText(page)
        typewriter.start_animation()

        time_color = get_time_based_color()

        time_reactiveBg = ft.Container(
            width=page.window.width,  # Використовуємо повну ширину вікна
            height=300,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[time_color, ft.colors.TRANSPARENT],
                stops=[0.0, 0.7]
            ),
            opacity=0.4,
            left=0,  #
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

        return(ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.SETTINGS,icon_color=ft.colors.WHITE,
                        on_click=lambda e: show_page("settings_page"),
                    ),
                    alignment=ft.alignment.top_right,
                    padding=ft.padding.only(right=10)
                ),

                ft.Container(
                    content=gif,
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
                        f"Сьогодні {todaysDate}",
                        size=13,
                        font_family="Helvetica",
                        weight=ft.FontWeight.W_600,
                        color=get_time_based_color()
                    ),
                    padding=ft.padding.only(top=-100),
                    alignment=ft.alignment.center,
                ),
                
                ft.Container(
                    ft.Column([
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.ElevatedButton(
                                        height=100,
                                        width=210,
                                        content=ft.Column([
                                            ft.Container(
                                                ft.Text("Останній запис",color=get_time_based_color()),
                                                alignment=ft.alignment.top_left,
                                                padding=ft.padding.only(top=15,left=-10)
                                            ),
                                            ft.Container(
                                                ft.Text("Сьогодні ви написали не занадто багато.", color=ft.colors.WHITE70),
                                                alignment=ft.alignment.center_left,
                                                padding=ft.padding.only(left=-10,top=-7),
                                            )
                                        ]),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                    ),
                                    ft.ElevatedButton(
                                        height=100,
                                        width=100,
                                        content=ft.Image(src="src/icons/chat.png", color=get_time_based_color(), width=32, height=32),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER  # Центрирование первой строки
                            ),
                            padding=ft.padding.only(top=32)
                        ),

                        # First row of buttons
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.ElevatedButton(
                                        height=100,
                                        width=100,
                                        content=ft.Image(src="src/icons/copy-writing.png", color=get_time_based_color(), width=32, height=32),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                        on_click=lambda e: show_page("write_page")
                                    ),
                                    ft.ElevatedButton(
                                        height=100,
                                        width=100,
                                        content=ft.Image(src="src/icons/editing.png", color=get_time_based_color(), width=32, height=32),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                        on_click=lambda e: show_page("record_page")
                                    ),
                                    ft.ElevatedButton(
                                        height=100,
                                        width=100,
                                        content=ft.Image(src="src/icons/button.png", color=get_time_based_color(), width=32, height=32),
                                        on_click=lambda e: show_page("chart_page"),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER 
                            ),
                            padding=ft.padding.only(top=10)
                        ),

                        # Second row of buttons
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.ElevatedButton(
                                        height=100,
                                        width=100,
                                        content=ft.Image(src="src/icons/chart.png", color=get_time_based_color(), width=32, height=32),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                                    ),
                                    ft.ElevatedButton(
                                        height=100,
                                        width=100,
                                        content=ft.Image(src="src/icons/neuron.png", color=get_time_based_color(), width=32, height=32),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                                    ),
                                    ft.ElevatedButton(
                                        height=100,
                                        width=100,
                                        content=ft.Image(src="src/icons/folder.png", color=get_time_based_color(), width=32, height=32),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                        on_click=lambda e: quit(ft.app)
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER  # Центрирование второй строки кнопок
                            ),
                            padding=ft.padding.only(top=10)
                        ),
                    ]),
                    alignment=ft.alignment.center
                )
            ]),
            padding=ft.padding.all(0), 
            margin=ft.margin.all(0)
        ))
    
    
    def write_page():


        def create_page(content):
            return ft.Container(
                content=ft.Container(content),
                alignment=ft.alignment.center,
                expand=True,
            )
        

        def handle_date_change(e):
            selected_date.value = f"Вибрана дата: {e.control.value.strftime('%Y-%m-%d')}"
            selected_date.data = e.control.value
            page.update()

        def handle_activity_change(e):
            activity_input.value = f"Вибрана активність: {e.control.value}"
            activity_input.data = e.control.value
            page.update()

        def handle_start_time_change(e):
            start_time.value = f"Вибраний час: {e.control.value.strftime('%H:%M:%S')}"
            start_time.data = e.control.value
            page.update()

        def handle_end_time_change(e):
            end_time.value = f"Вибраний час: {e.control.value.strftime('%H:%M:%S')}"
            end_time.data = e.control.value
            page.update()

        def json_load(file):
            try:
                with open(file, "r") as f:
                    data = json.load(f)
                return data
            except Exception as e:
                print(e)

        def save_activity(date,event,start_time,end_time,duration=None):
            folder_path
            data = json_load(date)


        selected_date = ft.Text("")
        start_time = ft.Text("")
        end_time = ft.Text("")
        activity_input = ft.Text("")
        
        note_page = create_page(ft.Column([
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color=get_time_based_color(),
                        on_click=lambda e: show_page("home")
                    ),
                    alignment=ft.alignment.top_left,
                    padding=ft.padding.only(left=10)
                ),
                
                ft.Container(
                    content=ft.Text(
                        "Додати лог",
                        color=get_time_based_color(),
                        font_family="Helvetica",
                        weight=ft.FontWeight.BOLD,
                        size=20
                    ),
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(top=-45)
                ),

                # Секція вибору дати
                ft.Container(
                    content=ft.Column([
                        ft.Container(ft.Text("Виберіть дату:", size=16),alignment=ft.alignment.center),
                        ft.Container(ft.ElevatedButton(
                            text="Відкрити календар", color=get_time_based_color(),
                            icon=ft.icons.CALENDAR_MONTH,
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
                        ft.Container(ft.Text("Назва активності:", size=16), alignment=ft.alignment.center),
                        ft.Container(ft.TextField(
                            width=200,
                            text_align=ft.TextAlign.LEFT,
                            label="Активність",
                            hint_text="Введіть назву активності",
                            color=ft.colors.WHITE,
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
                        ft.Container(ft.Text("Вкажіть час початку:", size=16), alignment=ft.alignment.center),
                        ft.Container(ft.ElevatedButton(
                            text="Вибрати час",color=get_time_based_color(),
                            icon=ft.icons.ACCESS_TIME,
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
                        ft.Container(ft.Text("Вкажіть час закінчення:", size=16), alignment=ft.alignment.center),
                        ft.Container(ft.ElevatedButton(
                            text="Вибрати час",color=get_time_based_color(),
                            icon=ft.icons.ACCESS_TIME,
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
                    content=ft.ElevatedButton(text="Додати",color=get_time_based_color(),on_click=lambda _: save_activity(selected_date,start_time,end_time,activity_input)),
                    alignment=ft.alignment.center
                )
            ])
        )

        start_value = "0:00:00"
        record_label = ft.Text(value="0:00:00",size=30,font_family="Helvetica", weight=ft.FontWeight.BOLD)

        activity_input = ft.Text("")

        def start_recording():
            global record_duration, stop_recording_flag, start_time, end_time
            stop_recording_flag = False
            record_duration = timedelta()  # Initialize record_duration here
            start_time = datetime.now()  # Use datetime object directly
            print(start_time.strftime("%H:%M:%S"))
            
            while True:
                if stop_recording_flag:
                    end_time = datetime.now()  # Set end_time as a datetime object
                    print(end_time.strftime("%H:%M:%S"))
                    break
                time.sleep(1)
                record_duration += timedelta(seconds=1)
                record_label.value = str(record_duration)
                page.update()


        def stop_recording():
            global stop_recording_flag
            stop_recording_flag = True  # Встановлюємо прапорець для зупинки запису
            record_label.value = str(record_duration)  # Оновлюємо значення тексту
            page.update()  # Оновлюємо сторінку

        def delete_recording():
            global record_duration
            record_duration = timedelta()  # Скидаємо тривалість
            record_label.value = start_value  # Скидаємо текст до початкового значення
            page.update()  # Оновлюємо сторінку

        def on_change_activity(e):
            activity_input.data = e.control.value
            page.update()


        record_page = create_page(ft.Column([
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color=get_time_based_color(),
                        on_click=lambda e: show_page("home")
                    ),
                    alignment=ft.alignment.top_left,
                    padding=ft.padding.only(left=10),
                ),
                ft.Container(
                    content=ft.Text(
                        "Записати лог",
                        color=get_time_based_color(),
                        font_family="Helvetica",
                        weight=ft.FontWeight.BOLD,
                        size=20
                    ),
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(top=-45)
                ),

                ft.Container(
                    content=ft.Column([
                        ft.Container(ft.Text("Назва активності:", size=16), alignment=ft.alignment.center),
                        ft.Container(ft.TextField(
                            width=200,
                            text_align=ft.TextAlign.LEFT,
                            label="Активність",
                            hint_text="Введіть назву активності",
                            color=ft.colors.WHITE,
                            border_color=get_time_based_color(),
                            label_style=ft.TextStyle(color=get_time_based_color()),
                            on_change=on_change_activity
                        ), alignment=ft.alignment.center),
                        activity_input
                    ])
                ),

                ft.Container(
                    content=record_label,
                    alignment=ft.alignment.top_center
                ),

                ft.Row([
                    ft.Container(
                        content=ft.IconButton(
                            icon_color=ft.colors.GREEN_ACCENT,
                            icon=ft.icons.PLAY_CIRCLE,
                            width=45,
                            height=45,
                            on_click=lambda e: start_recording()
                        )
                    ),

                    ft.Container(
                        content=ft.IconButton(
                            icon_color=ft.colors.YELLOW_ACCENT,
                            icon=ft.icons.STOP_CIRCLE,
                            width=45,
                            height=45,
                            on_click=lambda e: stop_recording()
                        )
                    ),
                    ft.Container(
                        content=ft.IconButton(
                            icon_color=ft.colors.RED_ACCENT,
                            icon=ft.icons.GPP_MAYBE_ROUNDED,
                            width=45,
                            height=45,
                            on_click=lambda e: delete_recording()
                        )
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Container(
                        content=ft.ElevatedButton(text="Додати",color=get_time_based_color(),on_click=lambda e: save_activity(todaysDate, start_time, end_time, activity_input)),
                        alignment=ft.alignment.center
                    )
                ])
            )
        edit_page = create_page(ft.Text("Член"))

        pages = [note_page,record_page, edit_page]

        stack = ft.Stack(
            [
                note_page,
                record_page,
                edit_page
            ],
            expand=True,
        )
        
        # Функция для переключения видимости страниц
        def switch_page(index):
            for i, p in enumerate(pages):
                p.visible = i == index
            page.update()
        
        # Изначально отображаем первую страницу
        switch_page(0)

        # NavigationBar для выбора страниц
        nav_bar = ft.Container(
            ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination("Додати", icon=ft.icons.ADD),
                    ft.NavigationBarDestination("Записати", icon=ft.icons.RECORD_VOICE_OVER),
                    ft.NavigationBarDestination("Редагувати", icon=ft.icons.CHANGE_CIRCLE),
                ],
                indicator_color=get_time_based_color(),
                on_change=lambda e: switch_page(e.control.selected_index),
                adaptive=True,
            ),
            alignment=ft.alignment.bottom_center,
            padding=ft.padding.only(left=-20, right=-20,bottom=-10),
        )

        return ft.Column(
            [
            stack,
            nav_bar
            ],
            expand=True
        )
    

    def chart_page():

        return ft.Column([
            ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color=get_time_based_color(),
                    on_click=lambda e: show_page("home")
                ),
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(left=10),
            ),
            ft.Container(
                content=ft.Text(
                    "Вивести графік",
                    color=get_time_based_color(),
                    font_family="Helvetica",
                    weight=ft.FontWeight.BOLD,
                    size=20
                ),
                alignment=ft.alignment.top_center,
                padding=ft.padding.only(top=-45)
            ),


        ])
    
    def settings_page():
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


        return ft.Column([
            ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color=get_time_based_color(),
                    on_click=lambda e: show_page("home")
                ),
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(left=10),
            ),
            ft.Container(
                content=ft.Text(
                    "Налаштування",
                    color=get_time_based_color(),
                    font_family="Helvetica",
                    weight=ft.FontWeight.BOLD,
                    size=20
                ),
                alignment=ft.alignment.top_center,
                padding=ft.padding.only(top=-45)
            ),

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
                content=ft.Row(
                    [
                        ft.Container(
                            ft.IconButton(
                                content=ft.Image(src="src/icons/github.png", color=get_time_based_color(), width=32, height=32),
                                url="https://github.com/desh0cc",
                            ),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            ft.IconButton(
                                content=ft.Image(src="src/icons/telegram.png", color=get_time_based_color(), width=32, height=32),
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
            )
          
        ])
    padding=ft.padding.all(0),  
    margin=ft.margin.all(0)
    show_page("home")

if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets"
    )