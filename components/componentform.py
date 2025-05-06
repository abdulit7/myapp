import os
os.environ["FLET_SECRET_KEY"] = "mysecret123"  # Set secret key before importing flet
import flet as ft  # For building the user interface
import mysql.connector  # For connecting to the MySQL database
import datetime  # For handling dates
from components.fields import CustomTextField  # Custom text input field

class ComponentForm(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()  # Initialize the container
        self.page = page  # Store the page object
        self.expand = True  # Fill available space
        self.selected_image = None  # Store the selected image file
        self.image_path = None  # Store the path after saving
        self.categories = {}  # Map category names to IDs

        # Set up file picker for images
        self.image_picker = ft.FilePicker(
            on_result=self.handle_image_picker,
            on_upload=self.handle_image_upload
        )
        self.page.overlay.append(self.image_picker)

        # Build the UI
        self.setup_page()
        self.create_form_fields()
        self.load_categories()  # Load categories from the database
        self.build_layout()

    def setup_page(self):
        """Set the page title."""
        self.page.window.title = "Asset Management System - Component Form"

    def create_form_fields(self):
        """Create all form fields and dialogs."""
        # File and date pickers
        self.file_picker = ft.FilePicker(on_result=self.handle_file_picker)
        self.date_picker = ft.DatePicker(
            on_change=self.handle_date_picker,
            on_dismiss=self.handle_date_dismiss,
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime.now()
        )
        self.deploy_date_picker = ft.DatePicker(
            on_change=self.handle_deploy_date_picker,
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime.now()
        )
        self.page.overlay.extend([self.file_picker, self.date_picker, self.deploy_date_picker])

        # Text input fields
        self.name_field = CustomTextField(label="Name")
        self.category_field = ft.Dropdown(
            label="Category",
            hint_text="Select Category",
            options=[]  # Populated by load_categories
        )
        self.company_field = CustomTextField(label="Company")
        self.model_field = CustomTextField(label="Model")
        self.serial_no_field = CustomTextField(label="Serial No")
        self.purchaser_field = CustomTextField(label="Purchaser")
        self.location_field = CustomTextField(label="Location")
        self.warranty_field = CustomTextField(label="Warranty")
        self.price_field = CustomTextField(label="Price")

        # Bill copy upload button
        self.bill_copy_button = ft.ElevatedButton(
            icon=ft.icons.FILE_UPLOAD,
            text="Select Bill Copy",
            on_click=lambda e: self.set_picker("bill_copy")
        )
        self.bill_copy_text = ft.Text("No file selected")

        # Image upload button
        self.image_button = ft.ElevatedButton(
            icon=ft.icons.IMAGE,
            text="Select Component Image",
            on_click=lambda e: self.image_picker.pick_files()
        )
        self.image_text = ft.Text("No image selected")

        # Date selection buttons
        self.purchase_date_text = ft.Text("No date selected")
        self.purchase_date_button = ft.ElevatedButton(
            icon=ft.icons.CALENDAR_MONTH,
            text="Select Purchase Date",
            on_click=lambda e: self.show_date_picker()
        )
        self.deploy_date_text = ft.Text("No deploy date selected")
        self.deploy_date_button = ft.ElevatedButton(
            icon=ft.icons.CALENDAR_MONTH,
            text="Select Deploy Date",
            on_click=lambda e: self.show_deploy_date_picker()
        )

        # Status dropdown
        self.status_field = ft.Dropdown(
            label="Status",
            options=[
                ft.dropdown.Option("Available"),
                ft.dropdown.Option("Deployed"),
            ],
            value="Available"
        )
        self.status_row = ft.Row(
            controls=[
                self.status_field,
                ft.Icon(name=ft.icons.ARROW_DROP_DOWN, color=ft.colors.BLUE_500, size=20)
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.END,
            expand=True
        )

        # Deployment dialog fields
        self.deployed_to_field = CustomTextField(label="Deployed To (User or Department)")
        self.user_department_field = CustomTextField(label="User Department")
        self.deployment_dialog = ft.AlertDialog(
            title=ft.Text("Deployment Details"),
            content=ft.Column([
                self.deployed_to_field,
                self.user_department_field,
                self.create_form_row("Deploy Date", self.deploy_date_button),
                self.deploy_date_text
            ], spacing=10),
            actions=[
                ft.TextButton("Save", on_click=self.save_deployment),
                ft.TextButton("Cancel", on_click=self.cancel_deployment)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

    def load_categories(self):
        """Load component categories from the database."""
        connection = self.connect_to_database()
        if not connection:
            self.page.open(ft.SnackBar(ft.Text("Failed to load categories."), duration=4000))
            return

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, name FROM category WHERE type = 'Component'")
            categories = cursor.fetchall()
            self.categories = {name: id for id, name in categories}
            self.category_field.options = [
                ft.dropdown.Option(name) for name in self.categories.keys()
            ]
            self.page.update()
        except mysql.connector.Error as error:
            print(f"Error loading categories: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Error loading categories: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Database connection closed")

    def build_layout(self):
        """Build the form layout."""
        self.content = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    expand=True,
                    col={"sm": 12, "md": 12},
                    bgcolor=ft.colors.GREY_100,
                    padding=30,
                    content=ft.Container(
                        bgcolor=ft.colors.WHITE,
                        border_radius=15,
                        padding=30,
                        shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.colors.GREY_400),
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Component Registration",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLUE_900
                                ),
                                self.create_form_row("Name", self.name_field),
                                self.category_field,
                                self.create_form_row("Company", self.company_field),
                                self.create_form_row("Model", self.model_field),
                                self.create_form_row("Serial No", self.serial_no_field),
                                self.create_form_row("Purchaser", self.purchaser_field),
                                self.create_form_row("Location", self.location_field),
                                self.create_form_row("Select Bill Copy", self.bill_copy_button),
                                self.bill_copy_text,
                                self.create_form_row("Select Component Image", self.image_button),
                                self.image_text,
                                self.create_form_row("Purchase Date", self.purchase_date_button),
                                self.purchase_date_text,
                                self.create_form_row("Warranty", self.warranty_field),
                                self.create_form_row("Price", self.price_field),
                                self.create_form_row("Status", self.status_row),
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Save",
                                            icon=ft.icons.SAVE,
                                            bgcolor=ft.colors.GREEN_600,
                                            color=ft.colors.WHITE,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                            on_click=self.save_component
                                        ),
                                        ft.ElevatedButton(
                                            "Cancel",
                                            icon=ft.icons.CANCEL,
                                            bgcolor=ft.colors.RED_600,
                                            color=ft.colors.WHITE,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                            on_click=self.cancel_form
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                    spacing=20
                                )
                            ],
                            spacing=20
                        )
                    )
                )
            ],
            spacing=20
        )

    def create_form_row(self, label: str, control: ft.Control):
        """Create a row with a label and input field."""
        return ft.ResponsiveRow(
            controls=[
                ft.Container(
                    width=150,
                    col={"xs": 12, "md": 3},
                    content=ft.Text(
                        label,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE_GREY_700
                    )
                ),
                ft.Container(
                    expand=True,
                    col={"xs": 12, "md": 9},
                    content=control
                )
            ],
            spacing=10
        )

    def set_picker(self, picker_type: str):
        """Set the file picker type and open it."""
        self.last_picker = picker_type
        self.file_picker.pick_files()

    def handle_image_picker(self, e: ft.FilePickerResultEvent):
        """Handle selected image from the file picker."""
        if not e.files:
            return
        self.selected_image = e.files[0]
        self.image_text.value = self.selected_image.name
        self.page.update()

    def handle_image_upload(self, e: ft.FilePickerUploadEvent):
        """Handle image upload completion."""
        if e.progress == 1:  # Upload completed
            component_name = self.name_field.value.replace(" ", "_") if self.name_field.value else "unnamed_component"
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            save_filename = f"{component_name}_{timestamp}{os.path.splitext(e.file_name)[1]}"
            save_dir = os.path.join("components", "images")
            save_path = os.path.join(save_dir, save_filename).replace("\\", "/")
            self.image_path = f"/images/{save_filename}"
            print(f"Image uploaded and saved to: {save_path}")

    def save_image(self):
        """Save the selected image to the folder and return the database path."""
        if not self.selected_image:
            return None

        file = self.selected_image
        component_name = self.name_field.value.replace(" ", "_") if self.name_field.value else "unnamed_component"
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        ext = os.path.splitext(file.name)[1]
        save_filename = f"{component_name}_{timestamp}{ext}"

        save_dir = os.path.join("components", "images")
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
                self.image_path = None
                self.image_picker.upload([
                    ft.FilePickerUploadFile(
                        name=file.name,
                        upload_url=self.page.get_upload_url(save_filename, 600)
                    )
                ])
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

    def show_date_picker(self):
        """Show the purchase date picker."""
        self.date_picker.open = True
        self.page.update()

    def show_deploy_date_picker(self):
        """Show the deploy date picker."""
        self.deploy_date_picker.open = True
        self.page.update()

    def handle_file_picker(self, e: ft.FilePickerResultEvent):
        """Handle selected bill copy file."""
        if not e.files:
            return

        file = e.files[0]
        component_name = self.name_field.value.replace(" ", "_") if self.name_field.value else "unnamed_component"
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        ext = os.path.splitext(file.name)[1]
        save_filename = f"{component_name}_{timestamp}{ext}"

        save_dir = os.path.join("components", "bill_copies")
        save_path = os.path.join(save_dir, save_filename).replace("\\", "/")
        db_path = f"/bill_copies/{save_filename}"

        try:
            os.makedirs(save_dir, exist_ok=True)
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
            print(f"Saved bill copy to: {save_path}")
            self.bill_copy_text.value = db_path
        except Exception as ex:
            print(f"Failed to save bill copy: {ex}")
            self.page.open(ft.SnackBar(ft.Text(f"Failed to save bill copy: {ex}"), duration=4000))
        self.page.update()

    def handle_date_picker(self, e: ft.ControlEvent):
        """Handle selected purchase date."""
        self.purchase_date_text.value = e.control.value.strftime("%Y-%m-%d") if e.control.value else "No date selected"
        self.date_picker.open = False
        self.page.update()

    def handle_date_dismiss(self, e: ft.ControlEvent):
        """Handle dismissal of purchase date picker."""
        self.purchase_date_text.value = "No date selected"
        self.date_picker.open = False
        self.page.update()

    def handle_deploy_date_picker(self, e: ft.ControlEvent):
        """Handle selected deploy date."""
        self.deploy_date_text.value = e.control.value.strftime("%Y-%m-%d") if e.control.value else "No deploy date selected"
        self.deploy_date_picker.open = False
        self.page.update()

    def validate_fields(self):
        """Check for required fields and return empty ones."""
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
            "Purchase Date": self.purchase_date_text.value
        }
        return [
            field for field, value in required_fields.items()
            if not value or value == "No date selected"
        ]

    def connect_to_database(self):
        """Connect to the MySQL database."""
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

    def save_deployment(self, e: ft.ControlEvent):
        """Save a deployed component to the database."""
        print("Saving deployed component")
        empty_fields = self.validate_fields()
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

        image_path = self.save_image()
        if self.selected_image and not image_path:
            return  # Stop if image saving failed

        connection = self.connect_to_database()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            component_data = self.prepare_component_data()
            if not component_data:
                return

            category_id = self.categories.get(self.category_field.value)
            if not category_id:
                self.page.open(ft.SnackBar(ft.Text("Invalid category selected."), duration=4000))
                return

            component_data["image_path"] = image_path

            print("Inserting into deployed_components")
            sql = """
                INSERT INTO deployed_components (
                    name, category_id, company, model, serial_no, purchaser, location, price, warranty,
                    bill_copy, purchase_date, image_path, deployed_to, user_department, deploy_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                component_data["name"], category_id, component_data["company"], component_data["model"],
                component_data["serial_no"], component_data["purchaser"], component_data["location"],
                component_data["price"], component_data["warranty"], component_data["bill_copy"],
                component_data["purchase_date"], component_data["image_path"],
                deployed_to, user_department, deploy_date
            ))

            connection.commit()
            print("Deployed component saved successfully")
            self.page.dialog.open = False
            self.clear_form()
            self.go_to_components()

        except mysql.connector.Error as error:
            print(f"Database error in save_deployment: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Database error: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Database connection closed")

    def cancel_deployment(self, e: ft.ControlEvent):
        """Close the deployment dialog and reset status."""
        print("Canceling deployment")
        self.page.dialog.open = False
        self.status_field.value = "Available"
        self.page.update()

    def save_component(self, e: ft.ControlEvent):
        """Save an available component to the database."""
        print("Saving component")
        empty_fields = self.validate_fields()
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

        image_path = self.save_image()
        if self.selected_image and not image_path:
            return  # Stop if image saving failed

        connection = self.connect_to_database()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            component_data = self.prepare_component_data()
            if not component_data:
                return

            category_id = self.categories.get(self.category_field.value)
            if not category_id:
                self.page.open(ft.SnackBar(ft.Text("Invalid category selected."), duration=4000))
                return

            component_data["image_path"] = image_path

            print("Inserting into component")
            sql = """
                INSERT INTO component (
                    name, category_id, company, model, serial_no, purchaser, location, price, warranty,
                    status, bill_copy, purchase_date, image_path
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                component_data["name"], category_id, component_data["company"], component_data["model"],
                component_data["serial_no"], component_data["purchaser"], component_data["location"],
                component_data["price"], component_data["warranty"], component_data["status"],
                component_data["bill_copy"], component_data["purchase_date"], component_data["image_path"]
            ))

            connection.commit()
            print("Component saved successfully")
            self.clear_form()
            self.go_to_components()

        except mysql.connector.Error as error:
            print(f"Database error in save_component: {error}")
            self.page.open(ft.SnackBar(ft.Text(f"Database error: {error}"), duration=4000))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Database connection closed")

    def prepare_component_data(self):
        """Prepare component data for saving."""
        component_data = {
            "name": self.name_field.value,
            "category_id": None,  # Updated in save_component or save_deployment
            "company": self.company_field.value,
            "model": self.model_field.value,
            "serial_no": self.serial_no_field.value,
            "purchaser": self.purchaser_field.value,
            "location": self.location_field.value,
            "price": None,
            "warranty": self.warranty_field.value,
            "status": self.status_field.value,
            "bill_copy": self.bill_copy_text.value if self.bill_copy_text.value != "No file selected" else None,
            "purchase_date": self.purchase_date_text.value if self.purchase_date_text.value != "No date selected" else None,
            "image_path": None  # Updated in save_component or save_deployment
        }

        try:
            if self.price_field.value:
                component_data["price"] = float(self.price_field.value)
        except ValueError:
            print("Invalid price format")
            self.page.open(ft.SnackBar(ft.Text("Invalid price format. Please enter a valid number."), duration=4000))
            return None

        return component_data

    def cancel_form(self, e: ft.ControlEvent):
        """Clear the form and go back to components page."""
        print("Canceling form")
        self.clear_form()
        self.go_to_components()

    def clear_form(self):
        """Reset all form fields."""
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
        self.bill_copy_text.value = "No file selected"
        self.image_text.value = "No image selected"
        self.selected_image = None
        self.image_path = None
        self.purchase_date_text.value = "No date selected"
        self.deployed_to_field.value = ""
        self.user_department_field.value = ""
        self.deploy_date_text.value = "No deploy date selected"
        self.page.update()

    def go_to_components(self):
        """Go to the components page."""
        print(f"Redirecting to /components from {self.page.route}")
        self.page.go("/components")
        self.page.update()

def create_component_form(page: ft.Page):
    """Create and return a ComponentForm instance."""
    return ComponentForm(page)