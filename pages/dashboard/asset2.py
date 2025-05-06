import flet as ft
import mysql.connector
from components.manageasset import ManageAssetDialog
from components.assetdialog import AssetDialog
import os.path

class AssetPagee(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True

        page.window.title = "Asset Management System - Assets"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.START

        # Supported image extensions
        self.supported_image_extensions = {".jpg", ".jpeg", ".png", ".gif"}

        # Fetch and cache category data to avoid repeated JOINs
        self.category_map = {}
        connection = self._get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id, name FROM category")
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
        self.manage_Asset = ManageAssetDialog(page, self)

        # Product Detail Banner
        def close_banner(e):
            page.close(self.banner)

        action_button_style = ft.ButtonStyle(color=ft.Colors.BLUE)

        # Placeholder banner content (will be updated dynamically)
        banner_content = ft.Row(
            controls=[
                ft.Column(
                    controls=[ft.Text("Asset Details:", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, size=20)],
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

        self.add_asset_button = ft.ElevatedButton(
            icon=ft.Icons.ADD,
            text="Add Asset",
            on_click=lambda e: page.go('/assetform'),
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
            on_click=self.filter_assets,
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

        # Fetch asset data
        self.asset_data = self._fetch_assets()
        self.deployed_data = self._fetch_deployed_assets()
        self.disposed_data = self._fetch_disposed_assets()

        # Fallback UI for empty tabs
        no_assets_message = ft.Container(
            content=ft.Text(
                "No Assets Found",
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
                    content=self.create_asset_card(
                        data=x,
                        status_color=ft.Colors.LIGHT_GREEN_ACCENT_400,
                        on_manage_click=lambda id, name: self.manage_Asset.open(asset_id=id, name=name),
                        on_select=lambda e, asset=x: self.show_banner(asset=asset, is_deployed=False),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for x in self.asset_data
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
                        on_manage_click=lambda e: self.show_manage_asset_bottomsheet(),
                        on_select=lambda e, asset=data: self.show_banner(asset=asset, is_deployed=True),
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

        self.disposed_cards = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self.create_disposed_card(
                        data=data,
                        status_color=ft.Colors.RED_ACCENT_400 if data[7] == "Scrap" else (ft.Colors.YELLOW_ACCENT_400 if data[7] == "Sold" else ft.Colors.GREY_400),
                        on_manage_click=lambda e: self.show_manage_asset_bottomsheet(),
                        on_select=lambda e, asset=data: self.show_banner(asset=asset, is_disposed=True),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for data in self.disposed_data
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
                        controls=[self.deployable_cards if self.asset_data else no_assets_message],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    )
                ),
                ft.Tab(
                    text="Assigned",
                    content=ft.Column(
                        controls=[self.deployed_cards if self.deployed_data else no_assets_message],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    )
                ),
                ft.Tab(
                    text="Disposed/Sold",
                    content=ft.Column(
                        controls=[self.disposed_cards if self.disposed_data else no_assets_message],
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
                        self.add_asset_button,
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

    def _fetch_assets(self, category_id=None):
        """Fetch available assets from the database, optionally filtered by category."""
        connection = self._get_db_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor()
            query = """
                SELECT id, name, category_id, company, model, status, image_path
                FROM assets
            """
            params = []
            if category_id and category_id != "all":
                query += " WHERE category_id = %s"
                params.append(int(category_id))

            cursor.execute(query, params)
            asset_data_raw = cursor.fetchall()
            # Map category_id to category name using the cached category_map
            asset_data = [
                (row[0], row[1], self.category_map.get(row[2], "Unknown"), row[3], row[4], row[5], row[6])
                for row in asset_data_raw
            ]
            print(f"Query returned {len(asset_data)} rows from assets: {asset_data}")
            return asset_data
        except mysql.connector.Error as err:
            print(f"Query failed for assets: {err}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching assets: {err}"), duration=4000))
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Database connection closed")

    def _fetch_deployed_assets(self, category_id=None):
        """Fetch deployed assets from the database, optionally filtered by category."""
        connection = self._get_db_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor()
            query = """
                SELECT da.id, da.name, da.category_id, da.company, da.model, 
                    u.name AS deployed_to_name, u.emp_id AS deployed_to_emp_id, 
                    da.user_department, da.deploy_date, da.image_path
                FROM deployed_assets da
                LEFT JOIN users u ON da.deployed_to = u.id
            """
            params = []
            if category_id and category_id != "all":
                query += " WHERE da.category_id = %s"
                params.append(int(category_id))

            cursor.execute(query, params)
            deployed_data_raw = cursor.fetchall()
            # Map category_id to category name using the cached category_map
            deployed_data = [
                (
                    row[0],  # Asset ID
                    row[1],  # Asset Name
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
            print(f"Query returned {len(deployed_data)} rows from deployed_assets: {deployed_data}")
            return deployed_data
        except mysql.connector.Error as err:
            print(f"Query failed for deployed_assets: {err}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching deployed assets: {err}"), duration=4000))
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Database connection closed")

    def _fetch_disposed_assets(self, category_id=None):
        """Fetch disposed assets from the database, optionally filtered by category."""
        connection = self._get_db_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor()
            query = """
                SELECT id, name, category_id, company, model, purchase_date, disposal_date, disposal_type,
                       amount_earned, disposal_reason, disposal_location, sale_details, sold_to, image_path
                FROM disposed_assets
            """
            params = []
            if category_id and category_id != "all":
                query += " WHERE category_id = %s"
                params.append(int(category_id))

            cursor.execute(query, params)
            disposed_data_raw = cursor.fetchall()
            # Map category_id to category name using the cached category_map
            disposed_data = [
                (row[0], row[1], self.category_map.get(row[2], "Unknown"), row[3], row[4], row[5], row[6], row[7],
                 row[8], row[9], row[10], row[11], row[12], row[13])
                for row in disposed_data_raw
            ]
            print(f"Query returned {len(disposed_data)} rows from disposed_assets: {disposed_data}")
            return disposed_data
        except mysql.connector.Error as err:
            print(f"Query failed for disposed_assets: {err}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching disposed assets: {err}"), duration=4000))
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

    def show_banner(self, asset=None, is_deployed=False, is_disposed=False):
        """Display asset details in a banner."""
        if asset:
            connection = self._get_db_connection()
            if not connection:
                return

            try:
                cursor = connection.cursor()
                if is_deployed:
                    cursor.execute(
                        """
                        SELECT name, category_id, company, model, serial_no, purchaser, location, price, warranty,
                               bill_copy, purchase_date, image_path, deployed_to, user_department, deploy_date
                        FROM deployed_assets WHERE id = %s
                        """,
                        (asset[0],)
                    )
                    asset_data = cursor.fetchone()
                    if asset_data:
                        asset_details = {
                            "Name": str(asset_data[0]) if asset_data[0] is not None else "",
                            "Category": self.category_map.get(asset_data[1], "Unknown"),
                            "Company": str(asset_data[2]) if asset_data[2] is not None else "",
                            "Model": str(asset_data[3]) if asset_data[3] is not None else "",
                            "Serial No": str(asset_data[4]) if asset_data[4] is not None else "",
                            "Purchaser": str(asset_data[5]) if asset_data[5] is not None else "",
                            "Location": str(asset_data[6]) if asset_data[6] is not None else "",
                            "Price": f"${asset_data[7]}" if asset_data[7] is not None else "",
                            "Warranty": str(asset_data[8]) if asset_data[8] is not None else "",
                            "Status": "Deployed",
                            "Deployed To": str(asset_data[12]) if asset_data[12] is not None else "",
                            "Department": str(asset_data[13]) if asset_data[13] is not None else "",
                            "Deploy Date": str(asset_data[14]) if asset_data[14] is not None else "",
                        }
                        image_path = str(asset_data[11]) if asset_data[11] is not None else None
                    else:
                        asset_details = {"Name": "Asset not found"}
                        image_path = None
                elif is_disposed:
                    cursor.execute(
                        """
                        SELECT name, category_id, company, model, serial_no, purchaser, location, price, warranty,
                               bill_copy, purchase_date, image_path, disposal_type, disposal_date, amount_earned,
                               disposal_reason, disposal_location, sale_details, sold_to
                        FROM disposed_assets WHERE id = %s
                        """,
                        (asset[0],)
                    )
                    asset_data = cursor.fetchone()
                    if asset_data:
                        asset_details = {
                            "Name": str(asset_data[0]) if asset_data[0] is not None else "",
                            "Category": self.category_map.get(asset_data[1], "Unknown"),
                            "Company": str(asset_data[2]) if asset_data[2] is not None else "",
                            "Model": str(asset_data[3]) if asset_data[3] is not None else "",
                            "Serial No": str(asset_data[4]) if asset_data[4] is not None else "",
                            "Purchaser": str(asset_data[5]) if asset_data[5] is not None else "",
                            "Location": str(asset_data[6]) if asset_data[6] is not None else "",
                            "Price": f"${asset_data[7]}" if asset_data[7] is not None else "",
                            "Warranty": str(asset_data[8]) if asset_data[8] is not None else "",
                            "Purchase Date": str(asset_data[10]) if asset_data[10] is not None else "",
                            "Disposal Type": str(asset_data[12]) if asset_data[12] is not None else "",
                            "Disposal Date": str(asset_data[13]) if asset_data[13] is not None else "",
                        }
                        if asset_data[14] is not None:  # amount_earned
                            asset_details["Amount Earned"] = f"${asset_data[14]}"
                        if asset_data[15]:  # disposal_reason
                            asset_details["Disposal Reason"] = str(asset_data[15])
                        if asset_data[16]:  # disposal_location
                            asset_details["Disposal Location"] = str(asset_data[16])
                        if asset_data[17]:  # sale_details
                            asset_details["Sale Details"] = str(asset_data[17])
                        if asset_data[18]:  # sold_to
                            asset_details["Sold To"] = str(asset_data[18])
                        image_path = str(asset_data[11]) if asset_data[11] is not None else None
                    else:
                        asset_details = {"Name": "Asset not found"}
                        image_path = None
                else:
                    cursor.execute(
                        """
                        SELECT name, category_id, company, model, serial_no, purchaser, location, price, warranty,
                               bill_copy, purchase_date, image_path, status
                        FROM assets WHERE id = %s
                        """,
                        (asset[0],)
                    )
                    asset_data = cursor.fetchone()
                    if asset_data:
                        asset_details = {
                            "Name": str(asset_data[0]) if asset_data[0] is not None else "",
                            "Category": self.category_map.get(asset_data[1], "Unknown"),
                            "Company": str(asset_data[2]) if asset_data[2] is not None else "",
                            "Model": str(asset_data[3]) if asset_data[3] is not None else "",
                            "Serial No": str(asset_data[4]) if asset_data[4] is not None else "",
                            "Purchaser": str(asset_data[5]) if asset_data[5] is not None else "",
                            "Location": str(asset_data[6]) if asset_data[6] is not None else "",
                            "Price": f"${asset_data[7]}" if asset_data[7] is not None else "",
                            "Warranty": str(asset_data[8]) if asset_data[8] is not None else "",
                            "Purchase Date": str(asset_data[10]) if asset_data[10] is not None else "",
                            "Status": str(asset_data[12]) if asset_data[12] is not None else "",
                        }
                        image_path = str(asset_data[11]) if asset_data[11] is not None else None
                    else:
                        asset_details = {"Name": "Asset not found"}
                        image_path = None

            except mysql.connector.Error as err:
                print(f"Error fetching asset details: {err}")
                asset_details = {"Name": "Error loading asset details"}
                image_path = None
                self.page.open(ft.SnackBar(ft.Text(f"Error fetching asset details: {err}"), duration=4000))
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("Database connection closed")

            # Create asset detail rows for the banner
            asset_detail_rows = [
                ft.Row(controls=[ft.Text(f"{key}: ", weight=ft.FontWeight.BOLD), ft.Text(value)])
                for key, value in asset_details.items() if value
            ]

            # Validate and update the banner's image
            if image_path and image_path.startswith("/images/") and self._is_supported_image_format(image_path):
                image_content = ft.Image(
                    src=image_path,
                    width=600,
                    height=500,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Text("Failed to load image"),
                )
            else:
                image_content = ft.Image(
                    src="/images/placeholder.jpg",
                    width=600,
                    height=500,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Text("Placeholder image not found"),
                )
                if image_path:
                    print(f"Unsupported or invalid image format for banner: {image_path}")
                    self.page.open(ft.SnackBar(
                        ft.Text(f"Unsupported image format in banner: {image_path}. Supported formats are jpg, jpeg, png, gif."),
                        duration=4000
                    ))

            # Update the banner content
            self.banner.content.controls[0].controls = [
                ft.Text("Asset Details:", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, size=20)
            ] + asset_detail_rows
            self.banner.content.controls[1].content = image_content

        self.page.open(self.banner)

    def show_manage_asset_bottomsheet(self):
        self.page.show_bottom_sheet(self.manage_Asset)

    def create_asset_card(self, data, status_color, on_manage_click, on_select):
        """Create a card for an available asset."""
        asset_id = data[0]
        name = str(data[1]) if data[1] is not None else ""
        category = str(data[2]) if data[2] is not None else ""
        company = str(data[3]) if data[3] is not None else ""
        model = str(data[4]) if data[4] is not None else ""
        status = str(data[5]) if data[5] is not None else ""
        image_path = str(data[6]) if data[6] is not None else None

        # Debug image path
        print(f"Processing asset: {name}, image_path: {image_path}")
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
            print(f"Unsupported or invalid image format for asset {name}: {image_path}")
            if image_path:
                self.page.open(ft.SnackBar(
                    ft.Text(f"Unsupported image format for asset {name}: {image_path}. Supported formats are jpg, jpeg, png, gif."),
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
                on_click=lambda e: on_manage_click(asset_id, name),
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
        """Create a card for a deployed asset."""
        asset_id = data[0]
        name = str(data[1]) if data[1] is not None else ""
        category = str(data[2]) if data[2] is not None else ""
        company = str(data[3]) if data[3] is not None else ""
        model = str(data[4]) if data[4] is not None else ""
        deployed_to = str(data[5]) if data[5] is not None else ""
        user_department = str(data[6]) if data[6] is not None else ""
        deploy_date = str(data[7]) if data[7] is not None else ""
        image_path = str(data[8]) if data[8] is not None else None

        # Debug image path
        print(f"Processing deployed asset: {name}, image_path: {image_path}")
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
            print(f"Unsupported or invalid image format for deployed asset {name}: {image_path}")
            if image_path:
                self.page.open(ft.SnackBar(
                    ft.Text(f"Unsupported image format for deployed asset {name}: {image_path}. Supported formats are jpg, jpeg, png, gif."),
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

    def create_disposed_card(self, data, status_color, on_manage_click, on_select):
        """Create a card for a disposed asset."""
        asset_id = data[0]
        name = str(data[1]) if data[1] is not None else ""
        category = str(data[2]) if data[2] is not None else ""
        company = str(data[3]) if data[3] is not None else ""
        model = str(data[4]) if data[4] is not None else ""
        purchase_date = str(data[5]) if data[5] is not None else ""
        disposal_date = str(data[6]) if data[6] is not None else ""
        disposal_type = str(data[7]) if data[7] is not None else ""
        amount_earned = f"${data[8]}" if data[8] is not None else ""
        disposal_reason = str(data[9]) if data[9] is not None else ""
        disposal_location = str(data[10]) if data[10] is not None else ""
        sale_details = str(data[11]) if data[11] is not None else ""
        sold_to = str(data[12]) if data[12] is not None else ""
        image_path = str(data[13]) if data[13] is not None else None

        # Debug image path
        print(f"Processing disposed asset: {name}, image_path: {image_path}")
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
            print(f"Unsupported or invalid image format for disposed asset {name}: {image_path}")
            if image_path:
                self.page.open(ft.SnackBar(
                    ft.Text(f"Unsupported image format for disposed asset {name}: {image_path}. Supported formats are jpg, jpeg, png, gif."),
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
                                ft.Text(disposal_type, color=ft.Colors.BLACK),
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
            ft.Text(f"Purchase Date: {purchase_date}", size=14, color="#263238"),
            ft.Text(f"Disposal Date: {disposal_date}", size=14, color="#263238"),
        ]

        if disposal_type == "Scrap" and amount_earned:
            card_content.append(ft.Text(f"Amount Earned: {amount_earned}", size=14, color="#263238"))
        elif disposal_type == "Dispose":
            if disposal_reason:
                card_content.append(ft.Text(f"Reason: {disposal_reason}", size=14, color="#263238"))
            if disposal_location:
                card_content.append(ft.Text(f"Disposal Location: {disposal_location}", size=14, color="#263238"))
        elif disposal_type == "Sold":
            if sold_to:
                card_content.append(ft.Text(f"Sold To: {sold_to}", size=14, color="#263238"))
            if sale_details:
                card_content.append(ft.Text(f"Sale Details: {sale_details}", size=14, color="#263238"))
            if amount_earned:
                card_content.append(ft.Text(f"Amount Earned: {amount_earned}", size=14, color="#263238"))

        card_content.append(
            ft.ElevatedButton(
                "Manage",
                icon=ft.Icons.PENDING_ACTIONS,
                bgcolor=ft.Colors.BLUE_300,
                color=ft.Colors.WHITE,
                on_click=on_manage_click,
                width=100,
            )
        )

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
                height=380 if image_content else 340,
            ),
            elevation=5,
        )

    def filter_assets(self, e):
        """Handle filter button click to fetch assets by selected category."""
        selected_category = self.category_dropdown.value
        print(f"Filtering assets by category: {selected_category}")
        self.refresh_cards(category_id=selected_category)

    def refresh_cards(self, category_id=None):
        """Refresh the asset cards by re-fetching data, optionally filtered by category."""
        try:
            self.asset_data = self._fetch_assets(category_id=category_id)
            self.deployed_data = self._fetch_deployed_assets(category_id=category_id)
            self.disposed_data = self._fetch_disposed_assets(category_id=category_id)

            # Update deployable cards
            self.deployable_cards.controls = [
                ft.Container(
                    content=self.create_asset_card(
                        data=x,
                        status_color=ft.Colors.LIGHT_GREEN_ACCENT_400,
                        on_manage_click=lambda id, name: self.manage_Asset.open(asset_id=id, name=name),
                        on_select=lambda e, asset=x: self.show_banner(asset=asset, is_deployed=False),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for x in self.asset_data
            ]

            # Update deployed cards
            self.deployed_cards.controls = [
                ft.Container(
                    content=self.create_deployed_card(
                        data=data,
                        status_color=ft.Colors.LIGHT_BLUE_ACCENT_700,
                        on_manage_click=lambda e: self.show_manage_asset_bottomsheet(),
                        on_select=lambda e, asset=data: self.show_banner(asset=asset, is_deployed=True),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for data in self.deployed_data
            ]

            # Update disposed cards
            self.disposed_cards.controls = [
                ft.Container(
                    content=self.create_disposed_card(
                        data=data,
                        status_color=ft.Colors.RED_ACCENT_400 if data[7] == "Scrap" else (ft.Colors.YELLOW_ACCENT_400 if data[7] == "Sold" else ft.Colors.GREY_400),
                        on_manage_click=lambda e: self.show_manage_asset_bottomsheet(),
                        on_select=lambda e, asset=data: self.show_banner(asset=asset, is_disposed=True),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for data in self.disposed_data
            ]

            self.page.update()

        except mysql.connector.Error as err:
            print(f"Error refreshing cards: {err}")
            self.page.open(ft.SnackBar(ft.Text(f"Error refreshing cards: {err}"), duration=4000))

def asset_page(page):
    return AssetPagee(page)