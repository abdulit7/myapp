import flet as ft
from components.fields import CustomTextField
import mysql.connector
import asyncio


class DepartDialog:
    def __init__(self, page: ft.Page, parent):
        self.page = page
        self.parent = parent
        self.dep_id = None
        self.snackbar_container = None

        # Form Fields
        self.name_field = CustomTextField(label="Name")
        self.Desc_field = CustomTextField(label="Desc")

        # Save and Cancel Buttons
        self.save_button = ft.ElevatedButton(
            "Save",
            icon=ft.icons.SAVE,
            bgcolor=ft.colors.GREEN_400,
            color=ft.colors.WHITE,
            width=200,
            on_click=lambda e: asyncio.run(self.save_button_clicked(e))
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
                    self.Desc_field,
                    ft.Row(
                        controls=[self.save_button, self.cancel_button],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=20,
                    ),
                ],
                scroll="adaptive"
            ),
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=self.on_dialog_dismiss,
        )
        page.overlay.append(self.dialog)
        page.update()

    def cancel(self, e):
        """Closes the dialog."""
        self.dialog.open = False
        self.page.update()

    async def save_button_clicked(self, e):
        """Handles saving the department."""
        name = self.name_field.value.strip()
        desc = self.Desc_field.value.strip()

        if not name:
            await self.show_snackbar("Name required!", ft.colors.RED_400)
            return

        conn = mysql.connector.connect(
            host="200.200.200.23",
            user="root",
            password="Pak@123",
            database="itasset",
            auth_plugin='mysql_native_password'
        )
        mycursor = conn.cursor()

        # Check if department name already exists
        mycursor.execute("SELECT id FROM department WHERE LOWER(name) = LOWER(%s) AND id != %s", (name, self.dep_id or 0))
        existing_dep = mycursor.fetchone()

        if existing_dep:
            await self.show_snackbar("Department name already exists!", ft.colors.AMBER_300)
            conn.close()
            return

        # Insert or update the department
        if self.dep_id:
            sql = "UPDATE department SET name = %s, description = %s WHERE id = %s"
            val = (name, desc, self.dep_id)
        else:
            sql = "INSERT INTO department (name, description) VALUES (%s, %s)"
            val = (name, desc)

        mycursor.execute(sql, val)
        conn.commit()
        conn.close()

        self.parent.load_departments()

        # Close the dialog
        self.dialog.open = False
        self.page.update()

        await self.show_snackbar("Department saved successfully!", ft.colors.GREEN_400)

    async def show_snackbar(self, message, color):
        """Simulates a SnackBar within the AlertDialog."""
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
        asyncio.create_task(self.remove_snackbar_after_delay())

    async def remove_snackbar_after_delay(self):
        await asyncio.sleep(3)
        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)
            self.snackbar_container = None
            self.page.update()

    def on_dialog_dismiss(self, e):
        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)
            self.snackbar_container = None
        print("Dialog dismissed!")
        self.page.update()

    def open(self, name="", desc="", dep_id=None):
        """Opens the dialog with the given department details."""
        self.dep_id = dep_id
        self.name_field.value = name
        self.Desc_field.value = desc

        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)
            self.snackbar_container = None
            self.page.update()

        self.dialog.open = True
        self.page.update()