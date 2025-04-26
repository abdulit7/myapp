import flet as ft
from components.managecomponent import ManageComponentDialog
from components.assetdialog import AssetDialog
import mysql.connector
import os

class Components(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True

        page.window.title = "Asset Management System - Components"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.START

        self.asset_dialog = AssetDialog(page)
        self.manage_component = ManageComponentDialog(page, self)

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
        banner_content = ft.Column(
            controls=[
                ft.Column(
                    controls=[ft.Text("Component Details:", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD, size=20)],
                    expand=True,
                    wrap=True,
                ),
                ft.Container(
                    content=ft.Image(src="images/jojo.jpg", width=get_image_size(), height=get_image_size(), fit=ft.ImageFit.CONTAIN),
                    alignment=ft.alignment.center,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ) if is_mobile() else ft.Row(
            controls=[
                ft.Column(
                    controls=[ft.Text("Component Details:", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD, size=20)],
                    expand=True,
                ),
                ft.Container(
                    content=ft.Image(src="images/jojo.jpg", width=get_image_size(), height=get_image_size(), fit=ft.ImageFit.CONTAIN),
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

        # Add Component Button
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

        # Fetch data for Available components
        self.available_data = []
        if mydb:
            try:
                mycur = mydb.cursor()
                mycur.execute("""
                    SELECT id, name, model_no, total_qty, status, image_path
                    FROM component
                    WHERE status = 'Available'
                """)
                self.available_data = mycur.fetchall()
                print(f"Available components query returned {len(self.available_data)} rows: {self.available_data}")
            except mysql.connector.Error as err:
                print(f"Available components query failed: {err}")
                self.available_data = []

        # Fetch data for Deployed components
        self.deployed_data = []
        if mydb:
            try:
                mycur = mydb.cursor()
                mycur.execute("""
                    SELECT id, category, company, model, deployed_to, user_department, deploy_date, status, image_path
                    FROM deployed_components
                    WHERE status = 'Deployed'
                """)
                self.deployed_data = mycur.fetchall()
                print(f"Deployed components query returned {len(self.deployed_data)} rows: {self.deployed_data}")
            except mysql.connector.Error as err:
                print(f"Deployed components query failed: {err}")
                self.deployed_data = []

        # Fetch data for Disposed components (Scrap, Dispose, Sold)
        self.disposed_data = []
        if mydb:
            try:
                mycur = mydb.cursor()
                mycur.execute("""
                    SELECT id, name, category, company, model, purchase_date, disposal_date, disposal_type,
                           amount_earned, disposal_reason, disposal_location, sale_details, sold_to, image_path
                    FROM disposed_components
                """)
                self.disposed_data = mycur.fetchall()
                print(f"Disposed components query returned {len(self.disposed_data)} rows: {self.disposed_data}")
            except mysql.connector.Error as err:
                print(f"Disposed components query failed: {err}")
                self.disposed_data = []
            finally:
                if mydb.is_connected():
                    mycur.close()
                    mydb.close()

        # Available Cards
        self.deployable_cards = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self.create_asset_card(
                        data=x,
                        status_color=ft.colors.LIGHT_GREEN_ACCENT_400,
                        on_manage_click=lambda id, name: self.manage_component.open(component_id=id, name=name),
                        on_select=lambda e, component=x: self.show_banner(component=component, is_deployed=False, is_disposed=False),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for x in self.available_data
            ] if self.available_data else [
                ft.Container(
                    content=ft.Text("No available components found.", color=ft.colors.GREY_600, size=16),
                    col={"xs": 12},
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            run_spacing=0,
        )

        # Deployed Cards
        self.deployed_cards = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self.create_deployed_card(
                        data=data,
                        status_color=ft.colors.LIGHT_BLUE_ACCENT_700,
                        on_manage_click=lambda id, name: self.manage_component.open(component_id=id, name=name),
                        on_select=lambda e, component=data: self.show_banner(component=component, is_deployed=True, is_disposed=False),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for data in self.deployed_data
            ] if self.deployed_data else [
                ft.Container(
                    content=ft.Text("No deployed components found.", color=ft.colors.GREY_600, size=16),
                    col={"xs": 12},
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            run_spacing=0,
        )

        # Disposed/Sold Cards
        self.disposed_cards = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=self.create_disposed_card(
                        data=data,
                        status_color=ft.colors.RED_ACCENT_400 if data[7] == "Scrap" else (ft.colors.YELLOW_ACCENT_400 if data[7] == "Sold" else ft.colors.GREY_400),
                        on_manage_click=lambda id, name: self.show_disposal_details(id, name),
                        on_select=lambda e, component=data: self.show_banner(component=component, is_deployed=False, is_disposed=True),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for data in self.disposed_data
            ] if self.disposed_data else [
                ft.Container(
                    content=ft.Text("No disposed components found.", color=ft.colors.GREY_600, size=16),
                    col={"xs": 12},
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center,
                )
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
                        controls=[self.disposed_cards],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    )
                ),
            ],
            expand=True,
        )

        self.content = ft.Column(
            controls=[
                ft.Divider(height=1, color=ft.colors.WHITE),
                ft.Row(controls=[self.add_asset_button], alignment=ft.MainAxisAlignment.START),
                self.tabs,
            ],
            expand=True,
            spacing=10,
        )

        # Update layout on resize
        def on_resize(e):
            print(f"Resizing Components: Window width={get_window_width()}")
            image_size = get_image_size()
            banner_content.controls[1].content.width = image_size
            banner_content.controls[1].content.height = image_size
            if is_mobile():
                banner_content.controls = [
                    ft.Column(
                        controls=[ft.Text("Component Details:", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD, size=20)],
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
                        controls=[ft.Text("Component Details:", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD, size=20)],
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

    def create_asset_card(self, data, status_color, on_manage_click, on_select):
        component_id = data[0]
        name = str(data[1]) if data[1] is not None else ""
        model_no = str(data[2]) if data[2] is not None else ""
        total_qty = str(data[3]) if data[3] is not None else ""
        status = str(data[4]) if data[4] is not None else "Unknown"
        image_path = str(data[5]) if data[5] is not None else None

        # Debug and validate image path
        print(f"Processing component: {name}, image_path: {image_path}")
        image_content = None
        if image_path:
            image_path = image_path.replace("\\", "/")
            print(f"Normalized image_path: {image_path}")
            if os.path.isfile(image_path):
                image_content = ft.Image(
                    src=image_path,
                    width=120,
                    height=120,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Icon(ft.icons.IMAGE_NOT_SUPPORTED, size=60, color=ft.colors.GREY_400),
                )
                print(f"Image file found: {image_path}")
            else:
                print(f"Image file not found: {image_path}")
        else:
            print(f"No image_path for {name}")

        card_content = [
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
            ft.Text(f"Assigned To: None", size=14, color="#263238"),
            ft.ElevatedButton(
                "Manage",
                icon=ft.icons.PENDING_ACTIONS,
                bgcolor=ft.colors.BLUE_300,
                color=ft.colors.WHITE,
                on_click=lambda e: on_manage_click(component_id, name),
                width=100,
            ),
        ]

        if image_content:
            card_content.insert(0, ft.Container(
                content=image_content,
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=10),
            ))

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    card_content,
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=15,
                bgcolor="#E3F2FD",
                border_radius=12,
                ink=True,
                on_click=on_select,
                width=300,
                height=340 if image_content else 300,
            ),
            elevation=5,
        )

    def create_deployed_card(self, data, status_color, on_manage_click, on_select):
        component_id = data[0]
        category = str(data[1]) if data[1] is not None else ""
        company = str(data[2]) if data[2] is not None else ""
        model = str(data[3]) if data[3] is not None else ""
        deployed_to = str(data[4]) if data[4] is not None else ""
        user_department = str(data[5]) if data[5] is not None else ""
        deploy_date = str(data[6]) if data[6] is not None else ""
        status = str(data[7]) if data[7] is not None else "Unknown"
        image_path = str(data[8]) if data[8] is not None else None

        # Debug and validate image path
        print(f"Processing deployed component: {category}, image_path: {image_path}")
        image_content = None
        if image_path:
            image_path = image_path.replace("\\", "/")
            print(f"Normalized image_path: {image_path}")
            if os.path.isfile(image_path):
                image_content = ft.Image(
                    src=image_path,
                    width=120,
                    height=120,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Icon(ft.icons.IMAGE_NOT_SUPPORTED, size=60, color=ft.colors.GREY_400),
                )
                print(f"Image file found: {image_path}")
            else:
                print(f"Image file not found: {image_path}")
        else:
            print(f"No image_path for {category}")

        card_content = [
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
            ft.Text(f"Assigned To: {deployed_to}", size=14, color="#263238"),
            ft.Text(f"Department: {user_department}", size=14, color="#263238"),
            ft.Text(f"Assign Date: {deploy_date}", size=14, color="#263238"),
            ft.ElevatedButton(
                "Manage",
                icon=ft.icons.PENDING_ACTIONS,
                bgcolor=ft.colors.BLUE_300,
                color=ft.colors.WHITE,
                on_click=lambda e: on_manage_click(component_id, category),
                width=100,
            ),
        ]

        if image_content:
            card_content.insert(0, ft.Container(
                content=image_content,
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=10),
            ))

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    card_content,
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=15,
                bgcolor="#E3F2FD",
                border_radius=12,
                ink=True,
                on_click=on_select,
                width=300,
                height=340 if image_content else 300,
            ),
            elevation=5,
        )

    def create_disposed_card(self, data, status_color, on_manage_click, on_select):
        component_id = data[0]
        name = str(data[1]) if data[1] is not None else ""
        category = str(data[2]) if data[2] is not None else ""
        company = str(data[3]) if data[3] is not None else ""
        model = str(data[4]) if data[4] is not None else ""
        purchase_date = str(data[5]) if data[5] is not None else ""
        disposal_date = str(data[6]) if data[6] is not None else ""
        disposal_type = str(data[7]) if data[7] is not None else ""
        amount_earned = f"${data[8]}" if data[8] is not None else ""
        disposal_reason = str(data[9]) if data[9] is not None else ""
        disposal_location = str(data[10]) if data[10] is not None else ""
        sale_details = str(data[11]) if data[11] is not None else ""
        sold_to = str(data[12]) if data[12] is not None else ""
        image_path = str(data[13]) if data[13] is not None else None

        # Truncate long text for display on the card
        def truncate_text(text, max_length=30):
            return text[:max_length] + "..." if len(text) > max_length else text

        disposal_reason_display = truncate_text(disposal_reason) if disposal_reason else ""
        disposal_location_display = truncate_text(disposal_location) if disposal_location else ""
        sale_details_display = truncate_text(sale_details) if sale_details else ""
        sold_to_display = truncate_text(sold_to) if sold_to else ""

        # Debug and validate image path
        print(f"Processing disposed component: {name}, image_path: {image_path}")
        image_content = None
        if image_path:
            image_path = image_path.replace("\\", "/")
            print(f"Normalized image_path: {image_path}")
            if os.path.isfile(image_path):
                image_content = ft.Image(
                    src=image_path,
                    width=120,
                    height=120,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Icon(ft.icons.IMAGE_NOT_SUPPORTED, size=60, color=ft.colors.GREY_400),
                )
                print(f"Image file found: {image_path}")
            else:
                print(f"Image file not found: {image_path}")
        else:
            print(f"No image_path for {name}")

        card_content = [
            ft.Row(
                [
                    ft.Text(f"Name: {name}", size=16, weight=ft.FontWeight.BOLD, color="#263238"),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(width=15, height=15, bgcolor=status_color, border_radius=10),
                                ft.Text(disposal_type, color=ft.colors.BLACK),
                            ],
                            spacing=5,
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        alignment=ft.alignment.center_right,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Text(f"Category: {category}", size=14, color="#263238"),
            ft.Text(f"Company: {company}", size=14, color="#263238"),
            ft.Text(f"Model: {model}", size=14, color="#263238"),
            ft.Text(f"Purchase Date: {purchase_date}", size=14, color="#263238"),
            ft.Text(f"Disposal Date: {disposal_date}", size=14, color="#263238"),
        ]

        if disposal_type == "Scrap" and amount_earned:
            card_content.append(ft.Text(f"Amount Earned: {amount_earned}", size=14, color="#263238"))
        elif disposal_type == "Dispose":
            if disposal_reason_display:
                card_content.append(ft.Text(f"Reason: {disposal_reason_display}", size=14, color="#263238"))
            if disposal_location_display:
                card_content.append(ft.Text(f"Disposal Location: {disposal_location_display}", size=14, color="#263238"))
        elif disposal_type == "Sold":
            if sold_to_display:
                card_content.append(ft.Text(f"Sold To: {sold_to_display}", size=14, color="#263238"))
            if sale_details_display:
                card_content.append(ft.Text(f"Sale Details: {sale_details_display}", size=14, color="#263238"))
            if amount_earned:
                card_content.append(ft.Text(f"Amount Earned: {amount_earned}", size=14, color="#263238"))

        card_content.append(
            ft.ElevatedButton(
                "View Details",
                icon=ft.icons.INFO,
                bgcolor=ft.colors.GREY_500,
                color=ft.colors.WHITE,
                on_click=lambda e: on_manage_click(component_id, name),
                width=100,
            )
        )

        if image_content:
            card_content.insert(0, ft.Container(
                content=image_content,
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=10),
            ))

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    card_content,
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=15,
                bgcolor="#E3F2FD",
                border_radius=12,
                ink=True,
                on_click=on_select,
                width=300,
                height=360,  # Fixed height for consistency
            ),
            elevation=5,
        )

    def show_banner(self, component=None, is_deployed=False, is_disposed=False):
        if component:
            try:
                mydb = mysql.connector.connect(
                    host="200.200.200.23",
                    user="root",
                    password="Pak@123",
                    database="itasset",
                    auth_plugin='mysql_native_password'
                )
                mycur = mydb.cursor()

                if is_deployed:
                    mycur.execute(
                        """
                        SELECT id, category, company, model, deployed_to, user_department, deploy_date, status, image_path
                        FROM deployed_components
                        WHERE id = %s
                        """,
                        (component[0],)
                    )
                    component_data = mycur.fetchone()
                    if component_data:
                        component_details = {
                            "Category": str(component_data[1]) if component_data[1] is not None else "",
                            "Company": str(component_data[2]) if component_data[2] is not None else "",
                            "Model": str(component_data[3]) if component_data[3] is not None else "",
                            "Assigned To": str(component_data[4]) if component_data[4] is not None else "",
                            "Department": str(component_data[5]) if component_data[5] is not None else "",
                            "Assign Date": str(component_data[6]) if component_data[6] is not None else "",
                            "Status": str(component_data[7]) if component_data[7] is not None else "",
                        }
                        image_path = str(component_data[8]) if component_data[8] is not None else None
                    else:
                        component_details = {"Category": "Component not found"}
                        image_path = None
                elif is_disposed:
                    mycur.execute(
                        """
                        SELECT name, category, company, model, purchase_date, disposal_date, disposal_type,
                               amount_earned, disposal_reason, disposal_location, sale_details, sold_to, image_path
                        FROM disposed_components
                        WHERE id = %s
                        """,
                        (component[0],)
                    )
                    component_data = mycur.fetchone()
                    if component_data:
                        component_details = {
                            "Name": str(component_data[0]) if component_data[0] is not None else "",
                            "Category": str(component_data[1]) if component_data[1] is not None else "",
                            "Company": str(component_data[2]) if component_data[2] is not None else "",
                            "Model": str(component_data[3]) if component_data[3] is not None else "",
                            "Purchase Date": str(component_data[4]) if component_data[4] is not None else "",
                            "Disposal Date": str(component_data[5]) if component_data[5] is not None else "",
                            "Disposal Type": str(component_data[6]) if component_data[6] is not None else "",
                        }
                        if component_data[7] is not None:
                            component_details["Amount Earned"] = f"${component_data[7]}"
                        if component_data[8]:
                            component_details["Disposal Reason"] = str(component_data[8])
                        if component_data[9]:
                            component_details["Disposal Location"] = str(component_data[9])
                        if component_data[10]:
                            component_details["Sale Details"] = str(component_data[10])
                        if component_data[11]:
                            component_details["Sold To"] = str(component_data[11])
                        image_path = str(component_data[12]) if component_data[12] is not None else None
                    else:
                        component_details = {"Name": "Component not found"}
                        image_path = None
                else:
                    mycur.execute(
                        """
                        SELECT id, name, model_no, total_qty, status, image_path
                        FROM component
                        WHERE id = %s
                        """,
                        (component[0],)
                    )
                    component_data = mycur.fetchone()
                    if component_data:
                        component_details = {
                            "Name": str(component_data[1]) if component_data[1] is not None else "",
                            "Model No": str(component_data[2]) if component_data[2] is not None else "",
                            "Total Qty": str(component_data[3]) if component_data[3] is not None else "",
                            "Status": str(component_data[4]) if component_data[4] is not None else "",
                            "Assigned To": "None",
                        }
                        image_path = str(component_data[5]) if component_data[5] is not None else None
                    else:
                        component_details = {"Name": "Component not found"}
                        image_path = None

                mycur.close()
                mydb.close()

            except mysql.connector.Error as err:
                print(f"Error fetching component details: {err}")
                component_details = {"Name": "Error loading component details"}
                image_path = None

            component_detail_rows = [
                ft.Row(controls=[ft.Text(f"{key}: ", weight=ft.FontWeight.BOLD), ft.Text(value)])
                for key, value in component_details.items() if value
            ]

            image_content = ft.Image(
                src=image_path if image_path else "images/jojo.jpg",
                width=150,
                height=150,
                fit=ft.ImageFit.CONTAIN,
                error_content=ft.Text("Image not found"),
            )

            self.banner.content.controls[0].controls = [
                ft.Text("Component Details:", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD, size=20)
            ] + component_detail_rows
            self.banner.content.controls[1].content = image_content

        self.page.open(self.banner)

    def show_disposal_details(self, component_id, name):
        """Show a dialog with disposal details for a disposed component."""
        try:
            mydb = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            mycur = mydb.cursor()
            mycur.execute(
                """
                SELECT name, category, company, model, purchase_date, disposal_date, disposal_type,
                       amount_earned, disposal_reason, disposal_location, sale_details, sold_to
                FROM disposed_components
                WHERE id = %s
                """,
                (component_id,)
            )
            component_data = mycur.fetchone()
            mycur.close()
            mydb.close()

            if component_data:
                details = {
                    "Name": str(component_data[0]) if component_data[0] is not None else "",
                    "Category": str(component_data[1]) if component_data[1] is not None else "",
                    "Company": str(component_data[2]) if component_data[2] is not None else "",
                    "Model": str(component_data[3]) if component_data[3] is not None else "",
                    "Purchase Date": str(component_data[4]) if component_data[4] is not None else "",
                    "Disposal Date": str(component_data[5]) if component_data[5] is not None else "",
                    "Disposal Type": str(component_data[6]) if component_data[6] is not None else "",
                }
                if component_data[7] is not None:
                    details["Amount Earned"] = f"${component_data[7]}"
                if component_data[8]:
                    details["Disposal Reason"] = str(component_data[8])
                if component_data[9]:
                    details["Disposal Location"] = str(component_data[9])
                if component_data[10]:
                    details["Sale Details"] = str(component_data[10])
                if component_data[11]:
                    details["Sold To"] = str(component_data[11])
            else:
                details = {"Name": "Component not found"}

        except mysql.connector.Error as err:
            print(f"Error fetching disposal details: {err}")
            details = {"Name": "Error loading disposal details"}

        detail_rows = [
            ft.Row(controls=[ft.Text(f"{key}: ", weight=ft.FontWeight.BOLD), ft.Text(value)])
            for key, value in details.items() if value
        ]

        dialog = ft.AlertDialog(
            title=ft.Text(f"Disposal Details for {name}"),
            content=ft.Column(detail_rows, spacing=5),
            actions=[
                ft.TextButton("Close", on_click=lambda e: self.page.close(dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.open(dialog)

    def refresh_cards(self):
        try:
            mydb = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            mycur = mydb.cursor()
            mycur.execute("""
                SELECT id, name, model_no, total_qty, status, image_path
                FROM component
                WHERE status = 'Available'
            """)
            self.available_data = mycur.fetchall()
            print(f"Refreshed available components: {len(self.available_data)} rows")
            mycur.close()

            mycur = mydb.cursor()
            mycur.execute("""
                SELECT id, category, company, model, deployed_to, user_department, deploy_date, status, image_path
                FROM deployed_components
                WHERE status = 'Deployed'
            """)
            self.deployed_data = mycur.fetchall()
            print(f"Refreshed deployed components: {len(self.deployed_data)} rows")
            mycur.close()

            mycur = mydb.cursor()
            mycur.execute("""
                SELECT id, name, category, company, model, purchase_date, disposal_date, disposal_type,
                       amount_earned, disposal_reason, disposal_location, sale_details, sold_to, image_path
                FROM disposed_components
            """)
            self.disposed_data = mycur.fetchall()
            print(f"Refreshed disposed components: {len(self.disposed_data)} rows")
            mycur.close()

            mydb.close()

            self.deployable_cards.controls = [
                ft.Container(
                    content=self.create_asset_card(
                        data=x,
                        status_color=ft.colors.LIGHT_GREEN_ACCENT_400,
                        on_manage_click=lambda id, name: self.manage_component.open(component_id=id, name=name),
                        on_select=lambda e, component=x: self.show_banner(component=component, is_deployed=False, is_disposed=False),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for x in self.available_data
            ] if self.available_data else [
                ft.Container(
                    content=ft.Text("No available components found.", color=ft.colors.GREY_600, size=16),
                    col={"xs": 12},
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center,
                )
            ]

            self.deployed_cards.controls = [
                ft.Container(
                    content=self.create_deployed_card(
                        data=data,
                        status_color=ft.colors.LIGHT_BLUE_ACCENT_700,
                        on_manage_click=lambda id, name: self.manage_component.open(component_id=id, name=name),
                        on_select=lambda e, component=data: self.show_banner(component=component, is_deployed=True, is_disposed=False),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for data in self.deployed_data
            ] if self.deployed_data else [
                ft.Container(
                    content=ft.Text("No deployed components found.", color=ft.colors.GREY_600, size=16),
                    col={"xs": 12},
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center,
                )
            ]

            self.disposed_cards.controls = [
                ft.Container(
                    content=self.create_disposed_card(
                        data=data,
                        status_color=ft.colors.RED_ACCENT_400 if data[7] == "Scrap" else (ft.colors.YELLOW_ACCENT_400 if data[7] == "Sold" else ft.colors.GREY_400),
                        on_manage_click=lambda id, name: self.show_disposal_details(id, name),
                        on_select=lambda e, component=data: self.show_banner(component=component, is_deployed=False, is_disposed=True),
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},
                    padding=ft.padding.all(10),
                )
                for data in self.disposed_data
            ] if self.disposed_data else [
                ft.Container(
                    content=ft.Text("No disposed components found.", color=ft.colors.GREY_600, size=16),
                    col={"xs": 12},
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center,
                )
            ]

            self.page.update()

        except mysql.connector.Error as err:
            print(f"Error refreshing cards: {err}")