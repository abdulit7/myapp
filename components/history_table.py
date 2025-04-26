import flet as ft
import mysql.connector
from datetime import datetime

class HistoryTable(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.history_data = []
        self.category_map = {}
        
        # Fetch category data for mapping
        self.fetch_categories()
        
        # Fetch history data
        self.fetch_history()
        
        # Create the DataTable
        self.data_table = ft.DataTable(
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=10,
            heading_row_color=ft.colors.BLUE_50,
            heading_row_height=50,
            data_row_color={"hovered": ft.colors.GREY_100},
            columns=[
                ft.DataColumn(
                    ft.Text("Action", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                    tooltip="Type of action performed"
                ),
                ft.DataColumn(
                    ft.Text("Asset Name", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                    tooltip="Name of the asset"
                ),
                ft.DataColumn(
                    ft.Text("Category", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                    tooltip="Category of the asset"
                ),
                ft.DataColumn(
                    ft.Text("User/Department", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                    tooltip="User or Department the asset was deployed to"
                ),
                ft.DataColumn(
                    ft.Text("Date", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                    tooltip="Date of the action"
                ),
                ft.DataColumn(
                    ft.Text("Details", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                    tooltip="Additional details about the action"
                ),
            ],
            rows=[],
        )
        
        # Populate the table with history data
        self.populate_table()
        
        # Wrap the DataTable in a scrollable container with styling
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Asset History",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLACK87,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(
                        content=self.data_table,
                        expand=True,
                        border_radius=10,
                        bgcolor=ft.colors.WHITE,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                        ),
                        padding=10,
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.colors.BLUE_50, ft.colors.WHITE],
            ),
            border_radius=15,
            padding=10,
            margin=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                offset=ft.Offset(0, 5),
            ),
            expand=True,
        )

    def fetch_categories(self):
        """Fetch and cache category data."""
        connection = self._get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id, name FROM category")
                self.category_map = {row[0]: row[1] for row in cursor.fetchall()}
                print(f"Cached categories: {self.category_map}")
            except mysql.connector.Error as err:
                print(f"Error fetching categories: {err}")
                self.show_snackbar(f"Error fetching categories: {err}", ft.colors.RED_700)
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("Database connection closed")

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
            self.show_snackbar(f"Database error: {error}", ft.colors.RED_700)
            return None

    def fetch_history(self):
        """Fetch history data from assets, deployed_assets, and disposed_assets tables."""
        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cursor = connection.cursor()

            # 1. Fetch "Added" actions from assets table
            cursor.execute(
                """
                SELECT name, category_id, purchase_date 
                FROM assets 
                WHERE purchase_date IS NOT NULL
                """
            )
            for row in cursor.fetchall():
                self.history_data.append({
                    "action": "Added",
                    "asset_name": row[0],
                    "category_id": row[1],
                    "user_department": "",
                    "date": row[2],
                    "details": "New asset added to inventory"
                })

            # 2. Fetch "Deployed" actions from deployed_assets table
            cursor.execute(
                """
                SELECT name, category_id, deployed_to, user_department, deploy_date 
                FROM deployed_assets 
                WHERE deploy_date IS NOT NULL
                """
            )
            for row in cursor.fetchall():
                self.history_data.append({
                    "action": "Deployed",
                    "asset_name": row[0],
                    "category_id": row[1],
                    "user_department": f"{row[3]} (ID: {row[2]})" if row[3] else f"ID: {row[2]}",
                    "date": row[4],
                    "details": "Asset deployed to user/department"
                })

            # 3. Fetch "Scrapped", "Disposed", "Sold" actions from disposed_assets table
            cursor.execute(
                """
                SELECT name, category_id, disposal_type, disposal_date, amount_earned, 
                       disposal_reason, disposal_location, sale_details, sold_to 
                FROM disposed_assets 
                WHERE disposal_date IS NOT NULL
                """
            )
            for row in cursor.fetchall():
                disposal_type = row[2]
                details = ""
                if disposal_type == "Scrap":
                    details = f"Amount Earned: ${row[4]}" if row[4] is not None else "Scrapped asset"
                elif disposal_type == "Dispose":
                    details = f"Reason: {row[5] or 'N/A'}, Location: {row[6] or 'N/A'}"
                elif disposal_type == "Sold":
                    details = f"Sold To: {row[8] or 'N/A'}, Amount: ${row[4] or 'N/A'}, Details: {row[7] or 'N/A'}"

                self.history_data.append({
                    "action": disposal_type,
                    "asset_name": row[0],
                    "category_id": row[1],
                    "user_department": "",
                    "date": row[3],
                    "details": details
                })

            # Sort history by date (newest first)
            self.history_data.sort(key=lambda x: x["date"], reverse=True)

        except mysql.connector.Error as err:
            print(f"Error fetching history: {err}")
            self.show_snackbar(f"Error fetching history: {err}", ft.colors.RED_700)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Database connection closed")

    def populate_table(self):
        """Populate the DataTable with history data."""
        for entry in self.history_data:
            category_name = self.category_map.get(entry["category_id"], "Unknown")
            date_str = entry["date"].strftime("%Y-%m-%d") if isinstance(entry["date"], datetime) else str(entry["date"])
            
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                entry["action"],
                                size=14,
                                color={
                                    "Added": ft.colors.GREEN_700,
                                    "Deployed": ft.colors.BLUE_700,
                                    "Scrapped": ft.colors.ORANGE_700,
                                    "Disposed": ft.colors.RED_700,
                                    "Sold": ft.colors.PURPLE_700,
                                }.get(entry["action"], ft.colors.GREY_700),
                                weight=ft.FontWeight.BOLD,
                            )
                        ),
                        ft.DataCell(ft.Text(entry["asset_name"], size=14, color=ft.colors.BLACK87)),
                        ft.DataCell(ft.Text(category_name, size=14, color=ft.colors.BLACK87)),
                        ft.DataCell(ft.Text(entry["user_department"] or "N/A", size=14, color=ft.colors.BLACK87)),
                        ft.DataCell(ft.Text(date_str, size=14, color=ft.colors.BLACK87)),
                        ft.DataCell(ft.Text(entry["details"], size=14, color=ft.colors.GREY_800)),
                    ]
                )
            )

    def show_snackbar(self, message, color):
        """Show a snackbar with the given message and color."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE),
            bgcolor=color,
            duration=3000,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def build(self):
        return self.content

def history_table(page):
    return HistoryTable(page)