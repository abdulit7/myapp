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
        self.deploy_target = ft.Dropdown(
            label="Select User",
            options=[],
            expand=True
        )
        self.deploy_options.controls.extend([self.deploy_to, self.deploy_target])

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
        if e.control.value == "Deployed":
            self.deploy_options.visible = True
            self.fetch_deploy_targets()
        else:
            self.deploy_options.visible = False
        self.page.update()

    def deploy_to_changed(self, e):
        if e.control.value == "User":
            self.deploy_target.label = "Select User"
        elif e.control.value == "Department":
            self.deploy_target.label = "Select Department"
        self.fetch_deploy_targets()
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
            if self.deploy_to.value == "User":
                cursor.execute("SELECT user_id FROM users ORDER BY user_id")
                options = [ft.dropdown.Option(row[0]) for row in cursor.fetchall()]
            else:  # Department
                cursor.execute("SELECT name FROM department ORDER BY name")
                options = [ft.dropdown.Option(row[0]) for row in cursor.fetchall()]
            self.deploy_target.options = options if options else [ft.dropdown.Option("No options available")]
            self.deploy_target.value = None
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error fetching deploy targets: {err}")
            self.deploy_target.options = [ft.dropdown.Option("Error loading options")]
        self.page.update()

    async def save_button_clicked(self, e):
        if not self.component_id:
            await self.show_snackbar("No component selected!", ft.colors.RED_400)
            return

        status = self.status.value
        if status == "Deployed" and (not self.deploy_to.value or not self.deploy_target.value):
            await self.show_snackbar("Please select Deploy To and User/Department!", ft.colors.RED_400)
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

            if status == self.initial_status:
                # No status change, just close the dialog
                await self.show_snackbar("No changes made.", ft.colors.BLUE_400)
                self.dialog.open = False
                self.page.update()
                return

            if status == "Deployed":
                # Fetch component details from component table
                cursor.execute(
                    """
                    SELECT name, category, company, model, serial_no, purchaser, location, warranty,
                           category_id, price, status, purchase_date, image_path, model_no, min_qty,
                           total_qty, remaining_qty, location_id, purchase_cost
                    FROM component WHERE id = %s
                    """,
                    (self.component_id,)
                )
                component = cursor.fetchone()
                if not component:
                    await self.show_snackbar("Component not found!", ft.colors.RED_400)
                    conn.close()
                    return

                # Get user_department for users
                user_department = ""
                if self.deploy_to.value == "User":
                    cursor.execute(
                        "SELECT d.name FROM users u LEFT JOIN department d ON u.department_id = d.id WHERE u.user_id = %s",
                        (self.deploy_target.value,)
                    )
                    result = cursor.fetchone()
                    user_department = result[0] if result and result[0] else ""

                # Insert into deployed_components
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
                # Delete from component
                cursor.execute("DELETE FROM component WHERE id = %s", (self.component_id,))

            elif status == "Available":
                # Check if the component is currently deployed
                cursor.execute(
                    """
                    SELECT name, category, company, model, serial_no, purchaser, location, warranty,
                           category_id, price, status, purchase_date, image_path, model_no, min_qty,
                           total_qty, remaining_qty, location_id, purchase_cost
                    FROM deployed_components WHERE id = %s
                    """,
                    (self.component_id,)
                )
                component = cursor.fetchone()
                if component:
                    # Move back to component table
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
                    # Delete from deployed_components
                    cursor.execute("DELETE FROM deployed_components WHERE id = %s", (self.component_id,))
                else:
                    # If not in deployed_components, just update the status in component
                    cursor.execute("UPDATE component SET status = %s WHERE id = %s", (status, self.component_id))

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
        self.deploy_to.value = None
        self.deploy_target.options = []
        self.deploy_target.value = None

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
                        self.fetch_deploy_targets()
            except mysql.connector.Error as err:
                print(f"Error fetching component status: {err}")

        if self.snackbar_container:
            self.dialog.content.controls.remove(self.snackbar_container)
            self.snackbar_container = None
        self.dialog.open = True
        self.page.update()