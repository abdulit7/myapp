import flet as ft
import datetime
import mysql.connector
import os
import shutil
from components.fields import CustomTextField

class ComponentForm(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        page.window.title = "Asset Management System"
        page.scroll = "adaptive"
        self.expand = True
        self.page = page

        # Helper methods for responsive design
        def get_window_width():
            return page.window.width if page.window.width > 0 else 800

        def is_mobile():
            return get_window_width() <= 600

        def is_tablet():
            return 601 <= get_window_width() <= 1024

        def get_title_size():
            if is_mobile():
                return 20
            elif is_tablet():
                return 24
            return 28

        def get_label_size():
            if is_mobile():
                return 14
            elif is_tablet():
                return 16
            return 18

        def get_button_size():
            if is_mobile():
                return {"width": 120, "height": 40}
            elif is_tablet():
                return {"width": 135, "height": 45}
            return {"width": 150, "height": 50}

        def get_upload_button_size():
            if is_mobile():
                return {"width": 140, "height": 40, "text_size": 12, "icon_size": 16}
            elif is_tablet():
                return {"width": 160, "height": 45, "text_size": 13, "icon_size": 18}
            return {"width": 180, "height": 50, "text_size": 14, "icon_size": 20}

        def get_form_padding():
            if is_mobile():
                return 20
            elif is_tablet():
                return 30
            return 40

        def get_container_padding():
            if is_mobile():
                return 15
            elif is_tablet():
                return 20
            return 30

        # Category Dropdown Options
        category_options = [
            ft.dropdown.Option("Desktop"),
            ft.dropdown.Option("Wyse"),
            ft.dropdown.Option("Keyboard"),
            ft.dropdown.Option("LCD"),
        ]

        # Form Fields with Enhanced Styling
        self.name_field = ft.TextField(
            label="Name",
            expand=True,
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=ft.border_radius.all(8),
            focused_border_color=ft.colors.BLUE_500,
            label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_700, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color=ft.colors.BLACK87),
            cursor_color=ft.colors.BLUE_500,
            hint_text="Enter asset name",
            hint_style=ft.TextStyle(color=ft.colors.GREY_500),
        )

        self.category_field = ft.Dropdown(
            label="Category",
            options=category_options,
            hint_text="Select Category",
            expand=True,
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=ft.border_radius.all(8),
            focused_border_color=ft.colors.BLUE_500,
            label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_700, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color=ft.colors.BLACK87),
            hint_style=ft.TextStyle(color=ft.colors.GREY_500),
        )
        self.category_field_row = ft.Row(
            controls=[
                self.category_field,
                ft.Icon(name=ft.icons.ARROW_DROP_DOWN, color=ft.colors.BLUE_500, size=20),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.END,
            expand=True,
        )

        self.company_field = ft.TextField(
            label="Company",
            hint_text="Enter Company Name",
            expand=True,
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=ft.border_radius.all(8),
            focused_border_color=ft.colors.BLUE_500,
            label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_700, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color=ft.colors.BLACK87),
            cursor_color=ft.colors.BLUE_500,
            hint_style=ft.TextStyle(color=ft.colors.GREY_500),
        )
        self.company_field.autocomplete = True

        self.model_field = ft.TextField(
            label="Model",
            expand=True,
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=ft.border_radius.all(8),
            focused_border_color=ft.colors.BLUE_500,
            label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_700, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color=ft.colors.BLACK87),
            cursor_color=ft.colors.BLUE_500,
            hint_text="Enter model name",
            hint_style=ft.TextStyle(color=ft.colors.GREY_500),
        )

        self.serial_no_field = CustomTextField(
            label="Serial No",
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=ft.border_radius.all(8),
            focused_border_color=ft.colors.BLUE_500,
            label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_700, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color=ft.colors.BLACK87),
            cursor_color=ft.colors.BLUE_500,
            hint_text="Enter serial number",
            hint_style=ft.TextStyle(color=ft.colors.GREY_500),
        )

        self.purchaser_field = CustomTextField(
            label="Purchaser",
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=ft.border_radius.all(8),
            focused_border_color=ft.colors.BLUE_500,
            label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_700, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color=ft.colors.BLACK87),
            cursor_color=ft.colors.BLUE_500,
            hint_text="Enter purchaser name",
            hint_style=ft.TextStyle(color=ft.colors.GREY_500),
        )

        self.location_field = CustomTextField(
            label="Location",
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=ft.border_radius.all(8),
            focused_border_color=ft.colors.BLUE_500,
            label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_700, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color=ft.colors.BLACK87),
            cursor_color=ft.colors.BLUE_500,
            hint_text="Enter location",
            hint_style=ft.TextStyle(color=ft.colors.GREY_500),
        )

        # Bill Copy Upload
        upload_button_size = get_upload_button_size()
        self.bill_copy_display = ft.Text("No file selected", color=ft.colors.GREY_700, size=upload_button_size["text_size"])
        self.file_picker = ft.FilePicker(on_result=self.bill_copy_picked)
        self.bill_copy_field = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(name=ft.icons.FILE_UPLOAD, color=ft.colors.WHITE, size=upload_button_size["icon_size"]),
                    ft.Text(
                        value="Upload Bill Copy",
                        size=upload_button_size["text_size"],
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            width=upload_button_size["width"],
            height=upload_button_size["height"],
            on_click=lambda e: self.file_picker.pick_files(),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: ft.colors.BLUE_600,
                    ft.ControlState.HOVERED: ft.colors.BLUE_700,
                },
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=3,
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                overlay_color=ft.colors.WHITE10,
                animation_duration=300,
            ),
            tooltip="Upload bill copy",
        )

        # Image Upload
        self.image_display = ft.Text("No image selected", color=ft.colors.GREY_700, size=upload_button_size["text_size"])
        self.image_picker = ft.FilePicker(on_result=self.image_picked)
        self.image_field = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(name=ft.icons.IMAGE, color=ft.colors.WHITE, size=upload_button_size["icon_size"]),
                    ft.Text(
                        value="Upload Asset Image",
                        size=upload_button_size["text_size"],
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            width=upload_button_size["width"],
            height=upload_button_size["height"],
            on_click=lambda e: self.image_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["jpg", "jpeg", "png"]
            ),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: ft.colors.BLUE_600,
                    ft.ControlState.HOVERED: ft.colors.BLUE_700,
                },
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=3,
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                overlay_color=ft.colors.WHITE10,
                animation_duration=300,
            ),
            tooltip="Upload asset image",
        )
        self.image_path = None  # Store the relative path of the saved image

        # Date Picker (Default to current date)
        self.purchase_date_text = ft.Text(
            datetime.datetime.today().strftime("%Y-%m-%d"),
            color=ft.colors.BLUE_GREY_700,
            size=upload_button_size["text_size"],
        )

        self.date_picker = ft.DatePicker(
            value=datetime.datetime.today(),
            first_date=datetime.datetime(year=2023, month=10, day=1),
            last_date=datetime.datetime(year=2025, month=12, day=31),
            on_change=self.handle_date_change,
        )

        self.purchase_date_button = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(name=ft.icons.CALENDAR_MONTH, color=ft.colors.WHITE, size=upload_button_size["icon_size"]),
                    ft.Text(
                        value="Select Purchase Date",
                        size=upload_button_size["text_size"],
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            width=upload_button_size["width"],
            height=upload_button_size["height"],
            on_click=lambda e: page.open(self.date_picker),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: ft.colors.BLUE_600,
                    ft.ControlState.HOVERED: ft.colors.BLUE_700,
                },
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=3,
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                overlay_color=ft.colors.WHITE10,
                animation_duration=300,
            ),
            tooltip="Select purchase date",
        )

        self.warranty_field = CustomTextField(
            label="Warranty",
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=ft.border_radius.all(8),
            focused_border_color=ft.colors.BLUE_500,
            label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_700, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color=ft.colors.BLACK87),
            cursor_color=ft.colors.BLUE_500,
            hint_text="Enter warranty period",
            hint_style=ft.TextStyle(color=ft.colors.GREY_500),
        )

        self.price_field = CustomTextField(
            label="Price",
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=ft.border_radius.all(8),
            focused_border_color=ft.colors.BLUE_500,
            label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_700, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color=ft.colors.BLACK87),
            cursor_color=ft.colors.BLUE_500,
            hint_text="Enter price",
            hint_style=ft.TextStyle(color=ft.colors.GREY_500),
        )

        self.status_field = ft.Dropdown(
            label="Status",
            options=[ft.dropdown.Option("Available")],
            value="Available",
            expand=True,
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=ft.border_radius.all(8),
            focused_border_color=ft.colors.BLUE_500,
            label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_700, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color=ft.colors.BLACK87),
            hint_style=ft.TextStyle(color=ft.colors.GREY_500),
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

        # Save and Cancel Buttons
        button_size = get_button_size()
        self.save_button = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(name=ft.icons.SAVE, color=ft.colors.WHITE, size=button_size["height"] * 0.5),
                    ft.Text(
                        value="Save",
                        size=button_size["height"] * 0.4,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            width=button_size["width"],
            height=button_size["height"],
            on_click=self.add_asset,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: ft.colors.GREEN_600,
                    ft.ControlState.HOVERED: ft.colors.GREEN_700,
                },
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation=5,
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                overlay_color=ft.colors.WHITE10,
                animation_duration=300,
            ),
            tooltip="Save asset",
        )

        self.cancel_button = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(name=ft.icons.CANCEL, color=ft.colors.WHITE, size=button_size["height"] * 0.5),
                    ft.Text(
                        value="Cancel",
                        size=button_size["height"] * 0.4,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            width=button_size["width"],
            height=button_size["height"],
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: ft.colors.RED_600,
                    ft.ControlState.HOVERED: ft.colors.RED_700,
                },
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation=5,
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                overlay_color=ft.colors.WHITE10,
                animation_duration=300,
            ),
            tooltip="Cancel",
        )

        # Form Layout
        self.title = ft.Text(
            "Asset Register",
            size=get_title_size(),
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE_900,
            text_align=ft.TextAlign.CENTER,
        )

        self.upload_fields_row = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Purchase Date",
                            size=get_label_size(),
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.BLUE_GREY_700,
                        ),
                        self.purchase_date_button,
                        self.purchase_date_text,
                    ], spacing=5, alignment=ft.MainAxisAlignment.START),
                    col={"xs": 12, "sm": 4},
                    padding=ft.padding.only(left=10),
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Bill Copy",
                            size=get_label_size(),
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.BLUE_GREY_700,
                        ),
                        self.bill_copy_field,
                        self.bill_copy_display,
                    ], spacing=5, alignment=ft.MainAxisAlignment.START),
                    col={"xs": 12, "sm": 4},
                    padding=ft.padding.only(left=10),
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Asset Image",
                            size=get_label_size(),
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.BLUE_GREY_700,
                        ),
                        self.image_field,
                        self.image_display,
                    ], spacing=5, alignment=ft.MainAxisAlignment.START),
                    col={"xs": 12, "sm": 4},
                    padding=ft.padding.only(left=10),
                ),
            ],
            spacing=20,
        )

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Container(
                                ft.Column(
                                    controls=[
                                        self.title,
                                        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                                        self.build_form_row("Name", self.name_field),
                                        self.build_form_row("Category", self.category_field_row),
                                        self.build_form_row("Company", self.company_field),
                                        self.build_form_row("Model", self.model_field),
                                        self.build_form_row("Serial No", self.serial_no_field),
                                        self.build_form_row("Purchaser", self.purchaser_field),
                                        self.build_form_row("Location", self.location_field),
                                        self.upload_fields_row,
                                        self.build_form_row("Warranty", self.warranty_field),
                                        self.build_form_row("Price", self.price_field),
                                        self.build_form_row("Status", self.status_field_row),
                                        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                                        ft.Row(
                                            controls=[self.save_button, self.cancel_button],
                                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                            spacing=20,
                                        ),
                                    ],
                                    scroll="adaptive",
                                    expand=True,
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=15,
                                ),
                                bgcolor=ft.colors.WHITE,
                                border_radius=ft.border_radius.all(15),
                                padding=get_container_padding(),
                                shadow=ft.BoxShadow(blur_radius=15, spread_radius=2, color=ft.colors.GREY_400),
                            ),
                            col={"xs": 12, "sm": 10, "md": 8, "lg": 6},
                            expand=True,
                            bgcolor=ft.colors.BLUE_50,
                            padding=get_form_padding(),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

        page.overlay.append(self.file_picker)
        page.overlay.append(self.image_picker)
        page.overlay.append(self.date_picker)

        # Resize handler
        def on_resize(e):
            print(f"Resizing AssetForm: Window width={get_window_width()}")
            self.title.size = get_title_size()
            button_size = get_button_size()
            upload_button_size = get_upload_button_size()

            # Update Save and Cancel buttons
            self.save_button.width = button_size["width"]
            self.save_button.height = button_size["height"]
            self.save_button.content.controls[0].size = button_size["height"] * 0.5
            self.save_button.content.controls[1].size = button_size["height"] * 0.4

            self.cancel_button.width = button_size["width"]
            self.cancel_button.height = button_size["height"]
            self.cancel_button.content.controls[0].size = button_size["height"] * 0.5
            self.cancel_button.content.controls[1].size = button_size["height"] * 0.4

            # Update upload buttons
            self.purchase_date_button.width = upload_button_size["width"]
            self.purchase_date_button.height = upload_button_size["height"]
            self.purchase_date_button.content.controls[0].size = upload_button_size["icon_size"]
            self.purchase_date_button.content.controls[1].size = upload_button_size["text_size"]
            self.purchase_date_text.size = upload_button_size["text_size"]

            self.bill_copy_field.width = upload_button_size["width"]
            self.bill_copy_field.height = upload_button_size["height"]
            self.bill_copy_field.content.controls[0].size = upload_button_size["icon_size"]
            self.bill_copy_field.content.controls[1].size = upload_button_size["text_size"]
            self.bill_copy_display.size = upload_button_size["text_size"]

            self.image_field.width = upload_button_size["width"]
            self.image_field.height = upload_button_size["height"]
            self.image_field.content.controls[0].size = upload_button_size["icon_size"]
            self.image_field.content.controls[1].size = upload_button_size["text_size"]
            self.image_display.size = upload_button_size["text_size"]

            # Update form padding
            self.content.controls[0].controls[0].padding = get_form_padding()
            self.content.controls[0].controls[0].content.padding = get_container_padding()

            page.update()

        page.on_resize = on_resize
        page.update()

    def build_form_row(self, label_text, input_control):
        """Builds a single row for the form with a label and input field."""
        return ft.ResponsiveRow(
            controls=[
                ft.Container(
                    width=150 if not self.page.window.width <= 600 else None,
                    col={"xs": 12, "md": 3},
                    content=ft.Text(label_text, size=self.get_label_size(), weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_700),
                    alignment=ft.alignment.center_left,
                ),
                ft.Container(
                    expand=True,
                    col={"xs": 12, "md": 9},
                    content=input_control,
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        )

    def get_label_size(self):
        window_width = self.page.window.width if self.page.window.width > 0 else 800
        if window_width <= 600:
            return 14
        elif window_width <= 1024:
            return 16
        return 18

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

    def image_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0]
            self.image_display.value = selected_file.name

            # Define the destination directory (D:\myapp\assets\images\)
            assets_dir = os.path.join("assets", "images")
            os.makedirs(assets_dir, exist_ok=True)  # Create the directory if it doesn't exist

            # Create a unique file name using the asset name and timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            asset_name = self.name_field.value.replace(" ", "_") if self.name_field.value else "asset"
            file_extension = os.path.splitext(selected_file.name)[1]  # e.g., .jpg
            new_filename = f"{asset_name}_{timestamp}{file_extension}"
            destination_path = os.path.join(assets_dir, new_filename)

            # Copy the file to the assets/images directory
            try:
                shutil.copy(selected_file.path, destination_path)
                # Store the relative path for the database
                self.image_path = os.path.join("images", new_filename).replace("\\", "/")
                print(f"Image saved to: {destination_path}")
                print(f"Image path for database: {self.image_path}")
            except Exception as err:
                print(f"Error saving image: {err}")
                self.image_display.value = "Error saving image"
                self.image_path = None
        else:
            self.image_display.value = "No image selected"
            self.image_path = None
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
                INSERT INTO component (name, category, company, model, serial_no, purchaser, purchase_date, location, warranty, price, status, bill_copy, image_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                self.name_field.value,
                self.category_field.value,
                self.company_field.value,
                self.model_field.value,
                self.serial_no_field.value,
                self.purchaser_field.value,
                self.purchase_date_text.value,
                self.location_field.value,
                self.warranty_field.value,
                self.price_field.value,
                self.status_field.value,
                self.bill_copy_display.value,
                self.image_path,
            )

            print(f"Executing SQL: {query} with values: {values}")

            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()

            self.page.snack_bar = ft.SnackBar(ft.Text("✅ Asset added successfully!"))
            self.page.snack_bar.open = True
            self.page.go('/asset')  # Redirect to the asset page after saving
            self.page.update()

        except mysql.connector.Error as err:
            print(f"❌ MySQL Error: {err}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {err}"))
            self.page.snack_bar.open = True
            self.page.update()

def ComponentFormPage(page):
    return ComponentForm(page)