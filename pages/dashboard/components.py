import flet as ft
from components.manageasset import ManageAssetDialog
from components.assetdialog import AssetDialog
import mysql.connector
class Components(ft.Container):
     def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True

        page.window.title = "Asset Management System - Assets"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.START

        self.asset_dialog = AssetDialog(page)
        self.manage_Asset = ManageAssetDialog(page, self)

        # Helper methods for responsive design
        def get_window_width():
            return page.window.width if page.window.width > 0 else 800

        def is_mobile():
            return get_window_width() <= 600

        def is_tablet():
            return 601 <= get_window_width() <= 1024

        def get_image_size():
            if is_mobile():
                return 100
            elif is_tablet():
                return 120
            return 150

        def get_button_size():
            if is_mobile():
                return {"width": 120, "height": 40}
            elif is_tablet():
                return {"width": 135, "height": 45}
            return {"width": 150, "height": 50}

        def get_asset_image_size():
            if is_mobile():
                return 80
            elif is_tablet():
                return 100
            return 120

        # Product Detail Banner
        def close_banner(e):
            page.close(self.banner)
            page.add(ft.Text("Action clicked: " + e.control.text))

        action_button_style = ft.ButtonStyle(color=ft.colors.BLUE)
        asset_details = {
            "Name": "Laptop",
            "Category": "Electronics",
            "Company": "Dell",
            "Model": "XPS 15",
            "Serial No": "123456789",
            "Purchase Date": "2023-01-15",
            "Warranty": "2 Years",
            "Price": "$1500",
            "Status": "Available"
        }
        asset_detail_rows = [
            ft.Row(controls=[ft.Text(f"{key}: ", weight=ft.FontWeight.BOLD), ft.Text(value)])
            for key, value in asset_details.items()
        ]

        image_size = get_image_size()
        banner_content = ft.Column(
            controls=[
                ft.Column(
                    controls=[ft.Text("Asset Details:", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD, size=20)] + asset_detail_rows,
                    expand=True,
                    wrap=True,
                ),
                ft.Container(
                    content=ft.Image(src="images/jojo.jpg", width=image_size, height=image_size, fit=ft.ImageFit.CONTAIN),
                    alignment=ft.alignment.center,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ) if is_mobile() else ft.Row(
            controls=[
                ft.Column(
                    controls=[ft.Text("Asset Details:", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD, size=20)] + asset_detail_rows,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Image(src="images/jojo.jpg", width=image_size, height=image_size, fit=ft.ImageFit.CONTAIN),
                    alignment=ft.alignment.center,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.banner = ft.Banner(
            bgcolor=ft.colors.WHITE70,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=banner_content,
            actions=[
                ft.ElevatedButton(text="View", icon=ft.icons.ACCESS_ALARM, width=100 if not is_mobile() else 80, style=action_button_style, on_click=close_banner),
                ft.TextButton(text="Ignore", style=action_button_style, on_click=close_banner),
                ft.TextButton(text="Cancel", style=action_button_style, on_click=close_banner),
            ],
        )

        # Add Asset Button
        button_size = get_button_size()
        self.add_asset_button = ft.ElevatedButton(
            icon=ft.icons.ADD,
            text="Add Component",
            bgcolor=ft.colors.GREEN_400,
            width=button_size["width"],
            height=button_size["height"],
            color=ft.colors.WHITE,
            on_click=lambda e: page.go('/componentform')  
        )

        # Database Connection
        try:
            mydb = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            print("Database connection successful")
        except mysql.connector.Error as err:
            print(f"Database connection failed: {err}")
            mydb = None

        # Fetch data (added image_path)
        self.asset_data = []
        if mydb:
            try:
                mycur = mydb.cursor()
                mycur.execute("SELECT name, model_no, total_qty FROM component")
                self.asset_data = mycur.fetchall()
                print(f"Query returned {len(self.asset_data)} rows: {self.asset_data}")
                mycur.close()
                mydb.close()
            except mysql.connector.Error as err:
                print(f"Query failed: {err}")
                self.asset_data = []

        # Card creation function for deployable assets (with image)
        def create_asset_card(data, status_color, on_manage_click, on_select):
            # Extract data fields
            name = str(data[0]) if data[0] is not None else ""
            model_no = str(data[1]) if data[1] is not None else ""
            total_qty = str(data[2]) if data[2] is not None else ""
            status = "Available"  # Placeholder for status
            

            asset_image_size = get_asset_image_size()
            return ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Image(
                                    src="image_path",
                                    width=asset_image_size,
                                    height=asset_image_size,
                                    fit=ft.ImageFit.CONTAIN,
                                    error_content=ft.Icon(ft.icons.IMAGE_NOT_SUPPORTED, size=asset_image_size / 2, color=ft.colors.GREY_400),
                                ),
                                alignment=ft.alignment.center,
                                margin=ft.margin.only(bottom=10),
                            ),
                            ft.Row(
                                [
                                    ft.Text(f"Name: {name}", size=16, weight=ft.FontWeight.BOLD, color="#263238"),
                                    ft.Container(
                                        content=ft.Row(
                                            [
                                                ft.Container(width=15, height=15, bgcolor=status_color, border_radius=10),
                                                ft.Text(status, color=ft.colors.BLACK),
                                            ],
                                            spacing=5,
                                            alignment=ft.MainAxisAlignment.END,
                                        ),
                                        alignment=ft.alignment.center_right,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text(f"Model No: {model_no}", size=14, color="#263238"),
                            ft.Text(f"Total Qty: {total_qty}", size=14, color="#263238"),
                            ft.Text(f"Assigned To: {name}", size=14, color="#263238"),
                            ft.ElevatedButton(
                                "Manage",
                                icon=ft.icons.PENDING_ACTIONS,
                                bgcolor=ft.colors.BLUE_300,
                                color=ft.colors.WHITE,
                                on_click=on_manage_click,
                                width=100,
                            ),
                        ],
                        spacing=5,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=15,
                    bgcolor="#E3F2FD",
                    border_radius=12,
                    ink=True,
                    on_click=on_select,
                ),
                elevation=5,
            )

        # Deployable Cards
        self.deployable_cards = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=create_asset_card(
                        data=x,
                        status_color=ft.colors.LIGHT_GREEN_ACCENT_400,
                        on_manage_click=lambda e: self.manage_Asset.open(),
                        on_select=lambda e: self.show_banner(),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for x in self.asset_data
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            run_spacing=0,
        )

        # Deployed Cards
        deployed_data = [
            ("Laptop", "Dell", "XPS 15", "Abdul Salam", "IT", "GFI", "19-02-2025", "Assigned", ft.colors.LIGHT_BLUE_ACCENT_700),
            ("Mouse", "Logitech", "MX Master 3", "Abdul Salam", "IT", "GFI", "19-02-2025", "Assigned", ft.colors.LIGHT_BLUE_ACCENT_700),
        ]

        def create_deployed_card(data, status_color, on_manage_click, on_select):
            category, company, model, assign_to, department, company_2, assign_date, status, _ = data
            return ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(f"Category: {category}", size=16, weight=ft.FontWeight.BOLD, color="#263238"),
                                    ft.Container(
                                        content=ft.Row(
                                            [
                                                ft.Container(width=15, height=15, bgcolor=status_color, border_radius=10),
                                                ft.Text(status, color=ft.colors.BLACK),
                                            ],
                                            spacing=5,
                                            alignment=ft.MainAxisAlignment.END,
                                        ),
                                        alignment=ft.alignment.center_right,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text(f"Company: {company}", size=14, color="#263238"),
                            ft.Text(f"Model: {model}", size=14, color="#263238"),
                            ft.Text(f"Assign To: {assign_to}", size=14, color="#263238"),
                            ft.Text(f"Department: {department}", size=14, color="#263238"),
                            ft.Text(f"Company: {company_2}", size=14, color="#263238"),
                            ft.Text(f"Assign Date: {assign_date}", size=14, color="#263238"),
                            ft.ElevatedButton(
                                "Manage",
                                icon=ft.icons.PENDING_ACTIONS,
                                bgcolor=ft.colors.BLUE_300,
                                color=ft.colors.WHITE,
                                on_click=on_manage_click,
                                width=100,
                            ),
                        ],
                        spacing=5,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=15,
                    bgcolor="#E3F2FD",
                    border_radius=12,
                    ink=True,
                    on_click=on_select,
                ),
                elevation=5,
            )

        self.deployed_cards = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=create_deployed_card(
                        data=data,
                        status_color=data[8],
                        on_manage_click=lambda e: self.show_manage_asset_bottomsheet(),
                        on_select=lambda e: self.show_banner(),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for data in deployed_data
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            run_spacing=0,
        )

        # Faulted Cards
        faulted_data = [
            ("Laptop", "Dell", "XPS 15", "19-02-2023", "19-02-2024", "Faulty Screen", "Scraped", "Disposed", ft.colors.RED_ACCENT_400),
            ("Mouse", "Logitech", "MX Master 3", "987654321", "2023-06-01", "1 Year", "$100", "Sold", ft.colors.YELLOW_ACCENT_400),
        ]

        def create_faulted_card(data, status_color, on_manage_click, on_select):
            category, company, model, purchase_date, defected_date, reason, action, status, _ = data
            return ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(f"Category: {category}", size=16, weight=ft.FontWeight.BOLD, color="#263238"),
                                    ft.Container(
                                        content=ft.Row(
                                            [
                                                ft.Container(width=15, height=15, bgcolor=status_color, border_radius=10),
                                                ft.Text(status, color=ft.colors.BLACK),
                                            ],
                                            spacing=5,
                                            alignment=ft.MainAxisAlignment.END,
                                        ),
                                        alignment=ft.alignment.center_right,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text(f"Company: {company}", size=14, color="#263238"),
                            ft.Text(f"Model: {model}", size=14, color="#263238"),
                            ft.Text(f"Purchase Date: {purchase_date}", size=14, color="#263238"),
                            ft.Text(f"Defected Date: {defected_date}", size=14, color="#263238"),
                            ft.Text(f"Reason: {reason}", size=14, color="#263238"),
                            ft.Text(f"Action: {action}", size=14, color="#263238"),
                            ft.ElevatedButton(
                                "Manage",
                                icon=ft.icons.PENDING_ACTIONS,
                                bgcolor=ft.colors.BLUE_300,
                                color=ft.colors.WHITE,
                                on_click=on_manage_click,
                                width=100,
                            ),
                        ],
                        spacing=5,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=15,
                    bgcolor="#E3F2FD",
                    border_radius=12,
                    ink=True,
                    on_click=on_select,
                ),
                elevation=5,
            )

        self.faulted_cards = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=create_faulted_card(
                        data=data,
                        status_color=data[8],
                        on_manage_click=lambda e: self.show_manage_asset_bottomsheet(),
                        on_select=lambda e: self.show_banner(),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for data in faulted_data
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            run_spacing=0,
        )

        # Tabs with cards
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Available",
                    content=ft.Column(
                        controls=[self.deployable_cards],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    )
                ),
                ft.Tab(
                    text="Assigned",
                    content=ft.Column(
                        controls=[self.deployed_cards],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    )
                ),
                ft.Tab(
                    text="Disposed/Sold",
                    content=ft.Column(
                        controls=[self.faulted_cards],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    )
                ),
            ],
            expand=True,
        )

        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.add_asset_button], alignment=ft.MainAxisAlignment.CENTER),
                self.tabs,
            ],
            expand=True,
            spacing=10,
        )

        # Update layout on resize
        def on_resize(e):
            print(f"Resizing AssetPagee: Window width={get_window_width()}")
            image_size = get_image_size()
            banner_content.controls[1].content.width = image_size
            banner_content.controls[1].content.height = image_size
            if is_mobile():
                banner_content.controls = [
                    ft.Column(
                        controls=[ft.Text("Asset Details:", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD, size=20)] + asset_detail_rows,
                        expand=True,
                        wrap=True,
                    ),
                    ft.Container(
                        content=ft.Image(src="images/jojo.jpg", width=image_size, height=image_size, fit=ft.ImageFit.CONTAIN),
                        alignment=ft.alignment.center,
                    ),
                ]
            else:
                banner_content.controls = [
                    ft.Column(
                        controls=[ft.Text("Asset Details:", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD, size=20)] + asset_detail_rows,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Image(src="images/jojo.jpg", width=image_size, height=image_size, fit=ft.ImageFit.CONTAIN),
                        alignment=ft.alignment.center,
                    ),
                ]
            self.banner.actions[0].width = 100 if not is_mobile() else 80

            button_size = get_button_size()
            self.add_asset_button.width = button_size["width"]
            self.add_asset_button.height = button_size["height"]

            page.update()

        page.on_resize = on_resize
        page.update()

     def show_banner(self):
        self.page.open(self.banner)

     def show_manage_asset_bottomsheet(self):
        self.page.show_bottom_sheet(self.manage_Asset)

