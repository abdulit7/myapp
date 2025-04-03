import flet as ft
import mysql.connector
from nav.sidebar import Sidebar
from nav.menubar import TopBarPage
from components.fields import CustomTextField

class UserForm(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        page.window.title = "Asset Management System"

        self.expand = True

        # File Picker for Uploading Image
        self.file_picker = ft.FilePicker(on_result=self.file_picker_result)
        page.overlay.append(self.file_picker)

        self.name_field = CustomTextField(label="Name")
        self.emp_id_field = CustomTextField(label="EMP ID")
        self.password_field = CustomTextField(label="Password", password=True, can_reveal_password=True)
        self.branch_field = CustomTextField(label="Branch")
        self.can_login_field = ft.Checkbox(label="This User Can Login")

        # Department Dropdown (Loads department ID and name)
        self.department_dropdown = ft.Dropdown(
            label="Department",
            options=self.dep_dropdown(),  # Fetch data dynamically
        )

        # Form Layout
        self.content = ft.ResponsiveRow(
            controls=[
                # Sidebar
                ft.Container(
                    width=250,
                    col={"sm": 12, "md": 3},
                    content=ft.Column(
                        controls=[
                            TopBarPage(page),
                            ft.Text("Menu", size=18, weight=ft.FontWeight.W_600),
                            Sidebar(page),
                        ],
                        spacing=20
                    )
                ),
                # Main Form Area
                ft.Container(
                    expand=True,
                    col={"sm": 12, "md": 9},
                    bgcolor=ft.Colors.GREY_100,
                    padding=30,
                    content=ft.Container(
                        bgcolor=ft.Colors.WHITE,
                        border_radius=ft.border_radius.all(15),
                        padding=30,
                        shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.Colors.GREY_400),
                        content=ft.Column(
                            controls=[
                                ft.Text("User Registration", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                self.build_form_row("Name", self.name_field),
                                self.build_form_row("EMP ID", self.emp_id_field),
                                self.build_form_row("Password", self.password_field),
                                self.build_form_row("Branch", self.branch_field),
                                self.build_form_row("Department", self.department_dropdown),
                                self.build_form_row("This User Can Login", self.can_login_field),
                                self.build_form_row("Upload Image", 
                                    ft.ElevatedButton("Choose File", 
                                        icon=ft.icons.UPLOAD_FILE, 
                                        on_click=lambda e: self.file_picker.pick_files(allow_multiple=False)
                                    )
                                ),
                                # Save and Cancel Buttons
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton("Save", 
                                            icon=ft.icons.SAVE, 
                                            bgcolor=ft.Colors.GREEN_600, 
                                            color=ft.Colors.WHITE, 
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10)
                                            ),
                                            on_click=self.save_user
                                        ),
                                        ft.ElevatedButton("Cancel", 
                                            icon=ft.icons.CANCEL, 
                                            bgcolor=ft.Colors.RED_600, 
                                            color=ft.Colors.WHITE, 
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10)
                                            )
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                    spacing=20,
                                )
                            ],
                            spacing=20,
                        )
                    )
                )
            ],
            spacing=20
        )

    def build_form_row(self, label_text, input_control):
        """Builds a single row for the form with a label and input field."""
        return ft.ResponsiveRow(
            controls=[
                ft.Container(
                    width=150,
                    col={"xs": 12, "md": 3},
                    content=ft.Text(label_text, size=18, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_GREY_700),
                ),
                ft.Container(
                    expand=True,
                    col={"xs": 12, "md": 9},
                    content=input_control,
                ),
            ],
            spacing=10,
        )

    def file_picker_result(self, e: ft.FilePickerResultEvent):
        """Handles the file selection result."""
        if e.files:
            print(f"Selected file: {e.files[0].name}")

    def save_user(self, e):
        """Saves the user data to the database with department_id."""
        name = self.name_field.value
        emp_id = self.emp_id_field.value
        password = self.password_field.value
        branch = self.branch_field.value
        department_id = self.department_dropdown.value  # Get department ID
        can_login = 1 if self.can_login_field.value else 0  # Convert checkbox to 0 or 1

        try:
            connection = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            cur = connection.cursor()
            sql = "INSERT INTO users (name, emp_id, password, branch, department_id, can_login) VALUES (%s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (name, emp_id, password, branch, department_id, can_login))
            connection.commit()
            print("User saved successfully.")
        except mysql.connector.Error as error:
            print("Failed to insert record into MySQL table: {}".format(error))
        finally:
            cur.close()
            connection.close()

    def dep_dropdown(self):
        """Fetch department names and IDs for dropdown."""
        conn = mysql.connector.connect(
            host="200.200.200.23",
            user="root",
            password="Pak@123",
            database="itasset",
            auth_plugin='mysql_native_password'
        )
        mycursor = conn.cursor()
        mycursor.execute("SELECT id, name FROM department")
        myresult = mycursor.fetchall()
        
        department_options = [ft.dropdown.Option(text=x[1], key=str(x[0])) for x in myresult]
        mycursor.close()
        conn.close()
        return department_options
