import flet as ft, json, os
from datetime import datetime
from libs.components.Back import BackToHome

def edit_page(page: ft.Page):
    from utils import get_time_based_color, load_log, folder_path

    def handle_name_change(e):
        new_name.data = e.control.value
        page.update()

    def handle_sTime_change(e):
        start_time.value = f"Новий початковий час: {e.control.value}"
        start_time.data = e.control.value
        page.update()

    def handle_eTime_change(e):
        end_time.value = f"Новий кінцевий час: {e.control.value}"
        end_time.data = e.control.value
        page.update()

    def handle_file_change(e):
        picked_file.value = f"Вибраний файл: {e.control.value}"
        picked_file.data = e.control.value
        activity_dropdown.options = act_loading()
        page.update()

    def handle_act_change(e):
        picked_act.value = f"Вибрана активність {e.control.value}"
        picked_act.data = e.control.value
        page.update()

    def file_loading():
        try:
            files = os.listdir(folder_path)
            files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
            return [ft.dropdown.Option(f) for f in files]
        except Exception as e:
            print(f"Помилка: {e}")
            return []

    def act_loading():
        if not picked_file.data:
            return []
        data = load_log(picked_file.data)
        return [ft.dropdown.Option(activity) for activity in data.keys()]
    
    def parse_time(time: str):
        return list(map(int, time.split(":")))
    
    def if_intersect(file, start_time, end_time):
        data = load_log(picked_file.data)
        for activity, time in data.items():
            time = parse_time(time)
        return False

    def to_redact(file, activity, start_time=None, end_time=None, new_name=None):
        data = load_log(file)

        if activity not in data:
            page.open(ft.SnackBar(ft.Text("Такої активності не знайдено"), bgcolor=ft.colors.RED_ACCENT))
            return
        if new_name and new_name != activity:
            data[new_name] = data.pop(activity)
            activity = new_name
        if start_time:
            data[activity]["start_time"] = str(start_time)
        if end_time:
            data[activity]["end_time"] = str(end_time)

        current_start = data[activity].get("start_time")
        current_end = data[activity].get("end_time")

        if current_start and current_end:
            try:
                duration = datetime.strptime(current_end, "%H:%M:%S") - datetime.strptime(current_start, "%H:%M:%S")
                data[activity]["duration"] = str(duration)
            except Exception as e:
                page.open(ft.SnackBar(ft.Text(f"Помилка: {e}"), bgcolor=ft.colors.RED_ACCENT))
                return

        with open(f"{folder_path}\\{file}", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        page.open(ft.SnackBar(ft.Text(f"Успішно записано у: {file}"), bgcolor=ft.colors.GREEN_ACCENT))
        print("є крутяк")

    def to_delete(file, activity):
        data = load_log(file)
        
        if activity in data:
            data.pop(activity)
            
            with open(f"{folder_path}\\{file}", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            page.open(ft.SnackBar(ft.Text(f"Активність '{activity}' Була видалена з {file}"), bgcolor=ft.colors.GREEN_ACCENT))
        else:
            page.open(ft.SnackBar(ft.Text("Активність не знайдена"), bgcolor=ft.colors.RED_ACCENT))

    def refresh_components():
        file_dropdown.options = file_loading()
        activity_dropdown.options = act_loading()
        page.update()

    picked_file = ft.Text("")
    picked_act = ft.Text("")

    new_name = ft.Text("")
    start_time = ft.Text("")
    end_time = ft.Text("")

    file_dropdown = ft.Dropdown(
                options=file_loading(),
                on_change=handle_file_change,
                width=180,  
                border_color=get_time_based_color(),
                border_radius=10,
                hint_text="Виберіть файл",
                hint_style=ft.TextStyle(
                    color=ft.colors.GREY_500,
                    size=14,
                ),
                content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
                focused_bgcolor=ft.colors.GREY_700,
            )

    activity_dropdown = ft.Dropdown(
        options=act_loading(),
        on_change=handle_act_change,
        border_color=get_time_based_color(),
        width=300,  
        border_radius=10,
        hint_text="Виберіть файл",
        hint_style=ft.TextStyle(
            color=ft.colors.GREY_500,
            size=14
        ),
        content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
    )

    navigator = BackToHome("Редагувати лог", page)

    content = ft.Column([
        navigator.add(),
        ft.Column([ft.Text("Виберіть файл логу:"), ft.Container(file_dropdown, picked_file,alignment=ft.alignment.center)], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
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
                    on_click=lambda e: page.open(
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
                    on_click=lambda e: page.open(
                        ft.TimePicker(on_change=handle_eTime_change)
                    ),
                ), alignment=ft.alignment.center),
                end_time
            ]),
            padding=ft.padding.only(top=-12)
        ),

        ft.Container(
            ft.Row([
                ft.Container(
                    ft.ElevatedButton(
                        text="Редагувати",
                        color=get_time_based_color(),
                        on_click=lambda _: to_redact(picked_file.data, picked_act.data, start_time.data, end_time.data, new_name.data)
                    ),
                    padding=ft.padding.only(left=150)
                ),
                ft.Container(
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_color=ft.colors.RED_ACCENT,
                            alignment=ft.alignment.center,
                            on_click=lambda _: to_delete(picked_file.data, picked_act.data)
                        ),
                        alignment=ft.alignment.bottom_right,
                        padding=ft.padding.only(left=50)
                    ),
                ft.Container(
                        ft.IconButton(
                            icon=ft.icons.REFRESH_ROUNDED,
                            icon_color=ft.colors.GREEN_ACCENT,
                            alignment=ft.alignment.center,
                            on_click=lambda _: refresh_components()
                        ),
                        alignment=ft.alignment.bottom_right,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=-10)
        )
    ])
    return ft.Column([content], expand=True)