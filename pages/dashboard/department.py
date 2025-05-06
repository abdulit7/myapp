import flet as ft  # For building the user interface
import mysql.connector  # For connecting to the MySQL database
from components.departmentform import DepartDialog  # For the add/edit department form

class Department(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()  # Initialize the container
        self.page = page  # Store the page object
        self.expand = True  # Make the container fill the available space
        page.window.title = "Asset Management System - Departments"  # Set the window title

        # Create the dialog for adding or editing departments
        self.department_form = DepartDialog(page, self)

        # Button to add a new department
        self.add_button = ft.ElevatedButton(
            icon=ft.icons.ADD,  # Add icon
            text="Add Department",  # Button text
            bgcolor=ft.colors.YELLOW_600,  # Yellow background
            color=ft.colors.WHITE,  # White text
            width=180,  # Button width
            height=50,  # Button height
            on_click=lambda e: self.department_form.open()  # Open the form when clicked
        )

        # Loading spinner to show while fetching data
        self.loading_spinner = ft.ProgressRing(visible=False)  # Hidden by default

        # Table to display department data
        self.table = ft.DataTable(
            bgcolor=ft.colors.WHITE,  # White background
            border=ft.border.all(1, ft.colors.GREY_300),  # Light grey border
            border_radius=10,  # Rounded corners
            vertical_lines=ft.BorderSide(1, ft.colors.GREY_200),  # Vertical grid lines
            horizontal_lines=ft.BorderSide(1, ft.colors.GREY_200),  # Horizontal grid lines
            heading_row_color=ft.colors.INDIGO_100,  # Light indigo header background
            heading_text_style=ft.TextStyle(
                color=ft.colors.INDIGO_900,  # Dark indigo text
                weight=ft.FontWeight.BOLD,  # Bold text
                size=16  # Font size
            ),
            data_row_color={ft.ControlState.HOVERED: ft.colors.LIGHT_BLUE_50},  # Light blue on hover
            data_row_min_height=50,  # Minimum row height
            data_text_style=ft.TextStyle(
                color=ft.colors.GREY_800,  # Dark grey text
                size=14  # Font size
            ),
            show_checkbox_column=False,  # No checkboxes
            column_spacing=30,  # Space between columns
            columns=[
                ft.DataColumn(ft.Text("Name", weight=ft.FontWeight.BOLD)),  # Name column
                ft.DataColumn(ft.Text("Description", weight=ft.FontWeight.BOLD)),  # Description column
                ft.DataColumn(ft.Text("Users", weight=ft.FontWeight.BOLD)),  # Users column
                ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.BOLD)),  # Action column
            ],
            rows=[]  # Start with empty rows
        )

        # Layout of the page
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[self.add_button, self.loading_spinner],  # Add button and spinner
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Space them apart
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER  # Center vertically
                                ),
                                self.table  # Department table
                            ],
                            expand=True,  # Fill available space
                            alignment=ft.MainAxisAlignment.START  # Align to top
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,  # Align to left
                    expand=True  # Fill available space
                )
            ],
            expand=True  # Fill available space
        )

        # Add the page to the UI and load department data
        page.add(self)
        self.load_departments()

    def connect_to_database(self):
        """Connect to the MySQL database and return the connection."""
        try:
            connection = mysql.connector.connect(
                host="200.200.200.23",  # Database server
                user="root",  # Database user
                password="Pak@123",  # Database password
                database="itasset",  # Database name
                auth_plugin='mysql_native_password'  # Authentication method
            )
            print("Connected to database successfully")
            return connection
        except mysql.connector.Error as error:
            print(f"Failed to connect to database: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Database error: {error}"), duration=4000))
            return None

    def load_departments(self):
        """Fetch department data from the database and update the table."""
        self.loading_spinner.visible = True  # Show the loading spinner
        self.page.update()  # Refresh the UI

        connection = self.connect_to_database()  # Get database connection
        if not connection:
            self.loading_spinner.visible = False  # Hide spinner
            self.page.update()  # Refresh UI
            return

        try:
            cursor = connection.cursor()  # Create a cursor to execute queries
            # Fetch departments and count of users in each
            cursor.execute("""
                SELECT department.id, department.name, department.description, COUNT(users.id) as user_count
                FROM department
                LEFT JOIN users ON department.id = users.department_id
                GROUP BY department.id
            """)
            departments = cursor.fetchall()  # Get all department data
            self.table.rows = []  # Clear existing rows

            # Add each department to the table
            for department in departments:
                dept_id, name, description, user_count = department
                self.table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(name or "N/A")),  # Department name
                            ft.DataCell(ft.Text(description or "N/A")),  # Description
                            ft.DataCell(
                                ft.TextButton(
                                    str(user_count),  # Number of users
                                    on_click=lambda e, count=user_count: self.show_users(count)  # Click to view users
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Edit",  # Edit button
                                            bgcolor=ft.colors.LIGHT_GREEN_500,  # Green background
                                            color=ft.colors.WHITE,  # White text
                                            on_click=lambda e, id=dept_id: self.edit_department(id)  # Open edit form
                                        ),
                                        ft.ElevatedButton(
                                            "Delete",  # Delete button
                                            bgcolor=ft.colors.RED_500,  # Red background
                                            color=ft.colors.WHITE,  # White text
                                            on_click=lambda e, id=dept_id: self.delete_department(id)  # Delete department
                                        )
                                    ],
                                    spacing=5,  # Space between buttons
                                    alignment=ft.MainAxisAlignment.CENTER  # Center buttons
                                )
                            )
                        ]
                    )
                )
        except mysql.connector.Error as error:
            print(f"Failed to load departments: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error loading departments: {error}"), duration=4000))
        finally:
            if connection and connection.is_connected():
                cursor.close()  # Close the cursor
                connection.close()  # Close the connection
                print("Database connection closed")
            self.loading_spinner.visible = False  # Hide the spinner
            self.page.update()  # Refresh the UI

    def show_users(self, user_count: int):
        """Go to the users page if the department has users."""
        if user_count > 0:
            self.page.go('/users')  # Navigate to users page
        else:
            self.page.open(ft.SnackBar(ft.Text("No users in this department."), duration=3000))  # Show message

    def edit_department(self, dept_id: int):
        """Open the form to edit a department's details."""
        connection = self.connect_to_database()  # Get database connection
        if not connection:
            return

        try:
            cursor = connection.cursor()  # Create a cursor
            cursor.execute("SELECT name, description FROM department WHERE id = %s", (dept_id,))  # Fetch department
            department = cursor.fetchone()  # Get department data
            if department:
                name, description = department
                self.department_form.open(name, description, dept_id)  # Open form with existing data
            else:
                self.page.open(ft.SnackBar(ft.Text(f"Department ID {dept_id} not found."), duration=4000))
        except mysql.connector.Error as error:
            print(f"Failed to fetch department: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching department: {error}"), duration=4000))
        finally:
            if connection and connection.is_connected():
                cursor.close()  # Close the cursor
                connection.close()  # Close the connection
                print("Database connection closed")

    def delete_department(self, dept_id: int):
        """Delete a department from the database."""
        connection = self.connect_to_database()  # Get database connection
        if not connection:
            return

        try:
            cursor = connection.cursor()  # Create a cursor
            cursor.execute("DELETE FROM department WHERE id = %s", (dept_id,))  # Delete department
            connection.commit()  # Save changes
            print(f"Deleted department ID: {dept_id}")
            self.page.open(ft.SnackBar(ft.Text("Department deleted successfully."), duration=3000))
            self.load_departments()  # Refresh the table
        except mysql.connector.Error as error:
            print(f"Failed to delete department: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error deleting department: {error}"), duration=4000))
        finally:
            if connection and connection.is_connected():
                cursor.close()  # Close the cursor
                connection.close()  # Close the connection
                print("Database connection closed")

def create_department_page(page: ft.Page) -> Department:
    """Create and return a Department page."""
    return Department(page)