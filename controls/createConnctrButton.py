import flet as ft
import os
from .appFunctions import (
    check_podman_machine_exists,
    check_container_image,
    init_and_start_machine,
    build_container,
)
from .KeyValueStore import KeyValueStore
from time import sleep

headingColor = ft.colors.DEEP_PURPLE_300
bodyColor = ft.colors.with_opacity(1, color=ft.colors.GREY_200)
fontSizeVal = 12

userPath = os.path.expanduser('~')
dir_path = userPath + "/.lucidlinkFrameIOapp"
db_file_path = f"{dir_path}/app.db"

kv_store = KeyValueStore()

def create_container(e, mount_path, createConn_progress_ind, configCol, stream_logs_callback, update_button_states):
    try:
        init_and_start_machine(e, mount_path, createConn_progress_ind, stream_logs_callback)
        while not check_podman_machine_exists():
            sleep(1)
        build_container(e, createConn_progress_ind, stream_logs_callback)
        while not check_container_image():
            sleep(1)
        kv_store.set("connector_created", "True")
        stream_logs_callback("INFO:     Connector created successfully.")
        update_button_states()  # Call the update_button_states function
        configCol.update_connector_status()
        e.page.update()
    except Exception as e:
        stream_logs_callback(f"ERROR:    {str(e)}")
    
def create_container_button(mount_path, createConn_progress_ind, configCol, stream_logs_callback, update_button_states):
    return ft.Container(
        width=150,
        content=ft.Row(
            [
                ft.OutlinedButton(
                    width=150,
                    style=ft.ButtonStyle(
                        side={
                            ft.MaterialState.DEFAULT: ft.BorderSide(
                                2, ft.colors.with_opacity(0.4, headingColor)
                            ),
                            ft.MaterialState.HOVERED: ft.BorderSide(2, headingColor),
                        },
                    ),
                    content=ft.Row(
                        [
                            ft.Text(
                                "Create connector", size=fontSizeVal, color=bodyColor
                            ),
                        ],
                        tight=True,
                    ),
                    on_click=lambda _: create_container(_, mount_path, createConn_progress_ind, configCol, stream_logs_callback, update_button_states),
                ),
            ],
        ),
    )