import flet as ft
import os
import json
from .fioAccountID import getAccountID
from .fioAccountName import getAccountName
from .fioWebhooks import getWebhooks
from .KeyValueStore import KeyValueStore

HEADING_COLOR = ft.colors.DEEP_PURPLE_300
BODY_COLOR = ft.colors.with_opacity(1, color=ft.colors.GREY_200)
FONT_SIZE_VAL = 12

USER_PATH = os.path.expanduser('~')
DIR_PATH = USER_PATH + "/.lucidlinkFrameIOapp"

kv_store = KeyValueStore()

def get_selected_webhook():
    return kv_store.get("selected_webhook")

def check_webhook_selected():
    return kv_store.get("selected_webhook") is not None

def fio_webhooks():
    wh_path = os.path.join(DIR_PATH, "webhooks.json")
    
    if not os.path.exists(wh_path):
        return []
    
    with open(wh_path, "r") as f:
        webhooks = json.load(f)
    
    return [
        ft.Container(
            theme=ft.Theme(text_theme=ft.TextTheme(body_medium=ft.TextStyle(size=10))),
            content=ft.Radio(
                value=f"{key}:{value}",
                label=key,
                label_style=ft.TextStyle(color=BODY_COLOR, size=FONT_SIZE_VAL),
                active_color=HEADING_COLOR,
            ),
        )
        for key, value in webhooks.items()
    ]

wh_selection = ft.Text()
wh_selection_name = ft.Text()
wh_selection_id = ft.Text()

wh_column = ft.Column(spacing=0, tight=True, controls=fio_webhooks())
wh_radio_buttons = ft.RadioGroup(content=wh_column, value=get_selected_webhook())

def selected_webhook(e):
    wh_selection.value = f"{e.control.value}"
    wh_radio_buttons.value = wh_selection.value
    wh_selection_split = wh_selection.value.split(":")
    wh_selection_name.value = wh_selection_split[0]
    kv_store.set("selected_webhook", wh_radio_buttons.value)
    kv_store.set("webhook_name", wh_selection_split[0])
    wh_selection_id.value = wh_selection_split[1]
    kv_store.set("webhook_id", wh_selection_split[1])
    kv_store.close()

wh_radio_buttons.on_change = selected_webhook

def create_fio_info_col():
    account_name = getAccountName(kv_store)
    account_id = getAccountID(kv_store)
    getWebhooks(kv_store, account_id)

    fio_user_label = ft.Text(
        "Account Name: ", size=12, weight=ft.FontWeight.BOLD, color=HEADING_COLOR
    )
    fio_user_id_label = ft.Text(
        "Account ID: ", size=12, weight=ft.FontWeight.BOLD, color=HEADING_COLOR
    )
    fio_webhook_label = ft.Text(
        "Selected webhook: ", size=12, weight=ft.FontWeight.BOLD, color=HEADING_COLOR
    )

    fio_user = ft.Text(
        value=account_name, size=FONT_SIZE_VAL, color=BODY_COLOR, selectable=True
    )
    fio_user_id = ft.Text(
        value=account_id, size=FONT_SIZE_VAL, color=BODY_COLOR, selectable=True
    )

    fio_col1 = ft.Column(
        spacing=5,
        tight=False,
        controls=[
            fio_user_label,
            fio_user,
        ],
    )

    fio_col2 = ft.Column(
        spacing=5,
        tight=False,
        controls=[
            fio_user_id_label,
            fio_user_id,
        ],
    )

    fio_col3 = ft.Column(
        spacing=5,
        tight=False,
        controls=[
            fio_webhook_label,
            wh_radio_buttons,
        ],
    )

    return ft.Container(
        height=480,
        width=280,
        content=ft.Column(
            width=300,
            spacing=15,
            controls=[
                ft.Text(
                    "FRAME.IO INFO:",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=HEADING_COLOR,
                ),
                ft.Stack(
                    [
                        ft.Column(
                            alignment=ft.MainAxisAlignment.START,
                            spacing=20,
                            tight=False,
                            controls=[
                                fio_col1,
                                fio_col2,
                                fio_col3,
                            ],
                        ),
                    ]
                ),
            ],
        ),
    ), wh_radio_buttons