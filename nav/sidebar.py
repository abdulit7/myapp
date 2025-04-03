import flet as ft

class Sidebar(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.expand = False  # Sidebar should not expand to fill available space

        # Define menu items with text, icon, and route
        menu_items = [
            {"text": "Dashboard", "icon": ft.Icons.DASHBOARD, "route": "/dashboard"},
            {"text": "Assets", "icon": ft.Icons.REPORT, "route": "/asset"},
            {"text": "Components", "icon": ft.Icons.INVENTORY, "route": "/component"},
            {"text": "Users", "icon": ft.Icons.PEOPLE, "route": "/user"},
            {"text": "Category", "icon": ft.Icons.LABEL, "route": "/category"},
            {"text": "Sale Force", "icon": ft.Icons.BUSINESS, "route": "/saleforce"},
            {"text": "Departments", "icon": ft.Icons.HDR_OFF_SELECT_OUTLINED, "route": "/department"},
            {"text": "Logout", "icon": ft.Icons.LOGOUT, "route": "/logout"}
        ]

        # Create menu buttons dynamically
        menu_buttons = [self.create_menu_button(item["text"], item["icon"], lambda e, route=item["route"]: page.go(route)) for item in menu_items]

        self.content = ft.Container(
            bgcolor="#263238",  # Darker shade for modern look
            padding=ft.padding.symmetric(vertical=20, horizontal=15),
            border_radius=8,
            width=250,  # Fixed width for the sidebar
            content=ft.Column(
                controls=menu_buttons,
                spacing=10,
                scroll="adaptive"
            )
        )

    def create_menu_button(self, text, icon, on_click):
        # Return a custom-styled button with hover effect using ButtonStyle
        return ft.TextButton(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color="#FFFFFF", size=24),  # White icon
                    ft.Text(text, color="#FFFFFF", size=16, weight=ft.FontWeight.W_600)
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=15,
                expand=True
            ),
            on_click=on_click,
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(vertical=10, horizontal=15),  # Uniform padding
                shape=ft.RoundedRectangleBorder(radius=8),
                overlay_color="rgba(255, 255, 255, 0.1)",  # Light hover effect
                bgcolor={"": "#37474F", "hovered": "#455A64"},  # Default and hover background colors
            )
        )


def SidebarPage(page):
    return Sidebar(page)
