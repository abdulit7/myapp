import flet as ft
import mysql.connector
import asyncio

class ListScroll(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.lv = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=True,
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

    def setup_list_view(self):
        # Get the total number of assets
        self.total_assets = self.fetch_total_assets()

        if self.total_assets == 0:
            print("No assets found, displaying fallback message")
            self.content = ft.Text(
                "No assets found",
                size=20,
                color=ft.Colors.RED_700,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            )
            return

        self.content = self.lv

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
                        category = asset[2] if len(asset) > 2 and asset[2] else "N/A"
                        status = asset[13] if len(asset) > 13 else "N/A"
                        model = str(asset[4]) if len(asset) > 4 and asset[4] is not None else "N/A"
                        image_path = asset[12] if len(asset) > 12 and asset[12] else "images/placeholder.jpg"

              
                        # Create the ListTile
                        item = ft.ListTile(
                            leading=ft.Image(
                                src=image_path,
                                width=50,
                                height=50,
                                fit=ft.ImageFit.CONTAIN,
                                error_content=ft.Text("No Image", size=12, color=ft.Colors.GREY_700),
                            ),
                            title=ft.Text(f"{name}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                            subtitle=ft.Column(
                                controls=[
                                    ft.Text(f"Category: {category}", size=14),
                                    ft.Text(f"Status: {status}", size=14, color=ft.Colors.GREEN_700),
                                    ft.Text(f"Model: ${model}", size=14),
                                ],
                                spacing=2,
                            ),
                        )

                        self.lv.controls.append(item)
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

def list_scroll(page):
    return ListScroll(page)
