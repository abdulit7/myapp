import flet as ft
import mysql.connector
import os.path
#from components.manageconsumable import ManageConsumableDialog
from components.assetdialog import AssetDialog

class Consumables(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True

        page.window.title = "Asset Management System - Consumables"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.START

        # Supported image extensions
        self.supported_image_extensions = {".jpg", ".jpeg", ".png", ".gif"}

        # Fetch and cache category data
        self.category_map = {}
        connection = self._get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id, name FROM category WHERE type = 'Consumable'")
                self.category_map = {row[0]: row[1] for row in cursor.fetchall()}
                print(f"Cached categories: {self.category_map}")
            except mysql.connector.Error as err:
                print(f"Error fetching categories: {err}")
                self.page.open(ft.SnackBar(ft.Text(f"Error fetching categories: {err}"), duration=4000))
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("Database connection closed")

        # Initialize dialogs
        self.asset_dialog = AssetDialog(page)
        #self.manage_consumable = ManageConsumableDialog(page, self)

        # Product Detail Banner
        def close_banner(e):
            page.close(self.banner)

        action_button_style = ft.ButtonStyle(color=ft.Colors.BLUE)
        banner_content = ft.Row(  # Fixed typo: 'ftuegosRow' to 'ft.Row'
            controls=[
                ft.Column(
                    controls=[ft.Text("Consumable Details:", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, size=20)],
                    expand=True,
                ),
                ft.Container(
                    content=ft.Image(
                        src="/images/placeholder.jpg",
                        width=150,
                        height=150,
                        fit=ft.ImageFit.CONTAIN,
                        error_content=ft.Text("Banner image not found"),
                    ),
                    alignment=ft.alignment.center,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.banner = ft.Banner(
            bgcolor=ft.Colors.WHITE70,
            leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
            content=banner_content,
            actions=[
                ft.ElevatedButton(text="View", icon=ft.Icons.ACCESS_ALARM, width=100, style=action_button_style, on_click=close_banner),
                ft.TextButton(text="Ignore", style=action_button_style, on_click=close_banner),
                ft.TextButton(text="Cancel", style=action_button_style, on_click=close_banner),
            ],
        )

        # Add Consumable Button
        self.add_consumable_button = ft.ElevatedButton(
            icon=ft.Icons.ADD,
            text="Add Consumable",
            on_click=lambda e: page.go('/consumableform'),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_500,
                color=ft.Colors.WHITE,
                padding=ft.Padding(16, 12, 16, 12),
                shape=ft.RoundedRectangleBorder(radius=12),
                overlay_color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                elevation=6,
            ),
            width=180,
            height=55,
        )

        # Category dropdown
        self.category_dropdown = ft.Dropdown(
            label="Select Category",
            options=[
                ft.dropdown.Option(key=str(id), text=name)
                for id, name in self.category_map.items()
            ] + [ft.dropdown.Option(key="all", text="All Categories")],
            value="all",
            width=200,
        )

        # Filter button
        self.filter_button = ft.ElevatedButton(
            text="Filter",
            icon=ft.Icons.FILTER_LIST,
            on_click=self.filter_consumables,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_500,
                color=ft.Colors.WHITE,
                padding=ft.Padding(16, 12, 16, 12),
                shape=ft.RoundedRectangleBorder(radius=12),
                elevation=6,
            ),
            width=120,
            height=55,
        )

        # Fetch consumable data
        self.consumable_data = self._fetch_consumables()
        self.deployed_data = self._fetch_deployed_consumables()

        # Fallback UI for empty tabs
        no_consumables_message = ft.Container(
            content=ft.Text(
                "No Consumables Found",
                size=20,
                color=ft.Colors.RED_700,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.all(50),
        )

        self.deployable_cards = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self.create_consumable_card(
                        data=x,
                        status_color=ft.Colors.LIGHT_GREEN_ACCENT_400,
                        on_manage_click=lambda id, name: self.manage_consumable.open(consumable_id=id, name=name),
                        on_select=lambda e, consumable=x: self.show_banner(consumable=x, is_deployed=False),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for x in self.consumable_data
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            run_spacing=0,
        )

        self.deployed_cards = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self.create_deployed_card(
                        data=data,
                        status_color=ft.Colors.LIGHT_BLUE_ACCENT_700,
                        on_manage_click=lambda e: self.show_manage_consumable_bottomsheet(),
                        on_select=lambda e, consumable=data: self.show_banner(consumable=data, is_deployed=True),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for data in self.deployed_data
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            run_spacing=0,
        )

        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Available",
                    content=ft.Column(
                        controls=[self.deployable_cards if self.consumable_data else no_consumables_message],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    )
                ),
                ft.Tab(
                    text="Assigned",
                    content=ft.Column(
                        controls=[self.deployed_cards if self.deployed_data else no_consumables_message],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    )
                ),
            ],
            expand=True,
        )

        self.content = ft.Column(
            controls=[
                ft.Divider(height=1, color=ft.Colors.WHITE),
                ft.Row(
                    controls=[
                        self.add_consumable_button,
                        self.category_dropdown,
                        self.filter_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                ),
                self.tabs,
            ],
            expand=True,
            spacing=10,
        )

        page.update()

    def _get_db_connection(self):
        """Establish and return a database connection."""
        try:
            connection = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            print("Database connection successful")
            return connection
        except mysql.connector.Error as error:
            print(f"Database connection failed: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Database error: {error}"), duration=4000))
            return None

    def _fetch_consumables(self, category_id=None):
        """Fetch available consumables from the database, optionally filtered by category."""
        connection = self._get_db_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor()
            query = """
                SELECT id, name, category_id, company, model, status, image_path
                FROM consumable
            """
            params = []
            if category_id and category_id != "all":
                query += " WHERE category_id = %s"
                params.append(int(category_id))

            cursor.execute(query, params)
            consumable_data_raw = cursor.fetchall()
            consumable_data = [
                (row[0], row[1], self.category_map.get(row[2], "Unknown"), row[3], row[4], row[5], row[6])
                for row in consumable_data_raw
            ]
            print(f"Query returned {len(consumable_data)} rows from consumable: {consumable_data}")
            return consumable_data
        except mysql.connector.Error as err:
            print(f"Query failed for consumable: {err}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching consumables: {err}"), duration=4000))
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Database connection closed")

    def _fetch_deployed_consumables(self, category_id=None):
        """Fetch deployed consumables from the database, optionally filtered by category."""
        connection = self._get_db_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor()
            query = """
                SELECT dc.id, dc.name, dc.category_id, dc.company, dc.model, 
                       u.name AS deployed_to_name, u.emp_id AS deployed_to_emp_id, 
                       dc.user_department, dc.deploy_date, dc.image_path
                FROM deployed_consumables dc
                LEFT JOIN users u ON dc.deployed_to = u.id
            """
            params = []
            if category_id and category_id != "all":
                query += " WHERE dc.category_id = %s"
                params.append(int(category_id))

            cursor.execute(query, params)
            deployed_data_raw = cursor.fetchall()
            deployed_data = [
                (
                    row[0],  # Consumable ID
                    row[1],  # Consumable Name
                    self.category_map.get(row[2], "Unknown"),  # Category Name
                    row[3],  # Company
                    row[4],  # Model
                    f"{row[5]} (Emp ID: {row[6]})" if row[5] and row[6] else "Not Assigned",  # Deployed To
                    row[7],  # User Department
                    row[8],  # Deploy Date
                    row[9],  # Image Path
                )
                for row in deployed_data_raw
            ]
            print(f"Query returned {len(deployed_data)} rows from deployed_consumables: {deployed_data}")
            return deployed_data
        except mysql.connector.Error as err:
            print(f"Query failed for deployed_consumables: {err}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching deployed consumables: {err}"), duration=4000))
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Database connection closed")

    def _is_supported_image_format(self, image_path: str) -> bool:
        """Check if the image path has a supported extension (jpg, jpeg, png, gif)."""
        if not image_path:
            return False
        _, ext = os.path.splitext(image_path.lower())
        return ext in self.supported_image_extensions

    def show_banner(self, consumable=None, is_deployed=False):
        """Display consumable details in a banner."""
        if consumable:
            connection = self._get_db_connection()
            if not connection:
                return

            try:
                cursor = connection.cursor()
                if is_deployed:
                    cursor.execute(
                        """
                        SELECT name, category_id, company, model, purchaser, location, price,
                               purchase_date, image_path, deployed_to, user_department, deploy_date
                        FROM deployed_consumables WHERE id = %s
                        """,
                        (consumable[0],)
                    )
                    consumable_data = cursor.fetchone()
                    if consumable_data:
                        consumable_details = {
                            "Name": str(consumable_data[0]) if consumable_data[0] is not None else "",
                            "Category": self.category_map.get(consumable_data[1], "Unknown"),
                            "Company": str(consumable_data[2]) if consumable_data[2] is not None else "",
                            "Model": str(consumable_data[3]) if consumable_data[3] is not None else "",
                            "Purchaser": str(consumable_data[4]) if consumable_data[4] is not None else "",
                            "Location": str(consumable_data[5]) if consumable_data[5] is not None else "",
                            "Price": f"${consumable_data[6]}" if consumable_data[6] is not None else "",
                            "Purchase Date": str(consumable_data[7]) if consumable_data[7] is not None else "",
                            "Status": "Deployed",
                            "Deployed To": str(consumable_data[9]) if consumable_data[9] is not None else "",
                            "Department": str(consumable_data[10]) if consumable_data[10] is not None else "",
                            "Deploy Date": str(consumable_data[11]) if consumable_data[11] is not None else "",
                        }
                        image_path = str(consumable_data[8]) if consumable_data[8] is not None else None
                    else:
                        consumable_details = {"Name": "Consumable not found"}
                        image_path = None
                else:
                    cursor.execute(
                        """
                        SELECT name, category_id, company, model, purchaser, location, price,
                               purchase_date, image_path, status
                        FROM consumable WHERE id = %s
                        """,
                        (consumable[0],)
                    )
                    consumable_data = cursor.fetchone()
                    if consumable_data:
                        consumable_details = {
                            "Name": str(consumable_data[0]) if consumable_data[0] is not None else "",
                            "Category": self.category_map.get(consumable_data[1], "Unknown"),
                            "Company": str(consumable_data[2]) if consumable_data[2] is not None else "",
                            "Model": str(consumable_data[3]) if consumable_data[3] is not None else "",
                            "Purchaser": str(consumable_data[4]) if consumable_data[4] is not None else "",
                            "Location": str(consumable_data[5]) if consumable_data[5] is not None else "",
                            "Price": f"${consumable_data[6]}" if consumable_data[6] is not None else "",
                            "Purchase Date": str(consumable_data[7]) if consumable_data[7] is not None else "",
                            "Status": str(consumable_data[9]) if consumable_data[9] is not None else "",
                        }
                        image_path = str(consumable_data[8]) if consumable_data[8] is not None else None
                    else:
                        consumable_details = {"Name": "Consumable not found"}
                        image_path = None

            except mysql.connector.Error as err:
                print(f"Error fetching consumable details: {err}")
                consumable_details = {"Name": "Error loading consumable details"}
                image_path = None
                self.page.open(ft.SnackBar(ft.Text(f"Error fetching consumable details: {err}"), duration=4000))
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("Database connection closed")

            consumable_detail_rows = [
                ft.Row(controls=[ft.Text(f"{key}: ", weight=ft.FontWeight.BOLD), ft.Text(value)])
                for key, value in consumable_details.items() if value
            ]

            if image_path and image_path.startswith("/images/") and self._is_supported_image_format(image_path):
                image_content = ft.Image(
                    src=image_path,
                    width=150,
                    height=150,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Text("Failed to load image"),
                )
            else:
                image_content = ft.Image(
                    src="/images/placeholder.jpg",
                    width=150,
                    height=150,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Text("Placeholder image not found"),
                )
                if image_path:
                    print(f"Unsupported or invalid image format for banner: {image_path}")
                    self.page.open(ft.SnackBar(
                        ft.Text(f"Unsupported image format in banner: {image_path}. Supported formats are jpg, jpeg, png, gif."),
                        duration=4000
                    ))

            self.banner.content.controls[0].controls = [
                ft.Text("Consumable Details:", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, size=20)
            ] + consumable_detail_rows
            self.banner.content.controls[1].content = image_content

        self.page.open(self.banner)

    def show_manage_consumable_bottomsheet(self):
        """Show the manage consumable bottom sheet."""
        self.page.show_bottom_sheet(self.manage_consumable)

    def create_consumable_card(self, data, status_color, on_manage_click, on_select):
        """Create a card for an available consumable."""
        consumable_id = data[0]
        name = str(data[1]) if data[1] is not None else ""
        category = str(data[2]) if data[2] is not None else ""
        company = str(data[3]) if data[3] is not None else ""
        model = str(data[4]) if data[4] is not None else ""
        status = str(data[5]) if data[5] is not None else ""
        image_path = str(data[6]) if data[6] is not None else None

        print(f"Processing consumable: {name}, image_path: {image_path}")
        image_content = None
        if image_path and image_path.startswith("/images/") and self._is_supported_image_format(image_path):
            image_content = ft.Image(
                src=image_path,
                width=120,
                height=120,
                fit=ft.ImageFit.CONTAIN,
                error_content=ft.Text("Failed to load image"),
            )
        else:
            print(f"Unsupported or invalid image format for consumable {name}: {image_path}")
            if image_path:
                self.page.open(ft.SnackBar(
                    ft.Text(f"Unsupported image format for consumable {name}: {image_path}. Supported formats are jpg, jpeg, png, gif."),
                    duration=4000
                ))

        card_content = [
            ft.Row(
                [
                    ft.Text(f"Name: {name}", size=16, weight=ft.FontWeight.BOLD, color="#263238"),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(width=15, height=15, bgcolor=status_color, border_radius=10),
                                ft.Text(status, color=ft.Colors.BLACK),
                            ],
                            spacing=5,
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        alignment=ft.alignment.center_right,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Text(f"Category: {category}", size=14, color="#263238"),
            ft.Text(f"Company: {company}", size=14, color="#263238"),
            ft.Text(f"Model: {model}", size=14, color="#263238"),
            ft.ElevatedButton(
                "Manage",
                icon=ft.Icons.PENDING_ACTIONS,
                bgcolor=ft.Colors.BLUE_300,
                color=ft.Colors.WHITE,
                on_click=lambda e: on_manage_click(consumable_id, name),
                width=100,
            ),
        ]

        if image_content:
            card_content.insert(0, ft.Container(
                content=image_content,
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=10),
            ))

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    card_content,
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=15,
                bgcolor="#E3F2FD",
                border_radius=12,
                ink=True,
                on_click=lambda e: on_select(e, data),
                width=300,
                height=340 if image_content else 300,
            ),
            elevation=5,
        )

    def create_deployed_card(self, data, status_color, on_manage_click, on_select):
        """Create a card for a deployed consumable."""
        consumable_id = data[0]
        name = str(data[1]) if data[1] is not None else ""
        category = str(data[2]) if data[2] is not None else ""
        company = str(data[3]) if data[3] is not None else ""
        model = str(data[4]) if data[4] is not None else ""
        deployed_to = str(data[5]) if data[5] is not None else ""
        user_department = str(data[6]) if data[6] is not None else ""
        deploy_date = str(data[7]) if data[7] is not None else ""
        image_path = str(data[8]) if data[8] is not None else None

        print(f"Processing deployed consumable: {name}, image_path: {image_path}")
        image_content = None
        if image_path and image_path.startswith("/images/") and self._is_supported_image_format(image_path):
            image_content = ft.Image(
                src=image_path,
                width=120,
                height=120,
                fit=ft.ImageFit.CONTAIN,
                error_content=ft.Text("Failed to load image"),
            )
        else:
            print(f"Unsupported or invalid image format for deployed consumable {name}: {image_path}")
            if image_path:
                self.page.open(ft.SnackBar(
                    ft.Text(f"Unsupported image format for deployed consumable {name}: {image_path}. Supported formats are jpg, jpeg, png, gif."),
                    duration=4000
                ))

        card_content = [
            ft.Row(
                [
                    ft.Text(f"Name: {name}", size=16, weight=ft.FontWeight.BOLD, color="#263238"),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(width=15, height=15, bgcolor=status_color, border_radius=10),
                                ft.Text("Assigned", color=ft.Colors.BLACK),
                            ],
                            spacing=5,
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        alignment=ft.alignment.center_right,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Text(f"Category: {category}", size=14, color="#263238"),
            ft.Text(f"Company: {company}", size=14, color="#263238"),
            ft.Text(f"Model: {model}", size=14, color="#263238"),
            ft.Text(f"Assigned To: {deployed_to}", size=14, color="#263238"),
            ft.Text(f"Department: {user_department}", size=14, color="#263238"),
            ft.Text(f"Deploy Date: {deploy_date}", size=14, color="#263238"),
            ft.ElevatedButton(
                "Manage",
                icon=ft.Icons.PENDING_ACTIONS,
                bgcolor=ft.Colors.BLUE_300,
                color=ft.Colors.WHITE,
                on_click=on_manage_click,
                width=100,
            ),
        ]

        if image_content:
            card_content.insert(0, ft.Container(
                content=image_content,
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=10),
            ))

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    card_content,
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=15,
                bgcolor="#E3F2FD",
                border_radius=12,
                ink=True,
                on_click=lambda e: on_select(e, data),
                width=300,
                height=340 if image_content else 300,
            ),
            elevation=5,
        )

    def filter_consumables(self, e):
        """Handle filter button click to fetch consumables by selected category."""
        selected_category = self.category_dropdown.value
        print(f"Filtering consumables by category: {selected_category}")
        self.refresh_cards(category_id=selected_category)

    def refresh_cards(self, category_id=None):
        """Refresh the consumable cards by re-fetching data, optionally filtered by category."""
        try:
            self.consumable_data = self._fetch_consumables(category_id=category_id)
            self.deployed_data = self._fetch_deployed_consumables(category_id=category_id)

            self.deployable_cards.controls = [
                ft.Container(
                    content=self.create_consumable_card(
                        data=x,
                        status_color=ft.Colors.LIGHT_GREEN_ACCENT_400,
                        on_manage_click=lambda id, name: self.manage_consumable.open(consumable_id=id, name=name),
                        on_select=lambda e, consumable=x: self.show_banner(consumable=x, is_deployed=False),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for x in self.consumable_data
            ]

            self.deployed_cards.controls = [
                ft.Container(
                    content=self.create_deployed_card(
                        data=data,
                        status_color=ft.Colors.LIGHT_BLUE_ACCENT_700,
                        on_manage_click=lambda e: self.show_manage_consumable_bottomsheet(),
                        on_select=lambda e, consumable=data: self.show_banner(consumable=data, is_deployed=True),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for data in self.deployed_data
            ]

            self.page.update()

        except mysql.connector.Error as err:
            print(f"Error refreshing cards: {err}")
            self.page.open(ft.SnackBar(ft.Text(f"Error refreshing cards: {err}"), duration=4000))

def consumables_page(page):
    return Consumables(page)