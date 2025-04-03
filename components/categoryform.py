import flet as ft
from components.fields import CustomTextField
import mysql.connector
import os

class CatDialog:
    def __init__(self, page: ft.Page):
        self.page = page

        


        # Form Fields
        self.name_field = CustomTextField(label="Name")
        self.image_field = ft.ElevatedButton(icon=ft.icons.FILE_UPLOAD, text="Upload Image", on_click=lambda e: self.file_picker.pick_files())
        self.image_display = ft.Text("No Image selected")
        self.type_field = CustomTextField(label="Type")
        self.qty_field = CustomTextField(label="QTY")
        self.desc_field = CustomTextField(label="Desc")

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
        self.page.overlay.append(self.file_picker)  # Add file picker to the page

        # Form inside dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor=ft.colors.RED_100,
            title=ft.Text("Add Category"),
            content=ft.Column(
                controls=[
                    self.build_form_row("Name", self.name_field),
                    self.build_form_row("Image", self.image_field),
                    self.build_form_row("Image", self.image_display),
                    self.build_form_row("Type", self.type_field),
                    self.build_form_row("QTY", self.qty_field),
                    self.build_form_row("Desc", self.desc_field),
                    # Save and Cancel Buttons
                    ft.Row(
                        controls=[self.save_button, self.cancel_button],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=20,
                    ),
                ],
                scroll="adaptive"
            ),
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Dialog dismissed!"),
        )

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

    def cancel(self, e):
        """Closes the dialog."""
        self.dialog.open = False
        self.page.update()

    def save_button_clicked(self, e):
        # Save the image to the directory
        image_path = self.save_image()

        # Save the form data to the database
        conn = mysql.connector.connect(
            host="200.200.200.23",
            user="root",
            password="Pak@123",
            database="itasset",
            auth_plugin='mysql_native_password'
        )
        mycursor = conn.cursor()
        sql = "INSERT INTO category (name, image, type, qty, description) VALUES (%s, %s, %s, %s, %s)"
        val = (self.name_field.value, image_path, self.type_field.value, self.qty_field.value, self.desc_field.value)
        mycursor.execute(sql, val)
        conn.commit()
        print(mycursor.rowcount, "record inserted.")
        conn.close()

        # Close the dialog
        self.dialog.open = False
        self.page.update()

    def save_image(self):
        """Saves the uploaded image to the directory and returns the file path."""
        if self.image_display.value != "No Image selected":
            # Define the directory to save the image
            directory = "assets/images/category"
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Save the image with a unique name
            file_name = f"{self.name_field.value}_{self.image_display.value}"
            file_path = os.path.join(directory, file_name)

            # Assuming the file is available in the file picker result
            selected_file = self.file_picker.result.files[0]
            with open(file_path, "wb") as f:
                with open(selected_file.path, "rb") as sf:
                    f.write(sf.read())

            return file_path
        return None

    def image_picked(self, e: ft.FilePickerResultEvent):
        """Handles file selection for image upload."""
        if e.files:
            selected_file = e.files[0]
            self.image_display.value = selected_file.name  # Display filename
            print(f"File picked: {selected_file.name}")
        else:
            self.image_display.value = "No file selected"
        self.page.update()

    def open(self):
        """Opens the dialog."""
        self.page.open(self.dialog)

