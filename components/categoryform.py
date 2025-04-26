import flet as ft
from components.fields import CustomTextField
import mysql.connector
import asyncio

class CatDialog:
    def __init__(self, page: ft.Page):
        self.page = page
        self.cat_id = None
        self.snackbar_container = None

        # Form Fields
        self.name_field = CustomTextField(label="Name", hint_text="Enter category name")
        self.type_field = ft.Dropdown(
            label="Type",
            hint_text="Select category type",
            options=[
                ft.dropdown.Option("Asset"),
                ft.dropdown.Option("Component"),
                ft.dropdown.Option("Consumable"),
            ],
        )
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
            bgcolor=ft.colors.RED_100,
            title=ft.Text("Add/Edit Category"),
            content=ft.Column(
                controls=[
                    self.build_form_row("Name", self.name_field),
                    self.build_form_row("Type", self.type_field),
                    self.build_form_row("Description", self.desc_field),
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

    def build_form_row(self, label_text, input_control):
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

    def cancel(self, e):
        """Closes the dialog."""
        self.dialog.open = False
        self.clear_form()
        self.page.update()

    async def save_button_clicked(self, e):
        """Handles saving the category."""
        name = self.name_field.value.strip()
        desc = self.desc_field.value.strip()
        cat_type = self.type_field.value

        # Validation
        if not name:
            await self.show_snackbar("Category name is required!", ft.colors.RED_400)
            return

        if len(name) > 100:
            await self.show_snackbar("Category name must be 100 characters or less!", ft.colors.RED_400)
            return

        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            # Check for duplicate category name (case-insensitive)
            cur.execute(
                "SELECT id FROM category WHERE LOWER(name) = LOWER(%s) AND id != %s",
                (name, self.cat_id or 0)
            )
            existing_cat = cur.fetchone()
            if existing_cat:
                await self.show_snackbar("Category name already exists!", ft.colors.AMBER_300)
                return

            # Insert or update the category
            if self.cat_id:
                sql = "UPDATE category SET name = %s, description = %s, type = %s WHERE id = %s"
                val = (name, desc, cat_type, self.cat_id)
            else:
                sql = "INSERT INTO category (name, description, type) VALUES (%s, %s, %s)"
                val = (name, desc, cat_type)

            cur.execute(sql, val)
            connection.commit()
            self.dialog.open = False
            self.clear_form()
            self.page.update()
            await self.show_snackbar(
                f"Category {'updated' if self.cat_id else 'added'} successfully!",
                ft.colors.GREEN_400
            )
        except mysql.connector.Error as error:
            print(f"Error saving category: {error}")
            await self.show_snackbar(f"Error saving category: {error}", ft.colors.RED_400)
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
        self.type_field.value = None
        self.cat_id = None
        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)
            self.snackbar_container = None

    def on_dialog_dismiss(self, e: ft.ControlEvent):
        """Handles dialog dismissal."""
        self.clear_form()
        print("Dialog dismissed!")
        self.page.update()

    def open(self, name: str = "", desc: str = "", image_path: str = "", cat_type: str = "", cat_id: int = None):
        """Opens the dialog with the given category details."""
        self.cat_id = cat_id
        self.name_field.value = name
        self.desc_field.value = desc
        self.type_field.value = cat_type
        self.dialog.open = True
        self.page.update()