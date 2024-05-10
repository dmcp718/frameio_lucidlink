import asyncio
import json
import os
import subprocess
from threading import Semaphore, Thread

import flet as ft
import requests

from controls.appFunctions import (
    check_container_image,
    check_podman_installed,
)
from controls.configCol import ConfigCol
from controls.createConnctrButton import create_container, create_container_button
from controls.exit_app import create_exit_app_button
from controls.fioAccountID import getAccountID
from controls.fioAccountName import getAccountName
from controls.fioWebhooks import getWebhooks
from controls.frameIOtable import create_fio_info_col
from controls.KeyValueStore import KeyValueStore
from controls.ngrokTunnelContainer import ngrokTunnelCntnr
from controls.selectConnName import create_conn_name_cntnr
from controls.selectDirPath import create_select_dir_cntr, get_directory_dialog
from controls.token_manager import TokenManager
from controls.topBanner import top_Banner

headingColor = ft.colors.DEEP_PURPLE_300
bodyColor = ft.colors.with_opacity(1, color=ft.colors.GREY_200)
logoColor = "#b3fb1e"
fontSizeVal = 12

user_path = os.path.expanduser("~")
dir_path = os.path.join(user_path, ".lucidlinkFrameIOapp")

kv_store = KeyValueStore()

log_thread = None
portVal = 8000


# State class for tracking messages scrolling
class State:
    i = 0


s = State()
sem = Semaphore()


def createDB():
    global kv_store

    # Define the app_list with default values
    app_list = [
        ("nTokn", None),
        ("fTokn", None),
        ("selected_webhook", None),
        ("connector_name", "lucidlink_connector_01"),
        ("connector_created", False),
        ("filepath", None),
        ("save_path", None),
        ("port", 8000),
        ("frameio_account_name", None),
        ("frameio_account_id", None),
        ("webhook_id", None),
        ("webhook_name", None),
        ("webhook_url", None),
        ("webhook_url_updated", False),
    ]

    # Iterate over the app_list
    for key, default_value in app_list:
        # Check if the key exists in the database
        existing_value = kv_store.get(key)

        if existing_value is None:
            # Key doesn't exist, set the default value
            kv_store.set(key, default_value)
        else:
            # Key exists, check if the existing value is None
            if existing_value is None:
                # Existing value is None, set the default value
                kv_store.set(key, default_value)
            else:
                pass

    kv_store.close()


accountName = kv_store.get("frameio_account_name")
if accountName is None:
    accountName = getAccountName(kv_store)
    kv_store.set("frameio_account_name", accountName)
    kv_store.close()
accountID = kv_store.get("frameio_account_id")
if accountID is None:
    accountID = getAccountID(kv_store)
    kv_store.set("frameio_account_id", accountID)
    kv_store.close()

webhooks = getWebhooks(kv_store, accountID)
if webhooks:
    selected_webhook = kv_store.get("selected_webhook")
    if selected_webhook is None or selected_webhook not in webhooks:
        selected_webhook = webhooks[0]
        kv_store.set("selected_webhook", selected_webhook)
        kv_store.set("webhook_name", selected_webhook)

        # Retrieve the webhook ID based on the selected webhook name
        userPath = os.path.expanduser("~")
        wh_path = userPath + "/.lucidlinkFrameIOapp/webhooks.json"
        with open(wh_path, "r") as file:
            webhooksKV = json.load(file)
        webhook_id = webhooksKV.get(selected_webhook)
        kv_store.set("webhook_id", webhook_id)
        kv_store.close()
    else:
        # Retrieve the webhook ID based on the selected webhook name
        userPath = os.path.expanduser("~")
        wh_path = userPath + "/.lucidlinkFrameIOapp/webhooks.json"
        with open(wh_path, "r") as file:
            webhooksKV = json.load(file)
        webhook_id = webhooksKV.get(selected_webhook)
        kv_store.set("webhook_id", webhook_id)
        kv_store.set("webhook_name", selected_webhook)
        kv_store.close()
else:
    kv_store.set("selected_webhook", None)
    kv_store.set("webhook_id", None)
    kv_store.set("webhook_name", None)
    kv_store.close()

mount_path = kv_store.get("save_path")
print(f"mount_path: {mount_path}")


def on_scroll(e: ft.OnScrollEvent):
    if e.pixels >= e.max_scroll_extent - 100:
        if sem.acquire(blocking=False):
            try:
                consoleCol.update()
            finally:
                sem.release()


consoleCol = ft.Column(
    alignment=ft.MainAxisAlignment.START,
    horizontal_alignment=ft.CrossAxisAlignment.START,
    spacing=0,
    tight=True,
    scroll=ft.ScrollMode.ALWAYS,
    auto_scroll=True,
    on_scroll_interval=0,
    on_scroll=on_scroll,
)


def main(page: ft.Page):
    global \
        accountName, \
        accountID, \
        bodyColor, \
        headingColor, \
        fontSizeVal, \
        webhooks, \
        kv_store, \
        consoleCol, \
        sem, \
        log_thread, \
        portVal

    createDB()
    exit_button = create_exit_app_button()

    configCol = ConfigCol(kv_store, page)
    configCol.update_nToken_status()
    configCol.update_fToken_status()
    configCol.update_podman_status()
    configCol.check_connector_status()

    topBanner = top_Banner()
    page.dark_theme = ft.Theme(color_scheme_seed=ft.colors.DEEP_PURPLE)
    page.window_height = 918
    page.window_width = 1352

    ngrokTunnStatus = ft.Text(
        value="",
        size=10,
        color=bodyColor,
        visible=False,
    )

    def stream_logs_callback(string):
        log = string.strip()
        consoleCol.controls.append(
            ft.Text(value=f"{log}", color=bodyColor, size=10, selectable=True)
        )
        consoleCol.update()

    def update_button_states():
        podman_installed = check_podman_installed()
        container_image_exists = check_container_image()

        nTokn = kv_store.get("nTokn")
        fTokn = kv_store.get("fTokn")
        connector_name = kv_store.get("connector_name")
        filepath = kv_store.get("filepath")
        selected_webhook = kv_store.get("selected_webhook")

        btn_pMan_install.disabled = podman_installed

        if podman_installed:
            btn_create_cntnr.disabled = (
                nTokn is None
                or fTokn is None
                or selected_webhook is None
                or connector_name is None
                or filepath is None
            )

            if container_image_exists:
                btn_start_tunnel.disabled = (
                    selected_webhook is None or nTokn is None or fTokn is None
                )
                btn_stop_tunnel.disabled = not ngrokTunnStatus.visible
                btn_start_server.disabled = not ngrokTunnStatus.visible
            else:
                btn_start_tunnel.disabled = True
                btn_stop_tunnel.disabled = True
                btn_start_server.disabled = True
        else:
            btn_create_cntnr.disabled = True
            btn_start_tunnel.disabled = True
            btn_stop_tunnel.disabled = True
            btn_start_server.disabled = True

        page.update()

    async def wait_for_podman_installation():
        while not check_podman_installed():
            await asyncio.sleep(1)  # Wait for 1 second before checking again

    def download_and_install_podman(e):
        global user_path
        url = "https://github.com/containers/podman/releases/download/v5.0.2/podman-installer-macos-universal.pkg"
        filename = f"{user_path}/Downloads/podman-installer-macos-universal.pkg"
        stream_logs_callback(
            "INFO:     Downloading Podman Installer macOS Universal...\n"
        )
        response = requests.get(url)
        with open(filename, "wb") as file:
            file.write(response.content)
        os.system(f"open {filename}")
        stream_logs_callback(
            "INFO:     Podman Installer downloaded. Please launch the Installer and complete the installation.\n"
        )

        # Wait for Podman installation to complete
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(wait_for_podman_installation())
        loop.close()

        stream_logs_callback("INFO:     Podman installation completed.\n")
        configCol.update_podman_status()

    def pManInstall_button():
        return ft.Container(
            margin=ft.margin.only(top=5),
            width=235,
            content=ft.Row(
                [
                    ft.OutlinedButton(
                        width=235,
                        style=ft.ButtonStyle(
                            side={
                                ft.MaterialState.DEFAULT: ft.BorderSide(
                                    2, ft.colors.with_opacity(0.4, headingColor)
                                ),
                                ft.MaterialState.HOVERED: ft.BorderSide(
                                    2, headingColor
                                ),
                            },
                        ),
                        content=ft.Row(
                            [
                                ft.Text(
                                    "Install Podman", size=fontSizeVal, color=bodyColor
                                ),
                            ],
                            tight=True,
                        ),
                        on_click=download_and_install_podman,
                    ),
                ],
            ),
        )

    btn_pMan_install = pManInstall_button()

    token_manager = TokenManager(kv_store, headingColor, bodyColor, configCol)

    def stream_logs(e, container_name):
        global log_thread
        if log_thread is None or not log_thread.is_alive():
            log_thread = Thread(target=stream_logs_thread, args=(e, container_name))
            log_thread.start()

    def stream_logs_thread(e, container_name):
        global consoleCol
        process = subprocess.Popen(
            ["/opt/podman/bin/podman", "logs", "-f", container_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        for line in process.stdout:
            filtered_line = line.replace("root:", "     ")
            filtered_line2 = filtered_line.replace("(Press CTRL+C to quit)", "")
            if not filtered_line2.startswith("INFO:httpx:HTTP Request: GET"):
                try:
                    stream_logs_callback(filtered_line2)
                except RuntimeError:
                    break

    def start_server(
        e,
        mount_path,
        container_name,
        btn_stop_server,
        btn_start_server,
        configCol,
        ):

        global consoleCol
        btn_stop_server.visible = True
        btn_stop_server.update()

        # Remove the existing container if it exists
        remove_result = subprocess.run(
            ["/opt/podman/bin/podman", "rm", "-f", container_name],
            capture_output=True,
            text=True,
        )
        consoleCol.controls.append(
            ft.Text(
                value=f"Removing existing container: {remove_result.stdout}",
                color=bodyColor,
                size=10,
            )
        )
        consoleCol.update()
        e.page.update()

        if remove_result.returncode == 0 or "no such container" in remove_result.stderr:
            start_result = subprocess.run(
                [
                    "/opt/podman/bin/podman",
                    "run",
                    "-d",
                    "-p",
                    f"{portVal}:{portVal}",
                    "-v",
                    f"{mount_path}:{mount_path}",
                    "--name",
                    container_name,
                    "--rm",
                    "localhost/webhook-listener:latest",
                ],
                capture_output=True,
                text=True,
            )

            if start_result.returncode == 0:
                btn_stop_server.disabled = False  # Enable btn_stop_server
                btn_start_server.disabled = True  # Disable btn_start_server
                configCol.update_webhook_status()
                page.update()
            else:
                stream_logs_callback("Failed to start server:")
                stream_logs_callback(start_result.stderr)
        else:
            stream_logs_callback("Failed to remove existing container:")
            stream_logs_callback(remove_result.stderr)

        btn_stop_server.update()
        btn_start_server.update()
        btn_stop_server.visible = True  # Keep btn_stop_server visible
        btn_stop_server.update()
        stream_logs(e, container_name)

    def stop_server(container_name, btn_stop_server, btn_start_server, configCol):
        global log_thread

        btn_stop_server.visible = True
        btn_stop_server.update()

        stop_result = subprocess.run(
            ["/opt/podman/bin/podman", "stop", container_name],
            capture_output=True,
            text=True,
        )
        rm_result = subprocess.run(
            ["/opt/podman/bin/podman", "rm", container_name],
            capture_output=True,
            text=True,
        )

        if stop_result.returncode == 0 and rm_result.returncode == 0:
            btn_stop_server.disabled = True  # Disable btn_stop_server
            btn_start_server.disabled = False  # Enable btn_start_server
            configCol.update_webhook_status()
            page.update()
        else:
            stream_logs_callback("Failed to stop server:\n")
            stream_logs_callback(stop_result.stderr + "\n" + rm_result.stderr)

        btn_stop_server.update()
        btn_start_server.update()

        btn_stop_server.update()

        if log_thread is not None:
            log_thread.join()

    consoleHeading = ft.Text(
        "CONSOLE", size=12, weight=ft.FontWeight.BOLD, color=headingColor
    )

    consoleColCntnr = ft.Container(
        width=1010,
        height=190,
        padding=ft.padding.symmetric(vertical=10, horizontal=20),
        bgcolor=ft.colors.with_opacity(0.2, ft.colors.BLACK),
        # border=ft.border.all(1, headingColor),
        border_radius=6,
        content=consoleCol,
    )

    consoleHeadCol = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        controls=[
            consoleHeading,
            consoleColCntnr,
        ],
    )

    consoleHeadColCntnr = ft.Container(
        margin=ft.margin.only(left=300, top=570), content=consoleHeadCol
    )

    def create_container_callback(e):
        try:
            createConn_progress_ind.visible = True
            stream_logs_callback("INFO:     Creating container...")
            page.update()

            def create_container_thread():
                create_container(
                    e,
                    mount_path,
                    createConn_progress_ind,
                    configCol,
                    stream_logs_callback,
                    update_button_states,
                )
                createConn_progress_ind.visible = False
                page.update()

            thread = Thread(target=create_container_thread)
            thread.start()
        except Exception as e:
            stream_logs_callback(f"ERROR:    Error creating container: {str(e)}")
            createConn_progress_ind.visible = False
            page.update()

    createConn_progress_ind = ft.CupertinoActivityIndicator(
        visible=False, color=logoColor
    )
    container_name = kv_store.get("connector_name")
    btn_create_cntnr = create_container_button(
        mount_path,
        createConn_progress_ind,
        configCol,
        stream_logs_callback,
        update_button_states,
    )
    btn_create_cntnr.on_click = create_container_callback

    btn_start_server = ft.OutlinedButton(
        content=ft.Text("Start Connector", size=fontSizeVal, color=bodyColor),
        width=150,
        style=ft.ButtonStyle(
            side={
                ft.MaterialState.DEFAULT: ft.BorderSide(
                    2,
                    ft.colors.with_opacity(0.4, ft.colors.DEEP_PURPLE_300),
                ),
                ft.MaterialState.HOVERED: ft.BorderSide(
                    2,
                    ft.colors.DEEP_PURPLE_300,
                ),
            },
        ),
        on_click=lambda _: start_server(
            _,
            mount_path,
            container_name,
            btn_stop_server,
            btn_start_server,
            configCol,
        ),
    )

    btn_stop_server = ft.OutlinedButton(
        content=ft.Text("Stop Connector", size=fontSizeVal, color=bodyColor),
        width=150,
        style=ft.ButtonStyle(
            side={
                ft.MaterialState.DEFAULT: ft.BorderSide(
                    2,
                    ft.colors.with_opacity(0.4, ft.colors.DEEP_PURPLE_300),
                ),
                ft.MaterialState.HOVERED: ft.BorderSide(
                    2,
                    ft.colors.DEEP_PURPLE_300,
                ),
            },
        ),
        on_click=lambda _: stop_server(
            container_name, btn_stop_server, btn_start_server, configCol
        ),
        disabled=True,
    )

    connectorBtnRow = ft.Row(
        spacing=20,
        controls=[
            btn_start_server,
            btn_stop_server,
        ],
    )

    connectorBtnRowCol = ft.Column(
        spacing=12,
        controls=[
            ft.Container(
                width=200,
                content=ft.Text(
                    "WEBHOOK CONNECTOR:",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=headingColor,
                ),
            ),
            connectorBtnRow,
        ],
    )

    connectorBtnRowCntnr = ft.Container(
        margin=ft.margin.only(left=620, top=460),
        content=connectorBtnRowCol,
    )

    # Access the UI elements
    ngrok_token_input = token_manager.ngrokToken
    ngrok_button = token_manager.ngrokButton
    frame_token_input = token_manager.frameToken
    frame_button = token_manager.frameButton

    exitAppContainer = ft.Container(
        height=106,
        content=exit_button,
    )

    tokenColumn = ft.Container(
        margin=ft.margin.only(left=20, top=0),
        padding=ft.padding.only(top=-5),
        content=ft.Column(
            controls=[
                ngrok_token_input,
                ngrok_button,
                frame_token_input,
                frame_button,
                btn_pMan_install,
                exitAppContainer,
            ],
        ),
    )

    fioInfoCol, wh_radio_buttons = create_fio_info_col()

    fioInfoColCntr = ft.Container(
        margin=ft.margin.only(left=300, top=28),
        padding=ft.padding.symmetric(vertical=20, horizontal=0),
        content=fioInfoCol,
    )

    connNameCol = create_conn_name_cntnr(kv_store)

    connNameColCntnr = ft.Container(
        margin=ft.margin.only(top=48),
        padding=ft.padding.symmetric(vertical=-20),
        content=connNameCol,
    )

    get_directory_dialog_instance = get_directory_dialog(kv_store, update_button_states)

    selectDirCol = create_select_dir_cntr(kv_store, page, get_directory_dialog_instance)

    def open_directory_dialog(_):
        get_directory_dialog_instance.get_directory_path(
            dialog_title="Select a directory"
        )

    btn_select_dir = ft.OutlinedButton(
        content=ft.Text(
            "Select directory",
            size=12,  # Replace with the actual value of fontSizeVal
            color=ft.colors.with_opacity(
                1, color=ft.colors.GREY_200
            ),  # Replace with the actual value of bodyColor
        ),
        width=150,
        style=ft.ButtonStyle(
            side={
                ft.MaterialState.DEFAULT: ft.BorderSide(
                    2,
                    ft.colors.with_opacity(
                        0.4, ft.colors.DEEP_PURPLE_300
                    ),  # Replace with the actual value of headingColor
                ),
                ft.MaterialState.HOVERED: ft.BorderSide(
                    2,
                    ft.colors.DEEP_PURPLE_300,  # Replace with the actual value of headingColor
                ),
            },
        ),
        on_click=open_directory_dialog,
    )

    selectDirCntnr = ft.Container(
        margin=ft.margin.only(left=0, top=0, bottom=-7),
        padding=ft.padding.only(top=0),
        content=selectDirCol,
    )

    cntnrButtonRow = ft.Container(
        margin=ft.margin.only(top=0, left=20),
        padding=ft.padding.symmetric(vertical=0, horizontal=0),
        content=ft.Row(
            spacing=20,
            controls=[
                btn_select_dir,
                btn_create_cntnr,
                createConn_progress_ind,
            ],
        ),
    )

    ngrokTunnlContnr_content, btn_start_tunnel, btn_stop_tunnel, webhookBottomSheet = (
        ngrokTunnelCntnr(page, webhooks, ngrokTunnStatus, configCol, btn_start_server)
    )

    ngrokTunnlContnr = ft.Container(
        margin=ft.margin.only(left=620, top=280),
        content=ngrokTunnlContnr_content,
    )

    pageCol1 = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        controls=[
            configCol.configContainer,
            tokenColumn,
        ],
    )

    pageCol2 = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=0,
        tight=True,
        controls=[
            connNameColCntnr,
            selectDirCntnr,
            cntnrButtonRow,
        ],
    )

    pageCol2Cntnr = ft.Container(
        margin=ft.margin.only(left=600, top=0),
        content=pageCol2,
    )

    pageCol1Stack = ft.Stack(
        [
            fioInfoColCntr,
            pageCol1,
            pageCol2Cntnr,
            ngrokTunnlContnr,
            connectorBtnRowCntnr,
            consoleHeadColCntnr,
        ]
    )

    pageRow1 = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            pageCol1Stack,
        ],
    )

    update_button_states()

    page.overlay.append(webhookBottomSheet)

    page.add(
        topBanner,
        pageRow1,
    )


ft.app(target=main, assets_dir="assets")
