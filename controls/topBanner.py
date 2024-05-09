import flet as ft

def top_Banner():
    return ft.Container(
        # margin=0,
        # padding=0,
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_right,
            end=ft.alignment.center_left,
        colors=[ft.colors.DEEP_PURPLE, ft.colors.DEEP_PURPLE_900],
        ),
        height=60,
        width=1352,
        content=ft.Container(
            alignment=ft.alignment.center_left,
            padding=ft.padding.symmetric(vertical=10, horizontal=20),
            content=ft.Text("Frame.io >> LucidLink Webhook Connector", color="white", size=18, weight="bold"),
        )
    )