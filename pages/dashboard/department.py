import flet as ft
import mysql.connector
#from nav.menubar import TopBarPage
#from nav.sidebar import SidebarPage
from components.departmentform import DepartDialog

class Department(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page  # Store page reference
        self.expand = True
        page.window.title = "Asset Management System - Departments"

        self.depart_dialog = DepartDialog(page, self)

        # Add Department Button
        add_department_button = ft.ElevatedButton(
            icon=ft.Icons.ADD,
            text="Add Department",
            bgcolor=ft.Colors.YELLOW_600,
            width=180,
            height=50,
            color=ft.Colors.WHITE,
            on_click=lambda e: self.depart_dialog.open()  
        )

        # Department Table
        self.department_table = ft.DataTable(
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            vertical_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            heading_row_color=ft.Colors.INDIGO_100,
            heading_text_style=ft.TextStyle(
                color=ft.Colors.INDIGO_900,
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            data_row_color={ft.ControlState.HOVERED: ft.Colors.LIGHT_BLUE_50},
            data_row_min_height=50,
            data_text_style=ft.TextStyle(
                color=ft.Colors.GREY_800,
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
                #TopBarPage(page),
                ft.Row(
                    controls=[
                        # ft.Column(
                        #     controls=[ft.Container(content=SidebarPage(page), width=200, expand=True)],
                        # ),
                        ft.Column(
                            controls=[
                                ft.Row(controls=[add_department_button]),
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

        # Load data only after UI is fully initialized
        page.add(self)  
        self.load_departments()

    def load_departments(self):
        """Fetches and displays department data, including user count."""
        try:
            conn = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            mycursor = conn.cursor()
            mycursor.execute("""
            SELECT department.id, department.name, department.description, COUNT(users.id) as user_count
            FROM department
            LEFT JOIN users ON department.id = users.department_id
            GROUP BY department.id
            """)
            myresult = mycursor.fetchall()
            self.department_table.rows.clear()  # Clear previous rows

            for x in myresult:
                self.department_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(x[1])),  # Department Name
                            ft.DataCell(ft.Text(x[2])),  # Department Description
                            ft.DataCell(ft.TextButton(str(x[3]), on_click=lambda e: self.page.go('/user'))),  # User Count with navigation
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton("Edit", 
                                            bgcolor=ft.Colors.LIGHT_GREEN_500, 
                                            color=ft.Colors.WHITE, 
                                            on_click=lambda e, dep_id=x[0]: self.edit_department(dep_id)
                                        ),
                                        ft.ElevatedButton("Delete", 
                                            bgcolor=ft.Colors.RED_500, 
                                            color=ft.Colors.WHITE, 
                                            on_click=lambda e, dep_id=x[0]: self.delete_department(dep_id)
                                        ),
                                    ],
                                    spacing=5,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                )
                            ),
                        ]
                    )
                )
            self.page.update()  # Update the entire page instead of self.update()
        except mysql.connector.Error as error:
            print(f"Error fetching departments: {error}")
        finally:
            if conn.is_connected():
                mycursor.close()
                conn.close()

    def edit_department(self, dep_id):
        """Handles editing a department (future implementation)."""
        conn = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
        mycursor = conn.cursor()
        mycursor.execute("SELECT name, description FROM department WHERE id = %s", (dep_id,))
        myresult = mycursor.fetchone()
        if myresult:
            self.depart_dialog.open(myresult[0], myresult[1], dep_id)
        else:
            print(f"Department ID {dep_id} not found.")
        mycursor.close()
        conn.close()

        
    


    def delete_department(self, dep_id):
        """Handles deleting a department from the database."""
        try:
            conn = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            mycursor = conn.cursor()
            mycursor.execute("DELETE FROM department WHERE id = %s", (dep_id,))
            conn.commit()
            print(f"Deleted department ID: {dep_id}")
            self.load_departments()  # Refresh table
        except mysql.connector.Error as error:
            print(f"Error deleting department: {error}")
        finally:
            if conn.is_connected():
                mycursor.close()
                conn.close()
