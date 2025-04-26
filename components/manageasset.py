import flet as ft
from components.fields import CustomTextField
import mysql.connector
import asyncio
import datetime

class ManageAssetDialog:
    def __init__(self, page: ft.Page, parent):
        self.page = page
        self.parent = parent
        self.asset_id = None
        self.asset_name = ""
        self.snackbar_container = None

        # Cache category data to avoid repeated JOINs (for future use)
        self.category_map = {}
        self.fetch_categories()

        # Form Fields
        self.name_field = CustomTextField(label="Asset Name", disabled=True)
        self.status = ft.Dropdown(
            label="Status",
            options=[
                ft.dropdown.Option("Available"),
                ft.dropdown.Option("Deployed"),
                ft.dropdown.Option("Scrap"),
                ft.dropdown.Option("Dispose"),
                ft.dropdown.Option("Sold"),
            ],
            on_change=self.status_changed,
            expand=True,
        )

        # Deployment Fields
        self.deploy_options = ft.Column(visible=False, expand=True)
        self.deploy_to = ft.Dropdown(
            label="Deploy To",
            options=[
                ft.dropdown.Option("User"),
                ft.dropdown.Option("Department"),
            ],
            on_change=self.deploy_to_changed,
            expand=True
        )
        self.department_dropdown = ft.Dropdown(
            label="Select Department",
            options=[],
            on_change=self.department_changed,
            expand=True,
            visible=False
        )
        self.deploy_target = ft.Dropdown(
            label="Select User",
            options=[],
            expand=True
        )
        self.deploy_options.controls.extend([self.deploy_to, self.department_dropdown, self.deploy_target])

        # Disposal Fields (for Scrap, Dispose, and Sold)
        self.disposal_options = ft.Column(visible=False, expand=True)
        # Scrap Fields
        self.scrap_amount_field = CustomTextField(
            label="Amount Earned from Scrap",
            hint_text="Enter amount (e.g., 500.00)",
            visible=False
        )
        # Dispose Fields
        self.dispose_reason_field = CustomTextField(
            label="Reason for Disposal",
            hint_text="Enter reason for disposal",
            visible=False
        )
        self.dispose_location_field = CustomTextField(
            label="Disposal Location",
            hint_text="Enter location where asset is kept",
            visible=False
        )
        # Sold Fields
        self.sold_to_field = CustomTextField(
            label="Sold To",
            hint_text="Enter person to whom asset was sold",
            visible=False
        )
        self.sale_details_field = CustomTextField(
            label="Sale Details",
            hint_text="Enter details of the sale",
            visible=False
        )
        self.sold_amount_field = CustomTextField(
            label="Amount Received from Sale",
            hint_text="Enter amount (e.g., 1000.00)",
            visible=False
        )

        self.disposal_options.controls.extend([
            self.scrap_amount_field,
            self.dispose_reason_field,
            self.dispose_location_field,
            self.sold_to_field,
            self.sale_details_field,
            self.sold_amount_field,
        ])

        # Save and Cancel Buttons
        self.save_button = ft.ElevatedButton(
            "Save",
            icon=ft.Icons.SAVE,
            bgcolor=ft.Colors.GREEN_400,
            color=ft.Colors.WHITE,
            width=200,
            on_click=self.save_button_clicked
        )
        self.cancel_button = ft.ElevatedButton(
            "Cancel",
            icon=ft.Icons.CANCEL,
            bgcolor=ft.Colors.RED_400,
            width=200,
            color=ft.Colors.WHITE,
            on_click=self.cancel,
        )

        # Form inside dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Manage Asset"),
            content=ft.Column(
                controls=[
                    self.name_field,
                    self.status,
                    self.deploy_options,
                    self.disposal_options,
                    ft.Row(
                        controls=[self.save_button, self.cancel_button],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=20,
                    ),
                ],
                scroll="adaptive",
                tight=True,
            ),
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=self.on_dialog_dismiss,
        )
        page.overlay.append(self.dialog)
        page.update()

    def fetch_categories(self):
        """Fetch and cache category data."""
        connection = self._get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id, name FROM category")
                self.category_map = {row[0]: row[1] for row in cursor.fetchall()}
                print(f"Cached categories in ManageAssetDialog: {self.category_map}")
            except mysql.connector.Error as err:
                print(f"Error fetching categories: {err}")
                self.show_snackbar(f"Error fetching categories: {err}", ft.Colors.RED_400)
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("Database connection closed")

    def _get_db_connection(self):
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
            self.show_snackbar(f"Database error: {error}", ft.Colors.RED_400)
            return None

    def cancel(self, e):
        self.dialog.open = False
        self.page.update()

    def status_changed(self, e):
        # Reset visibility of all disposal fields
        self.scrap_amount_field.visible = False
        self.dispose_reason_field.visible = False
        self.dispose_location_field.visible = False
        self.sold_to_field.visible = False
        self.sale_details_field.visible = False
        self.sold_amount_field.visible = False
        self.disposal_options.visible = False

        if e.control.value == "Deployed":
            self.deploy_options.visible = True
            self.disposal_options.visible = False
            self.fetch_departments()
        elif e.control.value == "Scrap":
            self.deploy_options.visible = False
            self.disposal_options.visible = True
            self.scrap_amount_field.visible = True
            self.department_dropdown.visible = False
            self.deploy_target.options = []
            self.deploy_target.value = None
        elif e.control.value == "Dispose":
            self.deploy_options.visible = False
            self.disposal_options.visible = True
            self.dispose_reason_field.visible = True
            self.dispose_location_field.visible = True
            self.department_dropdown.visible = False
            self.deploy_target.options = []
            self.deploy_target.value = None
        elif e.control.value == "Sold":
            self.deploy_options.visible = False
            self.disposal_options.visible = True
            self.sold_to_field.visible = True
            self.sale_details_field.visible = True
            self.sold_amount_field.visible = True
            self.department_dropdown.visible = False
            self.deploy_target.options = []
            self.deploy_target.value = None
        else:
            self.deploy_options.visible = False
            self.disposal_options.visible = False
            self.department_dropdown.visible = False
            self.deploy_target.options = []
            self.deploy_target.value = None
        self.page.update()

    def deploy_to_changed(self, e):
        self.department_dropdown.value = None
        self.deploy_target.value = None
        if e.control.value == "User":
            self.department_dropdown.visible = True
            self.deploy_target.label = "Select User"
            self.fetch_departments()
        elif e.control.value == "Department":
            self.department_dropdown.visible = False
            self.deploy_target.label = "Select Department"
            self.fetch_deploy_targets()
        self.page.update()

    def department_changed(self, e):
        if self.deploy_to.value == "User" and e.control.value:
            self.fetch_users_by_department(e.control.value)
        self.page.update()

    def fetch_departments(self):
        connection = self._get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id, name FROM department ORDER BY name")
                options = [ft.dropdown.Option(key=row[0], text=row[1]) for row in cursor.fetchall()]
                self.department_dropdown.options = options if options else [ft.dropdown.Option("No departments available")]
                self.department_dropdown.value = None
                self.deploy_target.options = []
                self.deploy_target.value = None
            except mysql.connector.Error as err:
                print(f"Error fetching departments: {err}")
                self.department_dropdown.options = [ft.dropdown.Option("Error loading departments")]
                self.show_snackbar(f"Error fetching departments: {err}", ft.Colors.RED_400)
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("Database connection closed")
        self.page.update()

    def fetch_users_by_department(self, department_id):
        connection = self._get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    """
                    SELECT u.id, u.name, u.emp_id
                    FROM users u
                    JOIN department d ON u.department_id = d.id
                    WHERE d.id = %s
                    ORDER BY u.name
                    """,
                    (department_id,)
                )
                users = cursor.fetchall()
                options = [
                    ft.dropdown.Option(
                        key=row[0],  # User ID as the value
                        text=f"{row[1]} (Emp ID: {row[2]})"  # Display as "Name (Emp ID: XXX)"
                    ) for row in users
                ]
                self.deploy_target.options = options if options else [ft.dropdown.Option("No users in this department")]
                self.deploy_target.value = None
            except mysql.connector.Error as err:
                print(f"Error fetching users: {err}")
                self.deploy_target.options = [ft.dropdown.Option("Error loading users")]
                self.show_snackbar(f"Error fetching users: {err}", ft.Colors.RED_400)
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("Database connection closed")
        self.page.update()

    def fetch_deploy_targets(self):
        connection = self._get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id, name FROM department ORDER BY name")
                options = [ft.dropdown.Option(key=row[0], text=row[1]) for row in cursor.fetchall()]
                self.deploy_target.options = options if options else [ft.dropdown.Option("No departments available")]
                self.deploy_target.value = None
            except mysql.connector.Error as err:
                print(f"Error fetching departments: {err}")
                self.deploy_target.options = [ft.dropdown.Option("Error loading departments")]
                self.show_snackbar(f"Error fetching departments: {err}", ft.Colors.RED_400)
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("Database connection closed")
        self.page.update()

    async def save_button_clicked(self, e):
        if not self.asset_id:
            await self.show_snackbar("No asset selected!", ft.Colors.RED_400)
            return

        status = self.status.value
        if status == "Deployed":
            if not self.deploy_to.value:
                await self.show_snackbar("Please select Deploy To!", ft.Colors.RED_400)
                return
            if self.deploy_to.value == "User" and not self.department_dropdown.value:
                await self.show_snackbar("Please select a Department!", ft.Colors.RED_400)
                return
            if not self.deploy_target.value:
                await self.show_snackbar("Please select a User or Department!", ft.Colors.RED_400)
                return
        elif status == "Scrap":
            if not self.scrap_amount_field.value:
                await self.show_snackbar("Please enter the amount earned from scrap!", ft.Colors.RED_400)
                return
            try:
                float(self.scrap_amount_field.value)
            except ValueError:
                await self.show_snackbar("Amount earned must be a valid number!", ft.Colors.RED_400)
                return
        elif status == "Dispose":
            if not self.dispose_reason_field.value:
                await self.show_snackbar("Please enter the reason for disposal!", ft.Colors.RED_400)
                return
            if not self.dispose_location_field.value:
                await self.show_snackbar("Please enter the disposal location!", ft.Colors.RED_400)
                return
        elif status == "Sold":
            if not self.sold_to_field.value:
                await self.show_snackbar("Please enter the person to whom the asset was sold!", ft.Colors.RED_400)
                return
            if not self.sale_details_field.value:
                await self.show_snackbar("Please enter the sale details!", ft.Colors.RED_400)
                return
            if not self.sold_amount_field.value:
                await self.show_snackbar("Please enter the amount received from the sale!", ft.Colors.RED_400)
                return
            try:
                float(self.sold_amount_field.value)
            except ValueError:
                await self.show_snackbar("Amount received must be a valid number!", ft.Colors.RED_400)
                return

        connection = self._get_db_connection()
        if not connection:
            return

        try:
            cursor = connection.cursor()

            if status == "Deployed":
                # Fetch asset details
                cursor.execute(
                    """
                    SELECT name, category_id, company, model, serial_no, purchaser, location, price, warranty,
                           bill_copy, purchase_date, image_path
                    FROM assets WHERE id = %s
                    """,
                    (self.asset_id,)
                )
                asset = cursor.fetchone()
                if not asset:
                    await self.show_snackbar("Asset not found!", ft.Colors.RED_400)
                    return

                # Get user_department for users
                user_department = ""
                deployed_to_value = self.deploy_target.value
                if self.deploy_to.value == "User":
                    try:
                        cursor.execute(
                            """
                            SELECT d.name 
                            FROM users u 
                            LEFT JOIN department d ON u.department_id = d.id 
                            WHERE u.id = %s
                            """,
                            (self.deploy_target.value,)
                        )
                        result = cursor.fetchone()
                        user_department = result[0] if result and result[0] else ""
                    except mysql.connector.Error as err:
                        print(f"Error fetching user department for user {self.deploy_target.value}: {err}")
                        await self.show_snackbar(f"Error fetching user department: {err}", ft.Colors.RED_400)
                        return
                else:  # Department
                    try:
                        # Fetch the department name for user_department
                        cursor.execute(
                            "SELECT name FROM department WHERE id = %s",
                            (self.deploy_target.value,)
                        )
                        result = cursor.fetchone()
                        user_department = result[0] if result and result[0] else ""
                    except mysql.connector.Error as err:
                        print(f"Error fetching department name for department {self.deploy_target.value}: {err}")
                        await self.show_snackbar(f"Error fetching department name: {err}", ft.Colors.RED_400)
                        return

                # Insert into deployed_assets
                cursor.execute(
                    """
                    INSERT INTO deployed_assets (
                        name, category_id, company, model, serial_no, purchaser, location, price, warranty,
                        bill_copy, purchase_date, image_path, deployed_to, user_department, deploy_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        asset[0],  # name
                        asset[1],  # category_id
                        asset[2],  # company
                        asset[3],  # model
                        asset[4],  # serial_no
                        asset[5],  # purchaser
                        asset[6],  # location
                        asset[7],  # price
                        asset[8],  # warranty
                        asset[9],  # bill_copy
                        asset[10],  # purchase_date
                        asset[11],  # image_path
                        deployed_to_value,
                        user_department,
                        datetime.datetime.now().strftime("%Y-%m-%d")
                    )
                )
                # Delete from assets
                cursor.execute("DELETE FROM assets WHERE id = %s", (self.asset_id,))

            elif status in ["Scrap", "Dispose", "Sold"]:
                # Fetch asset details
                cursor.execute(
                    """
                    SELECT name, category_id, company, model, serial_no, purchaser, location, price, warranty,
                           bill_copy, purchase_date, image_path
                    FROM assets WHERE id = %s
                    """,
                    (self.asset_id,)
                )
                asset = cursor.fetchone()
                if not asset:
                    await self.show_snackbar("Asset not found!", ft.Colors.RED_400)
                    return

                # Prepare data for disposed_assets
                disposal_type = status
                amount_earned = None
                disposal_reason = None
                disposal_location = None
                sold_to = None
                sale_details = None

                if status == "Scrap":
                    amount_earned = float(self.scrap_amount_field.value)
                elif status == "Dispose":
                    disposal_reason = self.dispose_reason_field.value
                    disposal_location = self.dispose_location_field.value
                elif status == "Sold":
                    sold_to = self.sold_to_field.value
                    sale_details = self.sale_details_field.value
                    amount_earned = float(self.sold_amount_field.value)

                # Insert into disposed_assets
                cursor.execute(
                    """
                    INSERT INTO disposed_assets (
                        name, category_id, company, model, serial_no, purchaser, location, price, warranty,
                        bill_copy, purchase_date, image_path, disposal_type, disposal_date, amount_earned,
                        disposal_reason, disposal_location, sale_details, sold_to
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        asset[0],  # name
                        asset[1],  # category_id
                        asset[2],  # company
                        asset[3],  # model
                        asset[4],  # serial_no
                        asset[5],  # purchaser
                        asset[6],  # location
                        asset[7],  # price
                        asset[8],  # warranty
                        asset[9],  # bill_copy
                        asset[10],  # purchase_date
                        asset[11],  # image_path
                        disposal_type,
                        datetime.datetime.now().strftime("%Y-%m-%d"),
                        amount_earned,
                        disposal_reason,
                        disposal_location,
                        sale_details,
                        sold_to,
                    )
                )
                # Delete from assets
                cursor.execute("DELETE FROM assets WHERE id = %s", (self.asset_id,))

            else:  # Available
                cursor.execute("UPDATE assets SET status = %s WHERE id = %s", (status, self.asset_id))

            connection.commit()

            # Refresh parent UI
            self.parent.refresh_cards()

            self.dialog.open = False
            self.page.update()
            await self.show_snackbar("Asset updated successfully!", ft.Colors.GREEN_400)

        except mysql.connector.Error as err:
            print(f"Database error in save_button_clicked: {err}")
            await self.show_snackbar(f"Database error: {err}", ft.Colors.RED_400)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Database connection closed")

    async def show_snackbar(self, message, color):
        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)

        self.snackbar_container = ft.Container(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color,
            padding=10,
            border_radius=5,
            margin=ft.margin.only(top=10),
        )
        self.dialog.content.controls.append(self.snackbar_container)
        self.page.update()
        await asyncio.sleep(3)
        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)
            self.snackbar_container = None
            self.page.update()

    def on_dialog_dismiss(self, e):
        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)
            self.snackbar_container = None
        print("Dialog dismissed!")
        self.page.update()

    def open(self, asset_id=None, name=""):
        self.asset_id = asset_id
        self.asset_name = name
        self.name_field.value = name
        self.status.value = None
        self.deploy_options.visible = False
        self.disposal_options.visible = False
        self.deploy_to.value = None
        self.department_dropdown.options = []
        self.department_dropdown.value = None
        self.department_dropdown.visible = False
        self.deploy_target.options = []
        self.deploy_target.value = None
        self.scrap_amount_field.value = ""
        self.dispose_reason_field.value = ""
        self.dispose_location_field.value = ""
        self.sold_to_field.value = ""
        self.sale_details_field.value = ""
        self.sold_amount_field.value = ""
        self.scrap_amount_field.visible = False
        self.dispose_reason_field.visible = False
        self.dispose_location_field.visible = False
        self.sold_to_field.visible = False
        self.sale_details_field.visible = False
        self.sold_amount_field.visible = False
        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)
            self.snackbar_container = None
        self.dialog.open = True
        self.page.update()