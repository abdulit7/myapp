import flet as ft  # Import the Flet library for building the user interface
import mysql.connector  # Import the MySQL connector to interact with the database
from components.managecomponent import ManageComponentDialog  # Import the dialog for managing components
# from components.componentdialog import ComponentDialog  # Commented-out import for ComponentDialog (not used)
import os.path  # Import os.path to handle file extensions for images

class ComponentPage(ft.Container):  # Define a class for the components page, inheriting from Flet Container
    def __init__(self, page: ft.Page):  # Initialize the ComponentPage with a Flet page object
        super().__init__()  # Call the parent class (Container) initializer
        self.page = page  # Store the Flet page object for use in the class
        self.expand = True  # Make the container expand to fill available space

        page.window.title = "Asset Management System - Components"  # Set the window title for the page
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Center content horizontally
        page.vertical_alignment = ft.MainAxisAlignment.START  # Align content to the top vertically

        # Supported image extensions
        self.supported_image_extensions = {".jpg", ".jpeg", ".png", ".gif"}  # Define supported image formats

        # Fetch and cache category data to avoid repeated JOINs
        self.category_map = {}  # Initialize an empty dictionary to store category IDs and names
        connection = self._get_db_connection()  # Get a database connection
        if connection:  # Check if the connection was successful
            try:  # Start a try block to handle potential database errors
                cursor = connection.cursor()  # Create a cursor to execute database queries
                cursor.execute("SELECT id, name FROM category WHERE type = 'Component'")  # Query categories for components
                self.category_map = {row[0]: row[1] for row in cursor.fetchall()}  # Store categories in a dictionary
                print(f"Cached categories: {self.category_map}")  # Print the cached categories for debugging
            except mysql.connector.Error as err:  # Catch any database errors
                print(f"Error fetching categories: {err}")  # Print the error message
                self.page.open(ft.SnackBar(ft.Text(f"Error fetching categories: {err}"), duration=4000))  # Show error message
            finally:  # Ensure resources are cleaned up
                if connection.is_connected():  # Check if the connection is still open
                    cursor.close()  # Close the database cursor
                    connection.close()  # Close the database connection
                    print("Database connection closed")  # Print confirmation of connection closure

        # Initialize dialogs
        # self.component_dialog = ComponentDialog(page)  # Commented-out initialization of ComponentDialog (not used)
        self.manage_component = ManageComponentDialog(page, self)  # Initialize the manage component dialog

        # Component Detail Banner
        def close_banner(e):  # Define a function to close the banner
            page.close(self.banner)  # Close the banner on the page

        action_button_style = ft.ButtonStyle(color=ft.Colors.BLUE)  # Define a button style with blue color

        # Placeholder banner content (will be updated dynamically)
        banner_content = ft.Row(  # Create a row to hold banner content
            controls=[  # Define the controls in the row
                ft.Column(  # Create a column for text details
                    controls=[  # Define the controls in the column
                        ft.Text(  # Create a text widget for the banner title
                            "Component Details:",  # Set the text content
                            color=ft.Colors.BLACK,  # Set text color to black
                            weight=ft.FontWeight.BOLD,  # Make text bold
                            size=20  # Set text size
                        )
                    ],
                    expand=True,  # Make the column expand to fill space
                ),
                ft.Container(  # Create a container for the banner image
                    content=ft.Image(  # Create an image widget
                        src="/images/placeholder.jpg",  # Set the default image path
                        width=150,  # Set image width
                        height=150,  # Set image height
                        fit=ft.ImageFit.CONTAIN,  # Ensure image fits within bounds
                        error_content=ft.Text("Banner image not found"),  # Show error text if image fails
                    ),
                    alignment=ft.alignment.center,  # Center the image
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Space out the column and image
        )

        self.banner = ft.Banner(  # Create a banner widget
            bgcolor=ft.Colors.WHITE70,  # Set background color with transparency
            leading=ft.Icon(  # Add a leading icon
                ft.Icons.WARNING_AMBER_ROUNDED,  # Use a warning icon
                color=ft.Colors.AMBER,  # Set icon color to amber
                size=40  # Set icon size
            ),
            content=banner_content,  # Set the banner content
            actions=[  # Define action buttons
                ft.ElevatedButton(  # Create a "View" button
                    text="View",  # Set button text
                    icon=ft.Icons.ACCESS_ALARM,  # Add an icon
                    width=100,  # Set button width
                    style=action_button_style,  # Apply the button style
                    on_click=close_banner  # Call close_banner when clicked
                ),
                ft.TextButton(  # Create an "Ignore" button
                    text="Ignore",  # Set button text
                    style=action_button_style,  # Apply the button style
                    on_click=close_banner  # Call close_banner when clicked
                ),
                ft.TextButton(  # Create a "Cancel" button
                    text="Cancel",  # Set button text
                    style=action_button_style,  # Apply the button style
                    on_click=close_banner  # Call close_banner when clicked
                ),
            ],
        )

        self.add_component_button = ft.ElevatedButton(  # Create a button to add a new component
            icon=ft.Icons.ADD,  # Add a plus icon
            text="Add Component",  # Set button text
            on_click=lambda e: page.go('/componentform'),  # Navigate to component form when clicked
            style=ft.ButtonStyle(  # Define button styling
                bgcolor=ft.Colors.GREEN_500,  # Set green background
                color=ft.Colors.WHITE,  # Set white text
                padding=ft.Padding(16, 12, 16, 12),  # Set padding
                shape=ft.RoundedRectangleBorder(radius=12),  # Round button corners
                overlay_color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),  # Set overlay color
                elevation=6,  # Set button elevation
            ),
            width=180,  # Set button width
            height=55,  # Set button height
        )

        # Category dropdown
        self.category_dropdown = ft.Dropdown(  # Create a dropdown for selecting categories
            label="Select Category",  # Set the dropdown label
            options=[  # Define dropdown options
                ft.dropdown.Option(key=str(id), text=name)  # Create an option for each category
                for id, name in self.category_map.items()  # Iterate over cached categories
            ] + [ft.dropdown.Option(key="all", text="All Categories")],  # Add "All Categories" option
            value="all",  # Set default value to "all"
            width=200,  # Set dropdown width
        )

        # Filter button
        self.filter_button = ft.ElevatedButton(  # Create a button to filter components
            text="Filter",  # Set button text
            icon=ft.Icons.FILTER_LIST,  # Add a filter icon
            on_click=self.filter_components,  # Call filter_components when clicked
            style=ft.ButtonStyle(  # Define button styling
                bgcolor=ft.Colors.BLUE_500,  # Set blue background
                color=ft.Colors.WHITE,  # Set white text
                padding=ft.Padding(16, 12, 16, 12),  # Set padding
                shape=ft.RoundedRectangleBorder(radius=12),  # Round button corners
                elevation=6,  # Set button elevation
            ),
            width=120,  # Set button width
            height=55,  # Set button height
        )

        # Fetch component data
        self.component_data = self._fetch_components()  # Fetch available components
        self.deployed_data = self._fetch_deployed_components()  # Fetch deployed components
        self.disposed_data = self._fetch_disposed_components()  # Fetch disposed components

        # Fallback UI for empty tabs
        no_components_message = ft.Container(  # Create a container for empty tab message
            content=ft.Text(  # Create a text widget
                "No Components Found",  # Set the text content
                size=20,  # Set text size
                color=ft.Colors.RED_700,  # Set text color to red
                weight=ft.FontWeight.BOLD,  # Make text bold
                text_align=ft.TextAlign.CENTER,  # Center the text
            ),
            alignment=ft.alignment.center,  # Center the content
            padding=ft.padding.all(50),  # Add padding around the content
        )

        # Define on_manage_click lambda for clarity
        manage_click_handler = lambda id, name: self.manage_component.open(component_id=id, name=name)  # Define handler for manage button

        self.deployable_cards = ft.ResponsiveRow(  # Create a row for available component cards
            controls=[  # Define the cards
                ft.Container(  # Create a container for each card
                    content=self.create_component_card(  # Create a card for the component
                        data=x,  # Pass component data
                        status_color=ft.Colors.LIGHT_GREEN_ACCENT_400,  # Set status color to green
                        on_manage_click=manage_click_handler,  # Set manage button handler
                        on_select=lambda e, component=x: self.show_banner(component=component, is_deployed=False),  # Set click handler
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},  # Set responsive column sizes
                    padding=ft.padding.all(10),  # Add padding around the card
                )
                for x in self.component_data  # Iterate over available components
            ],
            alignment=ft.MainAxisAlignment.START,  # Align cards to the start
            spacing=0,  # Set spacing between cards
            run_spacing=0,  # Set spacing between rows
        )

        self.deployed_cards = ft.ResponsiveRow(  # Create a row for deployed component cards
            controls=[  # Define the cards
                ft.Container(  # Create a container for each card
                    content=self.create_deployed_card(  # Create a card for the component
                        data=data,  # Pass component data
                        status_color=ft.Colors.LIGHT_BLUE_ACCENT_700,  # Set status color to blue
                        on_manage_click=manage_click_handler,  # Set manage button handler
                        on_select=lambda e, component=data: self.show_banner(component=component, is_deployed=True),  # Set click handler
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},  # Set responsive column sizes
                    padding=ft.padding.all(10),  # Add padding around the card
                )
                for data in self.deployed_data  # Iterate over deployed components
            ],
            alignment=ft.MainAxisAlignment.START,  # Align cards to the start
            spacing=0,  # Set spacing between cards
            run_spacing=0,  # Set spacing between rows
        )

        self.disposed_cards = ft.ResponsiveRow(  # Create a row for disposed component cards
            controls=[  # Define the cards
                ft.Container(  # Create a container for each card
                    content=self.create_disposed_card(  # Create a card for the component
                        data=data,  # Pass component data
                        status_color=ft.Colors.RED_ACCENT_400 if data[7] == "Scrap" else (ft.Colors.YELLOW_ACCENT_400 if data[7] == "Sold" else ft.Colors.GREY_400),  # Set status color
                        on_manage_click=lambda e: self.show_manage_component_bottomsheet(),  # Set manage button handler
                        on_select=lambda e, component=data: self.show_banner(component=component, is_disposed=True),  # Set click handler
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},  # Set responsive column sizes
                    padding=ft.padding.all(10),  # Add padding around the card
                )
                for data in self.disposed_data  # Iterate over disposed components
            ],
            alignment=ft.MainAxisAlignment.START,  # Align cards to the start
            spacing=0,  # Set spacing between cards
            run_spacing=0,  # Set spacing between rows
        )

        self.tabs = ft.Tabs(  # Create tabs for organizing components
            selected_index=0,  # Set the default selected tab to the first one
            animation_duration=300,  # Set animation duration for tab switching
            tabs=[  # Define the tabs
                ft.Tab(  # Create the "Available" tab
                    text="Available",  # Set tab text
                    content=ft.Column(  # Create a column for tab content
                        controls=[self.deployable_cards if self.component_data else no_components_message],  # Show cards or empty message
                        scroll=ft.ScrollMode.AUTO,  # Enable scrolling
                        expand=True,  # Make column expand to fill space
                    )
                ),
                ft.Tab(  # Create the "Assigned" tab
                    text="Assigned",  # Set tab text
                    content=ft.Column(  # Create a column for tab content
                        controls=[self.deployed_cards if self.deployed_data else no_components_message],  # Show cards or empty message
                        scroll=ft.ScrollMode.AUTO,  # Enable scrolling
                        expand=True,  # Make column expand to fill space
                    )
                ),
                ft.Tab(  # Create the "Disposed/Sold" tab
                    text="Disposed/Sold",  # Set tab text
                    content=ft.Column(  # Create a column for tab content
                        controls=[self.disposed_cards if self.disposed_data else no_components_message],  # Show cards or empty message
                        scroll=ft.ScrollMode.AUTO,  # Enable scrolling
                        expand=True,  # Make column expand to fill space
                    )
                ),
            ],
            expand=True,  # Make tabs expand to fill space
        )

        self.content = ft.Column(  # Create a column for the main page content
            controls=[  # Define the controls in the column
                ft.Divider(height=1, color=ft.Colors.WHITE),  # Add a divider line
                ft.Row(  # Create a row for buttons and dropdown
                    controls=[  # Define the controls in the row
                        self.add_component_button,  # Add the "Add Component" button
                        self.category_dropdown,  # Add the category dropdown
                        self.filter_button,  # Add the filter button
                    ],
                    alignment=ft.MainAxisAlignment.START,  # Align controls to the start
                    spacing=10,  # Set spacing between controls
                ),
                self.tabs,  # Add the tabs
            ],
            expand=True,  # Make column expand to fill space
            spacing=10,  # Set spacing between controls
        )

        page.update()  # Update the page to display the UI

    def _get_db_connection(self):  # Define a method to connect to the database
        """Establish and return a database connection."""
        try:  # Start a try block to handle connection errors
            connection = mysql.connector.connect(  # Create a database connection
                host="200.200.200.23",  # Set the database host
                user="root",  # Set the database user
                password="Pak@123",  # Set the database password
                database="itasset",  # Set the database name
                auth_plugin='mysql_native_password'  # Set the authentication plugin
            )
            print("Database connection successful")  # Print success message
            return connection  # Return the connection object
        except mysql.connector.Error as error:  # Catch any connection errors
            print(f"Database connection failed: {error}")  # Print the error message
            self.page.open(ft.SnackBar(ft.Text(f"Database error: {error}"), duration=4000))  # Show error message
            return None  # Return None if connection fails

    def _fetch_components(self, category_id=None):  # Define a method to fetch available components
        """Fetch available components from the database, optionally filtered by category."""
        connection = self._get_db_connection()  # Get a database connection
        if not connection:  # Check if connection failed
            return []  # Return an empty list if no connection

        try:  # Start a try block to handle database errors
            cursor = connection.cursor()  # Create a cursor for queries
            query = """  # Define the SQL query
                SELECT id, name, category_id, company, model, status, image_path
                FROM component
            """
            params = []  # Initialize an empty list for query parameters
            if category_id and category_id != "all":  # Check if filtering by category
                query += " WHERE category_id = %s"  # Add WHERE clause to query
                params.append(int(category_id))  # Add category ID to parameters

            cursor.execute(query, params)  # Execute the query with parameters
            component_data_raw = cursor.fetchall()  # Fetch all query results
            # Map category_id to category name using the cached category_map
            component_data = [  # Create a list of component data
                (row[0], row[1], self.category_map.get(row[2], "Unknown"), row[3], row[4], row[5], row[6])  # Map category ID to name
                for row in component_data_raw  # Iterate over raw data
            ]
            print(f"Query returned {len(component_data)} rows from component: {component_data}")  # Print query results
            return component_data  # Return the component data
        except mysql.connector.Error as err:  # Catch any database errors
            print(f"Query failed for component: {err}")  # Print the error message
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching components: {err}"), duration=4000))  # Show error message
            return []  # Return an empty list on error
        finally:  # Ensure resources are cleaned up
            if connection.is_connected():  # Check if connection is still open
                cursor.close()  # Close the cursor
                connection.close()  # Close the connection
                print("Database connection closed")  # Print confirmation

    def _fetch_deployed_components(self, category_id=None):  # Define a method to fetch deployed components
        """Fetch deployed components from the database, optionally filtered by category."""
        connection = self._get_db_connection()  # Get a database connection
        if not connection:  # Check if connection failed
            return []  # Return an empty list if no connection

        try:  # Start a try block to handle database errors
            cursor = connection.cursor()  # Create a cursor for queries
            query = """  # Define the SQL query
                SELECT dc.id, dc.name, dc.category_id, dc.company, dc.model, 
                    u.name AS deployed_to_name, u.emp_id AS deployed_to_emp_id, 
                    dc.user_department, dc.deploy_date, dc.image_path
                FROM deployed_components dc
                LEFT JOIN users u ON dc.deployed_to = u.id
            """
            params = []  # Initialize an empty list for query parameters
            if category_id and category_id != "all":  # Check if filtering by category
                query += " WHERE dc.category_id = %s"  # Add WHERE clause to query
                params.append(int(category_id))  # Add category ID to parameters

            cursor.execute(query, params)  # Execute the query with parameters
            deployed_data_raw = cursor.fetchall()  # Fetch all query results
            # Map category_id to category name using the cached category_map
            deployed_data = [  # Create a list of deployed component data
                (  # Create a tuple for each component
                    row[0],  # Component ID
                    row[1],  # Component Name
                    self.category_map.get(row[2], "Unknown"),  # Category Name
                    row[3],  # Company
                    row[4],  # Model
                    f"{row[5]} (Emp ID: {row[6]})" if row[5] and row[6] else "Not Assigned",  # Deployed To
                    row[7],  # User Department
                    row[8],  # Deploy Date
                    row[9],  # Image Path
                )
                for row in deployed_data_raw  # Iterate over raw data
            ]
            print(f"Query returned {len(deployed_data)} rows from deployed_components: {deployed_data}")  # Print query results
            return deployed_data  # Return the deployed component data
        except mysql.connector.Error as err:  # Catch any database errors
            print(f"Query failed for deployed_components: {err}")  # Print the error message
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching deployed components: {err}"), duration=4000))  # Show error message
            return []  # Return an empty list on error
        finally:  # Ensure resources are cleaned up
            if connection.is_connected():  # Check if connection is still open
                cursor.close()  # Close the cursor
                connection.close()  # Close the connection
                print("Database connection closed")  # Print confirmation

    def _fetch_disposed_components(self, category_id=None):  # Define a method to fetch disposed components
        """Fetch disposed components from the database, optionally filtered by category."""
        connection = self._get_db_connection()  # Get a database connection
        if not connection:  # Check if connection failed
            return []  # Return an empty list if no connection

        try:  # Start a try block to handle database errors
            cursor = connection.cursor()  # Create a cursor for queries
            query = """  # Define the SQL query
                SELECT id, name, category_id, company, model, purchase_date, disposal_date, disposal_type,
                       amount_earned, disposal_reason, disposal_location, sale_details, sold_to, image_path
                FROM disposed_components
            """
            params = []  # Initialize an empty list for query parameters
            if category_id and category_id != "all":  # Check if filtering by category
                query += " WHERE category_id = %s"  # Add WHERE clause to query
                params.append(int(category_id))  # Add category ID to parameters

            cursor.execute(query, params)  # Execute the query with parameters
            disposed_data_raw = cursor.fetchall()  # Fetch all query results
            # Map category_id to category name using the cached category_map
            disposed_data = [  # Create a list of disposed component data
                (row[0], row[1], self.category_map.get(row[2], "Unknown"), row[3], row[4], row[5], row[6], row[7],  # Map category ID to name
                 row[8], row[9], row[10], row[11], row[12], row[13])  # Include all fields
                for row in disposed_data_raw  # Iterate over raw data
            ]
            print(f"Query returned {len(disposed_data)} rows from disposed_components: {disposed_data}")  # Print query results
            return disposed_data  # Return the disposed component data
        except mysql.connector.Error as err:  # Catch any database errors
            print(f"Query failed for disposed_components: {err}")  # Print the error message
            self.page.open(ft.SnackBar(ft.Text(f"Error fetching disposed components: {err}"), duration=4000))  # Show error message
            return []  # Return an empty list on error
        finally:  # Ensure resources are cleaned up
            if connection.is_connected():  # Check if connection is still open
                cursor.close()  # Close the cursor
                connection.close()  # Close the connection
                print("Database connection closed")  # Print confirmation

    def _is_supported_image_format(self, image_path: str) -> bool:  # Define a method to check image format
        """Check if the image path has a supported extension (jpg, jpeg, png, gif)."""
        if not image_path:  # Check if image path is empty
            return False  # Return False if no path
        _, ext = os.path.splitext(image_path.lower())  # Get the file extension in lowercase
        return ext in self.supported_image_extensions  # Return True if extension is supported

    def show_banner(self, component=None, is_deployed=False, is_disposed=False):  # Define a method to show component details
        """Display component details in a banner."""
        if component:  # Check if a component is provided
            connection = self._get_db_connection()  # Get a database connection
            if not connection:  # Check if connection failed
                return  # Exit if no connection

            try:  # Start a try block to handle database errors
                cursor = connection.cursor()  # Create a cursor for queries
                if is_deployed:  # Check if the component is deployed
                    cursor.execute(  # Execute a query for deployed components
                        """
                        SELECT name, category_id, company, model, serial_no, purchaser, location, price, warranty,
                               bill_copy, purchase_date, image_path, deployed_to, user_department, deploy_date
                        FROM deployed_components WHERE id = %s
                        """,
                        (component[0],)  # Pass the component ID
                    )
                    component_data = cursor.fetchone()  # Fetch the query result
                    if component_data:  # Check if data was found
                        component_details = {  # Create a dictionary of component details
                            "Name": str(component_data[0]) if component_data[0] is not None else "",  # Set name
                            "Category": self.category_map.get(component_data[1], "Unknown"),  # Set category
                            "Company": str(component_data[2]) if component_data[2] is not None else "",  # Set company
                            "Model": str(component_data[3]) if component_data[3] is not None else "",  # Set model
                            "Serial No": str(component_data[4]) if component_data[4] is not None else "",  # Set serial number
                            "Purchaser": str(component_data[5]) if component_data[5] is not None else "",  # Set purchaser
                            "Location": str(component_data[6]) if component_data[6] is not None else "",  # Set location
                            "Price": f"${component_data[7]}" if component_data[7] is not None else "",  # Set price
                            "Warranty": str(component_data[8]) if component_data[8] is not None else "",  # Set warranty
                            "Status": "Deployed",  # Set status
                            "Deployed To": str(component_data[12]) if component_data[12] is not None else "",  # Set deployed to
                            "Department": str(component_data[13]) if component_data[13] is not None else "",  # Set department
                            "Deploy Date": str(component_data[14]) if component_data[14] is not None else "",  # Set deploy date
                        }
                        image_path = str(component_data[11]) if component_data[11] is not None else None  # Set image path
                    else:  # If no data was found
                        component_details = {"Name": "Component not found"}  # Set error message
                        image_path = None  # Set image path to None
                elif is_disposed:  # Check if the component is disposed
                    cursor.execute(  # Execute a query for disposed components
                        """
                        SELECT name, category_id, company, model, serial_no, purchaser, location, price, warranty,
                               bill_copy, purchase_date, image_path, disposal_type, disposal_date, amount_earned,
                               disposal_reason, disposal_location, sale_details, sold_to
                        FROM disposed_components WHERE id = %s
                        """,
                        (component[0],)  # Pass the component ID
                    )
                    component_data = cursor.fetchone()  # Fetch the query result
                    if component_data:  # Check if data was found
                        component_details = {  # Create a dictionary of component details
                            "Name": str(component_data[0]) if component_data[0] is not None else "",  # Set name
                            "Category": self.category_map.get(component_data[1], "Unknown"),  # Set category
                            "Company": str(component_data[2]) if component_data[2] is not None else "",  # Set company
                            "Model": str(component_data[3]) if component_data[3] is not None else "",  # Set model
                            "Serial No": str(component_data[4]) if component_data[4] is not None else "",  # Set serial number
                            "Purchaser": str(component_data[5]) if component_data[5] is not None else "",  # Set purchaser
                            "Location": str(component_data[6]) if component_data[6] is not None else "",  # Set location
                            "Price": f"${component_data[7]}" if component_data[7] is not None else "",  # Set price
                            "Warranty": str(component_data[8]) if component_data[8] is not None else "",  # Set warranty
                            "Purchase Date": str(component_data[10]) if component_data[10] is not None else "",  # Set purchase date
                            "Disposal Type": str(component_data[12]) if component_data[12] is not None else "",  # Set disposal type
                            "Disposal Date": str(component_data[13]) if component_data[13] is not None else "",  # Set disposal date
                        }
                        if component_data[14] is not None:  # Check if amount earned exists
                            component_details["Amount Earned"] = f"${component_data[14]}"  # Set amount earned
                        if component_data[15]:  # Check if disposal reason exists
                            component_details["Disposal Reason"] = str(component_data[15])  # Set disposal reason
                        if component_data[16]:  # Check if disposal location exists
                            component_details["Disposal Location"] = str(component_data[16])  # Set disposal location
                        if component_data[17]:  # Check if sale details exist
                            component_details["Sale Details"] = str(component_data[17])  # Set sale details
                        if component_data[18]:  # Check if sold to exists
                            component_details["Sold To"] = str(component_data[18])  # Set sold to
                        image_path = str(component_data[11]) if component_data[11] is not None else None  # Set image path
                    else:  # If no data was found
                        component_details = {"Name": "Component not found"}  # Set error message
                        image_path = None  # Set image path to None
                else:  # If the component is available
                    cursor.execute(  # Execute a query for available components
                        """
                        SELECT name, category_id, company, model, serial_no, purchaser, location, price, warranty,
                               bill_copy, purchase_date, image_path, status
                        FROM component WHERE id = %s
                        """,
                        (component[0],)  # Pass the component ID
                    )
                    component_data = cursor.fetchone()  # Fetch the query result
                    if component_data:  # Check if data was found
                        component_details = {  # Create a dictionary of component details
                            "Name": str(component_data[0]) if component_data[0] is not None else "",  # Set name
                            "Category": self.category_map.get(component_data[1], "Unknown"),  # Set category
                            "Company": str(component_data[2]) if component_data[2] is not None else "",  # Set company
                            "Model": str(component_data[3]) if component_data[3] is not None else "",  # Set model
                            "Serial No": str(component_data[4]) if component_data[4] is not None else "",  # Set serial number
                            "Purchaser": str(component_data[5]) if component_data[5] is not None else "",  # Set purchaser
                            "Location": str(component_data[6]) if component_data[6] is not None else "",  # Set location
                            "Price": f"${component_data[7]}" if component_data[7] is not None else "",  # Set price
                            "Warranty": str(component_data[8]) if component_data[8] is not None else "",  # Set warranty
                            "Purchase Date": str(component_data[10]) if component_data[10] is not None else "",  # Set purchase date
                            "Status": str(component_data[12]) if component_data[12] is not None else "",  # Set status
                        }
                        image_path = str(component_data[11]) if component_data[11] is not None else None  # Set image path
                    else:  # If no data was found
                        component_details = {"Name": "Component not found"}  # Set error message
                        image_path = None  # Set image path to None

            except mysql.connector.Error as err:  # Catch any database errors
                print(f"Error fetching component details: {err}")  # Print the error message
                component_details = {"Name": "Error loading component details"}  # Set error message
                image_path = None  # Set image path to None
                self.page.open(ft.SnackBar(ft.Text(f"Error fetching component details: {err}"), duration=4000))  # Show error message
            finally:  # Ensure resources are cleaned up
                if connection.is_connected():  # Check if connection is still open
                    cursor.close()  # Close the cursor
                    connection.close()  # Close the connection
                    print("Database connection closed")  # Print confirmation

            # Create component detail rows for the banner
            component_detail_rows = [  # Create a list of rows for details
                ft.Row(controls=[ft.Text(f"{key}: ", weight=ft.FontWeight.BOLD), ft.Text(value)])  # Create a row for each detail
                for key, value in component_details.items() if value  # Include only non-empty values
            ]

            # Validate and update the banner's image
            if image_path and image_path.startswith("/images/") and self._is_supported_image_format(image_path):  # Check if image is valid
                image_content = ft.Image(  # Create an image widget
                    src=image_path,  # Set the image path
                    width=600,  # Set image width
                    height=500,  # Set image height
                    fit=ft.ImageFit.CONTAIN,  # Ensure image fits within bounds
                    error_content=ft.Text("Failed to load image"),  # Show error text if image fails
                )
            else:  # If image is invalid
                image_content = ft.Image(  # Create a placeholder image
                    src="/images/placeholder.jpg",  # Set placeholder image path
                    width=600,  # Set image width
                    height=500,  # Set image height
                    fit=ft.ImageFit.CONTAIN,  # Ensure image fits within bounds
                    error_content=ft.Text("Placeholder image not found"),  # Show error text if image fails
                )
                if image_path:  # If an invalid image path was provided
                    print(f"Unsupported or invalid image format for banner: {image_path}")  # Print error message
                    self.page.open(ft.SnackBar(  # Show error message
                        ft.Text(f"Unsupported image format in banner: {image_path}. Supported formats are jpg, jpeg, png, gif."),
                        duration=4000
                    ))

            # Update the banner content
            self.banner.content.controls[0].controls = [  # Update the text column
                ft.Text("Component Details:", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD, size=20)  # Add title
            ] + component_detail_rows  # Add detail rows
            self.banner.content.controls[1].content = image_content  # Update the image

        self.page.open(self.banner)  # Open the banner on the page

    def show_manage_component_bottomsheet(self):  # Define a method to show the manage dialog
        """Display the manage component bottom sheet."""
        self.page.bottom_sheet = self.manage_component  # Set the bottom sheet to the manage dialog
        self.page.bottom_sheet.open = True  # Open the bottom sheet
        self.page.update()  # Update the page to show the dialog

    def create_component_card(self, data, status_color, on_manage_click, on_select):  # Define a method to create an available component card
        """Create a card for an available component."""
        component_id = data[0]  # Get the component ID
        name = str(data[1]) if data[1] is not None else ""  # Get the component name
        category = str(data[2]) if data[2] is not None else ""  # Get the category
        company = str(data[3]) if data[3] is not None else ""  # Get the company
        model = str(data[4]) if data[4] is not None else ""  # Get the model
        status = str(data[5]) if data[5] is not None else ""  # Get the status
        image_path = str(data[6]) if data[6] is not None else None  # Get the image path

        # Debug image path and on_manage_click
        print(f"Processing component: {name}, image_path: {image_path}")  # Print component info for debugging
        print(f"create_component_card: on_manage_click type: {type(on_manage_click)}, value: {on_manage_click}")  # Print manage click handler info
        image_content = None  # Initialize image content as None
        if image_path and image_path.startswith("/images/") and self._is_supported_image_format(image_path):  # Check if image is valid
            image_content = ft.Image(  # Create an image widget
                src=image_path,  # Set the image path
                width=120,  # Set image width
                height=120,  # Set image height
                fit=ft.ImageFit.CONTAIN,  # Ensure image fits within bounds
                error_content=ft.Text("Failed to load image"),  # Show error text if image fails
            )
        else:  # If image is invalid
            print(f"Unsupported or invalid image format for component {name}: {image_path}")  # Print error message
            if image_path:  # If an invalid image path was provided
                self.page.open(ft.SnackBar(  # Show error message
                    ft.Text(f"Unsupported image format for component {name}: {image_path}. Supported formats are jpg, jpeg, png, gif."),
                    duration=4000
                ))

        card_content = [  # Create a list of card content
            ft.Row(  # Create a row for name and status
                [  # Define row controls
                    ft.Text(f"Name: {name}", size=16, weight=ft.FontWeight.BOLD, color="#263238"),  # Add name text
                    ft.Container(  # Create a container for status
                        content=ft.Row(  # Create a row for status indicator
                            [  # Define row controls
                                ft.Container(width=15, height=15, bgcolor=status_color, border_radius=10),  # Add status color dot
                                ft.Text(status, color=ft.Colors.BLACK),  # Add status text
                            ],
                            spacing=5,  # Set spacing between controls
                            alignment=ft.MainAxisAlignment.END,  # Align to the end
                        ),
                        alignment=ft.alignment.center_right,  # Align container to the right
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Space out name and status
            ),
            ft.Text(f"Category: {category}", size=14, color="#263238"),  # Add category text
            ft.Text(f"Company: {company}", size=14, color="#263238"),  # Add company text
            ft.Text(f"Model: {model}", size=14, color="#263238"),  # Add model text
            ft.ElevatedButton(  # Create a manage button
                "Manage",  # Set button text
                icon=ft.Icons.PENDING_ACTIONS,  # Add an icon
                bgcolor=ft.Colors.BLUE_300,  # Set blue background
                color=ft.Colors.WHITE,  # Set white text
                on_click=lambda e: on_manage_click(component_id, name),  # Call manage handler when clicked
                width=100,  # Set button width
            ),
        ]

        if image_content:  # Check if there is an image
            card_content.insert(0, ft.Container(  # Insert image at the start
                content=image_content,  # Set the image content
                alignment=ft.alignment.center,  # Center the image
                margin=ft.margin.only(bottom=10),  # Add bottom margin
            ))

        return ft.Card(  # Create a card widget
            content=ft.Container(  # Create a container for card content
                content=ft.Column(  # Create a column for content
                    card_content,  # Set the card content
                    spacing=5,  # Set spacing between controls
                    alignment=ft.MainAxisAlignment.START,  # Align to the start
                ),
                padding=15,  # Add padding around content
                bgcolor="#E3F2FD",  # Set light blue background
                border_radius=12,  # Round corners
                ink=True,  # Enable click effects
                on_click=lambda e: on_select(e, data),  # Call select handler when clicked
                width=300,  # Set card width
                height=400 if image_content else 300,  # Set height based on image
            ),
            elevation=5,  # Set card elevation
        )

    def create_deployed_card(self, data, status_color, on_manage_click, on_select):  # Define a method to create a deployed component card
        """Create a card for a deployed component."""
        component_id = data[0]  # Get the component ID
        name = str(data[1]) if data[1] is not None else ""  # Get the component name
        category = str(data[2]) if data[2] is not None else ""  # Get the category
        company = str(data[3]) if data[3] is not None else ""  # Get the company
        model = str(data[4]) if data[4] is not None else ""  # Get the model
        deployed_to = str(data[5]) if data[5] is not None else ""  # Get the deployed to info
        user_department = str(data[6]) if data[6] is not None else ""  # Get the department
        deploy_date = str(data[7]) if data[7] is not None else ""  # Get the deploy date
        image_path = str(data[8]) if data[8] is not None else None  # Get the image path

        # Debug image path and on_manage_click
        print(f"Processing deployed component: {name}, image_path: {image_path}")  # Print component info for debugging
        print(f"create_deployed_card: on_manage_click type: {type(on_manage_click)}, value: {on_manage_click}")  # Print manage click handler info
        image_content = None  # Initialize image content as None
        if image_path and image_path.startswith("/images/") and self._is_supported_image_format(image_path):  # Check if image is valid
            image_content = ft.Image(  # Create an image widget
                src=image_path,  # Set the image path
                width=120,  # Set image width
                height=120,  # Set image height
                fit=ft.ImageFit.CONTAIN,  # Ensure image fits within bounds
                error_content=ft.Text("Failed to load image"),  # Show error text if image fails
            )
        else:  # If image is invalid
            print(f"Unsupported or invalid image format for deployed component {name}: {image_path}")  # Print error message
            if image_path:  # If an invalid image path was provided
                self.page.open(ft.SnackBar(  # Show error message
                    ft.Text(f"Unsupported image format for deployed component {name}: {image_path}. Supported formats are jpg, jpeg, png, gif."),
                    duration=4000
                ))

        card_content = [  # Create a list of card content
            ft.Row(  # Create a row for name and status
                [  # Define row controls
                    ft.Text(f"Name: {name}", size=16, weight=ft.FontWeight.BOLD, color="#263238"),  # Add name text
                    ft.Container(  # Create a container for status
                        content=ft.Row(  # Create a row for status indicator
                            [  # Define row controls
                                ft.Container(width=15, height=15, bgcolor=status_color, border_radius=10),  # Add status color dot
                                ft.Text("Assigned", color=ft.Colors.BLACK),  # Add status text
                            ],
                            spacing=5,  # Set spacing between controls
                            alignment=ft.MainAxisAlignment.END,  # Align to the end
                        ),
                        alignment=ft.alignment.center_right,  # Align container to the right
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Space out name and status
            ),
            ft.Text(f"Category: {category}", size=14, color="#263238"),  # Add category text
            ft.Text(f"Company: {company}", size=14, color="#263238"),  # Add company text
            ft.Text(f"Model: {model}", size=14, color="#263238"),  # Add model text
            ft.Text(f"Assigned To: {deployed_to}", size=14, color="#263238"),  # Add deployed to text
            ft.Text(f"Department: {user_department}", size=14, color="#263238"),  # Add department text
            ft.Text(f"Deploy Date: {deploy_date}", size=14, color="#263238"),  # Add deploy date text
            ft.ElevatedButton(  # Create a manage button
                "Manage",  # Set button text
                icon=ft.Icons.PENDING_ACTIONS,  # Add an icon
                bgcolor=ft.Colors.BLUE_300,  # Set blue background
                color=ft.Colors.WHITE,  # Set white text
                on_click=lambda e: on_manage_click(component_id, name),  # Call manage handler when clicked
                width=100,  # Set button width
            ),
        ]

        if image_content:  # Check if there is an image
            card_content.insert(0, ft.Container(  # Insert image at the start
                content=image_content,  # Set the image content
                alignment=ft.alignment.center,  # Center the image
                margin=ft.margin.only(bottom=10),  # Add bottom margin
            ))

        return ft.Card(  # Create a card widget
            content=ft.Container(  # Create a container for card content
                content=ft.Column(  # Create a column for content
                    card_content,  # Set the card content
                    spacing=5,  # Set spacing between controls
                    alignment=ft.MainAxisAlignment.START,  # Align to the start
                ),
                padding=15,  # Add padding around content
                bgcolor="#E3F2FD",  # Set light blue background
                border_radius=12,  # Round corners
                ink=True,  # Enable click effects
                on_click=lambda e: on_select(e, data),  # Call select handler when clicked
                width=300,  # Set card width
                height=400 if image_content else 300,  # Set height based on image
            ),
            elevation=5,  # Set card elevation
        )

    def create_disposed_card(self, data, status_color, on_manage_click, on_select):  # Define a method to create a disposed component card
        """Create a card for a disposed component."""
        component_id = data[0]  # Get the component ID
        name = str(data[1]) if data[1] is not None else ""  # Get the component name
        category = str(data[2]) if data[2] is not None else ""  # Get the category
        company = str(data[3]) if data[3] is not None else ""  # Get the company
        model = str(data[4]) if data[4] is not None else ""  # Get the model
        purchase_date = str(data[5]) if data[5] is not None else ""  # Get the purchase date
        disposal_date = str(data[6]) if data[6] is not None else ""  # Get the disposal date
        disposal_type = str(data[7]) if data[7] is not None else ""  # Get the disposal type
        amount_earned = f"${data[8]}" if data[8] is not None else ""  # Get the amount earned
        disposal_reason = str(data[9]) if data[9] is not None else ""  # Get the disposal reason
        disposal_location = str(data[10]) if data[10] is not None else ""  # Get the disposal location
        sale_details = str(data[11]) if data[11] is not None else ""  # Get the sale details
        sold_to = str(data[12]) if data[12] is not None else ""  # Get the sold to info
        image_path = str(data[13]) if data[13] is not None else None  # Get the image path

        # Validate image path
        if image_path and image_path.startswith("/images/") and self._is_supported_image_format(image_path):  # Check if image is valid
            image_content = ft.Image(  # Create an image widget
                src=image_path,  # Set the image path
                width=120,  # Set image width
                height=120,  # Set image height
                fit=ft.ImageFit.CONTAIN,  # Ensure image fits within bounds
                error_content=ft.Text("Failed to load image"),  # Show error text if image fails
            )
        else:  # If image is invalid
            image_content = ft.Image(  # Create a placeholder image
                src="/images/placeholder.jpg",  # Set placeholder image path
                width=120,  # Set image width
                height=120,  # Set image height
                fit=ft.ImageFit.CONTAIN,  # Ensure image fits within bounds
                error_content=ft.Text("Placeholder image not found"),  # Show error text if image fails
            )
            if image_path:  # If an invalid image path was provided
                print(f"Unsupported or invalid image format for disposed component {name}: {image_path}")  # Print error message

        card_content = [  # Create a list of card content
            ft.Row(  # Create a row for name and disposal type
                [  # Define row controls
                    ft.Text(f"Name: {name}", size=16, weight=ft.FontWeight.BOLD, color="#263238"),  # Add name text
                    ft.Container(  # Create a container for disposal type
                        content=ft.Row(  # Create a row for disposal type indicator
                            [  # Define row controls
                                ft.Container(width=15, height=15, bgcolor=status_color, border_radius=10),  # Add status color dot
                                ft.Text(disposal_type, color=ft.Colors.BLACK),  # Add disposal type text
                            ],
                            spacing=5,  # Set spacing between controls
                            alignment=ft.MainAxisAlignment.END,  # Align to the end
                        ),
                        alignment=ft.alignment.center_right,  # Align container to the right
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Space out name and disposal type
            ),
            ft.Text(f"Category: {category}", size=14, color="#263238"),  # Add category text
            ft.Text(f"Company: {company}", size=14, color="#263238"),  # Add company text
            ft.Text(f"Model: {model}", size=14, color="#263238"),  # Add model text
            ft.Text(f"Purchase Date: {purchase_date}", size=14, color="#263238"),  # Add purchase date text
            ft.Text(f"Disposal Date: {disposal_date}", size=14, color="#263238"),  # Add disposal date text
        ]

        if disposal_type == "Scrap" and amount_earned:  # Check if disposal type is Scrap and amount earned exists
            card_content.append(ft.Text(f"Amount Earned: {amount_earned}", size=14, color="#263238"))  # Add amount earned text
        elif disposal_type == "Dispose":  # Check if disposal type is Dispose
            if disposal_reason:  # Check if disposal reason exists
                card_content.append(ft.Text(f"Reason: {disposal_reason}", size=14, color="#263238"))  # Add reason text
            if disposal_location:  # Check if disposal location exists
                card_content.append(ft.Text(f"Disposal Location: {disposal_location}", size=14, color="#263238"))  # Add location text
        elif disposal_type == "Sold":  # Check if disposal type is Sold
            if sold_to:  # Check if sold to exists
                card_content.append(ft.Text(f"Sold To: {sold_to}", size=14, color="#263238"))  # Add sold to text
            if sale_details:  # Check if sale details exist
                card_content.append(ft.Text(f"Sale Details: {sale_details}", size=14, color="#263238"))  # Add sale details text
            if amount_earned:  # Check if amount earned exists
                card_content.append(ft.Text(f"Amount Earned: {amount_earned}", size=14, color="#263238"))  # Add amount earned text

        card_content.append(  # Add manage button to card content
            ft.ElevatedButton(  # Create a manage button
                "Manage",  # Set button text
                icon=ft.Icons.PENDING_ACTIONS,  # Add an icon
                bgcolor=ft.Colors.BLUE_300,  # Set blue background
                color=ft.Colors.WHITE,  # Set white text
                on_click=lambda e: on_manage_click(component_id, name),  # Call manage handler when clicked
                width=100,  # Set button width
            )
        )

        if image_content:  # Check if there is an image
            card_content.insert(0, ft.Container(  # Insert image at the start
                content=image_content,  # Set the image content
                alignment=ft.alignment.center,  # Center the image
                margin=ft.margin.only(bottom=10),  # Add bottom margin
            ))

        return ft.Card(  # Create a card widget
            content=ft.Container(  # Create a container for card content
                content=ft.Column(  # Create a column for content
                    card_content,  # Set the card content
                    spacing=5,  # Set spacing between controls
                    alignment=ft.MainAxisAlignment.START,  # Align to the start
                ),
                padding=15,  # Add padding around content
                bgcolor="#E3F2FD",  # Set light blue background
                border_radius=12,  # Round corners
                ink=True,  # Enable click effects
                on_click=lambda e: on_select(e, data),  # Call select handler when clicked
                width=300,  # Set card width
                height=380 if image_content else 340,  # Set height based on image
            ),
            elevation=5,  # Set card elevation
        )

    def filter_components(self, e):  # Define a method to filter components
        """Handle filter button click to fetch components by selected category."""
        selected_category = self.category_dropdown.value  # Get the selected category from dropdown
        print(f"Filtering components by category: {selected_category}")  # Print selected category for debugging
        self.refresh_cards(category_id=selected_category)  # Refresh cards with filtered data

    def refresh_cards(self, category_id=None):  # Define a method to refresh component cards
        """Refresh the component cards by re-fetching data, optionally filtered by category."""
        try:  # Start a try block to handle database errors
            self.component_data = self._fetch_components(category_id=category_id)  # Fetch available components
            self.deployed_data = self._fetch_deployed_components(category_id=category_id)  # Fetch deployed components
            self.disposed_data = self._fetch_disposed_components(category_id=category_id)  # Fetch disposed components

            # Define on_manage_click lambda for clarity
            manage_click_handler = lambda id, name: self.manage_component.open(component_id=id, name=name)  # Define manage button handler

            # Update deployable cards
            self.deployable_cards.controls = [  # Update the available cards
                ft.Container(  # Create a container for each card
                    content=self.create_component_card(  # Create a card
                        data=x,  # Pass component data
                        status_color=ft.Colors.LIGHT_GREEN_ACCENT_400,  # Set status color
                        on_manage_click=manage_click_handler,  # Set manage handler
                        on_select=lambda e, component=x: self.show_banner(component=component, is_deployed=False),  # Set click handler
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},  # Set responsive column sizes
                    padding=ft.padding.all(10),  # Add padding
                )
                for x in self.component_data  # Iterate over available components
            ]

            # Update deployed cards
            self.deployed_cards.controls = [  # Update the deployed cards
                ft.Container(  # Create a container for each card
                    content=self.create_deployed_card(  # Create a card
                        data=data,  # Pass component data
                        status_color=ft.Colors.LIGHT_BLUE_ACCENT_700,  # Set status color
                        on_manage_click=manage_click_handler,  # Set manage handler
                        on_select=lambda e, component=data: self.show_banner(component=component, is_deployed=True),  # Set click handler
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},  # Set responsive column sizes
                    padding=ft.padding.all(10),  # Add padding
                )
                for data in self.deployed_data  # Iterate over deployed components
            ]

            # Update disposed cards
            self.disposed_cards.controls = [  # Update the disposed cards
                ft.Container(  # Create a container for each card
                    content=self.create_disposed_card(  # Create a card
                        data=data,  # Pass component data
                        status_color=ft.Colors.RED_ACCENT_400 if data[7] == "Scrap" else (ft.Colors.YELLOW_ACCENT_400 if data[7] == "Sold" else ft.Colors.GREY_400),  # Set status color
                        on_manage_click=lambda e: self.show_manage_component_bottomsheet(),  # Set manage handler
                        on_select=lambda e, component=data: self.show_banner(component=component, is_disposed=True),  # Set click handler
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "xl": 3},  # Set responsive column sizes
                    padding=ft.padding.all(10),  # Add padding
                )
                for data in self.disposed_data  # Iterate over disposed components
            ]

            self.page.update()  # Update the page to reflect changes

        except mysql.connector.Error as err:  # Catch any database errors
            print(f"Error refreshing cards: {err}")  # Print the error message
            self.page.open(ft.SnackBar(ft.Text(f"Error refreshing cards: {err}"), duration=4000))  # Show error message

def components_page(page):  # Define a function to create the components page
    return ComponentPage(page)  # Return a new ComponentPage instance