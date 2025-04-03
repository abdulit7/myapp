import flet as ft


class CustomTextField(ft.TextField):
    def __init__(
            self,
            label,
            icon=None,
            password=False,
            border= ft.InputBorder.NONE,
            can_reveal_password=False,
            error_text=None,
            input_filter=None,
            **kwargs
    ):
        super().__init__(
            label=label,
            border=border,
            password=password,
            icon=icon,
            error_text=error_text,
            can_reveal_password=can_reveal_password,
            content_padding=ft.padding.only(top=10, bottom=10, left=20, right=20),
            hint_style=ft.TextStyle(size=14, color=ft.Colors.GREY_400),
            input_filter=input_filter,
            focused_color=ft.Colors.BLUE_400,
            width=450,
            **kwargs
        )

    
