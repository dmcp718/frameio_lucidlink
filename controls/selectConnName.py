import flet as ft

headingColor = ft.colors.DEEP_PURPLE_300
bodyColor = ft.colors.with_opacity(1, color=ft.colors.GREY_200)
fontSizeVal = 12

def create_conn_name_cntnr(kv_store):

    def getWorkflowNameVal(kv_store):
        state = kv_store.get("connector_name")
        return state

    def connector_changed(e, kv_store):
        connectorName.value = e.control.value
        kv_store.set("connector_name", connectorName.value)
        connectorName.update()

    workflowNameVal = getWorkflowNameVal(kv_store)

    connectorName = ft.TextField(
        content_padding=15,
        bgcolor=ft.colors.with_opacity(0.2, ft.colors.BLACK),
        label="connector name",
        label_style=ft.TextStyle(color=headingColor, size=fontSizeVal),
        value=workflowNameVal,
        cursor_color=bodyColor,
        selection_color=headingColor,
        width=205,
        height=60,
        dense=True,
        color=bodyColor,
        text_size=fontSizeVal,
        multiline=True,
        border_color=ft.colors.with_opacity(0.4, headingColor),
        border_radius=6,
        border_width=1,
        focused_border_width=2,
        focused_border_color=headingColor,
        on_change=connector_changed,
    )

    connNameCntr = ft.Container(
        padding=ft.padding.all(20),
        content=ft.Column(
            width=205,
            spacing=0,
            tight=True,
            controls=[
                ft.Text(
                    "CREATE WEBHOOK CONNECTOR",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=headingColor,
                ),
                ft.Container(
                    margin=ft.margin.only(top=18),
                    content=connectorName,
                ),
            ],
        ),
    )

    return connNameCntr