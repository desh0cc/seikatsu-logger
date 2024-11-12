import flet as ft, json, os
from datetime import datetime

class EditPage(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

    def build(self):
        from utils import get_time_based_color, show_page, load_log, folder_path

        def handle_name_change(e):
            new_name.value = f"Нова назва: {e.control.value}"
            new_name.data = e.control.value
            self.update()

        def handle_sTime_change(e):
            start_time.value = f"Новий початковий час: {e.control.value}"
            start_time.data = e.control.value
            self.update()

        def handle_eTime_change(e):
            end_time.value = f"Новий кінцевий час: {e.control.value}"
            end_time.data = e.control.value
            self.update()

        def handle_file_change(e):
            picked_file.value = f"Вибраний файл: {e.control.value}"
            picked_file.data = e.control.value
            # Update activity dropdown options based on selected file
            activity_dropdown.options = act_loading()
            self.update()

        def handle_act_change(e):
            picked_act.value = f"Вибрана активність {e.control.value}"
            picked_act.data = e.control.value
            self.update()

        def file_loading():
            try:
                files = os.listdir(folder_path)
                files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
                return [ft.dropdown.Option(f) for f in files]
            except Exception as e:
                print(f"Ошибка загрузки файлов: {e}")
                return []

        def act_loading():
            if not picked_file.data:
                return []  # No file selected yet
            data = load_log(picked_file.data)
            return [ft.dropdown.Option(activity) for activity in data.keys()]

        def to_redact(file, activity, start_time=None, end_time=None, new_name=None):
            data = load_log(file)

            start_time = str(start_time)
            end_time = str(end_time)

            if activity in data:
                if new_name:
                    data[new_name] = data.pop(activity)
                    activity = new_name
                if start_time:
                    data[activity]["start_time"] = start_time
                if end_time:
                    data[activity]["end_time"] = end_time
                if start_time or end_time:
                    data[activity]["duration"] = str(
                        datetime.strptime(end_time, "%H:%M:%S") - datetime.strptime(start_time, "%H:%M:%S")
                    )

                with open(f"{folder_path}\\{file}", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                    self.page.open(ft.SnackBar(content=ft.Text(f"Результат успішно занесено у {file}"), bgcolor=ft.colors.GREEN_ACCENT))
                    print("Успіх!!!!!")
            else:
                self.page.open(ft.SnackBar(content=ft.Text("error lmao loser"), bgcolor=ft.colors.RED_ACCENT))

        picked_file = ft.Text("")
        picked_act = ft.Text("")

        new_name = ft.Text("")
        start_time = ft.Text("")
        end_time = ft.Text("")

        activity_dropdown = ft.Dropdown(
            options=act_loading(),
            on_change=handle_act_change,
            border_color=get_time_based_color(),
            width=180,  
            border_radius=10,
            bgcolor=ft.colors.GREY_800,
            hint_text="Виберіть файл",
            hint_style=ft.TextStyle(
                color=ft.colors.GREY_500,
                size=14
            ),
            content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
            focused_bgcolor=ft.colors.GREY_700,
        )

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
                    "Редагувати лог",
                    color=get_time_based_color(),
                    font_family="Helvetica",
                    weight=ft.FontWeight.BOLD,
                    size=20
                ),
                alignment=ft.alignment.top_center,
                padding=ft.padding.only(top=-45)
            ),

            ft.Column([
                ft.Text("Виберіть файл логу:"),
                ft.Container(ft.Dropdown(
                    options=file_loading(),
                    on_change=handle_file_change,
                    width=180,  
                    border_color=get_time_based_color(),
                    border_radius=10,
                    bgcolor=ft.colors.GREY_800,
                    hint_text="Виберіть файл",
                    hint_style=ft.TextStyle(
                        color=ft.colors.GREY_500,
                        size=14
                    ),
                    content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
                    focused_bgcolor=ft.colors.GREY_700,
                ), picked_file, alignment=ft.alignment.center,)],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),


            ft.Column([ft.Text("Виберіть активність для ред.:"), ft.Container(activity_dropdown,picked_act,alignment=ft.alignment.center)], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), 

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
                        on_change=handle_name_change
                    ), alignment=ft.alignment.center),
                    new_name
                ])
            ),

            ft.Container(
                content=ft.Column([
                    ft.Container(ft.Text("Вкажіть новий час початку:", size=16), alignment=ft.alignment.center),
                    ft.Container(ft.ElevatedButton(
                        text="Вибрати час", color=get_time_based_color(),
                        icon=ft.icons.ACCESS_TIME,
                        icon_color=get_time_based_color(),
                        on_click=lambda e: self.page.open(
                            ft.TimePicker(on_change=handle_sTime_change)
                        ),
                    ), alignment=ft.alignment.center),
                    start_time
                ]),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=-12)
            ),

            ft.Container(
                content=ft.Column([
                    ft.Container(ft.Text("Вкажіть новий час закінчення:", size=16), alignment=ft.alignment.center),
                    ft.Container(ft.ElevatedButton(
                        text="Вибрати час", color=get_time_based_color(),
                        icon=ft.icons.ACCESS_TIME,
                        icon_color=get_time_based_color(),
                        on_click=lambda e: self.page.open(
                            ft.TimePicker(on_change=handle_eTime_change)
                        ),
                    ), alignment=ft.alignment.center),
                    end_time
                ]),
                padding=ft.padding.only(top=-12)
            ),

            # Edit button
            ft.Container(
                content=ft.ElevatedButton(
                    text="Редагувати",
                    color=get_time_based_color(),
                    on_click=lambda _: to_redact(picked_file.data, picked_act.data, start_time.data, end_time.data, new_name.data)
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=-5)
            )
        ])
        return ft.Column([content], expand=True)
