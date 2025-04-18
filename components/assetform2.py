import flet as ft
import datetime
#from nav.sidebar import SidebarPage
#from nav.menubar import TopBarPage
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
        self.bill_copy_display = ft.Text("No file selected")  # Text to display the file name
        self.bill_copy_field = ft.ElevatedButton(
            icon=ft.Icons.FILE_UPLOAD,
            text="Upload Bill Copy",
            on_click=lambda e: self.file_picker.pick_files()
        )
        self.file_picker = ft.FilePicker(on_result=self.bill_copy_picked)

        self.location_field = CustomTextField(label="Location")

        self.purchase_date_text = ft.Text("No date selected")  # Text to display the date
        self.purchase_date_field = ft.ElevatedButton(
            "Pick date",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=10, day=1),
                    last_date=datetime.datetime(year=2024, month=10, day=1),
                    on_change=self.handle_change,
                    on_dismiss=self.handle_dismissal,
                )
            ),
        )

        self.warranty_field = CustomTextField(label="Warranty")
        self.price_field = CustomTextField(label="Price")
        self.status_field = ft.Dropdown(
            options=[
                ft.dropdown.Option("Available"),
                #ft.dropdown.Option("Assigned"),
                
            ],
            #on_change=self.status_changed
        )

        # self.assign_to_field = ft.Dropdown(
        #     options=[
        #         ft.dropdown.Option("User"),
        #         ft.dropdown.Option("Department"),
        #     ],
        #     visible=False,
        #     on_change=self.assign_to_changed
        # )

        # self.select_user_field = ft.Dropdown(
        #     options=[
        #         ft.dropdown.Option("User 1"),
        #         ft.dropdown.Option("User 2"),
        #     ],
        #     visible=False
        # )

        # self.select_department_field = ft.Dropdown(
        #     options=[
        #         ft.dropdown.Option("Department 1"),
        #         ft.dropdown.Option("Department 2"),
        #     ],
        #     visible=False
        # )

        self.save_button = ft.ElevatedButton("Save", icon=ft.Icons.SAVE, bgcolor=ft.Colors.GREEN_400, color=ft.colors.WHITE, width=200)  # Add save handler
        self.cancel_button = ft.ElevatedButton("Cancel", icon=ft.Icons.CANCEL, bgcolor=ft.Colors.RED_400, width=200, color=ft.colors.WHITE)  # Add cancel handler

        # Form Layout (Modified)
        self.content = ft.Column(
            controls=[
                TopBarPage(page),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                # ft.Container(
                                #     content=SidebarPage(page),
                                #     width=200,
                                #     expand=True,
                                # ),
                            ],
                        ),
                        ft.Container(
                            content=ft.Container(
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Asset Register",
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.BLUE_900,
                                        ),
                                        self.build_form_row("Name", self.name_field),
                                        self.build_form_row("Category", self.category_field),
                                        self.build_form_row("Company", self.company_field),
                                        self.build_form_row("Model", self.model_field),
                                        self.build_form_row("Serial No", self.serial_no_field),
                                        self.build_form_row("Purchaser", self.purchaser_field),
                                        self.build_form_row("Location", self.location_field),
                                        # add button to upload bill copy
                                        self.build_form_row("Bill Copy", self.bill_copy_field),
                                        self.build_form_row("Bill Copy", self.bill_copy_display),

                                        # Modified Purchase Date Row
                                        ft.ResponsiveRow(
                                            controls=[
                                                ft.Container(
                                                    width=150,
                                                    col={"xs": 12, "md": 3},
                                                    content=ft.Text(
                                                        "Purchase Date",
                                                        size=18,
                                                        weight=ft.FontWeight.W_500,
                                                        color=ft.Colors.BLUE_GREY_700,
                                                    ),
                                                ),
                                                ft.Container(
                                                    expand=True,
                                                    col={"xs": 12, "md": 9},
                                                    content=ft.Row([  # Row for button and text
                                                        self.purchase_date_field,
                                                        self.purchase_date_text,
                                                    ]),
                                                ),
                                            ],
                                            spacing=10,
                                        ),
                                        self.build_form_row("Warranty", self.warranty_field),
                                        self.build_form_row("Price", self.price_field),
                                        self.build_form_row("Status", self.status_field),
                                        # self.build_form_row("Assign To", self.assign_to_field),
                                        # self.build_form_row("Select User", self.select_user_field),
                                        # self.build_form_row("Select Department", self.select_department_field),
                                        # Save and Cancel Buttons
                                        ft.Row(
                                            controls=[
                                                self.save_button,
                                                self.cancel_button,
                                            ],
                                            alignment=ft.MainAxisAlignment.END,
                                            spacing=20,
                                        ),
                                    ],
                                    scroll="adaptive",
                                    expand=True,
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                
                                bgcolor=ft.Colors.WHITE,
                                border_radius=ft.border_radius.all(15),
                                padding=20,
                                shadow=ft.BoxShadow(
                                    blur_radius=10,
                                    spread_radius=1,
                                    color=ft.Colors.GREY_400,
                                ),
                            ),
                            col={"sm": 12, "md": 9},
                            expand=True,
                            bgcolor=ft.Colors.GREY_100,
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
        page.update()

    def build_form_row(self, label_text, input_control):
        """Builds a single row for the form with a label and input field."""
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

    def handle_change(e, self):
        self.purchase_date_text.value = self.control.value.strftime("%Y-%m-%d")
        self.page.update()


    def handle_dismissal(e, self):
        self.purchase_date_text.value = "No date selected"
        self.purchase_date_field.text = "Change Date"
        self.page.update()

    # def status_changed(self, e):
    #     if e.control.value == "Assigned":
    #         self.assign_to_field.visible = True
    #     else:
    #         self.assign_to_field.visible = False
    #         self.select_user_field.visible = False
    #         self.select_department_field.visible = False
    #     self.page.update()

    # def assign_to_changed(self, e):
    #     if e.control.value == "User":
    #         self.select_user_field.visible = True
    #         self.select_department_field.visible = False
    #     elif e.control.value == "Department":
    #         self.select_user_field.visible = False
    #         self.select_department_field.visible = True
    #     self.page.update()

    def bill_copy_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0]  # Get the first selected file
            self.bill_copy_display.value = selected_file.name  # Update the text display
            self.bill_copy_field.value = selected_file.path  # Store the path or content in the hidden field if needed
            print(f"File picked: {selected_file.path}")  # Print the path (for demonstration)

            # Here you can implement your logic to upload the file to your server or storage
            # You can access the file content using selected_file.read_bytes() or selected_file.read_text()
        else:
            self.bill_copy_display.value = "No file selected"
            self.bill_copy_field.value = ""
        self.update()

def AssetFormPage(page):
    return AssetForm(page)