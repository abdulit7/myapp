import flet as ft
import mysql.connector
from nav.sidebar import SidebarPage
from nav.menubar import TopBarPage

class Users(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.expand = True
        page.window.title = "Asset Management System"
    

        mydb = mysql.connector.connect(
            host="200.200.200.23",
            user="root",
            password="Pak@123",
            database="itasset",
            auth_plugin='mysql_native_password'
        )

        mycur = mydb.cursor()
        mycur.execute("SELECT * FROM users")
        myresult = mycur.fetchall()

        self.add_user_button = ft.ElevatedButton("Add User", on_click=lambda e: page.go("/userform"))

        # Admin DataTable
        admin_table = ft.DataTable(
            width=5000,
            height=500,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(0.5, "red"),
            border_radius=20,
            vertical_lines=ft.BorderSide(0.2, "blue"),
            horizontal_lines=ft.BorderSide(0.2, "green"),
            heading_row_color=ft.Colors.GREY_300,
            heading_row_height=100,
            heading_text_style=ft.TextStyle(
                color=ft.Colors.INDIGO_900,
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            data_row_color={ft.ControlState.HOVERED: "#6fa8dc"},
            column_spacing=30,
            columns=[
                ft.DataColumn(ft.Text("Name", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("EMP ID", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Branch", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Department", weight=ft.FontWeight.W_600)),
                
                ft.DataColumn(ft.Text("Total Asset", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Can Login", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.W_600)),
            ],
          
            rows=[ ],
        )
        for x in myresult:
            admin_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(x[1])),
                        ft.DataCell(ft.Text(x[2])),
                        ft.DataCell(ft.Text(x[3])),
                        ft.DataCell(ft.Text(x[4])),
                        ft.DataCell(ft.Text(x[5])),
                        ft.DataCell(ft.Text("Yes" if x[6] == 1 else "No")),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton("Edit", bgcolor=ft.Colors.LIGHT_GREEN_500, color=ft.Colors.WHITE),
                                    ft.ElevatedButton("Delete", bgcolor=ft.Colors.RED_500, color=ft.Colors.WHITE),
                                ],
                                spacing=5,
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),
                    ],
                    selected=True,
                     # Show banner on selection
                )
            )

        # User DataTable
        user_table = ft.DataTable(
            width=5000,
            height=500,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=30,
            vertical_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            heading_row_color=ft.Colors.INDIGO_100,
            heading_text_style=ft.TextStyle(
                color=ft.Colors.INDIGO_900,
                weight=ft.FontWeight.BOLD,
                size=16
            ),
            data_row_color={
                ft.ControlState.HOVERED: ft.Colors.LIGHT_BLUE_50,
            },
            data_row_min_height=50,
            data_text_style=ft.TextStyle(
                color=ft.Colors.GREY_800,
                size=14,
            ),
            show_checkbox_column=False,
            column_spacing=30,
            columns=[
                ft.DataColumn(ft.Text("Name", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("EMP ID", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Branch", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Department", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Can Login", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.W_600)),
            ],
           
        )

        # Tabs
        t = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Admin",
                    content=ft.Container(
                        content=admin_table,
                        alignment=ft.alignment.top_left,
                        expand=True,
                    )
                ),
                ft.Tab(
                    text="Users",
                    content=ft.Container(
                        content=user_table,
                        alignment=ft.alignment.top_left,
                        expand=True,
                    )
                ),
                
            ],
            expand=True,
        )


        # Layout
        self.content = ft.Column(
            controls=[
                TopBarPage(page),
                ft.Row(
                    controls=[
                        ft.Column(  # Use Column to align sidebar to top
                            controls=[
                                ft.Container(
                                    content=SidebarPage(page),
                                    width=200,
                                    expand=True,  # Make sidebar fill available height
                                ),
                            ],
                            #expand=True,  # Make the column expand to fill the row
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        
                                        self.add_user_button
                                    ],
                                    #alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                t
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.START,
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

        page.update()

     