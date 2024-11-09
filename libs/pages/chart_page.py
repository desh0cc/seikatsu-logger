import flet as ft, os, json
import matplotlib.pyplot as plt

from datetime import timedelta
from flet.matplotlib_chart import MatplotlibChart 

from utils import *

class ChartPage(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.selected_file = None  # Инициализация selected_file как None

    def build(self):
        from utils import get_time_based_color, folder_path, show_page

        def load_files():
            try:
                # Получаем список файлов в папке
                files = os.listdir(folder_path)
                # Фильтруем, чтобы отображать только файлы (не папки)
                files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
                # Создаем элементы для Dropdown
                return [ft.dropdown.Option(f) for f in files]
            except Exception as e:
                print(f"Ошибка загрузки файлов: {e}")
                return []

        def on_file_selected(e):
            self.selected_file = os.path.join(folder_path, e.control.value)  # Сохраняем полный путь к выбранному файлу
            if self.selected_file:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Вы выбрали: {self.selected_file}"))
                self.page.snack_bar.open = True
                self.page.update()

        def load_activity_data(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data
            except Exception as e:
                print(f"Ошибка загрузки данных: {e}")
                return {}

        def parse_duration(duration_str):
            h, m, s = map(int, duration_str.split(":"))
            return timedelta(hours=h, minutes=m, seconds=s)

        def plotting():
            if not self.selected_file:
                print("Файл не выбран.")
                return

            data = load_activity_data(self.selected_file)

            # Подготовка данных для графика
            activity_names = []
            activity_durations = []

            for activity, times in data.items():
                activity_names.append(activity)
                duration = parse_duration(times["duration"])
                activity_durations.append(duration.total_seconds())

            # Создание круговой диаграммы
            fig = plt.figure(figsize=(8, 8))
            plt.pie(activity_durations, labels=activity_names, autopct='%1.1f%%', startangle=140)
            plt.title("Распределение активности за день")

            # Используем MatplotlibChart для отображения графика в Flet
            chart = MatplotlibChart(fig, expand=True)
            self.page.controls.append(chart)
            self.page.update()

        return ft.Column([
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
                    "Вивести графік",
                    color=get_time_based_color(),
                    font_family="Helvetica",
                    weight=ft.FontWeight.BOLD,
                    size=20
                ),
                alignment=ft.alignment.top_center,
                padding=ft.padding.only(top=-45)
            ),
            ft.Container(
                ft.Dropdown(
                    options=load_files(),
                    on_change=on_file_selected,
                    hint_text="Виберіть файл"
                )
            ),
            ft.Container(
                ft.ElevatedButton(
                    "Вивести графік дня",
                    on_click=lambda _: plotting()
                )
            )
        ])
