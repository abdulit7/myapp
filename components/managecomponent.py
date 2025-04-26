import flet as ft
from components.fields import CustomTextField
import mysql.connector
import asyncio
import datetime

class ManageComponentDialog:
    def __init__(self, page: ft.Page, parent):
        self.page = page
        self.parent = parent
        self.component_id = None
        self.component_name = ""
        self.initial_status = None  # To track the component's current status
        self.snackbar_container = None

        # Form Fields
        self.name_field = CustomTextField(label="Component Name", disabled=True)
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
            label="Select Target",
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
            hint_text="Enter location where component is kept",
            visible=False
        )
        # Sold Fields
        self.sold_to_field = CustomTextField(
            label="Sold To",
            hint_text="Enter person to whom component was sold",
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
            icon=ft.icons.SAVE,
            bgcolor=ft.colors.GREEN_400,
            color=ft.colors.WHITE,
            width=200,
            on_click=self.save_button_clicked
        )
        self.cancel_button = ft.ElevatedButton(
            "Cancel",
            icon=ft.icons.CANCEL,
            bgcolor=ft.colors.RED_400,
            width=200,
            color=ft.colors.WHITE,
            on_click=self.cancel,
        )

        # Form inside dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Manage Component"),
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
        try:
            conn = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM department ORDER BY name")
            options = [ft.dropdown.Option(row[0]) for row in cursor.fetchall()]
            self.department_dropdown.options = options if options else [ft.dropdown.Option("No departments available")]
            self.department_dropdown.value = None
            self.deploy_target.options = []
            self.deploy_target.value = None
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error fetching departments: {err}")
            self.department_dropdown.options = [ft.dropdown.Option("Error loading departments")]
        self.page.update()

    def fetch_users_by_department(self, department_name):
        try:
            conn = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT u.user_id 
                FROM users u 
                JOIN department d ON u.department_id = d.id 
                WHERE d.name = %s 
                ORDER BY u.user_id
                """,
                (department_name,)
            )
            options = [ft.dropdown.Option(row[0]) for row in cursor.fetchall()]
            self.deploy_target.options = options if options else [ft.dropdown.Option("No users in this department")]
            self.deploy_target.value = None
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error fetching users: {err}")
            self.deploy_target.options = [ft.dropdown.Option("Error loading users")]
        self.page.update()

    def fetch_deploy_targets(self):
        try:
            conn = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM department ORDER BY name")
            options = [ft.dropdown.Option(row[0]) for row in cursor.fetchall()]
            self.deploy_target.options = options if options else [ft.dropdown.Option("No departments available")]
            self.deploy_target.value = None
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error fetching departments: {err}")
            self.deploy_target.options = [ft.dropdown.Option("Error loading departments")]
        self.page.update()

    async def save_button_clicked(self, e):
        if not self.component_id:
            await self.show_snackbar("No component selected!", ft.colors.RED_400)
            return

        status = self.status.value
        if status == "Deployed":
            if not self.deploy_to.value:
                await self.show_snackbar("Please select Deploy To!", ft.colors.RED_400)
                return
            if self.deploy_to.value == "User" and not self.department_dropdown.value:
                await self.show_snackbar("Please select a Department!", ft.colors.RED_400)
                return
            if not self.deploy_target.value:
                await self.show_snackbar("Please select a User or Department!", ft.colors.RED_400)
                return
        elif status == "Scrap":
            if not self.scrap_amount_field.value:
                await self.show_snackbar("Please enter the amount earned from scrap!", ft.colors.RED_400)
                return
            try:
                float(self.scrap_amount_field.value)
            except ValueError:
                await self.show_snackbar("Amount earned must be a valid number!", ft.colors.RED_400)
                return
        elif status == "Dispose":
            if not self.dispose_reason_field.value:
                await self.show_snackbar("Please enter the reason for disposal!", ft.colors.RED_400)
                return
            if not self.dispose_location_field.value:
                await self.show_snackbar("Please enter the disposal location!", ft.colors.RED_400)
                return
        elif status == "Sold":
            if not self.sold_to_field.value:
                await self.show_snackbar("Please enter the person to whom the component was sold!", ft.colors.RED_400)
                return
            if not self.sale_details_field.value:
                await self.show_snackbar("Please enter the sale details!", ft.colors.RED_400)
                return
            if not self.sold_amount_field.value:
                await self.show_snackbar("Please enter the amount received from the sale!", ft.colors.RED_400)
                return
            try:
                float(self.sold_amount_field.value)
            except ValueError:
                await self.show_snackbar("Amount received must be a valid number!", ft.colors.RED_400)
                return

        try:
            conn = mysql.connector.connect(
                host="200.200.200.23",
                user="root",
                password="Pak@123",
                database="itasset",
                auth_plugin='mysql_native_password'
            )
            cursor = conn.cursor()

            # Determine the source table based on initial status
            source_table = "component" if self.initial_status == "Available" else "deployed_components"
            cursor.execute(
                """
                SELECT name, category, company, model, serial_no, purchaser, location, warranty,
                       category_id, price, status, purchase_date, image_path, model_no, min_qty,
                       total_qty, remaining_qty, location_id, purchase_cost
                FROM {} WHERE id = %s
                """.format(source_table),
                (self.component_id,)
            )
            component = cursor.fetchone()
            if not component:
                await self.show_snackbar("Component not found!", ft.colors.RED_400)
                conn.close()
                return

            if status == "Deployed":
                # Insert into deployed_components
                user_department = ""
                if self.deploy_to.value == "User":
                    cursor.execute(
                        "SELECT d.name FROM users u LEFT JOIN department d ON u.department_id = d.id WHERE u.user_id = %s",
                        (self.deploy_target.value,)
                    )
                    result = cursor.fetchone()
                    user_department = result[0] if result and result[0] else ""

                cursor.execute(
                    """
                    INSERT INTO deployed_components (
                        name, category, company, model, serial_no, purchaser, location, warranty,
                        category_id, price, status, purchase_date, image_path, model_no, min_qty,
                        total_qty, remaining_qty, location_id, purchase_cost, deployed_to,
                        user_department, deploy_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        component[0], component[1], component[2], component[3], component[4],
                        component[5], component[6], component[7], component[8], component[9],
                        "Deployed", component[11], component[12], component[13], component[14],
                        component[15], component[16], component[17], component[18],
                        self.deploy_target.value,
                        self.deploy_target.value if self.deploy_to.value == "Department" else user_department,
                        datetime.datetime.now().strftime("%Y-%m-%d")
                    )
                )
                # Delete from source table
                cursor.execute(f"DELETE FROM {source_table} WHERE id = %s", (self.component_id,))

            elif status in ["Scrap", "Dispose", "Sold"]:
                # Prepare data for disposed_components
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

                # Insert into disposed_components
                cursor.execute(
                    """
                    INSERT INTO disposed_components (
                        name, category, company, model, serial_no, purchaser, location, warranty,
                        category_id, price, purchase_date, image_path, model_no, min_qty,
                        total_qty, remaining_qty, location_id, purchase_cost, disposal_type,
                        disposal_date, amount_earned, disposal_reason, disposal_location,
                        sale_details, sold_to
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        component[0], component[1], component[2], component[3], component[4],
                        component[5], component[6], component[7], component[8], component[9],
                        component[11], component[12], component[13], component[14],
                        component[15], component[16], component[17], component[18],
                        disposal_type,
                        datetime.datetime.now().strftime("%Y-%m-%d"),
                        amount_earned,
                        disposal_reason,
                        disposal_location,
                        sale_details,
                        sold_to,
                    )
                )
                # Delete from source table
                cursor.execute(f"DELETE FROM {source_table} WHERE id = %s", (self.component_id,))

            else:  # Available
                if self.initial_status == "Deployed":
                    cursor.execute(
                        """
                        INSERT INTO component (
                            name, category, company, model, serial_no, purchaser, location, warranty,
                            category_id, price, status, purchase_date, image_path, model_no, min_qty,
                            total_qty, remaining_qty, location_id, purchase_cost
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            component[0], component[1], component[2], component[3], component[4],
                            component[5], component[6], component[7], component[8], component[9],
                            "Available", component[11], component[12], component[13], component[14],
                            component[15], component[16], component[17], component[18]
                        )
                    )
                    cursor.execute("DELETE FROM deployed_components WHERE id = %s", (self.component_id,))
                else:
                    cursor.execute("UPDATE component SET status = %s WHERE id = %s", ("Available", self.component_id))

            conn.commit()
            cursor.close()
            conn.close()

            # Refresh parent UI
            self.parent.refresh_cards()

            self.dialog.open = False
            self.page.update()
            await self.show_snackbar("Component updated successfully!", ft.colors.GREEN_400)

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            await self.show_snackbar(f"Database error: {err}", ft.colors.RED_400)
        except ValueError as ve:
            print(f"Value error: {ve}")
            await self.show_snackbar(f"Value error: {ve}", ft.colors.RED_400)

    async def show_snackbar(self, message, color):
        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)

        self.snackbar_container = ft.Container(
            content=ft.Text(message, color=ft.colors.WHITE),
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

    def open(self, component_id=None, name=""):
        self.component_id = component_id
        self.component_name = name
        self.name_field.value = name
        self.status.value = None
        self.initial_status = None
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

        # Determine the initial status
        if component_id:
            try:
                conn = mysql.connector.connect(
                    host="200.200.200.23",
                    user="root",
                    password="Pak@123",
                    database="itasset",
                    auth_plugin='mysql_native_password'
                )
                cursor = conn.cursor()
                # Check component table
                cursor.execute("SELECT status FROM component WHERE id = %s", (component_id,))
                result = cursor.fetchone()
                if result:
                    self.initial_status = result[0]
                else:
                    # Check deployed_components table
                    cursor.execute("SELECT status FROM deployed_components WHERE id = %s", (component_id,))
                    result = cursor.fetchone()
                    if result:
                        self.initial_status = result[0]
                cursor.close()
                conn.close()

                if self.initial_status:
                    self.status.value = self.initial_status
                    if self.initial_status == "Deployed":
                        self.deploy_options.visible = True
                        self.fetch_departments()
            except mysql.connector.Error as err:
                print(f"Error fetching component status: {err}")

        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)
            self.snackbar_container = None
        self.dialog.open = True
        self.page.update()