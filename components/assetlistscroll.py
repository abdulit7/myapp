import flet as ft
import mysql.connector
import asyncio
import os.path

class ListScroll(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True  # Make the container expand to fill available space
        self.padding = ft.padding.all(20)
        
        # Supported image extensions
        self.supported_image_extensions = {".jpg", ".jpeg", ".png", ".gif"}
        
        # Stylish ListView with gradient background
        self.lv = ft.ListView(
            expand=True,
            spacing=15,
            padding=ft.padding.all(10),
            auto_scroll=True,
        )
        self.current_asset_index = 0
        self.total_assets = 0
        
        # Cache category data to avoid repeated JOINs
        self.category_map = {}
        self.fetch_categories()
        
        self.setup_list_view()

    def fetch_categories(self):
        """Fetch and cache category data."""
        try:
            connection = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            cursor = connection.cursor()
            cursor.execute("SELECT id, name FROM category")
            self.category_map = {row[0]: row[1] for row in cursor.fetchall()}
            cursor.close()
            connection.close()
            print(f"Cached categories: {self.category_map}")
        except mysql.connector.Error as err:
            print(f"Error fetching categories: {err}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error fetching categories: {err}"))
            self.page.snack_bar.open = True
            self.page.update()

    def fetch_total_assets(self):
        """Fetch the total number of assets in the database."""
        try:
            connection = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM assets")
            total = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            print(f"Total assets in database: {total}")
            return total
        except mysql.connector.Error as err:
            print(f"Error fetching total assets: {err}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error fetching total assets: {err}"))
            self.page.snack_bar.open = True
            self.page.update()
            return 0

    def fetch_asset_by_index(self, index):
        """Fetch a single asset by its row number (using LIMIT and OFFSET)."""
        try:
            connection = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM assets LIMIT 1 OFFSET %s", (index,))
            asset = cursor.fetchone()
            cursor.close()
            connection.close()
            if asset:
                print(f"Fetched asset at index {index}: {asset[1] if len(asset) > 1 else 'N/A'}")
            return asset
        except mysql.connector.Error as err:
            print(f"Error fetching asset at index {index}: {err}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error fetching asset: {err}"))
            self.page.snack_bar.open = True
            self.page.update()
            return None

    def is_supported_image_format(self, image_path: str) -> bool:
        """Check if the image path has a supported extension (jpg, jpeg, png, gif)."""
        if not image_path:
            return False
        _, ext = os.path.splitext(image_path.lower())
        return ext in self.supported_image_extensions

    def setup_list_view(self):
        # Get the total number of assets
        self.total_assets = self.fetch_total_assets()

        if self.total_assets == 0:
            print("No assets found, displaying fallback message")
            self.content = ft.Container(
                content=ft.Text(
                    "No Assets Found",
                    size=24,
                    color=ft.Colors.RED_700,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    italic=True,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.all(50),
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.Colors.GREY_300,
                    offset=ft.Offset(0, 2),
                ),
            )
            return

        # Add a gradient background to the ListView container
        self.content = ft.Container(
            content=self.lv,
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[ft.Colors.BLUE_50, ft.Colors.WHITE],
            ),
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=15,
                color=ft.Colors.GREY_400,
                offset=ft.Offset(0, 5),
            ),
        )

        # Start the process of fetching assets one by one
        self.page.run_task(self.display_assets_one_by_one)

    async def display_assets_one_by_one(self):
        while True:
            # Reset the ListView when starting the loop again
            self.lv.controls.clear()
            self.current_asset_index = 0

            # Fetch and display assets one by one
            while self.current_asset_index < self.total_assets:
                asset = self.fetch_asset_by_index(self.current_asset_index)
                if asset:
                    try:
                        # Extract asset details with error handling
                        name = asset[1] if len(asset) > 1 and asset[1] else "N/A"
                        category_id = asset[2] if len(asset) > 2 and asset[2] is not None else None
                        category = self.category_map.get(category_id, "N/A")
                        status = asset[13] if len(asset) > 13 and asset[13] is not None else "N/A"
                        model = str(asset[4]) if len(asset) > 4 and asset[4] is not None else "N/A"
                        image_path = asset[15] if len(asset) > 15 and asset[15] else None

                        # Validate image path
                        if image_path and self.is_supported_image_format(image_path):
                            # Assuming images are in the assets directory or served via a URL
                            final_image_path = image_path
                            print(f"Using image path for {name}: {final_image_path}")
                        else:
                            final_image_path = "/images/placeholder.jpg"
                            print(f"Invalid or missing image path for {name}: {image_path}, using placeholder")

                        # Determine status color and icon
                        status_color = {
                            "Available": ft.Colors.GREEN_600,
                            "Deployed": ft.Colors.BLUE_600,
                            "Disposed": ft.Colors.RED_600,
                        }.get(status, ft.Colors.GREY_600)
                        status_icon = {
                            "Available": ft.Icons.CHECK_CIRCLE,
                            "Deployed": ft.Icons.SEND,
                            "Disposed": ft.Icons.DELETE,
                        }.get(status, ft.Icons.INFO)

                        # Create a card-like ListTile with hover effect
                        item = ft.Container(
                            content=ft.Row(
                                controls=[
                                    # Circular image
                                    ft.Container(
                                        content=ft.Image(
                                            src=final_image_path,
                                            width=60,
                                            height=60,
                                            fit=ft.ImageFit.COVER,
                                            border_radius=30,
                                            error_content=ft.Icon(
                                                ft.Icons.IMAGE_NOT_SUPPORTED,
                                                color=ft.Colors.GREY_500,
                                                size=30,
                                            ),
                                        ),
                                        width=60,
                                        height=60,
                                        border_radius=30,
                                        border=ft.border.all(2, ft.Colors.BLUE_200),
                                        padding=ft.padding.all(2),
                                    ),
                                    # Asset details
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                name,
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.BLUE_900,
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(
                                                        ft.Icons.CATEGORY,
                                                        size=16,
                                                        color=ft.Colors.BLUE_GREY_600,
                                                    ),
                                                    ft.Text(
                                                        f"Category: {category}",
                                                        size=14,
                                                        color=ft.Colors.BLUE_GREY_800,
                                                    ),
                                                ],
                                                spacing=5,
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(
                                                        status_icon,
                                                        size=16,
                                                        color=status_color,
                                                    ),
                                                    ft.Text(
                                                        f"Status: {status}",
                                                        size=14,
                                                        color=status_color,
                                                    ),
                                                ],
                                                spacing=5,
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(
                                                        ft.Icons.DEVICES,
                                                        size=16,
                                                        color=ft.Colors.BLUE_GREY_600,
                                                    ),
                                                    ft.Text(
                                                        f"Model: {model}",
                                                        size=14,
                                                        color=ft.Colors.BLUE_GREY_800,
                                                    ),
                                                ],
                                                spacing=5,
                                            ),
                                        ],
                                        spacing=5,
                                        expand=True,
                                    ),
                                ],
                                spacing=15,
                                alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            padding=ft.padding.all(15),
                            bgcolor=ft.Colors.WHITE,
                            border_radius=12,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=8,
                                color=ft.Colors.GREY_300,
                                offset=ft.Offset(0, 2),
                            ),
                            # Hover effect
                            on_hover=lambda e: self.on_card_hover(e),
                            width=400,  # Fixed width for consistency
                        )

                        self.lv.controls.append(item)
                        self.page.update()
                        print(f"Displayed asset: {name}")
                    except Exception as e:
                        print(f"Error displaying asset at index {self.current_asset_index}: {e}")
                        self.page.snack_bar = ft.SnackBar(ft.Text(f"Error displaying asset: {e}"))
                        self.page.snack_bar.open = True
                        self.page.update()
                else:
                    print(f"No asset found at index {self.current_asset_index}")

                self.current_asset_index += 1
                await asyncio.sleep(5)  # Wait 5 seconds before displaying the next asset

            # After displaying all assets, wait a bit before restarting the loop
            await asyncio.sleep(5)

    def on_card_hover(self, e):
        """Handle hover effect for the card."""
        e.control.shadow = ft.BoxShadow(
            spread_radius=2 if e.data == "true" else 1,
            blur_radius=12 if e.data == "true" else 8,
            color=ft.Colors.BLUE_200 if e.data == "true" else ft.Colors.GREY_300,
            offset=ft.Offset(0, 4 if e.data == "true" else 2),
        )
        e.control.bgcolor = ft.Colors.BLUE_50 if e.data == "true" else ft.Colors.WHITE
        e.control.update()

def list_scroll(page):
    return ListScroll(page)