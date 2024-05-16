import flet as ft
import os
import json
import ngrok    
from time import sleep
from .KeyValueStore import KeyValueStore
from .fioUpdateWebhook import updateWebhook

headingColor = ft.colors.DEEP_PURPLE_300
bodyColor = ft.colors.with_opacity(1, color=ft.colors.GREY_200)
logoColor = "#b3fb1e"
fontSizeVal = 12

kv_store = KeyValueStore()

# Create an instance of NgrokTunnel
ngrok_tunnel = None

# Add UI elements for ngrok tunnel management
txt_tunnel_url = ft.Text(
    value="",
    overflow=ft.TextOverflow.FADE,
    size=fontSizeVal,
    color=bodyColor,
)

def start_tunnel(_, page, ngrokTunnStatus, configCol):
    global webhook_url, kv_store, ngrok_tunnel
    page.splash = ft.ProgressBar()
    btn_start_tunnel.disabled = False
    btn_stop_tunnel.disabled = True
    
    ngrokTunnStatus.visible = False
    page.update()

    # Retrieve the ngrok authtoken from the key-value store
    ngrok_authtoken = kv_store.get("nTokn")

    if ngrok_authtoken:
        ngrok.set_auth_token(f"{ngrok_authtoken}")

        try:
            ngrok_tunnel = ngrok.forward(8000)
            tunnel_url = ngrok_tunnel.url()
            webhook_url = f"{tunnel_url}/webhook"
            kv_store.set("webhook_url", webhook_url)
            kv_store.set("webhook_url_updated", True)
            txt_tunnel_url.value = webhook_url
            ngrokTunnStatus.visible = True
            btn_start_tunnel.disabled = True
            btn_stop_tunnel.disabled = False
            configCol.update_tunnel_status()
            page.update()

        except Exception as e:
            ngrokTunnStatus.value = f"Error starting tunnel: {e}"
            btn_start_tunnel.disabled = True
            btn_stop_tunnel.disabled = False
            page.update()
    else:
        btn_start_tunnel.disabled = True
        btn_stop_tunnel.disabled = False
        page.update()

    page.splash = None
    page.update()
    
def stop_tunnel(_):
    global ngrok_tunnel
    if ngrok_tunnel:
        ngrok.disconnect(ngrok_tunnel.url())
        ngrok_tunnel = None
        txt_tunnel_url.value = "Stopped."
        btn_start_tunnel.disabled = False
        btn_stop_tunnel.disabled = True

def start_tunnel_and_update(_, page, ngrokTunnStatus, configCol):
    start_tunnel(_, page, ngrokTunnStatus, configCol)
    page.update()

def stop_tunnel_and_update(_, page, configCol):
    stop_tunnel(_)
    configCol.update_tunnel_status()
    page.update()

webhookUpdateStatus = ft.Text("", size=18, color=ft.colors.WHITE)

def show_webhook_bottom_sheet(_):
    webhookBottomSheet.open = True
    webhookBottomSheet.update()
    sleep(3)
    webhookBottomSheet.open = False
    webhookBottomSheet.update()

webhookBottomSheet = ft.BottomSheet(
    ft.Container(
        alignment=ft.alignment.center,
        padding=ft.padding.all(20),
        width=350,
        height=80,
        bgcolor=ft.colors.DEEP_PURPLE_900,
        border_radius=ft.border_radius.only(top_left=10, top_right=10),
        content=webhookUpdateStatus,
    ),
    dismissible=True,
)

def updateWebhookButton(page, webhooks, btn_start_server):
    global kv_store
    try:
        # Get the selected webhook ID and name from the key-value store
        webhook_id = kv_store.get("webhook_id")
        webhook_name = kv_store.get("webhook_name")

        if webhook_id and webhook_name:
            whurl = txt_tunnel_url.value

            updateWebhook(kv_store, webhook_id, webhook_name, whurl)
            sleep(1)
            status = kv_store.get("webhook_url_updated")
            if status is True:
                webhookUpdateStatus.value = "frame.io webhook URL updated."
            elif status is False:
                webhookUpdateStatus.value = "Error updating frame.io Webhook."
            else:
                webhookUpdateStatus.value = "Webhook updated successfully."            
            show_webhook_bottom_sheet(page)
            btn_start_server.disabled = False
            page.update()
        else:
            # If no webhook is selected or the selection is invalid, retrieve the first webhook
            if webhooks:
                selected_webhook = webhooks[0]
                kv_store.set("selected_webhook", selected_webhook)
                kv_store.set("webhook_name", selected_webhook)

                # Retrieve the webhook ID based on the selected webhook name
                userPath = os.path.expanduser('~')
                wh_path = userPath + "/.lucidlinkFrameIOapp/webhooks.json"
                with open(wh_path, 'r') as file:
                    webhooksKV = json.load(file)
                webhook_id = webhooksKV.get(selected_webhook)
                kv_store.set("webhook_id", webhook_id)

                # Update the webhook with the first webhook
                url = txt_tunnel_url.value
                updateWebhook(webhook_id, selected_webhook, url)
                sleep(1)
                status = kv_store.get("webhook_url_updated")
                if status is True:
                    webhookUpdateStatus.value = "frame.io Webhook updated with tunnel URL."
                elif status is False:
                    webhookUpdateStatus.value = "Error updating frame.io Webhook."
                else:
                    webhookUpdateStatus.value = "Webhook updated successfully."                
                show_webhook_bottom_sheet(page)
                btn_start_server.disabled = False
                page.update()
            else:
                print("No webhooks available.")
                webhookUpdateStatus.value = "No webhooks available."
                show_webhook_bottom_sheet(page)
                btn_start_server.disabled = True
                page.update()
                return

    except Exception as e:
        print(f"Error updating webhook: {str(e)}")

def updateWebhookButton_and_update(_, page):
    updateWebhookButton(_)
    page.update()

btn_start_tunnel = ft.OutlinedButton(
    width=150,
    style=ft.ButtonStyle(
        side={
            ft.MaterialState.DEFAULT: ft.BorderSide(
                2, ft.colors.with_opacity(0.4, headingColor)
            ),
            ft.MaterialState.HOVERED: ft.BorderSide(2, headingColor),
        },
    ),
    content=ft.Text("Start Tunnel", size=fontSizeVal, color=bodyColor),
)

btn_stop_tunnel = ft.OutlinedButton(
    width=150,
    style=ft.ButtonStyle(
        side={
            ft.MaterialState.DEFAULT: ft.BorderSide(
                2, ft.colors.with_opacity(0.4, headingColor)
            ),
            ft.MaterialState.HOVERED: ft.BorderSide(2, headingColor),
        },
    ),
    content=ft.Text("Stop Tunnel", size=fontSizeVal, color=bodyColor),
)

# In ngrokTunnelContainer.py

def ngrokTunnelCntnr(
        page, 
        webhooks, 
        ngrokTunnStatus, 
        configCol, 
        btn_start_server):
    btn_start_tunnel.on_click = lambda _: start_tunnel_and_update(_, page, ngrokTunnStatus, configCol)
    btn_stop_tunnel.on_click = lambda _: stop_tunnel_and_update(_, page, configCol)
    
    return ft.Container(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            controls=[
                ft.Container(
                    margin=ft.margin.only(top=20),
                    padding=ft.padding.all(0),
                    content=ft.Container(
                        padding=ft.padding.all(0),
                        margin=ft.margin.only(bottom=-15),
                        content=ft.Column(
                            spacing=12,
                            controls=[
                                ft.Container(
                                    width=110,
                                    content=ft.Text(
                                        "NGROK TUNNEL:",
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                        color=headingColor,
                                    ),  
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            margin=ft.margin.only(top=0),
                                            padding=ft.padding.all(15),
                                            height=50,
                                            width=640,
                                            bgcolor=ft.colors.with_opacity(
                                                0.3, ft.colors.BLACK
                                            ),
                                            border_radius=6,
                                            content=txt_tunnel_url,
                                        ),
                                        ft.Container(
                                            margin=ft.margin.symmetric(horizontal=-5),
                                            padding=ft.padding.only(top=5),
                                            content=ft.IconButton(
                                                icon=ft.icons.UPLOAD,
                                                icon_color=headingColor,
                                                icon_size=26,
                                                highlight_color=ft.colors.DEEP_PURPLE_200,
                                                tooltip="Update frame.io webhook URL",
                                                on_click=lambda _: updateWebhookButton(page, webhooks, btn_start_server),
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                ),
                ft.Container(
                    margin=ft.margin.only(top=30),
                    content=ft.Row(
                        spacing=20,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            btn_start_tunnel,
                            btn_stop_tunnel,
                        ],
                    ),
                ),
            ],
        )
    ), btn_start_tunnel, btn_stop_tunnel, webhookBottomSheet