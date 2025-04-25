import os
os.environ["FLET_SECRET_KEY"] = "mysecret123"  # This must be before importing flet
import flet as ft
import mysql.connector
import datetime
import re
from typing import Dict, List, Optional

from components.fields import CustomTextField

class AssetForm(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.selected_image = None  # Store the selected image file
        self.image_path = None  # Store the path after upload

        # Initialize file pickers
        self.image_picker = ft.FilePicker(
            on_result=self._handle_image_picker_result,
            on_upload=self._handle_image_upload
        )
        self.page.overlay.append(self.image_picker)

        # Build the UI
        self._setup_page()
        self._initialize_components()
        self._build_ui()

    def _setup_page(self) -> None:
        """Set up the page properties."""
        self.page.window.title = "Asset Management System"

    def _initialize_components(self) -> None:
        """Initialize all UI components and overlays."""
        # File and Date Pickers
        self.file_picker = ft.FilePicker(on_result=self._handle_file_picker_result)
        self.date_picker = ft.DatePicker(
            on_change=self._handle_date_picker_result,
            on_dismiss=self._handle_date_picker_dismiss,
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime.now()
        )
        self.deploy_date_picker = ft.DatePicker(
            on_change=self._handle_deploy_date_picker_result,
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime.now()
        )
        self.page.overlay.extend([self.file_picker, self.date_picker, self.deploy_date_picker])

        # Form Fields
        self.name_field = CustomTextField(label="Name")
        self.category_field = ft.Dropdown(
            label="Category",
            options=[
                ft.dropdown.Option("Desktop"),
                ft.dropdown.Option("Wyse"),
                ft.dropdown.Option("Keyboard"),
                ft.dropdown.Option("LCD"),
            ],
            hint_text="Select Category",
        )
        self.company_field = CustomTextField(label="Company")
        self.model_field = CustomTextField(label="Model")
        self.serial_no_field = CustomTextField(label="Serial No")
        self.purchaser_field = CustomTextField(label="Purchaser")
        self.location_field = CustomTextField(label="Location")
        self.warranty_field = CustomTextField(label="Warranty")
        self.price_field = CustomTextField(label="Price")

        # File Upload Fields
        self.bill_copy_field = ft.ElevatedButton(
            icon=ft.icons.FILE_UPLOAD,
            text="Select Bill Copy",
            on_click=lambda e: self._set_picker_button("bill_copy")
        )
        self.bill_copy_display = ft.Text("No file selected")

        # Image Selection Field
        self.image_field = ft.ElevatedButton(
            icon=ft.icons.IMAGE,
            text="Select Asset Image",
            on_click=lambda e: self.image_picker.pick_files()
        )
        self.image_display = ft.Text("No image selected")

        # Date Fields
        self.purchase_date_text = ft.Text("No date selected")
        self.purchase_date_button = ft.ElevatedButton(
            icon=ft.icons.CALENDAR_MONTH,
            text="Select Purchase Date",
            on_click=lambda e: self._show_date_picker()
        )
        self.deploy_date_text = ft.Text("No deploy date selected")
        self.deploy_date_button = ft.ElevatedButton(
            icon=ft.icons.CALENDAR_MONTH,
            text="Select Deploy Date",
            on_click=lambda e: self._show_deploy_date_picker()
        )

        # Status Field
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

        # Deployment Fields
        self.deployed_to_field = CustomTextField(label="Deployed To (User or Department)")
        self.user_department_field = CustomTextField(label="User Department")
        self.deployment_dialog = ft.AlertDialog(
            title=ft.Text("Deployment Details"),
            content=ft.Column([
                self.deployed_to_field,
                self.user_department_field,
                self._build_form_row("Deploy Date", self.deploy_date_button),
                self.deploy_date_text,
            ], spacing=10),
            actions=[
                ft.TextButton("Save", on_click=self._save_deployment),
                ft.TextButton("Cancel", on_click=self._cancel_deployment),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _build_ui(self) -> None:
        """Build the main UI layout."""
        self.content = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    expand=True,
                    col={"sm": 12, "md": 12},
                    bgcolor=ft.colors.GREY_100,
                    padding=30,
                    content=ft.Container(
                        bgcolor=ft.colors.WHITE,
                        border_radius=ft.border_radius.all(15),
                        padding=30,
                        shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.colors.GREY_400),
                        content=ft.Column(
                            controls=[
                                ft.Text("Asset Registration", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                                self._build_form_row("Name", self.name_field),
                                self.category_field,
                                self._build_form_row("Company", self.company_field),
                                self._build_form_row("Model", self.model_field),
                                self._build_form_row("Serial No", self.serial_no_field),
                                self._build_form_row("Purchaser", self.purchaser_field),
                                self._build_form_row("Location", self.location_field),
                                self._build_form_row("Select Bill Copy", self.bill_copy_field),
                                self.bill_copy_display,
                                self._build_form_row("Select Asset Image", self.image_field),
                                self.image_display,
                                self._build_form_row("Purchase Date", self.purchase_date_button),
                                self.purchase_date_text,
                                self._build_form_row("Warranty", self.warranty_field),
                                self._build_form_row("Price", self.price_field),
                                self._build_form_row("Status", self.status_field_row),
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Save",
                                            icon=ft.icons.SAVE,
                                            bgcolor=ft.colors.GREEN_600,
                                            color=ft.colors.WHITE,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                            on_click=self._save_asset
                                        ),
                                        ft.ElevatedButton(
                                            "Cancel",
                                            icon=ft.icons.CANCEL,
                                            bgcolor=ft.colors.RED_600,
                                            color=ft.colors.WHITE,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                            on_click=self._cancel_form
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

    def _build_form_row(self, label_text: str, input_control: ft.Control) -> ft.ResponsiveRow:
        """Create a form row with a label and input control."""
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

    def _set_picker_button(self, button_type: str) -> None:
        """Set the last picker button type and trigger file picker."""
        self.last_picker_button = button_type
        self.file_picker.pick_files()

    def _handle_image_picker_result(self, e: ft.FilePickerResultEvent) -> None:
        """Handle the result of image picking."""
        if not e.files:
            return

        self.selected_image = e.files[0]  # Store the selected image file
        self.image_display.value = self.selected_image.name  # Display the file name
        self.page.update()

    def _handle_image_upload(self, e: ft.FilePickerUploadEvent) -> None:
        """Handle the image upload completion."""
        if e.progress == 1:  # Upload completed
            # Use the asset name and timestamp for the filename
            asset_name = self.name_field.value.replace(" ", "_") if self.name_field.value else "unnamed_asset"
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            save_filename = f"{asset_name}_{timestamp}{os.path.splitext(e.file_name)[1]}"
            save_dir = os.path.join("assets", "images")
            save_path = os.path.join(save_dir, save_filename).replace("\\", "/")
            self.image_path = f"/images/{save_filename}"
            print(f"Image uploaded and saved to: {save_path}")

    def _save_image_to_folder(self) -> Optional[str]:
        """Save the selected image to the folder and return the database path."""
        if not self.selected_image:
            return None

        file = self.selected_image
        # Use asset name and timestamp for the filename
        asset_name = self.name_field.value.replace(" ", "_") if self.name_field.value else "unnamed_asset"
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        ext = os.path.splitext(file.name)[1]
        save_filename = f"{asset_name}_{timestamp}{ext}"

        # Ensure the path is relative to the container's working directory
        save_dir = os.path.join("assets", "images")
        save_path = os.path.join(save_dir, save_filename).replace("\\", "/")
        db_path = f"/images/{save_filename}"

        try:
            os.makedirs(save_dir, exist_ok=True)
            if file.path:  # Desktop mode
                with open(file.path, "rb") as src, open(save_path, "wb") as dst:
                    dst.write(src.read())
                print(f"Saved image to: {save_path}")
                return db_path
            else:  # Web mode
                # Initiate the upload process
                self.image_path = None  # Reset before upload
                self.image_picker.upload([
                    ft.FilePickerUploadFile(
                        name=file.name,
                        upload_url=self.page.get_upload_url(save_filename, 600)
                    )
                ])
                # Wait for the upload to complete (simplified; in production, use async or callbacks)
                timeout = 10  # seconds
                elapsed = 0
                while self.image_path is None and elapsed < timeout:
                    self.page.update()
                    elapsed += 0.1
                    import time
                    time.sleep(0.1)
                if self.image_path:
                    return self.image_path
                else:
                    raise TimeoutError("Image upload timed out")
        except Exception as ex:
            print(f"Failed to save image: {ex}")
            self.page.open(ft.SnackBar(ft.Text(f"Failed to save image: {ex}"), duration=4000))
            return None

    def _show_date_picker(self) -> None:
        """Show the purchase date picker."""
        self.date_picker.open = True
        self.page.update()

    def _show_deploy_date_picker(self) -> None:
        """Show the deploy date picker."""
        self.deploy_date_picker.open = True
        self.page.update()

    def _handle_file_picker_result(self, e: ft.FilePickerResultEvent) -> None:
        """Handle the result of file picking for bill copies."""
        if not e.files:
            return

        file = e.files[0]
        # Use asset name and timestamp for the filename
        asset_name = self.name_field.value.replace(" ", "_") if self.name_field.value else "unnamed_asset"
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        ext = os.path.splitext(file.name)[1]
        save_filename = f"{asset_name}_{timestamp}{ext}"

        # Ensure the path is relative to the container's working directory
        save_dir = os.path.join("assets", "bill_copies")
        save_path = os.path.join(save_dir, save_filename).replace("\\", "/")
        db_path = f"/bill_copies/{save_filename}"

        try:
            os.makedirs(save_dir, exist_ok=True)
            # Check if running in web mode (file.path is None)
            if file.path is None:  # Web mode
                if hasattr(file, 'bytes') and file.bytes:
                    with open(save_path, "wb") as dst:
                        dst.write(file.bytes)
                else:
                    self.page.open(ft.SnackBar(ft.Text("Bill copy upload in web mode requires a different approach."), duration=4000))
                    return
            else:  # Desktop mode
                with open(file.path, "rb") as src, open(save_path, "wb") as dst:
                    dst.write(src.read())
            print(f"Saved file to: {save_path}")

            self.bill_copy_display.value = db_path
        except Exception as ex:
            print(f"Failed to save file: {ex}")
            self.page.open(ft.SnackBar(ft.Text(f"Failed to save file: {ex}"), duration=4000))
            return

        self.page.update()

    def _handle_date_picker_result(self, e: ft.ControlEvent) -> None:
        """Handle the result of the purchase date picker."""
        self.purchase_date_text.value = e.control.value.strftime("%Y-%m-%d") if e.control.value else "No date selected"
        self.date_picker.open = False
        self.page.update()

    def _handle_date_picker_dismiss(self, e: ft.ControlEvent) -> None:
        """Handle dismissal of the purchase date picker."""
        self.purchase_date_text.value = "No date selected"
        self.date_picker.open = False
        self.page.update()

    def _handle_deploy_date_picker_result(self, e: ft.ControlEvent) -> None:
        """Handle the result of the deploy date picker."""
        self.deploy_date_text.value = e.control.value.strftime("%Y-%m-%d") if e.control.value else "No deploy date selected"
        self.deploy_date_picker.open = False
        self.page.update()

    def _validate_asset_fields(self) -> List[str]:
        """Validate required asset fields and return a list of empty fields."""
        required_fields = {
            "Name": self.name_field.value,
            "Category": self.category_field.value,
            "Company": self.company_field.value,
            "Model": self.model_field.value,
            "Serial No": self.serial_no_field.value,
            "Purchaser": self.purchaser_field.value,
            "Location": self.location_field.value,
            "Price": self.price_field.value,
            "Warranty": self.warranty_field.value,
            "Status": self.status_field.value,
            "Purchase Date": self.purchase_date_text.value,
        }
        return [
            field for field, value in required_fields.items()
            if not value or value == "No date selected"
        ]

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

    def _save_deployment(self, e: ft.ControlEvent) -> None:
        """Save deployment details to the database."""
        print("Entering save_deployment")
        empty_fields = self._validate_asset_fields()
        if empty_fields:
            print(f"Validation failed: {empty_fields}")
            self.page.open(ft.SnackBar(ft.Text(f"Please fill all required fields: {', '.join(empty_fields)}"), duration=4000))
            return

        deployed_to = self.deployed_to_field.value
        user_department = self.user_department_field.value
        deploy_date = self.deploy_date_text.value if self.deploy_date_text.value != "No deploy date selected" else None

        if not all([deployed_to, user_department, deploy_date]):
            print("Deployment fields missing")
            self.page.open(ft.SnackBar(ft.Text("Please fill all deployment details: Deployed To, User Department, Deploy Date"), duration=4000))
            return

        # Save the image before saving to the database
        image_path = self._save_image_to_folder()
        if self.selected_image and not image_path:
            return  # Stop if image saving failed

        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            asset_data = self._prepare_asset_data()
            if not asset_data:
                return

            asset_data["image_path"] = image_path

            print("Inserting into deployed_assets")
            sql = """
                INSERT INTO deployed_assets (
                    name, category, company, model, serial_no, purchaser, location, price, warranty,
                    bill_copy, purchase_date, image_path, deployed_to, user_department, deploy_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, (
                asset_data["name"], asset_data["category"], asset_data["company"], asset_data["model"],
                asset_data["serial_no"], asset_data["purchaser"], asset_data["location"], asset_data["price"],
                asset_data["warranty"], asset_data["bill_copy"], asset_data["purchase_date"], asset_data["image_path"],
                deployed_to, user_department, deploy_date
            ))

            connection.commit()
            print("Deployed asset saved successfully")
            self.page.dialog.open = False
            self._clear_form()
            self._redirect_to_asset_page("save_deployment")

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

    def _cancel_deployment(self, e: ft.ControlEvent) -> None:
        """Cancel the deployment dialog and reset status."""
        print("Canceling deployment dialog")
        self.page.dialog.open = False
        self.status_field.value = "Available"
        self.page.update()

    def _save_asset(self, e: ft.ControlEvent) -> None:
        """Save asset details to the database."""
        print("Entering save_asset")
        empty_fields = self._validate_asset_fields()
        if empty_fields:
            print(f"Validation failed: {empty_fields}")
            self.page.open(ft.SnackBar(ft.Text(f"Please fill all required fields: {', '.join(empty_fields)}"), duration=4000))
            return

        if self.status_field.value == "Deployed":
            print("Showing deployment dialog")
            self.page.dialog = self.deployment_dialog
            self.page.dialog.open = True
            self.page.update()
            return

        # Save the image before saving to the database
        image_path = self._save_image_to_folder()
        if self.selected_image and not image_path:
            return  # Stop if image saving failed

        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cur = connection.cursor()
            asset_data = self._prepare_asset_data()
            if not asset_data:
                return

            asset_data["image_path"] = image_path

            print("Inserting into assets")
            sql = """
                INSERT INTO assets (
                    name, category, company, model, serial_no, purchaser, location, price, warranty,
                    status, bill_copy, purchase_date, image_path
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, (
                asset_data["name"], asset_data["category"], asset_data["company"], asset_data["model"],
                asset_data["serial_no"], asset_data["purchaser"], asset_data["location"], asset_data["price"],
                asset_data["warranty"], asset_data["status"], asset_data["bill_copy"],
                asset_data["purchase_date"], asset_data["image_path"]
            ))

            connection.commit()
            print("Asset saved successfully")
            self._clear_form()
            self._redirect_to_asset_page("save_asset")

        except mysql.connector.Error as error:
            print(f"Database error in save_asset: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Database error: {error}"), duration=4000))
        except Exception as e:
            print(f"Unexpected error in save_asset: {e}")
            self.page.open(ft.SnackBar(ft.Text(f"Unexpected error: {e}"), duration=4000))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()
                print("Database connection closed")

    def _prepare_asset_data(self) -> Optional[Dict[str, any]]:
        """Prepare asset data for database insertion."""
        asset_data = {
            "name": self.name_field.value,
            "category": self.category_field.value,
            "company": self.company_field.value,
            "model": self.model_field.value,
            "serial_no": self.serial_no_field.value,
            "purchaser": self.purchaser_field.value,
            "location": self.location_field.value,
            "price": None,
            "warranty": self.warranty_field.value,
            "status": self.status_field.value,
            "bill_copy": self.bill_copy_display.value if self.bill_copy_display.value != "No file selected" else None,
            "purchase_date": self.purchase_date_text.value if self.purchase_date_text.value != "No date selected" else None,
            "image_path": None,  # Will be updated in _save_asset or _save_deployment
        }

        try:
            if self.price_field.value:
                asset_data["price"] = float(self.price_field.value)
        except ValueError as ve:
            print(f"Price conversion error: {ve}")
            self.page.open(ft.SnackBar(ft.Text("Invalid price format. Please enter a valid number."), duration=4000))
            return None

        return asset_data

    def _cancel_form(self, e: ft.ControlEvent) -> None:
        """Cancel the form and redirect to the asset page."""
        print("Entering cancel_form")
        self._clear_form()
        self._redirect_to_asset_page("cancel_form")

    def _clear_form(self) -> None:
        """Clear all form fields."""
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
        self.status_field.value = "Available"
        self.bill_copy_display.value = "No file selected"
        self.image_display.value = "No image selected"
        self.selected_image = None
        self.image_path = None
        self.purchase_date_text.value = "No date selected"
        self.deployed_to_field.value = ""
        self.user_department_field.value = ""
        self.deploy_date_text.value = "No deploy date selected"
        self.page.update()

    def _redirect_to_asset_page(self, method: str) -> None:
        """Redirect to the asset page after an action."""
        print(f"Before redirect from {method}, current route: {self.page.route}")
        self.page.go("/asset")
        print(f"After redirect attempt from {method}, current route: {self.page.route}")
        self.page.update()

def AssetFormPage(page: ft.Page) -> AssetForm:
    """Factory function to create an AssetForm instance."""
    return AssetForm(page)