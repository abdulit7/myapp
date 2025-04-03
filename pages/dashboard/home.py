import flet as ft
from nav.sidebar import SidebarPage
from nav.menubar import TopBarPage
from components.cards import MainCards

class Home(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.expand = True

        page.window.title = "Asset Management System"

        self.content = ft.Column(
            controls=[
                TopBarPage(page),  # Menubar at the top
                ft.Row(
                    controls=[
                        ft.Container(
                              # Fixed width for the sidebar
                            content=SidebarPage(page),  # Sidebar container
                        ),
                        ft.Container(
                            expand=True,  # Ensure the content area expands to take remaining space
                            content=ft.Column(
                                controls=[
                                    ft.ElevatedButton(
                                        icon=ft.Icons.ADD, text="Add Asset more"
                                    ),
                                    MainCards(page)
                                ],
                                spacing=10,  # Adds spacing between the button and the cards
                            ),
                            bgcolor=ft.Colors.GREY_200,
                            padding=10,  # Padding for the main content area
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=0,  # No space between the sidebar and the content area
                ),
            ],
            spacing=0,  # Ensure no space between menubar and the row
        )
