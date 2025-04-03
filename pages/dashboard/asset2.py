import flet as ft
from nav.sidebar import SidebarPage
from nav.menubar import TopBarPage
from components.manageasset import ManageAssetDialog
from components.assetdialog import AssetDialog
import mysql.connector

class AssetPagee(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page
        self.expand = True
        page.window.title = "Asset Management System - Assets"

        



        asset_dialog = AssetDialog(page)
        
        self.manage_Asset = ManageAssetDialog(page, self)


# Product Detail Banner Start############################################################################################################

        def close_banner(e):
            page.close(self.banner)
            page.add(ft.Text("Action clicked: " + e.control.text))

        action_button_style = ft.ButtonStyle(color=ft.Colors.BLUE)
        
        # Asset details
        asset_details = {
            "Name": "Laptop",
            "Category": "Electronics",
            "Company": "Dell",
            "Model": "XPS 15",
            "Serial No": "123456789",
            "Purchase Date": "2023-01-15",
            "Warranty": "2 Years",
            "Price": "$1500",
            "Status": "Available"
        }

        # Create asset detail rows
        asset_detail_rows = [
            ft.Row(
                controls=[
                    ft.Text(f"{key}: ", weight=ft.FontWeight.BOLD),
                    ft.Text(value)
                ]
            )
            for key, value in asset_details.items()
        ]

        self.banner = ft.Banner(
            bgcolor=ft.Colors.WHITE70,
            leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(
                                value="Asset Details:",
                                color=ft.Colors.BLACK,
                                weight=ft.FontWeight.BOLD,
                                size=20
                            ),
                            *asset_detail_rows
                        ],
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Image(
                            src="images/jojo.jpg",  # Replace with the actual image URL
                            width=150,
                            height=150,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        alignment=ft.alignment.center
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            actions=[
                ft.ElevatedButton(text="View", icon=ft.Icons.ACCESS_ALARM, width=100, style=action_button_style, on_click=close_banner),
                ft.TextButton(text="Ignore", style=action_button_style, on_click=close_banner),
                ft.TextButton(text="Cancel", style=action_button_style, on_click=close_banner),
            ],
        )
### Product Detail Banner End############################################################################################################

        # Add Asset Button
        add_asset_button = ft.ElevatedButton(
            icon=ft.Icons.ADD,
            text="Add Asset",
            bgcolor=ft.Colors.GREEN_400,
            width=150,
            height=50,
            color=ft.Colors.WHITE,
            on_click=lambda e: page.go('/assetform')  # Assuming you have a route for adding assets
        )

        # Example Asset Table (You can customize this part)
        mydb = mysql.connector.connect(
            host="200.200.200.23",
            user="root",
            password="Pak@123",
            database="itasset",
            auth_plugin='mysql_native_password'
        )
        mycur = mydb.cursor()
        mycur.execute("SELECT name, category, company, model, serial_no, purchaser, purchase_date, location, price, warranty, status FROM asset")
        myresult = mycur.fetchall()

        deployable_table = ft.DataTable(
            width=5000,
            height=500,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(0.5, "red"),
            border_radius=20,
            vertical_lines=ft.BorderSide(0.2, "blue"),
            horizontal_lines=ft.BorderSide(0.2, "green"),
            heading_row_color=ft.Colors.GREY_300,
            heading_row_height=100,
            heading_text_style=ft.TextStyle(
                color=ft.Colors.INDIGO_900,
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            data_row_color={ft.ControlState.HOVERED: "#6fa8dc"},
            column_spacing=30,
            columns=[
                ft.DataColumn(ft.Text("Name", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Category", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Company", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Model", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Serial No", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Purchaser", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Purchase Date", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Location", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Price", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Warranty", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.W_600)),
            ],
     

            rows=[ ],
        )
        for x in myresult:
            deployable_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(x[0])),
                        ft.DataCell(ft.Text(x[1])),
                        ft.DataCell(ft.Text(x[2])),
                        ft.DataCell(ft.Text(x[3])),
                        ft.DataCell(ft.Text(x[4])),
                        ft.DataCell(ft.Text(x[5])),
                        ft.DataCell(ft.Text(x[6])),
                        ft.DataCell(ft.Text(x[7])),
                        ft.DataCell(ft.Text(x[8])),
                        ft.DataCell(ft.Text(x[9])),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                            width=15,
                                            height=15,
                                            bgcolor=ft.Colors.LIGHT_GREEN_ACCENT_400,
                                            border_radius=10,  # Make it a circle
                                        ),
                                        ft.Text(x[10], color=ft.Colors.BLACK),
                                    ],
                                    spacing=10,  # Space between the circle and the text
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                bgcolor=ft.Colors.WHITE,
                                padding=10,  # Direct padding applied
                                border_radius=5
                            )
                        ),
                        ft.DataCell(ft.ElevatedButton("Manage", icon=ft.Icons.PENDING_ACTIONS, bgcolor=ft.Colors.BLUE_300, color=ft.Colors.WHITE, on_click=lambda e: self.manage_Asset.open())),
                    ],
                    selected=True,
                    on_select_changed=lambda e: self.show_banner(),  # Show banner on selection
                )
            )

        deployed_table = ft.DataTable(
            width=5000,
            height=500,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(0.5, "red"),
            border_radius=20,
            vertical_lines=ft.BorderSide(0.2, "blue"),
            horizontal_lines=ft.BorderSide(0.2, "green"),
            heading_row_color=ft.Colors.GREY_300,
            heading_row_height=100,
            heading_text_style=ft.TextStyle(
                color=ft.Colors.INDIGO_900,
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            data_row_color={ft.ControlState.HOVERED: "#6fa8dc"},
            column_spacing=30,
            columns=[
                ft.DataColumn(ft.Text("Category", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Company", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Model", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Assign To", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Department", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Company", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Assign Date", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.W_600)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Laptop")),
                        ft.DataCell(ft.Text("Dell")),
                        ft.DataCell(ft.Text("XPS 15")),
                        ft.DataCell(ft.Text("Abdul Salam")),
                        ft.DataCell(ft.Text("IT")),
                        ft.DataCell(ft.Text("GFI")),
                        ft.DataCell(ft.Text("19-02-2025")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                            width=15,
                                            height=15,
                                            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_700,
                                            border_radius=10,  # Make it a circle
                                        ),
                                        ft.Text("Assigned", color=ft.Colors.BLACK),
                                    ],
                                    spacing=10,  # Space between the circle and the text
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                bgcolor=ft.Colors.WHITE,
                                padding=10,  # Direct padding applied
                                border_radius=5
                            )
                        ),
                        ft.DataCell(ft.ElevatedButton("Manage", icon=ft.Icons.PENDING_ACTIONS, bgcolor=ft.Colors.BLUE_300, color=ft.Colors.WHITE, on_click=lambda e: self.show_manage_asset_bottomsheet())),
                    ],
                    selected=True,
                    on_select_changed=lambda e: self.show_banner(),  # Show banner on selection
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Mouse")),
                        ft.DataCell(ft.Text("Logitech")),
                        ft.DataCell(ft.Text("MX Master 3")),
                        ft.DataCell(ft.Text("Abdul Salam")),
                        ft.DataCell(ft.Text("IT")),
                        ft.DataCell(ft.Text("GFI")),
                        ft.DataCell(ft.Text("19-02-2025")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                            width=15,
                                            height=15,
                                            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_700,
                                            border_radius=10,  # Make it a circle
                                        ),
                                        ft.Text("Assigned", color=ft.Colors.BLACK),
                                    ],
                                    spacing=10,  # Space between the circle and the text
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                bgcolor=ft.Colors.WHITE,
                                padding=10,  # Direct padding applied
                                border_radius=5
                            )
                        ),
                        ft.DataCell(ft.ElevatedButton("Manage", icon=ft.Icons.PENDING_ACTIONS, bgcolor=ft.Colors.BLUE_300, color=ft.Colors.WHITE, on_click=lambda e: self.show_manage_asset_bottomsheet())),
                    ],
                    selected=True,
                    on_select_changed=lambda e: self.show_banner(),  # Show banner on selection
                ),
                # Add more rows as needed
            ],
        )

        faulted_table = ft.DataTable(
            width=5000,
            height=500,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(0.5, "red"),
            border_radius=20,
            vertical_lines=ft.BorderSide(0.2, "blue"),
            horizontal_lines=ft.BorderSide(0.2, "green"),
            heading_row_color=ft.Colors.GREY_300,
            heading_row_height=100,
            heading_text_style=ft.TextStyle(
                color=ft.Colors.INDIGO_900,
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            data_row_color={ft.ControlState.HOVERED: "#6fa8dc"},
            column_spacing=30,
            columns=[
                ft.DataColumn(ft.Text("Category", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Company", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Model", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Purchase Date", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Defected Date", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Reason", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Manage", weight=ft.FontWeight.W_600)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Laptop")),
                        ft.DataCell(ft.Text("Dell")),
                        ft.DataCell(ft.Text("XPS 15")),
                        ft.DataCell(ft.Text("19-02-2023")),
                        ft.DataCell(ft.Text("19-02-2024")),
                        ft.DataCell(ft.Text("Faulty Screen")),
                        ft.DataCell(ft.Text("Scraped")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                            width=15,
                                            height=15,
                                            bgcolor=ft.Colors.RED_ACCENT_400,
                                            border_radius=10,  # Make it a circle
                                        ),
                                        ft.Text("Disposed", color=ft.Colors.BLACK),
                                    ],
                                    spacing=10,  # Space between the circle and the text
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                bgcolor=ft.Colors.WHITE,
                                padding=10,  # Direct padding applied
                                border_radius=5
                            )
                        ),
                        ft.DataCell(ft.ElevatedButton("Manage", icon=ft.Icons.PENDING_ACTIONS, bgcolor=ft.Colors.BLUE_300, color=ft.Colors.WHITE, on_click=lambda e: self.show_manage_asset_bottomsheet())),
                    ],
                    selected=True,
                    on_select_changed=lambda e: self.show_banner(),  # Show banner on selection
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Mouse")),
                        ft.DataCell(ft.Text("Logitech")),
                        ft.DataCell(ft.Text("MX Master 3")),
                        ft.DataCell(ft.Text("987654321")),
                        ft.DataCell(ft.Text("2023-06-01")),
                        ft.DataCell(ft.Text("1 Year")),
                        ft.DataCell(ft.Text("$100")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                            width=15,
                                            height=15,
                                            bgcolor=ft.Colors.YELLOW_ACCENT_400,
                                            border_radius=10,  # Make it a circle
                                        ),
                                        ft.Text("Sold", color=ft.Colors.BLACK),
                                    ],
                                    spacing=10,  # Space between the circle and the text
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                bgcolor=ft.Colors.WHITE,
                                padding=10,  # Direct padding applied
                                border_radius=5
                            )
                        ),
                        ft.DataCell(ft.ElevatedButton("Manage", icon=ft.Icons.PENDING_ACTIONS, bgcolor=ft.Colors.BLUE_300, color=ft.Colors.WHITE, on_click=lambda e: self.show_manage_asset_bottomsheet())),
                    ],
                    selected=True,
                    on_select_changed=lambda e: self.show_banner(),  # Show banner on selection
                ),
                # Add more rows as needed
            ],
        )

        t = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Available",
                    content=ft.Container(
                        content=deployable_table,
                        alignment=ft.alignment.top_left,
                        expand=True,
                    )
                ),
                ft.Tab(
                    text="Assigned",
                    content=ft.Container(
                        content=deployed_table,
                        alignment=ft.alignment.top_left,
                        expand=True,
                    )
                ),
                ft.Tab(
                    text="Disposed/Sold",
                    content=ft.Container(
                        content=faulted_table,
                        alignment=ft.alignment.top_left,
                        expand=True,
                    )
                ),
            ],
            expand=True,
        )

        # Page Layout
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
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        add_asset_button
                                    ],
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
        

    def show_banner(self):
        self.page.open(self.banner)
    
    def show_asset_dialog(self):
        self.page.open(self.page_asset_dialog)


    
        





def asset_page(page):
    return AssetPagee(page)