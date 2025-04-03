import flet as ft

class MainCards(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.expand = True

        # Improved color scheme
        card_colors = [
            {"card": "#E3F2FD", "icon": "#42A5F5"},
            {"card": "#F3E5F5", "icon": "#AB47BC"},
            {"card": "#E8F5E9", "icon": "#66BB6A"},
            {"card": "#FFF3E0", "icon": "#FFA726"}
        ]

        card_data = [
            {"icon": ft.Icons.COMPUTER, "title": "TOTAL ASSETS", "subtitle": "50"},
            {"icon": ft.Icons.PERSON, "title": "TOTAL USERS", "subtitle": "50"},
            {"icon": ft.Icons.DASHBOARD, "title": "TOTAL DEPARTMENTS", "subtitle": "50"},
            {"icon": ft.Icons.CATEGORY, "title": "TOTAL CATEGORIES", "subtitle": "50"}
        ]

        self.content = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self.create_card(item["icon"], item["title"], item["subtitle"], colors["card"], colors["icon"]),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10)
                ) 
                for item, colors in zip(card_data, card_colors)
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0
        )

    def create_card(self, icon, title, subtitle, card_bgcolor, icon_bgcolor):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Icon(icon, color="#FFFFFF", size=30),
                            bgcolor=icon_bgcolor,
                            width=50,
                            height=50,
                            alignment=ft.alignment.center,
                            border_radius=25
                        ),
                        ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color="#263238"),
                        ft.Text(subtitle, size=30, weight=ft.FontWeight.BOLD, color="#42A5F5")
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                padding=20,
                bgcolor=card_bgcolor,
                border_radius=12,
                ink=True  # Add ripple effect on click
            ),
            elevation=5,
            
        )

def MainCardsPage(page):
    return MainCards(page)
