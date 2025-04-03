import flet as ft
import datetime
import mysql.connector
from nav.sidebar import SidebarPage
from nav.menubar import TopBarPage
from components.fields import CustomTextField

class AssetForm(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        page.window.title = "Asset Management System"
        page.scroll = "adaptive"
        self.expand = True
        self.page = page

        # Form Fields
        self.name_field = CustomTextField(label="Name")
        self.category_field = CustomTextField(label="Category")
        self.company_field = CustomTextField(label="Company")
        self.model_field = CustomTextField(label="Model")
        self.serial_no_field = CustomTextField(label="Serial No")
        self.purchaser_field = CustomTextField(label="Purchaser")
        self.location_field = CustomTextField(label="Location")

        # Bill Copy Upload
        self.bill_copy_display = ft.Text("No file selected")  
        self.file_picker = ft.FilePicker(on_result=self.bill_copy_picked)
        self.bill_copy_field = ft.ElevatedButton(
            icon=ft.icons.FILE_UPLOAD,
            text="Upload Bill Copy",
            on_click=lambda e: self.file_picker.pick_files()
        )

        # Date Picker (Default to current date)
        self.purchase_date_text = ft.Text(datetime.datetime.today().strftime("%Y-%m-%d"))

        self.date_picker = ft.DatePicker(
            value=datetime.datetime.today(),
            first_date=datetime.datetime(year=2023, month=10, day=1),
            last_date=datetime.datetime(year=2025, month=12, day=31),
            on_change=self.handle_date_change
        )

        self.purchase_date_button = ft.ElevatedButton(
            "Pick date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e: page.open(self.date_picker)
        )

        self.warranty_field = CustomTextField(label="Warranty")
        self.price_field = CustomTextField(label="Price")
        self.status_field = ft.Dropdown(
            options=[ft.dropdown.Option("Available")],
        )

        self.save_button = ft.ElevatedButton(
            "Save", icon=ft.icons.SAVE, bgcolor=ft.colors.GREEN_400, 
            color=ft.colors.WHITE, on_click=self.add_asset
        )
        self.cancel_button = ft.ElevatedButton(
            "Cancel", icon=ft.icons.CANCEL, bgcolor=ft.colors.RED_400, 
            color=ft.colors.WHITE
        )

        # Form Layout
        self.content = ft.Column(
            controls=[
                TopBarPage(page),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[ft.Container(content=SidebarPage(page), width=200, expand=True)],
                        ),
                        ft.Container(
                            content=ft.Container(
                                ft.Column(
                                    controls=[
                                        ft.Text("Asset Register", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                                        self.build_form_row("Name", self.name_field),
                                        self.build_form_row("Category", self.category_field),
                                        self.build_form_row("Company", self.company_field),
                                        self.build_form_row("Model", self.model_field),
                                        self.build_form_row("Serial No", self.serial_no_field),
                                        self.build_form_row("Purchaser", self.purchaser_field),
                                        self.build_form_row("Location", self.location_field),
                                        self.build_form_row("Bill Copy", self.bill_copy_field),
                                        self.build_form_row("Bill Copy", self.bill_copy_display),

                                        # Purchase Date Row
                                        ft.ResponsiveRow(
                                            controls=[
                                                ft.Container(
                                                    width=150,
                                                    col={"xs": 12, "md": 3},
                                                    content=ft.Text("Purchase Date", size=18, weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_700),
                                                ),
                                                ft.Container(
                                                    expand=True,
                                                    col={"xs": 12, "md": 9},
                                                    content=ft.Row([
                                                        self.purchase_date_button,
                                                        self.purchase_date_text,
                                                    ]),
                                                ),
                                            ],
                                            spacing=10,
                                        ),

                                        self.build_form_row("Warranty", self.warranty_field),
                                        self.build_form_row("Price", self.price_field),
                                        self.build_form_row("Status", self.status_field),
                                        
                                        ft.Row(
                                            controls=[self.save_button, self.cancel_button],
                                            alignment=ft.MainAxisAlignment.END,
                                            spacing=20,
                                        ),
                                    ],
                                    scroll="adaptive",
                                    expand=True,
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                bgcolor=ft.colors.WHITE,
                                border_radius=ft.border_radius.all(15),
                                padding=20,
                                shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.colors.GREY_400),
                            ),
                            col={"sm": 12, "md": 9},
                            expand=True,
                            bgcolor=ft.colors.GREY_100,
                            padding=30,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=0,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

        page.overlay.append(self.file_picker)
        page.overlay.append(self.date_picker)
        page.update()

    def build_form_row(self, label_text, input_control):
        """Builds a single row for the form with a label and input field."""
        return ft.ResponsiveRow(
            controls=[
                ft.Container(
                    width=150,
                    col={"xs": 9,"md": 9},
                    content=ft.Text(label_text, size=18, weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_700),
                ),
                ft.Container(
                    expand=True,
                    col={"xs": 9,"md": 9},
                    content=input_control,
                ),
            ],
            spacing=10,
        )

    def handle_date_change(self, e):
        """Updates the text when a date is selected."""
        selected_date = self.date_picker.value
        if selected_date:
            self.purchase_date_text.value = selected_date.strftime("%Y-%m-%d")
        self.page.update()

    def bill_copy_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0]  
            self.bill_copy_display.value = selected_file.name  
        else:
            self.bill_copy_display.value = "No file selected"
        self.update()

    def add_asset(self, e):
        """Adds a new asset to the database."""
        try:
            connection = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            cursor = connection.cursor()

            query = """
                INSERT INTO asset (name, category, company, model, serial_no, purchaser, location, warranty, price, status, bill_copy)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                self.name_field.value,
                self.category_field.value,
                self.company_field.value,
                self.model_field.value,
                self.serial_no_field.value,
                self.purchaser_field.value,
                self.location_field.value,
                self.warranty_field.value,
                self.price_field.value,
                self.status_field.value,
                self.bill_copy_display.value,
            )

            print(f"Executing SQL: {query} with values: {values}")

            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()

            self.page.snack_bar = ft.SnackBar(ft.Text("✅ Asset added successfully!"))
            self.page.snack_bar.open = True
            self.page.update()

        except mysql.connector.Error as err:
            print(f"❌ MySQL Error: {err}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {err}"))
            self.page.snack_bar.open = True
            self.page.update()

def AssetFormPage(page):
    return AssetForm(page)
