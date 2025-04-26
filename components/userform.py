import flet as ft
import mysql.connector
import os
import datetime
from typing import Optional, List, Tuple
import re
import asyncio

from components.fields import CustomTextField

class UserDialog:
    def __init__(self, page: ft.Page):
        self.page = page
        self.user_id = None
        self.selected_image = None
        self.snackbar_container = None

        # Form Fields
        self.name_field = CustomTextField(label="Name", hint_text="Enter user name")
        self.emp_id_field = CustomTextField(label="EMP ID", hint_text="Enter employee ID")
        self.password_field = CustomTextField(label="Password", hint_text="Enter password", password=True, can_reveal_password=True)
        self.branch_field = CustomTextField(label="Branch", hint_text="Enter branch name")
        self.department_dropdown = ft.Dropdown(
            label="Department",
            hint_text="Select Department",
            options=self._fetch_departments(),
        )
        self.can_login_field = ft.Checkbox(label="This User Can Login", value=False, on_change=self._toggle_password_field)
        self.image_button = ft.ElevatedButton(
            icon=ft.icons.FILE_UPLOAD,
            text="Upload Image",
            on_click=lambda e: self.file_picker.pick_files(
                allowed_extensions=["jpg", "jpeg", "png", "gif"]
            )
        )
        self.image_display = ft.Text("No Image selected")

        # Password field row (initially hidden)
        self.password_row = self.build_form_row("Password", self.password_field)
        self.password_row.visible = False  # Hide by default

        # Save and Cancel Buttons
        self.save_button = ft.ElevatedButton(
            "Save",
            icon=ft.icons.SAVE,
            bgcolor=ft.colors.GREEN_400,
            color=ft.colors.WHITE,
            width=200,
            on_click=self.save_button_clicked
        )

        self.cancel_button = ft.ElevatedButton(
            "Cancel",
            icon=ft.icons.CANCEL,
            bgcolor=ft.colors.RED_400,
            width=200,
            color=ft.colors.WHITE,
            on_click=self.cancel,
        )

        # File Picker
        self.file_picker = ft.FilePicker(on_result=self.image_picked)
        self.page.overlay.append(self.file_picker)

        # Form inside dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor=ft.colors.RED_100,
            title=ft.Text("Add/Edit User"),
            content=ft.Column(
                controls=[
                    self.build_form_row("Name", self.name_field),
                    self.build_form_row("EMP ID", self.emp_id_field),
                    self.password_row,
                    self.build_form_row("Branch", self.branch_field),
                    self.build_form_row("Department", self.department_dropdown),
                    self.build_form_row("Can Login", self.can_login_field),
                    self.build_form_row("Image", self.image_button),
                    self.build_form_row("Image", self.image_display),
                    ft.Row(
                        controls=[self.save_button, self.cancel_button],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=20,
                    ),
                ],
                scroll="adaptive",
                tight=True,
                spacing=15,
            ),
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=self.on_dialog_dismiss,
        )
        page.overlay.append(self.dialog)
        page.update()

    def build_form_row(self, label_text: str, input_control: ft.Control) -> ft.Row:
        """Builds a single row for the form with a label and input field."""
        return ft.Row(
            controls=[
                ft.Container(
                    width=150,
                    content=ft.Text(label_text, size=16, weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_700),
                ),
                ft.Container(
                    expand=True,
                    content=input_control,
                ),
            ],
            spacing=10,
        )

    def _get_db_connection(self) -> Optional[mysql.connector.connection.MySQLConnection]:
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

    def _fetch_departments(self) -> List[ft.dropdown.Option]:
        """Fetch department names and IDs for the dropdown."""
        connection = self._get_db_connection()
        if not connection:
            return []

        try:
            cur = connection.cursor()
            cur.execute("SELECT id, name FROM department")
            departments = cur.fetchall()
            return [ft.dropdown.Option(key=str(dep[0]), text=dep[1]) for dep in departments]
        except mysql.connector.Error as error:
            print(f"Error fetching departments: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching departments: {error}"), duration=4000))
            return []
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

    def _toggle_password_field(self, e: ft.ControlEvent):
        """Show or hide the password field based on the can_login checkbox."""
        self.password_row.visible = self.can_login_field.value
        if not self.can_login_field.value:
            self.password_field.value = ""  # Clear password if user cannot login
        self.page.update()

    def image_picked(self, e: ft.FilePickerResultEvent):
        """Handles file selection for image upload."""
        if e.files:
            self.selected_image = e.files[0]
            self.image_display.value = self.selected_image.name
            print(f"File picked: {self.selected_image.name}")
        else:
            self.selected_image = None
            self.image_display.value = "No Image selected"
        self.page.update()

    def save_image(self) -> Optional[str]:
        """Saves the uploaded image to the directory and returns the file path."""
        if not self.selected_image:
            return None

        # Define the directory to save the image
        directory = "assets/images/user"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Sanitize the file name
        name = re.sub(r'[^a-zA-Z0-9]', '_', self.name_field.value.lower())
        original_filename = self.selected_image.name
        file_ext = os.path.splitext(original_filename)[1]
        file_name = f"{name}_{int(self.page.session_id)}_{file_ext}"
        file_path = os.path.join(directory, file_name)

        # Save the image
        with open(file_path, "wb") as f:
            with open(self.selected_image.path, "rb") as sf:
                f.write(sf.read())

        return file_path

    async def save_button_clicked(self, e):
        """Handles saving the user."""
        name = self.name_field.value.strip()
        emp_id = self.emp_id_field.value.strip()
        password = self.password_field.value.strip() if self.can_login_field.value else None
        branch = self.branch_field.value.strip()
        department_id = int(self.department_dropdown.value) if self.department_dropdown.value else None
        can_login = 1 if self.can_login_field.value else 0

        # Validation
        if not name:
            await self.show_snackbar("Name is required!", ft.colors.RED_400)
            return
        if len(name) > 100:
            await self.show_snackbar("Name must be 100 characters or less!", ft.colors.RED_400)
            return

        if not emp_id:
            await self.show_snackbar("Employee ID is required!", ft.colors.RED_400)
            return
        if len(emp_id) > 50:
            await self.show_snackbar("Employee ID must be 50 characters or less!", ft.colors.RED_400)
            return

        if not branch:
            await self.show_snackbar("Branch is required!", ft.colors.RED_400)
            return
        if len(branch) > 100:
            await self.show_snackbar("Branch must be 100 characters or less!", ft.colors.RED_400)
            return

        if not department_id:
            await self.show_snackbar("Department is required!", ft.colors.RED_400)
            return

        if can_login and not password:
            await self.show_snackbar("Password is required if user can login!", ft.colors.RED_400)
            return

        # Save the image
        image_path = self.save_image()

        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            # Check for duplicate emp_id (case-insensitive)
            cur.execute(
                "SELECT id FROM users WHERE LOWER(emp_id) = LOWER(%s) AND id != %s",
                (emp_id, self.user_id or 0)
            )
            existing_user = cur.fetchone()
            if existing_user:
                await self.show_snackbar("Employee ID already exists!", ft.colors.AMBER_300)
                return

            # Insert or update the user
            if self.user_id:
                sql = """
                    UPDATE users
                    SET name=%s, emp_id=%s, password=%s, branch=%s, department_id=%s, can_login=%s, image_path=%s
                    WHERE id=%s
                """
                val = (name, emp_id, password, branch, department_id, can_login, image_path, self.user_id)
            else:
                sql = """
                    INSERT INTO users (name, emp_id, password, branch, department_id, can_login, image_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                val = (name, emp_id, password, branch, department_id, can_login, image_path)

            cur.execute(sql, val)
            connection.commit()
            self.dialog.open = False
            self.clear_form()
            self.page.update()
            await self.show_snackbar(
                f"User {'updated' if self.user_id else 'added'} successfully!",
                ft.colors.GREEN_400
            )
        except mysql.connector.Error as error:
            print(f"Error saving user: {error}")
            await self.show_snackbar(f"Error saving user: {error}", ft.colors.RED_400)
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

    async def show_snackbar(self, message: str, color: str):
        """Displays a snackbar within the dialog."""
        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)

        self.snackbar_container = ft.Container(
            content=ft.Text(message, color=ft.colors.WHITE),
            bgcolor=color,
            padding=10,
            border_radius=5,
            margin=ft.margin.only(top=10),
        )
        self.dialog.content.controls.append(self.snackbar_container)
        self.page.update()
        await asyncio.sleep(3)
        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)
            self.snackbar_container = None
            self.page.update()

    def clear_form(self):
        """Clears the form fields."""
        self.name_field.value = ""
        self.emp_id_field.value = ""
        self.password_field.value = ""
        self.branch_field.value = ""
        self.department_dropdown.value = None
        self.can_login_field.value = False
        self.password_row.visible = False
        self.image_display.value = "No Image selected"
        self.selected_image = None
        self.user_id = None
        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)
            self.snackbar_container = None

    def on_dialog_dismiss(self, e: ft.ControlEvent):
        """Handles dialog dismissal."""
        self.clear_form()
        print("Dialog dismissed!")
        self.page.update()

    def cancel(self, e):
        """Closes the dialog."""
        self.dialog.open = False
        self.clear_form()
        self.page.update()

    def open(self, name: str = "", emp_id: str = "", password: str = "", branch: str = "", department_id: int = None, can_login: bool = False, image_path: str = "", user_id: int = None):
        """Opens the dialog with the given user details."""
        self.user_id = user_id
        self.name_field.value = name
        self.emp_id_field.value = emp_id
        self.password_field.value = password
        self.branch_field.value = branch
        self.department_dropdown.value = str(department_id) if department_id else None
        self.can_login_field.value = can_login
        self.password_row.visible = can_login
        self.image_display.value = os.path.basename(image_path) if image_path else "No Image selected"
        self.dialog.open = True
        self.page.update()