import flet as ft

class CustomTextField(ft.TextField):
    def __init__(
            self,
            label,
            icon=None,
            password=False,
            border=ft.InputBorder.NONE,
            can_reveal_password=False,
            error_text=None,
            input_filter=None,
            **kwargs
    ):
        # Extract hint_style from kwargs if provided
        custom_hint_style = kwargs.pop("hint_style", None)

        # Define default hint_style
        default_hint_style = ft.TextStyle(size=14, color=ft.Colors.GREY_400)

        # Merge hint_style: custom_hint_style overrides default
        if custom_hint_style:
            hint_style = ft.TextStyle(
                size=custom_hint_style.size if custom_hint_style.size else default_hint_style.size,
                color=custom_hint_style.color if custom_hint_style.color else default_hint_style.color,
                weight=custom_hint_style.weight if custom_hint_style.weight else default_hint_style.weight,
            )
        else:
            hint_style = default_hint_style

        super().__init__(
            label=label,
            border=border,
            password=password,
            icon=icon,
            error_text=error_text,
            can_reveal_password=can_reveal_password,
            content_padding=ft.padding.only(top=10, bottom=10, left=20, right=20),
            hint_style=hint_style,
            input_filter=input_filter,
            focused_color=ft.Colors.BLUE_400,
            width=450,
            **kwargs
        )
    
