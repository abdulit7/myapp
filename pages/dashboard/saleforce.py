import flet as ft

from nav.menubar import TopBarPage
from nav.sidebar import SidebarPage

class SaleForce(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.expand = True
        ft.ScrollMode.AUTO
        page.window.title = "Asset Management System"
        page.bgcolor = ft.Colors.BLUE_GREY_50  # Light background for contrast
     

        add_device_button = ft.ElevatedButton(icon=ft.Icons.ADD, text="ADD Device", on_click=lambda e: page.go("/deviceform"))

        # Deployable DataTable
        deployable_table = ft.DataTable(
            width=5000,
            height=500,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=30,
            vertical_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            heading_row_color=ft.Colors.INDIGO_100,
            heading_text_style=ft.TextStyle(
                color=ft.Colors.INDIGO_900,
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            data_row_color={
                ft.ControlState.HOVERED: ft.Colors.LIGHT_BLUE_50,
            },
            data_row_min_height=50,
            data_text_style=ft.TextStyle(
                color=ft.Colors.GREY_800,
                size=14,
            ),
            show_checkbox_column=False,
            column_spacing=30,
            columns=[
                ft.DataColumn(ft.Text("Category", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Company", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Model", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Serial No", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Purchase Date", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Warranty", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Price", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.W_600)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Bio-Metric")),
                        ft.DataCell(ft.Text("ZKTeco")),
                        ft.DataCell(ft.Text("UA860")),
                        ft.DataCell(ft.Text("123456789")),
                        ft.DataCell(ft.Text("2023-01-15")),
                        ft.DataCell(ft.Text("1 Years")),
                        ft.DataCell(ft.Text("$1500")),
                        ft.DataCell(ft.Text("Active")),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.LIGHT_GREEN_500, on_click=lambda e: print("Edit Clicked")),
                                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_500, on_click=lambda e: print("Delete Clicked"))
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Bio-Metric")),
                        ft.DataCell(ft.Text("ZKTeco")),
                        ft.DataCell(ft.Text("UA860")),
                        ft.DataCell(ft.Text("123456789")),
                        ft.DataCell(ft.Text("2023-01-15")),
                        ft.DataCell(ft.Text("1 Years")),
                        ft.DataCell(ft.Text("$1500")),
                        ft.DataCell(ft.Text("Active")),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.LIGHT_GREEN_500, on_click=lambda e: print("Edit Clicked")),
                                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_500, on_click=lambda e: print("Delete Clicked"))
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ),
                    ],
                ),
            ],
        )

        # Deployed DataTable
        deployed_table = ft.DataTable(
            width=5000,
            height=500,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=30,
            vertical_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            heading_row_color=ft.Colors.INDIGO_100,
            heading_text_style=ft.TextStyle(
                color=ft.Colors.INDIGO_900,
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            data_row_color={
                ft.ControlState.HOVERED: ft.Colors.LIGHT_BLUE_50,
            },
            data_row_min_height=50,
            data_text_style=ft.TextStyle(
                color=ft.Colors.GREY_800,
                size=14,
            ),
            show_checkbox_column=False,
            column_spacing=30,
            columns=[
                ft.DataColumn(ft.Text("Category", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Device Name", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Company", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Model", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Serial No", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Purchase Date", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Warranty", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Price", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Distibutor", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("City", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.W_600)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Bio-Metric")),
                        ft.DataCell(ft.Text("GRW01")),
                        ft.DataCell(ft.Text("ZKTeco")),
                        ft.DataCell(ft.Text("UA860")),
                        ft.DataCell(ft.Text("123456789")),
                        ft.DataCell(ft.Text("2023-01-15")),
                        ft.DataCell(ft.Text("1 Years")),
                        ft.DataCell(ft.Text("$1500")),
                        ft.DataCell(ft.Text("Bilal Traders")),
                        ft.DataCell(ft.Text("Gujranwala")),
                        ft.DataCell(ft.Text("Active")),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.LIGHT_GREEN_500, on_click=lambda e: print("Edit Clicked")),
                                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_500, on_click=lambda e: print("Delete Clicked"))
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ),
                    ],
                ),
                ft.DataRow(
                    cells=[
                       ft.DataCell(ft.Text("Bio-Metric")),
                        ft.DataCell(ft.Text("GRW01")),
                        ft.DataCell(ft.Text("ZKTeco")),
                        ft.DataCell(ft.Text("UA860")),
                        ft.DataCell(ft.Text("123456789")),
                        ft.DataCell(ft.Text("2023-01-15")),
                        ft.DataCell(ft.Text("1 Years")),
                        ft.DataCell(ft.Text("$1500")),
                        ft.DataCell(ft.Text("Bilal Traders")),
                        ft.DataCell(ft.Text("Gujranwala")),
                        ft.DataCell(ft.Text("Active")),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.LIGHT_GREEN_500, on_click=lambda e: print("Edit Clicked")),
                                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_500, on_click=lambda e: print("Delete Clicked"))
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ),
                    ],
                ),
            ],
        )

        # Tabs
        t = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Deployable",
                    content=ft.Container(
                        content=deployable_table,
                        alignment=ft.alignment.top_left,
                        expand=True,
                    )
                ),
                ft.Tab(
                    text="Deployed",
                    content=ft.Container(
                        content=deployed_table,
                        alignment=ft.alignment.top_left,
                        expand=True,
                    )
                ),
                
            ],
            expand=True,
        )
        # Layout
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
                                        
                                        add_device_button
                                    ],
                                    #alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                t
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=0,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

        page.update()


def SaleForcePage(page):
    return SaleForce(page)
