import flet as ft

headingColor = ft.colors.DEEP_PURPLE_300
bodyColor = ft.colors.with_opacity(1, color=ft.colors.GREY_200)
fontSizeVal = 12

def exit_app(e):
    page = e.page
    page.window_close()

def create_exit_app_button():
    return ft.Container(
        width=235,
        content=ft.OutlinedButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                tight=True,
                spacing=5,
                controls=[
                    ft.Icon(
                        ft.icons.CLOSE,
                        size=16,
                        color=ft.colors.RED_400,
                    ),
                    ft.Text(
                        "Exit Application",
                        size=fontSizeVal,
                        color=bodyColor,
                    ),
                ],
            ),
            style=ft.ButtonStyle(
                side={
                    ft.MaterialState.DEFAULT: ft.BorderSide(
                        2,
                        ft.colors.with_opacity(
                            0.4,
                            headingColor,
                        ),
                    ),
                    ft.MaterialState.HOVERED: ft.BorderSide(
                        2, headingColor
                    ),
                },
            ),
            width=235,
            on_click=exit_app,
        ),
        alignment=ft.alignment.bottom_center,
    )