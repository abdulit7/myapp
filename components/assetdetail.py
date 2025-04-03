import flet as ft
from nav.sidebar import SidebarPage
from nav.menubar import TopBarPage

class AssetDetail(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        page.title = "Asset Management System - Asset Details"
        page.bgcolor = ft.colors.BLUE_GREY_50

        # Detail Row Function (Improved)
        def detail_row(label, value, value_color=ft.colors.BLACK):
            return ft.Row(
                controls=[
                    ft.Text(label, weight=ft.FontWeight.W_600, color=ft.colors.BLUE_GREY_800, width=150),  # Fixed width for label
                    ft.Text(value, color=value_color, expand=True)  # Value expands to fill space
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,  # Align items vertically
                spacing=20,  # Reduced spacing
            )

        # Asset Image Frame (Improved)
        asset_image = ft.Container(
            content=ft.Image(
                src="assets/images/jojo.jpg",
                width=300,
                height=200,
                fit=ft.ImageFit.CONTAIN,
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            padding=10,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.GREY_300)  # Add shadow
        )

        # Asset Details (Left Column) (Improved)
        asset_details = ft.Column(
            controls=[
                detail_row("Asset Name", "ThinClient 3040"),
                detail_row("Status", "Deployable", ft.colors.GREEN),
                detail_row("Company", "Dell"),
                detail_row("Manufacturer", "Dell"),
                detail_row("Category", "Thin Client"),
                detail_row("Model", "3040"),
                detail_row("Purchase Date", "Fri Nov 01, 2024"),  # Simplified date
                detail_row("Purchase Cost", "USD 2,000.00"),
                detail_row("Current Value", "USD 1,910.00"),
                detail_row("Depreciation", "3040 2GB RAM 16 GB Rom"),
                detail_row("Notes", ""),
                detail_row("Created At", "Fri Feb 14, 2025 11:26 AM"),  # Improved time format
                detail_row("Updated At", "Mon Feb 17, 2025 11:49 PM"),  # Improved time format
                detail_row("Last Checkin Date", "Mon Feb 17, 2025 1:46 PM"),  # Improved time format
            ],
            spacing=15,  # Increased spacing
            width=600,  # Increased width
            expand=True
        )

        # Action Buttons (Right Column) (Improved)
        action_buttons = ft.Column(
            controls=[
                ft.ElevatedButton("Edit Asset", bgcolor=ft.colors.ORANGE_400, color=ft.colors.WHITE, icon=ft.icons.EDIT),
                ft.ElevatedButton("Checkin Asset", bgcolor=ft.colors.INDIGO_400, color=ft.colors.WHITE, icon=ft.icons.CHECK),
                ft.ElevatedButton("Generate Label", bgcolor=ft.colors.TEAL_400, color=ft.colors.WHITE, icon=ft.icons.LABEL),
                ft.ElevatedButton("Checkin and Delete", bgcolor=ft.colors.RED_400, color=ft.colors.WHITE, icon=ft.icons.DELETE),
            ],
            spacing=10,
            width=300
        )

         # Tabs
        t = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Info",
                    content=ft.Container(
                        content= asset_details,
                       
                        expand=True,
                    )
                ),
                ft.Tab(
                    text="Components",
                    content=ft.Container(
                        content=ft.Text("In Use Assets", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                    
                        expand=True,
                    )
                ),
                ft.Tab(
                    text="License",
                    content=ft.Container(
                        content=ft.Text("Maintenance Assets", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                    
                        expand=True,
                    )
                ),

                ft.Tab(
                    text="History",
                    content=ft.Container(
                        content=ft.Text("Maintenance Assets", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                       
                        expand=True,
                    )
                ),
            ],
            expand=True,
        )


        # Main Layout
        self.content = ft.Column(
            controls=[
                TopBarPage(page),
                ft.Row(
                    controls=[
                        ft.Column(  # Use Column to align sidebar to top
                            controls=[
                                ft.Container(
                                    content=SidebarPage(page),
                                    width=200,
                                    expand=True,  # Make sidebar fill available height
                                ),
                            ],
                            #expand=True,  # Make the column expand to fill the row
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        
                                        asset_image,
                                        action_buttons,
                                        
                                        
                                    ],
                                    #alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=20,
                    expand=True,
                ),
                t,
            ],
            spacing=0,
            expand=True,
        )

        page.update()

def asset_detail_page(page):
    return AssetDetail(page)