import flet as ft
import mysql.connector
import asyncio
from components.fields import CustomTextField

class DepartDialog:
    def __init__(self, page: ft.Page, parent):
        self.page = page
        self.parent = parent
        self.dep_id = None
        self.snackbar_container = None

        # Form Fields
        self.name_field = CustomTextField(label="Department Name", hint_text="Enter department name")
        self.desc_field = CustomTextField(label="Description", hint_text="Enter description (optional)")

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

        # Form inside dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add/Edit Department"),
            content=ft.Column(
                controls=[
                    self.name_field,
                    self.desc_field,
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

    def cancel(self, e: ft.ControlEvent):
        """Closes the dialog."""
        self.dialog.open = False
        self.clear_form()
        self.page.update()

    async def save_button_clicked(self, e: ft.ControlEvent):
        """Handles saving the department."""
        name = self.name_field.value.strip()
        desc = self.desc_field.value.strip()

        # Validation
        if not name:
            await self.show_snackbar("Department name is required!", ft.colors.RED_400)
            return

        if len(name) > 100:
            await self.show_snackbar("Department name must be 100 characters or less!", ft.colors.RED_400)
            return

        if desc and len(desc) > 255:
            await self.show_snackbar("Description must be 255 characters or less!", ft.colors.RED_400)
            return

        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            # Check for duplicate department name (case-insensitive)
            cur.execute(
                "SELECT id FROM department WHERE LOWER(name) = LOWER(%s) AND id != %s",
                (name, self.dep_id or 0)
            )
            existing_dep = cur.fetchone()
            if existing_dep:
                await self.show_snackbar("Department name already exists!", ft.colors.AMBER_300)
                return

            # Insert or update the department
            if self.dep_id:
                sql = "UPDATE department SET name = %s, description = %s WHERE id = %s"
                val = (name, desc, self.dep_id)
            else:
                sql = "INSERT INTO department (name, description) VALUES (%s, %s)"
                val = (name, desc)

            cur.execute(sql, val)
            connection.commit()
            self.parent.load_departments()
            self.dialog.open = False
            self.clear_form()
            self.page.update()
            await self.show_snackbar(
                f"Department {'updated' if self.dep_id else 'added'} successfully!",
                ft.colors.GREEN_400
            )
        except mysql.connector.Error as error:
            print(f"Error saving department: {error}")
            await self.show_snackbar(f"Error saving department: {error}", ft.colors.RED_400)
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
        self.desc_field.value = ""
        self.dep_id = None
        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)
            self.snackbar_container = None

    def on_dialog_dismiss(self, e: ft.ControlEvent):
        """Handles dialog dismissal."""
        self.clear_form()
        print("Dialog dismissed!")
        self.page.update()

    def open(self, name: str = "", desc: str = "", dep_id: int = None):
        """Opens the dialog with the given department details."""
        self.dep_id = dep_id
        self.name_field.value = name
        self.desc_field.value = desc
        self.dialog.open = True
        self.page.update()