import flet as ft
import mysql.connector
import datetime
import os
import re

from components.fields import CustomTextField

class ConsumableForm(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        page.window.title = "Asset Management System - Add Consumable"
        self.page = page
        self.expand = True

        self.stack_width = 300
        self.stack_height = 250
        self.container_size = 50

        # Decorative stack for UI
        self.c1 = ft.Container(
            width=self.container_size,
            height=self.container_size,
            bgcolor="red",
            top=0,
            left=0
        )

        self.c2 = ft.Container(
            width=self.container_size,
            height=self.container_size,
            bgcolor="green",
            top=60,
            left=0
        )

        self.c3 = ft.Container(
            width=self.container_size,
            height=self.container_size,
            bgcolor="blue",
            top=120,
            left=0
        )

        # File picker for image and bill copy upload
        self.file_picker = ft.FilePicker(on_result=self.file_picker_result)
        page.overlay.append(self.file_picker)

        # Date pickers
        self.date_picker = ft.DatePicker(
            on_change=self.date_picker_result,
            on_dismiss=self.date_picker_dismiss,
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime.now()
        )
        page.overlay.append(self.date_picker)

        self.deploy_date_picker = ft.DatePicker(
            on_change=self.deploy_date_picker_result,
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime.now()
        )
        page.overlay.append(self.deploy_date_picker)

        # Form fields
        category_options = [
            ft.dropdown.Option("Printer Cartridge"),
            ft.dropdown.Option("Battery"),
            ft.dropdown.Option("Cell"),
            ft.dropdown.Option("Printer Paper"),
            ft.dropdown.Option("Other"),
        ]

        self.name_field = CustomTextField(label="Consumable Name")
        self.category_field = ft.Dropdown(
            label="Category",
            options=category_options,
            hint_text="Select Category",
        )
        self.company_field = CustomTextField(label="Company")
        self.model_field = CustomTextField(label="Model")
        self.serial_no_field = CustomTextField(label="Serial No")
        self.purchaser_field = CustomTextField(label="Purchaser")
        self.location_field = CustomTextField(label="Location")
        self.bill_copy_field = ft.ElevatedButton(
            icon=ft.icons.FILE_UPLOAD,
            text="Upload Bill Copy",
            on_click=lambda e: setattr(self, 'last_picker_button', "bill_copy") or self.file_picker.pick_files()
        )
        self.bill_copy_display = ft.Text("No file selected")
        self.image_field = ft.ElevatedButton(
            icon=ft.icons.IMAGE,
            text="Upload Consumable Image",
            on_click=lambda e: setattr(self, 'last_picker_button', "image") or self.file_picker.pick_files()
        )
        self.image_display = ft.Image(
            src=None,
            width=100,
            height=100,
            fit=ft.ImageFit.CONTAIN,
            visible=False,
            error_content=ft.Text("No image selected")
        )
        self.purchase_date_text = ft.Text("No date selected")
        self.purchase_date_button = ft.ElevatedButton(
            icon=ft.icons.CALENDAR_MONTH,
            text="Select Purchase Date",
            on_click=lambda e: self.show_date_picker()
        )
        self.warranty_field = CustomTextField(label="Warranty")
        self.price_field = CustomTextField(label="Price")
        self.total_qty_field = CustomTextField(label="Total Quantity")
        self.status_field = ft.Dropdown(
            label="Status",
            options=[
                ft.dropdown.Option("Available"),
                ft.dropdown.Option("Deployed"),
            ],
            value="Available",
        )
        self.status_field_row = ft.Row(
            controls=[
                self.status_field,
                ft.Icon(name=ft.icons.ARROW_DROP_DOWN, color=ft.colors.BLUE_500, size=20),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.END,
            expand=True,
        )

        # Deployment fields
        self.deployed_to_field = CustomTextField(label="Deployed To (User, Department, or Printer)")
        self.deploy_target_type_field = ft.Dropdown(
            label="Deploy Target Type",
            options=[
                ft.dropdown.Option("User"),
                ft.dropdown.Option("Department"),
                ft.dropdown.Option("Printer"),
            ],
            hint_text="Select Target Type",
        )
        self.deploy_date_text = ft.Text("No deploy date selected")
        self.deploy_date_button = ft.ElevatedButton(
            icon=ft.icons.CALENDAR_MONTH,
            text="Select Deploy Date",
            on_click=lambda e: self.show_deploy_date_picker()
        )

        self.deployment_dialog = ft.AlertDialog(
            title=ft.Text("Deployment Details"),
            content=ft.Column([
                self.deployed_to_field,
                self.deploy_target_type_field,
                self.build_form_row("Deploy Date", self.deploy_date_button),
                self.deploy_date_text,
            ], spacing=10),
            actions=[
                ft.TextButton("Save", on_click=self.save_deployment),
                ft.TextButton("Cancel", on_click=self.cancel_deployment),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Form layout
        self.content = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    width=250,
                    col={"sm": 12, "md": 3},
                    content=ft.Column(
                        controls=[
                            ft.Stack([self.c1, self.c2, self.c3], width=self.stack_width, height=self.stack_height)
                        ],
                        spacing=20
                    )
                ),
                ft.Container(
                    expand=True,
                    col={"sm": 12, "md": 9},
                    bgcolor=ft.colors.GREY_100,
                    padding=30,
                    content=ft.Container(
                        bgcolor=ft.colors.WHITE,
                        border_radius=ft.border_radius.all(15),
                        padding=30,
                        shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.colors.GREY_400),
                        content=ft.Column(
                            controls=[
                                ft.Text("Consumable Registration", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                                self.build_form_row("Consumable Name", self.name_field),
                                self.category_field,
                                self.build_form_row("Company", self.company_field),
                                self.build_form_row("Model", self.model_field),
                                self.build_form_row("Serial No", self.serial_no_field),
                                self.build_form_row("Purchaser", self.purchaser_field),
                                self.build_form_row("Location", self.location_field),
                                self.build_form_row("Upload Bill Copy", self.bill_copy_field),
                                self.bill_copy_display,
                                self.build_form_row("Upload Consumable Image", self.image_field),
                                self.image_display,
                                self.build_form_row("Purchase Date", self.purchase_date_button),
                                self.purchase_date_text,
                                self.build_form_row("Warranty", self.warranty_field),
                                self.build_form_row("Price", self.price_field),
                                self.build_form_row("Total Quantity", self.total_qty_field),
                                self.build_form_row("Status", self.status_field_row),
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Save",
                                            icon=ft.icons.SAVE,
                                            bgcolor=ft.colors.GREEN_600,
                                            color=ft.colors.WHITE,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10)
                                            ),
                                            on_click=self.save_consumable
                                        ),
                                        ft.ElevatedButton(
                                            "Cancel",
                                            icon=ft.icons.CANCEL,
                                            bgcolor=ft.colors.RED_600,
                                            color=ft.colors.WHITE,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10)
                                            ),
                                            on_click=self.cancel_form
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
        return ft.ResponsiveRow(
            controls=[
                ft.Container(
                    width=150,
                    col={"xs": 12, "md": 3},
                    content=ft.Text(label_text, size=18, weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_700),
                ),
                ft.Container(
                    expand=True,
                    col={"xs": 12, "md": 9},
                    content=input_control,
                ),
            ],
            spacing=10,
        )

    def show_date_picker(self):
        self.date_picker.open = True
        self.page.update()

    def show_deploy_date_picker(self):
        self.deploy_date_picker.open = True
        self.page.update()

    def file_picker_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            ext = os.path.splitext(file.name)[1]
            if self.last_picker_button == "image":
                # Validate consumable name
                consumable_name = self.name_field.value.strip()
                if not consumable_name:
                    self.page.open(ft.SnackBar(ft.Text("Please enter a consumable name before uploading an image"), duration=4000))
                    return
                # Sanitize consumable name for filename
                safe_name = re.sub(r'[^\w\s-]', '', consumable_name).replace(' ', '_')
                if not safe_name:
                    safe_name = "consumable"
                # Generate filename with consumable name and timestamp
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                save_filename = f"{safe_name}_{timestamp}{ext}"
                save_path = os.path.join("images", save_filename).replace("\\", "/")
                # Ensure images/ folder exists
                os.makedirs("images", exist_ok=True)
                # Save the file
                try:
                    with open(file.path, "rb") as src, open(save_path, "wb") as dst:
                        dst.write(src.read())
                    print(f"Saved image to: {save_path}")
                    self.image_display.src = save_path
                    self.image_display.visible = True
                except Exception as ex:
                    print(f"Failed to save image: {ex}")
                    self.page.open(ft.SnackBar(ft.Text(f"Failed to save image: {ex}"), duration=4000))
                    return
            else:
                # Handle bill copy
                file_name = file.name
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                save_filename = f"{os.path.splitext(file_name)[0]}_{timestamp}{ext}"
                save_path = os.path.join("images", save_filename).replace("\\", "/")
                os.makedirs("images", exist_ok=True)
                try:
                    with open(file.path, "rb") as src, open(save_path, "wb") as dst:
                        dst.write(src.read())
                    print(f"Saved bill copy to: {save_path}")
                except Exception as ex:
                    print(f"Failed to save bill copy: {ex}")
                    self.page.open(ft.SnackBar(ft.Text(f"Failed to save bill copy: {ex}"), duration=4000))
                    return
                self.bill_copy_display.value = save_path
            self.page.update()

    def date_picker_result(self, e):
        if e.control.value:
            self.purchase_date_text.value = e.control.value.strftime("%Y-%m-%d")
        else:
            self.purchase_date_text.value = "No date selected"
        self.date_picker.open = False
        self.page.update()

    def date_picker_dismiss(self, e):
        self.purchase_date_text.value = "No date selected"
        self.date_picker.open = False
        self.page.update()

    def deploy_date_picker_result(self, e):
        if e.control.value:
            self.deploy_date_text.value = e.control.value.strftime("%Y-%m-%d")
        else:
            self.deploy_date_text.value = "No deploy date selected"
        self.deploy_date_picker.open = False
        self.page.update()

    def validate_consumable_fields(self):
        required_fields = {
            "Consumable Name": self.name_field.value,
            "Category": self.category_field.value,
            "Company": self.company_field.value,
            "Model": self.model_field.value,
            "Serial No": self.serial_no_field.value,
            "Purchaser": self.purchaser_field.value,
            "Location": self.location_field.value,
            "Price": self.price_field.value,
            "Warranty": self.warranty_field.value,
            "Total Quantity": self.total_qty_field.value,
            "Status": self.status_field.value,
            "Purchase Date": self.purchase_date_text.value,
            "Image": self.image_display.src
        }

        empty_fields = [
            field for field, value in required_fields.items()
            if not value or value == "No date selected" or value is None
        ]

        return empty_fields

    def save_deployment(self, e):
        print("Entering save_deployment")
        empty_fields = self.validate_consumable_fields()
        if empty_fields:
            print(f"Validation failed: {empty_fields}")
            self.page.open(ft.SnackBar(ft.Text(f"Please fill all required fields: {', '.join(empty_fields)}"), duration=4000))
            return

        deployed_to = self.deployed_to_field.value
        deploy_target_type = self.deploy_target_type_field.value
        deploy_date = self.deploy_date_text.value if self.deploy_date_text.value != "No deploy date selected" else None

        if not deployed_to or not deploy_target_type or not deploy_date:
            print("Deployment fields missing")
            self.page.open(ft.SnackBar(ft.Text("Please fill all deployment details: Deployed To, Deploy Target Type, Deploy Date"), duration=4000))
            return

        # Validate total quantity
        try:
            total_qty = int(self.total_qty_field.value)
            if total_qty < 0:
                self.page.open(ft.SnackBar(ft.Text("Total Quantity cannot be negative"), duration=4000))
                return
        except ValueError as ve:
            print(f"Quantity conversion error: {ve}")
            self.page.open(ft.SnackBar(ft.Text("Total Quantity must be a valid number"), duration=4000))
            return

        try:
            print("Connecting to database")
            connection = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            cur = connection.cursor()

            consumable_data = {
                "name": self.name_field.value,
                "category": self.category_field.value,
                "company": self.company_field.value,
                "model": self.model_field.value,
                "serial_no": self.serial_no_field.value,
                "purchaser": self.purchaser_field.value,
                "location": self.location_field.value,
                "price": None,
                "warranty": self.warranty_field.value,
                "total_qty": total_qty,
                "bill_copy": self.bill_copy_display.value if self.bill_copy_display.value != "No file selected" else None,
                "purchase_date": self.purchase_date_text.value if self.purchase_date_text.value != "No date selected" else None,
                "image_path": self.image_display.src if self.image_display.src else None,
            }

            try:
                if self.price_field.value:
                    consumable_data["price"] = float(self.price_field.value)
            except ValueError as ve:
                print(f"Price conversion error: {ve}")
                self.page.open(ft.SnackBar(ft.Text("Invalid price format. Please enter a valid number."), duration=4000))
                return

            print("Inserting into deployed_consumables")
            sql = """
                INSERT INTO deployed_consumables (
                    name, category, company, model, serial_no, purchaser, location, price, warranty,
                    total_qty, bill_copy, purchase_date, image_path,
                    status, deployed_to, deploy_target_type, deploy_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, (
                consumable_data["name"], consumable_data["category"], consumable_data["company"], consumable_data["model"],
                consumable_data["serial_no"], consumable_data["purchaser"], consumable_data["location"], consumable_data["price"],
                consumable_data["warranty"], consumable_data["total_qty"],
                consumable_data["bill_copy"], consumable_data["purchase_date"], consumable_data["image_path"],
                "Deployed", deployed_to, deploy_target_type, deploy_date
            ))

            connection.commit()
            print("Deployed consumable saved successfully")
            self.page.dialog.open = False
            self.clear_form()
            print("Before redirect from save_deployment, current route:", self.page.route)
            self.page.go("/consumables")
            print("After redirect attempt from save_deployment, current route:", self.page.route)
            self.page.update()

        except mysql.connector.Error as error:
            print(f"Database error in save_deployment: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Database error: {error}"), duration=4000))
        except Exception as e:
            print(f"Unexpected error in save_deployment: {e}")
            self.page.open(ft.SnackBar(ft.Text(f"Unexpected error: {e}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

    def cancel_deployment(self, e):
        print("Canceling deployment dialog")
        self.page.dialog.open = False
        self.status_field.value = "Available"
        self.page.update()

    def save_consumable(self, e):
        print("Entering save_consumable")
        empty_fields = self.validate_consumable_fields()
        if empty_fields:
            print(f"Validation failed: {empty_fields}")
            self.page.open(ft.SnackBar(ft.Text(f"Please fill all required fields: {', '.join(empty_fields)}"), duration=4000))
            return

        # Validate total quantity
        try:
            total_qty = int(self.total_qty_field.value)
            if total_qty < 0:
                self.page.open(ft.SnackBar(ft.Text("Total Quantity cannot be negative"), duration=4000))
                return
        except ValueError as ve:
            print(f"Quantity conversion error: {ve}")
            self.page.open(ft.SnackBar(ft.Text("Total Quantity must be a valid number"), duration=4000))
            return

        if self.status_field.value == "Deployed":
            print("Showing deployment dialog")
            self.page.dialog = self.deployment_dialog
            self.page.dialog.open = True
            self.page.update()
            return

        try:
            print("Connecting to database")
            connection = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            cur = connection.cursor()

            price = None
            try:
                if self.price_field.value:
                    price = float(self.price_field.value)
            except ValueError as ve:
                print(f"Price conversion error: {ve}")
                self.page.open(ft.SnackBar(ft.Text("Invalid price format. Please enter a valid number."), duration=4000))
                return

            print("Inserting into consumables")
            sql = """
                INSERT INTO consumables (
                    name, category, company, model, serial_no, purchaser, location, price, warranty,
                    total_qty, status, bill_copy, purchase_date, image_path
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, (
                self.name_field.value,
                self.category_field.value,
                self.company_field.value,
                self.model_field.value,
                self.serial_no_field.value,
                self.purchaser_field.value,
                self.location_field.value,
                price,
                self.warranty_field.value,
                total_qty,
                self.status_field.value,
                self.bill_copy_display.value if self.bill_copy_display.value != "No file selected" else None,
                self.purchase_date_text.value if self.purchase_date_text.value != "No date selected" else None,
                self.image_display.src if self.image_display.src else None
            ))

            connection.commit()
            print("Consumable saved successfully")
            self.clear_form()
            print("Before redirect from save_consumable, current route:", self.page.route)
            self.page.go("/consumables")
            print("After redirect attempt from save_consumable, current route:", self.page.route)
            self.page.update()

        except mysql.connector.Error as error:
            print(f"Database error in save_consumable: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Database error: {error}"), duration=4000))
        except Exception as e:
            print(f"Unexpected error in save_consumable: {e}")
            self.page.open(ft.SnackBar(ft.Text(f"Unexpected error: {e}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

    def cancel_form(self, e):
        print("Entering cancel_form")
        self.clear_form()
        print("Before redirect from cancel_form, current route:", self.page.route)
        self.page.go("/consumables")
        print("After redirect attempt from cancel_form, current route:", self.page.route)
        self.page.update()

    def clear_form(self):
        print("Clearing form")
        self.name_field.value = ""
        self.category_field.value = None
        self.company_field.value = ""
        self.model_field.value = ""
        self.serial_no_field.value = ""
        self.purchaser_field.value = ""
        self.location_field.value = ""
        self.price_field.value = ""
        self.warranty_field.value = ""
        self.total_qty_field.value = ""
        self.status_field.value = "Available"
        self.bill_copy_display.value = "No file selected"
        self.image_display.src = None
        self.image_display.visible = False
        self.purchase_date_text.value = "No date selected"
        self.deployed_to_field.value = ""
        self.deploy_target_type_field.value = None
        self.deploy_date_text.value = "No deploy date selected"
        self.page.update()

def ConsumableFormPage(page):
    return ConsumableForm(page)