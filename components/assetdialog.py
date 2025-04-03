import flet as ft
from components.fields import CustomTextField
import datetime

class AssetDialog:
    def __init__(self, page: ft.Page):
        self.page = page
        

        # Form Fields
        self.name_field = CustomTextField(label="Name")
        self.category_field = CustomTextField(label="Category")
        self.company_field = CustomTextField(label="Company")
        self.model_field = CustomTextField(label="Model")
        self.serial_no_field = CustomTextField(label="Serial No")
        self.purchaser_field = CustomTextField(label="Purchaser")
        self.bill_copy_display = ft.Text("No file selected")  # Text to display the file name
        self.bill_copy_field = ft.ElevatedButton(
            icon=ft.icons.FILE_UPLOAD,
            text="Upload Bill Copy",
            on_click=lambda e: self.file_picker.pick_files()
        )
        self.file_picker = ft.FilePicker(on_result=self.bill_copy_picked)

        self.location_field = CustomTextField(label="Location")

        self.purchase_date_text = ft.Text("No date selected")  # Text to display the date
        self.purchase_date_field = ft.ElevatedButton(
            icon=ft.icons.CALENDAR_MONTH,
            text="Select Date",
            on_click=lambda e: self.show_date_picker()
        )

        self.warranty_field = CustomTextField(label="Warranty")
        self.price_field = CustomTextField(label="Price")
        self.status_field = ft.Dropdown(
            options=[
                ft.dropdown.Option("Available"),
                ft.dropdown.Option("Assigned"),
            ],
            on_change=self.status_changed
        )

        self.assign_to_field = ft.Dropdown(
            options=[
                ft.dropdown.Option("User"),
                ft.dropdown.Option("Department"),
            ],
            visible=False,
            on_change=self.assign_to_changed
        )

        self.select_user_field = ft.Dropdown(
            options=[
                ft.dropdown.Option("User 1"),
                ft.dropdown.Option("User 2"),
            ],
            visible=False
        )

        self.select_department_field = ft.Dropdown(
            options=[
                ft.dropdown.Option("Department 1"),
                ft.dropdown.Option("Department 2"),
            ],
            visible=False
        )

        self.save_button = ft.ElevatedButton(
            "Save",
            icon=ft.icons.SAVE,
            bgcolor=ft.colors.GREEN_400,
            color=ft.colors.WHITE,
            width=500,
            on_click=self.handle_save
        )
        self.cancel_button = ft.ElevatedButton(
            "Cancel",
            icon=ft.icons.CANCEL,
            bgcolor=ft.colors.RED_400,
            width=500,
            color=ft.colors.WHITE,
            on_click=self.handle_close
        )

        # Form inside dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor=ft.colors.RED_100,
           
            title=ft.Text("Add Asset"),
            content=ft.Column(
                controls=[
                    self.build_form_row("Name", self.name_field),
                    self.build_form_row("Category", self.category_field),
                    self.build_form_row("Company", self.company_field),
                    self.build_form_row("Model", self.model_field),
                    self.build_form_row("Serial No", self.serial_no_field),
                    self.build_form_row("Purchaser", self.purchaser_field),
                    self.build_form_row("Location", self.location_field),
                    # Bill Copy
                    self.build_form_row("Bill Copy", self.bill_copy_field),
                    self.build_form_row("Selected File", self.bill_copy_display),
                    # Purchase Date
                    ft.Row([self.purchase_date_field, self.purchase_date_text], spacing=10),
                    self.build_form_row("Warranty", self.warranty_field),
                    self.build_form_row("Price", self.price_field),
                    self.build_form_row("Status", self.status_field),
                    self.build_form_row("Assign To", self.assign_to_field),
                    self.build_form_row("Select User", self.select_user_field),
                    self.build_form_row("Select Department", self.select_department_field),
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
            on_dismiss=lambda e: self.page.add(ft.Text("Dialog dismissed!")),
            
            
        )

        self.page.overlay.append(self.file_picker)

    def build_form_row(self, label_text, input_control):
        """Builds a single row for the form with a label and input field."""
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
        def handle_change(e):
            selected_date = e.control.value
            self.purchase_date_text.value = selected_date.strftime("%Y-%m-%d")
            self.purchase_date_field.text = "Change Date"
            self.page.update()

        date_picker = ft.DatePicker(
            first_date=datetime.date(2023, 10, 1),
            last_date=datetime.date(2024, 10, 1),
            on_change=handle_change,
        )
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Select Purchase Date"),
            content=date_picker,
        )
        self.page.dialog.open = True
        self.page.update()

    def status_changed(self, e):
        if e.control.value == "Assigned":
            self.assign_to_field.visible = True
        else:
            self.assign_to_field.visible = False
            self.select_user_field.visible = False
            self.select_department_field.visible = False
        self.page.update()

    def assign_to_changed(self, e):
        if e.control.value == "User":
            self.select_user_field.visible = True
            self.select_department_field.visible = False
        elif e.control.value == "Department":
            self.select_user_field.visible = False
            self.select_department_field.visible = True
        self.page.update()

    def bill_copy_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0]
            self.bill_copy_display.value = selected_file.name
            print(f"File picked: {selected_file.path}")
        else:
            self.bill_copy_display.value = "No file selected"
        self.page.update()

    def handle_save(self, e):
        """Handles saving the asset data (can be extended to store in a database)."""
        if not self.name_field.value or not self.category_field.value:
            self.page.add(ft.Text("Error: Name and Category are required!", color="red"))
            return

        asset_data = {
            "name": self.name_field.value,
            "category": self.category_field.value,
            "company": self.company_field.value,
            "model": self.model_field.value,
            "serial_no": self.serial_no_field.value,
            "purchaser": self.purchaser_field.value,
            "location": self.location_field.value,
            "price": self.price_field.value,
            "warranty": self.warranty_field.value,
            "status": self.status_field.value,
        }

        print("Saved Asset Data:", asset_data)

        self.page.close(self.dialog)
        self.page.add(ft.Text(f"Asset '{self.name_field.value}' added successfully!", color="green"))
        self.clear_fields()

    def handle_close(self, e):
        """Closes the dialog without saving."""
        self.page.close(self.dialog)

    def clear_fields(self):
        """Clears form fields after submission."""
        self.name_field.value = ""
        self.category_field.value = ""
        self.company_field.value = ""
        self.model_field.value = ""
        self.serial_no_field.value = ""
        self.purchaser_field.value = ""
        self.location_field.value = ""
        self.price_field.value = ""
        self.warranty_field.value = ""
        self.status_field.value = ""
        self.page.update()

    def open(self):
        """Opens the dialog."""
        self.page.open(self.dialog)
