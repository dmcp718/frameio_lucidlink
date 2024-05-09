import flet as ft
import subprocess

class ConfigCol:
    def __init__(self, kv_store, page):
        self.kv_store = kv_store
        self.page = page
        self.headingColor = ft.colors.DEEP_PURPLE_300
        self.bodyColor = ft.colors.with_opacity(1, color=ft.colors.GREY_200)
        self.logoColor = "#b3fb1e"
        self.fontSizeVal = 12

        self.nTokenStatusIcon = ft.Icon(name=ft.icons.CHECK_CIRCLE_OUTLINED, size=24, color=self.logoColor, visible=False)
        self.fTokenStatusIcon = ft.Icon(name=ft.icons.CHECK_CIRCLE_OUTLINED, size=24, color=self.logoColor, visible=False)
        self.podmanStatusIcon = ft.Icon(name=ft.icons.CHECK_CIRCLE_OUTLINED, size=24, color=self.logoColor, visible=False)
        self.connctrStatusIcon = ft.Icon(name=ft.icons.CHECK_CIRCLE_OUTLINED, size=24, color=self.logoColor, visible=False)
        self.ngrokTunnStatus = ft.CupertinoActivityIndicator(radius=12, color=self.logoColor, animating=True, visible=False)
        self.webhookStatus = ft.CupertinoActivityIndicator(radius=12, color=self.logoColor, animating=True, visible=False)

        self.configDataCols = [
            ft.DataColumn(ft.Text("COMPONENT", size=12, weight=ft.FontWeight.BOLD, color=self.headingColor)),
            ft.DataColumn(ft.Text("STATUS", size=12, weight=ft.FontWeight.BOLD, color=self.headingColor)),
        ]

        self.configDataRows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("nGrok token:", size=12, color=self.bodyColor)),
                    ft.DataCell(ft.Container(
                        width=50,
                        content=self.nTokenStatusIcon
                        ),
                    ),
                ],
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("frame.io token:", size=12, color=self.bodyColor)),
                    ft.DataCell(ft.Container(
                        width=50,
                        content=self.fTokenStatusIcon
                        ),
                    ),
                ],
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Podman installed:", size=12, color=self.bodyColor)),
                    ft.DataCell(ft.Container(
                        width=50,
                        content=self.podmanStatusIcon
                        ),
                    ),
                ],
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Connector created:", size=12, color=self.bodyColor)),
                    ft.DataCell(ft.Container(
                        width=50,
                        content=self.connctrStatusIcon
                        ),
                    ),
                ],
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Ngrok Tunnel:", size=12, color=self.bodyColor)),
                    ft.DataCell(ft.Container(
                        width=50,
                        content=self.ngrokTunnStatus
                        ),
                    ),
                ],
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Webhook Connector:", size=12, color=self.bodyColor)),
                    ft.DataCell(ft.Container(
                        width=50,
                        content=self.webhookStatus
                        ),
                    ),
                ],
            ),
        ]

        self.configDataTable = ft.DataTable(
            column_spacing=20,
            heading_row_height=20,
            columns=self.configDataCols,
            rows=self.configDataRows,
            divider_thickness=0.1)

        self.configContainer = ft.Container(
            margin=ft.margin.symmetric(vertical=20, horizontal=20),
            padding=ft.padding.symmetric(vertical=20, horizontal=10),
            width=235,
            height=350,
            content=self.configDataTable,
            border=ft.border.all(1, self.headingColor),
            border_radius=16
        )
        
    def update_token_status(self, token_key, status_icon):
        token_status = self.kv_store.get(token_key)
        status_icon.visible = token_status is not None
        self.page.update()

    def update_nToken_status(self):
        self.update_token_status("nTokn", self.nTokenStatusIcon)

    def update_fToken_status(self):
        self.update_token_status("fTokn", self.fTokenStatusIcon)

    def check_podman_installed(self):
        try:
            result = subprocess.run(["/opt/podman/bin/podman", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                return True
        except FileNotFoundError:
            return False
        
    def update_podman_status(self):
        installed = self.check_podman_installed()
        if installed:
            self.kv_store.set("podman_installed", "true")
            self.podmanStatusIcon.visible = True
        else:
            self.kv_store.set("podman_installed", "false")
            self.podmanStatusIcon.visible = False
        self.page.update()
    
    def check_connector_status(self):
        self.connctrStatusIcon.visible = self.kv_store.get("connector_created") == "True"
        self.page.update()

    def update_connector_status(self):
        if self.connctrStatusIcon.visible:
            self.connctrStatusIcon.visible = False
        else:
            self.connctrStatusIcon.visible = True
        self.page.update()

    def update_tunnel_status(self):
        if self.ngrokTunnStatus.visible:
            self.ngrokTunnStatus.visible = False
        else:
            self.ngrokTunnStatus.visible = True
        self.page.update()

    def update_webhook_status(self):
        if self.webhookStatus.visible:
            self.webhookStatus.visible = False
        else:
            self.webhookStatus.visible = True
        self.page.update()