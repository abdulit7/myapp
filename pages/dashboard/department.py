import flet as ft
import mysql.connector
from components.departmentform import DepartDialog

class Department(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        page.window.title = "Asset Management System - Departments"

        # Dialog for adding/editing departments
        self.depart_dialog = DepartDialog(page, self)

        # Add Department Button
        self.add_department_button = ft.ElevatedButton(
            icon=ft.icons.ADD,
            text="Add Department",
            bgcolor=ft.colors.YELLOW_600,
            width=180,
            height=50,
            color=ft.colors.WHITE,
            on_click=lambda e: self.depart_dialog.open()
        )

        # Loading indicator
        self.loading_indicator = ft.ProgressRing(visible=False)

        # Department Table
        self.department_table = ft.DataTable(
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
                ft.DataColumn(ft.Text("Description", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Users", weight=ft.FontWeight.W_600)),
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
                                    controls=[self.add_department_button, self.loading_indicator],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                self.department_table,
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
        self.load_departments()

    def _get_db_connection(self) -> mysql.connector.connection.MySQLConnection:
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

    def load_departments(self):
        """Fetches and displays department data, including user count."""
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
                SELECT department.id, department.name, department.description, COUNT(users.id) as user_count
                FROM department
                LEFT JOIN users ON department.id = users.department_id
                GROUP BY department.id
            """)
            departments = cur.fetchall()
            self.department_table.rows.clear()

            for dep in departments:
                dep_id, name, description, user_count = dep
                self.department_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(name or "N/A")),
                            ft.DataCell(ft.Text(description or "N/A")),
                            ft.DataCell(
                                ft.TextButton(
                                    str(user_count),
                                    on_click=lambda e, count=user_count: self.navigate_to_users(count)
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Edit",
                                            bgcolor=ft.colors.LIGHT_GREEN_500,
                                            color=ft.colors.WHITE,
                                            on_click=lambda e, dep_id=dep_id: self.edit_department(dep_id)
                                        ),
                                        ft.ElevatedButton(
                                            "Delete",
                                            bgcolor=ft.colors.RED_500,
                                            color=ft.colors.WHITE,
                                            on_click=lambda e, dep_id=dep_id: self.delete_department(dep_id)
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
            print(f"Error fetching departments: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching departments: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")
            self.loading_indicator.visible = False
            self.page.update()

    def navigate_to_users(self, user_count: int):
        """Navigates to the users page if there are users to display."""
        if user_count > 0:
            self.page.go('/users')
        else:
            self.page.open(ft.SnackBar(ft.Text("No users in this department."), duration=3000))

    def edit_department(self, dep_id: int):
        """Handles editing a department by opening the dialog with existing data."""
        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            cur.execute("SELECT name, description FROM department WHERE id = %s", (dep_id,))
            department = cur.fetchone()
            if department:
                name, description = department
                self.depart_dialog.open(name, description, dep_id)
            else:
                self.page.open(ft.SnackBar(ft.Text(f"Department ID {dep_id} not found."), duration=4000))
        except mysql.connector.Error as error:
            print(f"Error fetching department: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching department: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

    def delete_department(self, dep_id: int):
        """Handles deleting a department from the database."""
        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            cur.execute("DELETE FROM department WHERE id = %s", (dep_id,))
            connection.commit()
            print(f"Deleted department ID: {dep_id}")
            self.page.open(ft.SnackBar(ft.Text("Department deleted successfully."), duration=3000))
            self.load_departments()
        except mysql.connector.Error as error:
            print(f"Error deleting department: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error deleting department: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

def DepartmentPage(page: ft.Page) -> Department:
    """Factory function to create a Department instance."""
    return Department(page)