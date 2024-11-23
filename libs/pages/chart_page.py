import flet as ft, os, json
import matplotlib.pyplot as plt

from datetime import timedelta
from flet.matplotlib_chart import MatplotlibChart 
from libs.components.Back import BackToHome

def chart_page(page: ft.Page) -> ft.View:
    from utils import get_time_based_color, load_config

    config = load_config()
    folder_path = config.get("folder_path")

    selected_file = None 

    def load_files():
        try:
            files = os.listdir(folder_path)
            files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
            return [ft.dropdown.Option(f) for f in files]
        except Exception as e:
            print(f"Ошибка загрузки файлов: {e}")
            return []

    def on_file_selected(e):
        selected_file = os.path.join(folder_path, e.control.value)  # Сохраняем полный путь к выбранному файлу
        if selected_file:
            page.snack_bar = ft.SnackBar(ft.Text(f"Вы выбрали: {selected_file}"))
            page.snack_bar.open = True
            page.update()

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
        if not selected_file:
            print("Файл не выбран.")
            return

        data = load_activity_data(selected_file)

        # Подготовка данных для графика
        activity_names = []
        activity_durations = []

        for activity, times in data.items():
            activity_names.append(activity)
            duration = parse_duration(times["duration"])
            activity_durations.append(duration.total_seconds())

        fig = plt.figure(figsize=(8, 8))
        plt.pie(activity_durations, labels=activity_names, autopct='%1.1f%%', startangle=140)
        plt.title("Распределение активности за день")

        chart = MatplotlibChart(fig, expand=True)
        page.controls.append(chart)
        page.update()

    navigator = BackToHome("Вивести графік", page)

    return ft.View(
        route="/analyze",
        controls=[
            navigator.add(),
            ft.Container(
                ft.Dropdown(
                    options=load_files(),
                    on_change=on_file_selected,
                    hint_text="Виберіть файл",
                    width=200,
                    height=35,
                    border_color=get_time_based_color(),
                    text_style=ft.alignment.center
                ),
                alignment=ft.alignment.center,
            ),
            ft.Container(
                ft.ElevatedButton(
                    text="Вивести графік дня",
                    on_click=lambda _: plotting(),
                    color=get_time_based_color()
                ),
                alignment=ft.alignment.center
            )
        ])
