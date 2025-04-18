import flet as ft
import mysql.connector
import random
import asyncio
import datetime

from components.fields import CustomTextField

class AssetForm(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        page.window.title = "Asset Management System"
        self.page = page
        self.expand = True

        # Stack and container dimensions
        self.stack_width = 300
        self.stack_height = 250
        self.container_size = 50

        # Initial positions of the containers
        self.c1 = ft.Container(
            width=self.container_size,
            height=self.container_size,
            bgcolor="red",
            top=0,
            left=0,
            animate_position=1000
        )

        self.c2 = ft.Container(
            width=self.container_size,
            height=self.container_size,
            bgcolor="green",
            top=60,
            left=0,
            animate_position=500
        )

        self.c3 = ft.Container(
            width=self.container_size,
            height=self.container_size,
            bgcolor="blue",
            top=120,
            left=0,
            animate_position=1000
        )

        # File Picker for Uploading Files
        self.file_picker = ft.FilePicker(on_result=self.file_picker_result)
        page.overlay.append(self.file_picker)

        # Date Picker for Purchase Date
        self.date_picker = ft.DatePicker(
            on_change=self.date_picker_result,
            on_dismiss=self.date_picker_dismiss,
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime.now()
        )
        page.overlay.append(self.date_picker)

        # Form Fields
        category_options = [
            ft.dropdown.Option("Desktop"),
            ft.dropdown.Option("Wyse"),
            ft.dropdown.Option("Keyboard"),
            ft.dropdown.Option("LCD"),
        ]

        self.name_field = CustomTextField(label="Name")
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
            text="Upload Asset Image",
            on_click=lambda e: setattr(self, 'last_picker_button', "image") or self.file_picker.pick_files()
        )
        self.image_display = ft.Text("No image selected")
        self.purchase_date_text = ft.Text("No date selected")
        self.purchase_date_button = ft.ElevatedButton(
            icon=ft.icons.CALENDAR_MONTH,
            text="Select Purchase Date",
            on_click=lambda e: self.show_date_picker()
        )
        self.warranty_field = CustomTextField(label="Warranty")
        self.price_field = CustomTextField(label="Price")
        self.status_field = ft.Dropdown(
            label="Status",
            options=[ft.dropdown.Option("Available")],
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

        # Form Layout
        self.content = ft.ResponsiveRow(
            controls=[
                # Sidebar Area with Animated Containers
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
                # Main Form Area
                ft.Container(
                    expand=True,
                    col={"sm": 12, "md": 9},
                    bgcolor=ft.Colors.GREY_100,
                    padding=30,
                    content=ft.Container(
                        bgcolor=ft.Colors.WHITE,
                        border_radius=ft.border_radius.all(15),
                        padding=30,
                        shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.Colors.GREY_400),
                        content=ft.Column(
                            controls=[
                                ft.Text("Asset Registration", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                self.build_form_row("Name", self.name_field),
                                self.category_field,
                                self.build_form_row("Company", self.company_field),
                                self.build_form_row("Model", self.model_field),
                                self.build_form_row("Serial No", self.serial_no_field),
                                self.build_form_row("Purchaser", self.purchaser_field),
                                self.build_form_row("Location", self.location_field),
                                self.build_form_row("Upload Bill Copy", self.bill_copy_field),
                                self.bill_copy_display,
                                self.build_form_row("Upload Asset Image", self.image_field),
                                self.image_display,
                                self.build_form_row("Purchase Date", self.purchase_date_button),
                                self.purchase_date_text,
                                self.build_form_row("Warranty", self.warranty_field),
                                self.build_form_row("Price", self.price_field),
                                self.build_form_row("Status", self.status_field_row),
                                # Save and Cancel Buttons
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Save",
                                            icon=ft.icons.SAVE,
                                            bgcolor=ft.Colors.GREEN_600,
                                            color=ft.Colors.WHITE,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10)
                                            ),
                                            on_click=self.save_asset
                                        ),
                                        ft.ElevatedButton(
                                            "Cancel",
                                            icon=ft.icons.CANCEL,
                                            bgcolor=ft.Colors.RED_600,
                                            color=ft.Colors.WHITE,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10)
                                            )
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

        # Start the automatic movement
        page.run_task(self.move_containers)

    async def move_containers(self):
        max_top = self.stack_height - self.container_size
        max_left = self.stack_width - self.container_size

        while True:
            self.c1.top = random.randint(0, max_top)
            self.c1.left = random.randint(0, max_left)

            self.c2.top = random.randint(0, max_top)
            self.c2.left = random.randint(0, max_left)

            self.c3.top = random.randint(0, max_top)
            self.c3.left = random.randint(0, max_left)

            self.page.update()
            await asyncio.sleep(1)

    def build_form_row(self, label_text, input_control):
        return ft.ResponsiveRow(
            controls=[
                ft.Container(
                    width=150,
                    col={"xs": 12, "md": 3},
                    content=ft.Text(label_text, size=18, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_GREY_700),
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

    def file_picker_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            if hasattr(self, 'last_picker_button') and self.last_picker_button == "bill_copy":
                self.bill_copy_display.value = f"Selected: {e.files[0].name}"
            elif hasattr(self, 'last_picker_button') and self.last_picker_button == "image":
                self.image_display.value = f"Selected: {e.files[0].name}"
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

    def save_asset(self, e):
        name = self.name_field.value
        purchase_date = self.purchase_date_text.value if self.purchase_date_text.value != "No date selected" else None

        try:
            connection = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            cur = connection.cursor()
            sql = "INSERT INTO users (name, purchase_date) VALUES (%s, %s)"
            cur.execute(sql, (name, purchase_date))
            connection.commit()
            print("Asset saved successfully.")
        except mysql.connector.Error as error:
            print("Failed to insert record into MySQL table: {}".format(error))
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()

def AssetFormPage(page):
    return AssetForm(page)