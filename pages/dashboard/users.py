import flet as ft
import mysql.connector
from components.userform import UserDialog

class Users(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        page.window.title = "Asset Management System - Users"

        self.user_dialog = UserDialog(page)

        # Add User Button
        self.add_user_button = ft.ElevatedButton(
            icon=ft.icons.ADD,
            text="Add User",
            bgcolor=ft.colors.GREEN_400,
            width=150,
            height=50,
            color=ft.colors.WHITE,
            on_click=lambda e: self.user_dialog.open()
        )

        # Loading indicator
        self.loading_indicator = ft.ProgressRing(visible=False)

        # Users Table
        self.users_table = ft.DataTable(
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
                ft.DataColumn(ft.Text("EMP ID", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Branch", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Department", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Can Login", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Image", weight=ft.FontWeight.W_600)),
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
                                        self.add_user_button,
                                        self.loading_indicator,
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                self.users_table,
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
        self.load_users()

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

    def load_users(self):
        """Fetches and displays user data."""
        self.loading_indicator.visible = True
        self.page.update()

        connection = self._get_db_connection()
        if not connection:
            self.loading_indicator.visible = False
            self.page.update()
            return

        try:
            cur = connection.cursor()
            cur.execute("""
                SELECT u.id, u.name, u.emp_id, u.branch, d.name, u.can_login, u.image_path
                FROM users u
                LEFT JOIN department d ON u.department_id = d.id
            """)
            users = cur.fetchall()
            self.users_table.rows.clear()

            for user in users:
                user_id, name, emp_id, branch, dept_name, can_login, image_path = user
                self.users_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(name or "N/A")),
                            ft.DataCell(ft.Text(emp_id or "N/A")),
                            ft.DataCell(ft.Text(branch or "N/A")),
                            ft.DataCell(ft.Text(dept_name or "N/A")),
                            ft.DataCell(ft.Text("Yes" if can_login else "No")),
                            ft.DataCell(ft.Text(image_path or "N/A")),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Edit",
                                            bgcolor=ft.colors.LIGHT_GREEN_500,
                                            color=ft.colors.WHITE,
                                            on_click=lambda e, user_id=user_id: self.edit_user(user_id)
                                        ),
                                        ft.ElevatedButton(
                                            "Delete",
                                            bgcolor=ft.colors.RED_500,
                                            color=ft.colors.WHITE,
                                            on_click=lambda e, user_id=user_id: self.delete_user(user_id)
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
            print(f"Error fetching users: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching users: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")
            self.loading_indicator.visible = False
            self.page.update()

    def edit_user(self, user_id: int):
        """Handles editing a user by opening the dialog with existing data."""
        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            cur.execute("SELECT name, emp_id, password, branch, department_id, can_login, image_path FROM users WHERE id = %s", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                name, emp_id, password, branch, department_id, can_login, image_path = user_data
                self.user_dialog.open(
                    name=name,
                    emp_id=emp_id,
                    password=password,
                    branch=branch,
                    department_id=department_id,
                    can_login=bool(can_login),
                    image_path=image_path,
                    user_id=user_id
                )
            else:
                self.page.open(ft.SnackBar(ft.Text(f"User ID {user_id} not found."), duration=4000))
        except mysql.connector.Error as error:
            print(f"Error fetching user: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching user: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

    def delete_user(self, user_id: int):
        """Handles deleting a user from the database."""
        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            connection.commit()
            print(f"Deleted user ID: {user_id}")
            self.page.open(ft.SnackBar(ft.Text("User deleted successfully."), duration=3000))
            self.load_users()  # Refresh table
        except mysql.connector.Error as error:
            print(f"Error deleting user: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error deleting user: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

def UsersPage(page: ft.Page) -> Users:
    """Factory function to create a Users instance."""
    return Users(page)