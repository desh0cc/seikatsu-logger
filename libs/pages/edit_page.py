import flet as ft, json, os
from datetime import datetime
from libs.components.NavigationComp import BackToHome

def edit_page(page: ft.Page):
    from utils import get_time_based_color, load_log, load_config, lang_load, if_intersect, duration_to_seconds

    config = load_config()
    folder_path = config.get("folder_path")

    act_data = []

    page_num = 1
    picked_act = ft.Text("")
    picked_file = ft.Text("")

    def file_loading():
        try:
            logs_path = os.path.join(folder_path, "logs")
            files = os.listdir(logs_path)
            files = [f for f in files if os.path.isfile(os.path.join(logs_path, f))]
            return [ft.dropdown.Option(f) for f in files]
        except Exception as e:
            print(f"Помилка: {e}")
            return []

    def act_loading():
        if not picked_file.data:
            return []
        data = load_log(picked_file.data)
        return [ft.dropdown.Option(activity) for activity in data.keys()]
    
    def handle_act_change(e):
        picked_act.data = e.control.value
        page.update()

    def handle_file_change(e):
        picked_file.data = e.control.value
        activity_dropdown.options = act_loading()
        page.update()

    def load_act_data():
        nonlocal act_data
        act_data.clear()

        data = load_log(picked_file.data)
        data = data[picked_act.data]

        for times in data.values():
            act_data.append(times)
        
    def to_redact(file, activity, start_time=None, end_time=None, new_name=None):
        data = load_log(file)

        if not if_intersect(start_time, end_time, data):
            pass
        else:
            page.open(ft.SnackBar(ft.Text("Час не має пересікатися з іншими активностями"), bgcolor=ft.Colors.RED_ACCENT))
            return

        if activity not in data:
            page.open(ft.SnackBar(ft.Text(lang_load("edit_page_error_activity_not_found")), bgcolor=ft.Colors.RED_ACCENT))
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
                if duration_to_seconds(str(duration)) <= 0:
                    raise ValueError
                data[activity]["duration"] = str(duration)
            except Exception as e:
                page.open(ft.SnackBar(ft.Text(f"Помилка: {e}"), bgcolor=ft.Colors.RED_ACCENT))
                print(e)
                return

        with open(f"{folder_path}\\logs\\{file}", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        page.open(ft.SnackBar(ft.Text(lang_load("edit_page_success_message", file=picked_file.data)), bgcolor=ft.Colors.GREEN_ACCENT))

    def to_delete(file, activity):
        data = load_log(file)
        
        if activity in data:
            data.pop(activity)
            
            with open(f"{folder_path}\\logs\\{file}", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            page.open(ft.SnackBar(ft.Text(lang_load("edit_page_delete_success", activity=picked_act.data, file=picked_file.data)), bgcolor=ft.Colors.GREEN_ACCENT))
        else:
            page.open(ft.SnackBar(ft.Text("Error"), bgcolor=ft.Colors.RED_ACCENT))

    def refresh_components():
        file_dropdown.options = file_loading()
        activity_dropdown.options = act_loading()
        page.update()


    file_dropdown = ft.Dropdown(
                options=file_loading(),
                on_change=handle_file_change,
                width=180,  
                border_color=get_time_based_color(),
                border_radius=10,
                hint_style=ft.TextStyle(
                    color=ft.Colors.GREY_500,
                    size=14,
                ),
                content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
                focused_bgcolor=ft.Colors.GREY_700,
                animate_offset=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                animate_opacity=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT)
            )

    activity_dropdown = ft.Dropdown(
        options=act_loading(),
        on_change=handle_act_change,
        border_color=get_time_based_color(),
        width=180,  
        border_radius=10,
        text_style=ft.TextStyle(
            overflow=ft.TextOverflow.ELLIPSIS
        ),
        hint_style=ft.TextStyle(
            color=ft.Colors.GREY_500,
            size=14
        ),
        content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
        animate_offset=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
        animate_opacity=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT)
    )

    def confirm_action():
        nonlocal page_num
        if page_num == 1:
            elements.controls[0], elements.controls[1] = elements.controls[1], elements.controls[0]

            back_btn.opacity = 1.0
            back_btn.disabled = False

            file_dropdown.opacity = 0.0
            file_dropdown.disabled = True

            activity_dropdown.opacity = 1.0
            activity_dropdown.disabled = False

            top_title.value = lang_load("edit_page_toptitle_2")

            page_num = 2
        elif page_num == 2:
            load_act_data()

            activity_name_display.value = f"{picked_act.data}"
            activity_start_time.value = f"{act_data[0]}"
            activity_end_time.value = f"{act_data[1]}"

        page.update()

    def back_action():
        nonlocal page_num

        elements.controls[0], elements.controls[1] = elements.controls[1], elements.controls[0]
        page_num = 1

        back_btn.opacity = 0.0
        back_btn.disabled = True

        file_dropdown.opacity = 1.0
        file_dropdown.disabled = False

        activity_dropdown.opacity = 0.0
        activity_dropdown.disabled = True

        top_title.value = lang_load("edit_page_toptitle_1")

        page.update()

    confirm_btn = ft.IconButton(
        icon=ft.Icons.CHECK,
        icon_color=get_time_based_color(),
        on_click=lambda _: confirm_action()
    )

    back_btn = ft.IconButton(
        icon=ft.Icons.ARROW_BACK_ROUNDED,
        icon_color=get_time_based_color(),
        opacity=0.0,
        disabled=True,
        animate_offset=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
        animate_opacity=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
        on_click=lambda _: back_action()
    )

    elements = ft.Stack([
        activity_dropdown,
        file_dropdown
    ])

    activity_name_display = ft.Text("")
    activity_start_time = ft.Text("")
    activity_end_time = ft.Text("")

    def handle_close(dialog):
        def close_event(e):
            page.close(dialog)
        return close_event

    edit_name_dialog = ft.AlertDialog(
        title=ft.Text(lang_load("edit_page_edit_name")),
        content=ft.TextField(
            border_color=get_time_based_color(),
            border_radius=10,
            cursor_color=get_time_based_color()
        ),
        actions=[
            ft.ElevatedButton(text=lang_load("edit_page_cancel_btn"), color=get_time_based_color(), on_click=lambda e: handle_close(edit_name_dialog)(e)),
            ft.ElevatedButton(text=lang_load("edit_page_save_btn"),color=get_time_based_color(), on_click=lambda _: save_name_changes()),
        ],
    )

    edit_start_dialog = ft.AlertDialog(
        title=ft.Text(lang_load("edit_page_edit_st")),
        content=ft.TextField(
            border_color=get_time_based_color(),
            border_radius=10,
            cursor_color=get_time_based_color()
        ),
        actions=[
            ft.ElevatedButton(text=lang_load("edit_page_cancel_btn"), color=get_time_based_color(), on_click=lambda e: handle_close(edit_start_dialog)(e)),
            ft.ElevatedButton(text=lang_load("edit_page_save_btn"),color=get_time_based_color(), on_click=lambda _: save_start_changes()),
        ],
    )

    edit_end_dialog = ft.AlertDialog(
        title=ft.Text(lang_load("edit_page_edit_et")),
        content=ft.TextField(
            border_color=get_time_based_color(),
            border_radius=10,
            cursor_color=get_time_based_color(),
        ),
        actions=[
            ft.ElevatedButton(text=lang_load("edit_page_cancel_btn"), color=get_time_based_color(), on_click=lambda e: handle_close(edit_end_dialog)(e)),
            ft.ElevatedButton(text=lang_load("edit_page_save_btn"),color=get_time_based_color(), on_click=lambda _: save_end_changes()),
        ],
    )

    def save_name_changes():
        activity_name_display.value = edit_name_dialog.content.value
        page.close(edit_name_dialog)
        page.update()

    def save_start_changes():
        activity_start_time.value = edit_start_dialog.content.value
        page.close(edit_start_dialog)
        page.update()

    def save_end_changes():
        activity_end_time.value = edit_end_dialog.content.value
        page.close(edit_end_dialog)
        page.update()

    navigator = BackToHome(lang_load("edit_page_title"), page)

    top_title = ft.Text(lang_load("edit_page_toptitle_1"), size=15, font_family="CaskaydiaCove", weight=ft.FontWeight.W_500, animate_offset=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                animate_opacity=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT))

    return ft.Column([
        navigator.add(),

        ft.Container(
            ft.Column(
                [
                    ft.Row([
                        back_btn,
                        ft.Container(expand=True),
                        top_title,
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK_ROUNDED,
                            opacity=0,
                            disabled=True,
                        )
                    ]),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ABC,
                            disabled=True,
                            opacity=0.0
                        ),
                        elements,
                        confirm_btn
                    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                ]
            ),
            bgcolor=ft.Colors.with_opacity(0.4, "#333333"),
            border_radius=15,
            padding=ft.padding.only(bottom=10)
        ),
        ft.Container(
            ft.Column([
                ft.Container(
                    ft.Row([
                        ft.Container(
                            ft.Text(lang_load("edit_page_activity_name")),
                        ),
                        ft.Container(
                            activity_name_display,
                            alignment=ft.alignment.center_right,
                            expand=1
                        ),
                        ft.Container(
                            ft.ElevatedButton(
                                height=64,
                                width=64,
                                content=ft.Icon(ft.Icons.EDIT_ROUNDED, color=get_time_based_color()),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                on_click=lambda _: page.open(edit_name_dialog)
                            )
                        )
                    ]),
                    padding=ft.padding.all(7),
                    border_radius=10,
                    bgcolor=ft.Colors.with_opacity(0.4, "#444444")
                ),
                ft.Container(
                    ft.Row([
                        ft.Container(
                            ft.Text(lang_load("edit_page_start_time")),
                        ),
                        ft.Container(
                            activity_start_time,
                            alignment=ft.alignment.center_right,
                            expand=1
                        ),
                        ft.Container(
                            ft.ElevatedButton(
                                height=64,
                                width=64,
                                content=ft.Icon(ft.Icons.EDIT_ROUNDED, color=get_time_based_color()),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                on_click=lambda _: page.open(edit_start_dialog)
                            )
                        )
                    ]),
                    padding=ft.padding.all(7),
                    border_radius=10,
                    bgcolor=ft.Colors.with_opacity(0.4, "#444444")
                ),
                ft.Container(
                    ft.Row([
                        ft.Container(
                            ft.Text(lang_load("edit_page_end_time")),
                        ),
                        ft.Container(
                            activity_end_time,
                            alignment=ft.alignment.center_right,
                            expand=1
                        ),
                        ft.Container(
                            ft.ElevatedButton(
                                height=64,
                                width=64,
                                content=ft.Icon(ft.Icons.EDIT_ROUNDED, color=get_time_based_color()),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                on_click=lambda _: page.open(edit_end_dialog)
                            )
                        )
                    ]),
                    padding=ft.padding.all(7),
                    border_radius=10,
                    bgcolor=ft.Colors.with_opacity(0.4, "#444444")
                ),
                ft.Container(expand=True, margin=ft.margin.only(bottom=15)),
                ft.Container(
                    ft.Row([
                        ft.ElevatedButton(
                            text=lang_load("edit_page_refresh_btn"),
                            icon=ft.Icons.REFRESH_ROUNDED,
                            icon_color=ft.Colors.YELLOW_ACCENT,
                            color=ft.Colors.YELLOW_ACCENT,
                            on_click=lambda _: refresh_components()
                        ),
                        ft.ElevatedButton(
                            text=lang_load("edit_page_save_btn"),
                            icon=ft.Icons.SAVE_ROUNDED,
                            icon_color=get_time_based_color(),
                            color=get_time_based_color(),
                            on_click=lambda _: to_redact(
                                file=picked_file.data,
                                activity=picked_act.data,
                                new_name=activity_name_display.value, 
                                start_time=activity_start_time.value,
                                end_time=activity_end_time.value
                            )
                        ),
                        ft.ElevatedButton(
                            text=lang_load("edit_page_delete_btn"),
                            icon=ft.Icons.DELETE_ROUNDED,
                            icon_color=ft.Colors.RED_ACCENT,
                            color=ft.Colors.RED_ACCENT,
                            on_click=lambda _: to_delete(picked_file.data, picked_act.data)
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.END),
                    padding=ft.padding.only(bottom=10)
                ),
            ]),
            border_radius=15,
            padding=ft.padding.all(5),
            expand=True
        )
    ])