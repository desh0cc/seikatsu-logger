import flet as ft, time, os, json, threading
from datetime import datetime, timedelta


class RecordPage(ft.UserControl):

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.stop_recording_flag = False  # Флаг для остановки записи
        self.record_duration = timedelta()  # Для отслеживания продолжительности записи
        self.start_time = None  # Время начала записи
        self.end_time = None  # Время окончания записи

    def build(self):
        from utils import todaysDate, show_page, get_time_based_color, folder_path

        start_value = "0:00:00"
        record_label = ft.Text(value=start_value, size=30, font_family="Helvetica", weight=ft.FontWeight.BOLD)

        activity_input = ft.Text("")

        def start_recording():
            self.stop_recording_flag = False
            self.record_duration = timedelta()  # Инициализация продолжительности записи
            self.start_time = datetime.now()  # Запись текущего времени начала
            print(self.start_time.strftime("%H:%M:%S"))

            def record_loop():
                while not self.stop_recording_flag:
                    time.sleep(1)
                    self.record_duration += timedelta(seconds=1)
                    record_label.value = str(self.record_duration)
                    self.update()  # Обновление интерфейса в основном потоке

                # Установка времени окончания записи
                self.end_time = datetime.now()
                print(self.end_time.strftime("%H:%M:%S"))

            # Запуск цикла записи в отдельном потоке
            threading.Thread(target=record_loop).start()

        def stop_recording():
            self.stop_recording_flag = True  # Устанавливаем флаг для остановки записи
            record_label.value = str(self.record_duration)  # Обновляем текстовое поле
            self.update()

        def delete_recording():
            self.record_duration = timedelta()  # Сбрасываем продолжительность
            record_label.value = start_value  # Возвращаем текстовое поле к начальному значению
            self.update()

        def on_change_activity(e):
            activity_input.data = e.control.value
            self.update()

        def write_down(event, start_time, end_time, total_time):
            try:
                with open(f"{todaysDate}.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = {}

            file_path = os.path.join(folder_path, f"{todaysDate}.json")
            start_time_str = start_time.strftime('%H:%M:%S') if start_time else "Not recorded"
            end_time_str = end_time.strftime('%H:%M:%S') if end_time else "Not recorded"

            data[event] = {
                "start_time": start_time_str,
                "end_time": end_time_str,
                "duration": str(total_time)
            }

            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                self.page.open(ft.SnackBar(ft.Text(f"Успішно занесено у {todaysDate}.json!"), bgcolor=ft.colors.GREEN_ACCENT))
            except Exception as e:
                print(f"Error writing to file: {e}")
                self.page.open(ft.SnackBar(ft.Text("Виникла проблема"), bgcolor=ft.colors.RED_ACCENT))

        content = ft.Column([
            ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color=get_time_based_color(),
                    on_click=lambda e: show_page("home", self.page)
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
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(
                content=ft.ElevatedButton(
                    text="Додати",
                    color=get_time_based_color(),
                    on_click=lambda e: write_down(activity_input.data, self.start_time, self.end_time, record_label.value)
                ),
                alignment=ft.alignment.center
            )
        ])
        return ft.Column([content], expand=True)
