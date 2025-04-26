import flet as ft
import mysql.connector
import asyncio

class CompoListScroll(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # Style the container with a gradient background, shadow, and rounded corners
        self.bgcolor = ft.colors.TRANSPARENT
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[ft.colors.BLUE_50, ft.colors.WHITE],
        )
        self.border_radius = 15
        self.padding = 10
        self.margin = 10
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
            offset=ft.Offset(0, 5),
        )

        # Create the ListView with custom styling
        self.lv = ft.ListView(
            expand=True,
            spacing=10,
            padding=ft.padding.symmetric(vertical=20, horizontal=15),
            auto_scroll=True,
        )

        # Add a custom scrollbar
        self.lv_scroll_container = ft.Container(
            content=self.lv,
            expand=True,
            border_radius=10,
            bgcolor=ft.colors.with_opacity(0.9, ft.colors.WHITE),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
            ),
        )

        self.current_asset_index = 0
        self.total_assets = 0
        self.setup_list_view()

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
            cursor.execute("SELECT COUNT(*) FROM component")
            total = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            print(f"Total components in database: {total}")
            return total
        except mysql.connector.Error as err:
            print(f"Error fetching total assets: {err}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error fetching total assets: {err}", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_700,
                duration=3000,
            )
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
            cursor.execute("SELECT * FROM component LIMIT 1 OFFSET %s", (index,))
            asset = cursor.fetchone()
            cursor.close()
            connection.close()
            if asset:
                print(f"Fetched asset at index {index}: {asset[1] if len(asset) > 1 else 'N/A'}")
            return asset
        except mysql.connector.Error as err:
            print(f"Error fetching asset at index {index}: {err}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error fetching asset: {err}", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_700,
                duration=3000,
            )
            self.page.snack_bar.open = True
            self.page.update()
            return None

    def setup_list_view(self):
        # Get the total number of assets
        self.total_assets = self.fetch_total_assets()

        if self.total_assets == 0:
            print("No components found, displaying fallback message")
            self.content = ft.Container(
                content=ft.Text(
                    "No components found",
                    size=20,
                    color=ft.colors.RED_700,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                alignment=ft.alignment.center,
                bgcolor=ft.colors.with_opacity(0.1, ft.colors.RED_100),
                padding=20,
                border_radius=10,
                margin=10,
            )
            return

        # Set the content to the scrollable ListView container
        self.content = self.lv_scroll_container

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
                        asset_id = asset[0] if len(asset) > 0 else None
                        name = asset[1] if len(asset) > 1 and asset[1] else "N/A"
                        category = asset[2] if len(asset) > 2 and asset[2] else "N/A"
                        status = asset[11] if len(asset) > 11 and asset[11] else "N/A"
                        price = str(asset[10]) if len(asset) > 10 and asset[10] is not None else "N/A"
                        image_path = asset[13] if len(asset) > 13 and asset[13] else "images/placeholder.jpg"

                        # Status indicator color
                        status_color = ft.colors.GREEN_700 if status.lower() == "active" else ft.colors.RED_700

                        # Create the ListTile with enhanced styling
                        item = ft.Container(
                            content=ft.ListTile(
                                leading=ft.Container(
                                    content=ft.Image(
                                        src=image_path,
                                        width=50,
                                        height=50,
                                        fit=ft.ImageFit.CONTAIN,
                                        error_content=ft.Text("No Image", size=12, color=ft.colors.GREY_700),
                                    ),
                                    border_radius=8,
                                    bgcolor=ft.colors.with_opacity(0.05, ft.colors.BLACK),
                                    padding=5,
                                ),
                                title=ft.Text(
                                    f"{name}",
                                    size=18,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.colors.BLACK87,
                                ),
                                subtitle=ft.Column(
                                    controls=[
                                        ft.Text(f"Category: {category}", size=14, color=ft.colors.GREY_800),
                                        ft.Text(f"Status: {status}", size=14, color=status_color, weight=ft.FontWeight.BOLD),
                                        ft.Text(f"Price: ${price}", size=14, color=ft.colors.GREY_800),
                                    ],
                                    spacing=4,
                                ),
                            ),
                            bgcolor=ft.colors.WHITE,
                            border_radius=10,
                            padding=ft.padding.symmetric(horizontal=10, vertical=5),
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=5,
                                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                            ),
                            # Hover effect
                            on_hover=lambda e: self.on_item_hover(e),
                            # Animation on appearance
                            animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
                            opacity=0,  # Start with 0 opacity for fade-in effect
                        )

                        self.lv.controls.append(item)
                        self.page.update()

                        # Trigger fade-in animation
                        item.opacity = 1
                        self.page.update()

                        print(f"Displayed asset: {name}")
                    except Exception as e:
                        print(f"Error displaying asset at index {self.current_asset_index}: {e}")
                else:
                    print(f"No asset found at index {self.current_asset_index}")

                self.current_asset_index += 1
                await asyncio.sleep(5)  # Wait 5 seconds before displaying the next asset

            # After displaying all assets, wait a bit before restarting the loop
            await asyncio.sleep(5)

    def on_item_hover(self, e: ft.HoverEvent):
        """Handle hover effect for ListTile items."""
        e.control.scale = 1.02 if e.data == "true" else 1.0
        e.control.shadow = ft.BoxShadow(
            spread_radius=2,
            blur_radius=8,
            color=ft.colors.with_opacity(0.2, ft.colors.BLACK) if e.data == "true" else ft.colors.with_opacity(0.1, ft.colors.BLACK),
        )
        e.control.update()

def compo_scroll(page):
    return CompoListScroll(page)