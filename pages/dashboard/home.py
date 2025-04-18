import flet as ft
from components.cards import MainCards
from components.chart import chart_page
from components.assetlistscroll import list_scroll
from components.componentlistscroll import compo_scroll


class Home(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.expand = True
        page.window.title = "Asset Management System"
       

        self.content = ft.Column(
            controls=[
                MainCards(page),
                ft.Divider(height=50, thickness=1),
                ft.Row(
                    controls=[
                        ft.Container(   # Chart container
                            content=chart_page(page),
                            width=420,   # fixed width
                            height=400,  # fixed height to prevent stretching
                            padding=10,
                            #bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),  # optional background to visualize size
                        ),
                        ft.Container(   # List Scroll container
                            content=list_scroll(page),
                            width=420,   # fixed width
                            height=400,  # fixed height
                            padding=10,
                            #bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),  # optional
                        ),
                        ft.Container(   # List Scroll container
                            content=compo_scroll(page),
                            width=420,   # fixed width
                            height=400,  # fixed height
                            padding=10,
                            #bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),  # optional
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=200,
                ),
            ],
            spacing=20,
        )



        # self.content = ft.Column(
        #     controls=[
        #         #TopBarPage(page),  # Menubar at the top
        #         ft.Row(
        #             controls=[
        #                 # ft.Container(
        #                 #       # Fixed width for the sidebar
        #                 #     #content=SidebarPage(page),  # Sidebar container
        #                 # ),
        #                 ft.Container(
        #                     expand=True,  # Ensure the content area expands to take remaining space
        #                     content=ft.Column(
        #                         controls=[
        #                             ft.ElevatedButton(
        #                                 icon=ft.Icons.ADD, text="Add Asset more"
        #                             ),
        #                             MainCards(page)
        #                         ],
        #                         spacing=10,  # Adds spacing between the button and the cards
        #                     ),
        #                     bgcolor=ft.Colors.GREY_200,
        #                     padding=10,  # Padding for the main content area
        #                 ),
        #             ],
        #             alignment=ft.MainAxisAlignment.START,
        #             spacing=0,  # No space between the sidebar and the content area
        #         ),
        #     ],
        #     spacing=0,  # Ensure no space between menubar and the row
        # )
