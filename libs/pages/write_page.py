import flet as ft, json, os
from datetime import datetime

class WritePage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        from utils import get_time_based_color, show_page, folder_path
        
        def handle_date_change(e):
            selected_date.value = f"Вибрана дата: {e.control.value.strftime('%Y-%m-%d')}"
            selected_date.data = e.control.value
            self.update()

        def handle_activity_change(e):
            activity_input.value = f"Вибрана активність: {e.control.value}"
            activity_input.data = e.control.value
            self.update()

        def handle_start_time_change(e):
            start_time.value = f"Вибраний час: {e.control.value.strftime('%H:%M:%S')}"
            start_time.data = e.control.value
            self.update()

        def handle_end_time_change(e):
            end_time.value = f"Вибраний час: {e.control.value.strftime('%H:%M:%S')}"
            end_time.data = e.control.value
            self.update()

        def json_load(file):
            try:
                with open(file, "r") as f:
                    data = json.load(f)
                return data
            except Exception as e:
                print(e)

        def save_activity():
            try:
                # Перевірка на заповнення всіх полів
                if not all([selected_date.data, start_time.data, end_time.data, activity_input.data]):
                    self.page.open(
                        ft.SnackBar(content=ft.Text("Будь ласка, заповніть всі поля"), bgcolor=ft.colors.ERROR)
                    )
                    return

                # Форматування дати та отримання шляху до файлу
                file_date = selected_date.data.strftime('%Y-%m-%d')
                
                
                # Об'єднання дати і часу
                start_datetime = datetime.combine(selected_date.data, start_time.data)
                end_datetime = datetime.combine(selected_date.data, end_time.data)
                duration = end_datetime - start_datetime
                file_path = os.path.join(folder_path, f"{file_date}.json")

                # Створення папки, якщо її немає
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Завантаження даних з файлу або створення нового словника
                data = {}
                if os.path.exists(file_path):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                    except json.decoder.JSONDecodeError:
                        data = {}

                # Додавання нової активності
                data[activity_input.data] = {
                    "start_time": start_time.data.strftime('%H:%M:%S'),
                    "end_time": end_time.data.strftime('%H:%M:%S'),
                    "duration": str(duration)
                }

                # Збереження оновлених даних у файлі
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                # Повідомлення про успішне збереження
                self.page.open(
                    ft.SnackBar(content=ft.Text("Активність успішно збережено"), bgcolor=ft.colors.GREEN)
                )

                # Очищення полів
                activity_input.value = ""
                selected_date.value = ""
                start_time.value = ""
                end_time.value = ""
                selected_date.data = None
                start_time.data = None
                end_time.data = None
                self.page.update()

            except Exception as e:
                self.page.open(
                    ft.SnackBar(content=ft.Text(f"Помилка: {str(e)}"), bgcolor=ft.colors.ERROR)
                )



        selected_date = ft.Text("")
        start_time = ft.Text("")
        end_time = ft.Text("")
        activity_input = ft.Text("")

        content = ft.Column([
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color=get_time_based_color(),
                        on_click=lambda e: show_page("home", self.page)
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
                            on_click=lambda e: self.page.open(
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
                            on_click=lambda e: self.page.open(
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
                            on_click=lambda e: self.page.open(
                                ft.TimePicker(
                                    on_change=handle_end_time_change,
                                )
                            ),
                        ),alignment=ft.alignment.center),
                        end_time,
                    ])
                ),

                ft.Container(
                    content=ft.ElevatedButton(text="Додати",color=get_time_based_color(),on_click=lambda _: save_activity()),
                    alignment=ft.alignment.center
                )
            ]
        )
        return ft.Column([content], expand=True)
        
