import flet as ft
import mysql.connector
from components.categoryform import CatDialog

class Category(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        page.window.title = "Asset Management System - Categories"

        self.cat_dialog = CatDialog(page)

        # Add Category Button
        self.add_category_button = ft.ElevatedButton(
            icon=ft.icons.ADD,
            text="Add Category",
            bgcolor=ft.colors.GREEN_400,
            width=150,
            height=50,
            color=ft.colors.WHITE,
            on_click=lambda e: self.cat_dialog.open()
        )

        # Loading indicator
        self.loading_indicator = ft.ProgressRing(visible=False)

        # Category Table
        self.category_table = ft.DataTable(
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=10,
            vertical_lines=ft.BorderSide(1, ft.colors.GREY_200),
            horizontal_lines=ft.BorderSide(1, ft.colors.GREY_200),
            heading_row_color=ft.colors.INDIGO_100,
            heading_text_style=ft.TextStyle(
                color=ft.colors.INDIGO_900,
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            data_row_color={ft.ControlState.HOVERED: ft.colors.LIGHT_BLUE_50},
            data_row_min_height=50,
            data_text_style=ft.TextStyle(
                color=ft.colors.GREY_800,
                size=14,
            ),
            show_checkbox_column=False,
            column_spacing=30,
            columns=[
                ft.DataColumn(ft.Text("Name", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Type", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Total Items", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Description", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.W_600)),
            ],
            rows=[],
        )

        # Page Layout
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        self.add_category_button,
                                        self.loading_indicator,
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                self.category_table,
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

        # Load data after UI initialization
        page.add(self)
        self.load_categories()

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

    def load_categories(self):
        """Fetches and displays category data, including total items."""
        self.loading_indicator.visible = True
        self.page.update()

        connection = self._get_db_connection()
        if not connection:
            self.loading_indicator.visible = False
            self.page.update()
            return

        try:
            cur = connection.cursor()
            # Fetch category data (removed image_path)
            cur.execute("""
                SELECT id, name, type, description
                FROM category
            """)
            categories = cur.fetchall()
            self.category_table.rows.clear()

            for cat in categories:
                cat_id, name, cat_type, description = cat
                # Calculate total items in this category
                total_items = self._get_total_items(cat_id, connection)
                self.category_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(name or "N/A")),
                            ft.DataCell(ft.Text(cat_type or "N/A")),
                            ft.DataCell(ft.Text(str(total_items))),
                            ft.DataCell(ft.Text(description or "N/A")),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Edit",
                                            bgcolor=ft.colors.LIGHT_GREEN_500,
                                            color=ft.colors.WHITE,
                                            on_click=lambda e, cat_id=cat_id: self.edit_category(cat_id)
                                        ),
                                        ft.ElevatedButton(
                                            "Delete",
                                            bgcolor=ft.colors.RED_500,
                                            color=ft.colors.WHITE,
                                            on_click=lambda e, cat_id=cat_id: self.delete_category(cat_id)
                                        ),
                                    ],
                                    spacing=5,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                )
                            ),
                        ]
                    )
                )
        except mysql.connector.Error as error:
            print(f"Error fetching categories: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching categories: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")
            self.loading_indicator.visible = False
            self.page.update()

    def _get_total_items(self, category_id: int, connection) -> int:
        """Calculate the total number of items (assets, components, consumables) in a category."""
        try:
            cur = connection.cursor()
            # Count assets
            cur.execute("SELECT COUNT(*) FROM assets WHERE category_id = %s", (category_id,))
            asset_count = cur.fetchone()[0]
            # Count components (using total_qty)
            cur.execute("SELECT SUM(total_qty) FROM components WHERE category_id = %s", (category_id,))
            component_count = cur.fetchone()[0] or 0
            # Count consumables (using total_qty)
            cur.execute("SELECT SUM(total_qty) FROM consumables WHERE category_id = %s", (category_id,))
            consumable_count = cur.fetchone()[0] or 0
            return asset_count + component_count + consumable_count
        except mysql.connector.Error as error:
            print(f"Error calculating total items: {error}")
            return 0

    def edit_category(self, cat_id: int):
        """Handles editing a category by opening the dialog with existing data."""
        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            cur.execute("SELECT name, description, type FROM category WHERE id = %s", (cat_id,))
            category = cur.fetchone()
            if category:
                name, description, cat_type = category
                self.cat_dialog.open(name=name, desc=description, cat_type=cat_type, cat_id=cat_id)
            else:
                self.page.open(ft.SnackBar(ft.Text(f"Category ID {cat_id} not found."), duration=4000))
        except mysql.connector.Error as error:
            print(f"Error fetching category: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching category: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

    def delete_category(self, cat_id: int):
        """Handles deleting a category from the database."""
        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            cur.execute("DELETE FROM category WHERE id = %s", (cat_id,))
            connection.commit()
            print(f"Deleted category ID: {cat_id}")
            self.page.open(ft.SnackBar(ft.Text("Category deleted successfully."), duration=3000))
            self.load_categories()  # Refresh table
        except mysql.connector.Error as error:
            print(f"Error deleting category: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error deleting category: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

def CategoryPage(page: ft.Page) -> Category:
    """Factory function to create a Category instance."""
    return Category(page)