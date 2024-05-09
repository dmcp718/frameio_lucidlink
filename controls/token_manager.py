import flet as ft
import ngrok

class TokenManager:
    def __init__(self, kv_store, headingColor, bodyColor, configCol):
        self.kv_store = kv_store
        self.headingColor = headingColor
        self.bodyColor = bodyColor
        self.configCol = configCol
        self.fontSizeVal = 12

        self.nToknVal = self.nToknValGet()
        self.fToknVal = self.fToknValGet()

        self.ngrokToken = self.create_ngrok_token_input()
        self.ngrokButton = self.create_ngrok_button()
        self.nToknUpdate = self.create_nTokn_update()

        self.frameToken = self.create_frame_token_input()
        self.frameButton = self.create_frame_button()

    def nToknValGet(self):
        nTokn = self.kv_store.get("nTokn")
        return nTokn if nTokn is not None else str()

    def fToknValGet(self):
        fTokn = self.kv_store.get("fTokn")
        return fTokn if fTokn is not None else str()
    
    def ngrok_token_focus(self, e):
        self.ngrokToken.width = 500
        self.ngrokToken.update()
    
    def ngrok_token_submit(self, e):
        self.ngrokToken.width = 235
        self.ngrokToken.update()
        
        # Call configCol.update_nToken_status() after updating the token value
        self.configCol.update_nToken_status()

    def create_nTokn_update(self):
        ngrok.set_auth_token(self.nToknVal)

    def ngrok_token_changed(self, e):
        rawInput = e.control.value
        self.ngrokToken.value = rawInput.strip()
        nTokn = self.ngrokToken.value
        self.kv_store.set("nTokn", nTokn)
        self.ngrokToken.update()
        self.nToknUpdate
        # Call configCol.update_nToken_status() after updating the token value
        self.configCol.update_nToken_status()

    def create_ngrok_token_input(self):
        return ft.Container(
            margin=ft.margin.only(top=10),
            height=40,
            width=235,
            content=ft.TextField(
                content_padding=10,
                bgcolor=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                label="ngrok Authtoken",
                label_style=ft.TextStyle(color=self.headingColor, size=12),
                value=self.nToknVal,
                width=235,
                height=60,
                dense=True,
                color=self.bodyColor,
                cursor_color=self.bodyColor,
                selection_color=self.headingColor,
                text_size=10,
                password=True,
                can_reveal_password=True,
                border_color=ft.colors.with_opacity(0.4, self.headingColor),
                border_radius=6,
                border_width=1,
                focused_border_width=2,
                focused_border_color=self.headingColor,
                on_focus=self.ngrok_token_focus,
                on_change=self.ngrok_token_changed,
                on_submit=self.ngrok_token_submit
            )
        )

    def create_ngrok_button(self):
        return ft.Container(
            margin=ft.margin.only(top=5),
            content=ft.Row(
                [
                    ft.OutlinedButton(
                        width=235,
                        style=ft.ButtonStyle(
                            side={
                                ft.MaterialState.DEFAULT: ft.BorderSide(2, ft.colors.with_opacity(0.4, self.headingColor)),
                                ft.MaterialState.HOVERED: ft.BorderSide(2, self.headingColor),
                            },
                        ),                                                              
                        content=ft.Row(
                            [
                                ft.Text("Get ngrok Tunnel Authtokens", size=self.fontSizeVal, color=self.bodyColor),
                            ],
                            tight=True,
                        ),
                        url="https://dashboard.ngrok.com/tunnels/authtokens",
                    ),
                ],
            ),
        )
    
    def frame_token_focus(self, e):
        self.frameToken.width = 500
        self.frameToken.update()
    
    def frame_token_submit(self, e):
        self.frameToken.width = 235
        self.frameToken.update()
        # Call configCol.update_nToken_status() after updating the token value
        self.configCol.update_fToken_status()

    def frame_token_changed(self, e):
        rawInput = e.control.value
        self.frameToken.value = rawInput.strip()
        fTokn = self.frameToken.value
        self.kv_store.set("fTokn", fTokn)
        self.frameToken.update()

    def create_frame_token_input(self):
        return ft.Container(
            margin=ft.margin.only(top=10),
            height=40,
            width=235,
            content=ft.TextField(
                content_padding=10,
                bgcolor=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                label="frame.io token",
                label_style=ft.TextStyle(color=self.headingColor, size=12),
                value=self.fToknVal,
                width=235,
                height=60,
                dense=True,
                color=self.bodyColor,
                cursor_color=self.bodyColor,
                selection_color=self.headingColor,
                text_size=10,
                password=True,
                can_reveal_password=True,
                border_color=ft.colors.with_opacity(0.4, self.headingColor),
                border_radius=6,
                border_width=1,
                focused_border_width=2,
                focused_border_color=self.headingColor,
                on_focus=self.frame_token_focus,
                on_change=self.frame_token_changed,
                on_submit=self.frame_token_submit
            )
        )

    def create_frame_button(self):
        return ft.Container(
            margin=ft.margin.only(top=5),
            content=ft.Row(
                [
                    ft.OutlinedButton(
                        width=235,
                        style=ft.ButtonStyle(
                            side={
                                ft.MaterialState.DEFAULT: ft.BorderSide(2, ft.colors.with_opacity(0.4, self.headingColor)),
                                ft.MaterialState.HOVERED: ft.BorderSide(2, self.headingColor),
                            },
                        ),                                                              
                        content=ft.Row(
                            [
                                ft.Text("Get frame.io Developer Token", size=self.fontSizeVal, color=self.bodyColor),
                            ],
                            tight=True,
                        ),
                        url="https://developer.frame.io/app/tokens",
                    ),
                ],
            ),
        )