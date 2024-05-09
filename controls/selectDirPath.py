import flet as ft

headingColor = ft.colors.DEEP_PURPLE_300
bodyColor = ft.colors.with_opacity(1, color=ft.colors.GREY_200)
fontSizeVal = 12

def get_directory_result(e: ft.FilePickerResultEvent, kv_store, update_button_states):
    global workflowPath
    if e.path:
        path = e.path
        slashPath = path + "/"
        workflowPath.value = slashPath
        kv_store.set("filepath", slashPath)
        save_path = path.replace("/Volumes", "")
        kv_store.set("save_path", save_path)
        workflowPath.update()
        kv_store.close()
        update_button_states()  # Call update_button_states() after directory selection
    else:
        workflowPath.value = "Cancelled!"
        workflowPath.update()

def create_select_dir_cntr(kv_store, page, get_directory_dialog):
    global workflowPath
    workflowPath = ft.TextField(
        content_padding=15,
        bgcolor=ft.colors.with_opacity(0.2, ft.colors.BLACK),
        label="LucidLink filepath",
        label_style=ft.TextStyle(color=headingColor, size=fontSizeVal),
        value=kv_store.get("filepath"),
        cursor_color=bodyColor,
        selection_color=headingColor,
        width=690,
        height=60,
        dense=True,
        color=bodyColor,
        text_size=12,
        multiline=True,
        border_color=ft.colors.with_opacity(0.4, headingColor),
        border_radius=6,
        border_width=1,
        focused_border_width=2,
        focused_border_color=headingColor,
        # on_change=workflowPath_changed
    )
    kv_store.set("filepath", workflowPath.value)

    selectDirCntr = ft.Container(
        padding=ft.padding.all(20),
        content=ft.Column(
            width=690,
            spacing=0,
            tight=True,
            controls=[
                ft.Container(
                    margin=ft.margin.only(top=10),
                    content=workflowPath,
                ),
            ],
        ),
    )

    page.overlay.append(get_directory_dialog)

    return selectDirCntr

def get_directory_dialog(kv_store, update_button_states):
    return ft.FilePicker(on_result=lambda e: get_directory_result(e, kv_store, update_button_states))