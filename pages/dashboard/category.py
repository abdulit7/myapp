import flet as ft
import mysql.connector
#from nav.menubar import TopBarPage
#from nav.sidebar import SidebarPage
from components.categoryform import CatDialog

class Category(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.expand = True
        page.window.title = "Asset Management System - Assets"

        self.cat_dialog = CatDialog(page)
       


        # Add Asset Button
        add_category_button = ft.ElevatedButton(
            icon=ft.Icons.ADD,
            text="Category",
            bgcolor=ft.Colors.GREEN_400,
            width=150,
            height=50,
            color=ft.Colors.WHITE,
            on_click=lambda e: self.cat_dialog.open()  # Assuming you have a route for adding assets
        )

        # Example Asset Table (You can customize this part)
        category_table = ft.DataTable(
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
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
                ft.DataColumn(ft.Text("Image", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Type", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("QTY", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Desc", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Action", weight=ft.FontWeight.W_600)),
            ],
            rows=[ ],
        )

        conn = mysql.connector.connect(
            host="200.200.200.23",
            user="root",
            password="Pak@123",
            database="itasset",
            auth_plugin='mysql_native_password'
        )
        mycursor = conn.cursor()
        mycursor.execute("SELECT name, image, type, qty FROM category ")
        myresult = mycursor.fetchall()

        for x in myresult:
            category_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(x[0])),
                        ft.DataCell(ft.Image(x[1], width=50, height=50)),
                        ft.DataCell(ft.Text(x[2])),
                        ft.DataCell(ft.Text(x[3])),
                        ft.DataCell(ft.Text("High-end laptop", weight=ft.FontWeight.W_600)),
                       
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
                    ]
                )
            )

        self.content = ft.Column(
                controls=[
                    #TopBarPage(page),
                    ft.Row(
                        controls=[
                            ft.Column(  # Use Column to align sidebar to top
                                controls=[
                                    # ft.Container(
                                    #     content=SidebarPage(page),
                                    #     width=200,
                                    #     expand=True,  # Make sidebar fill available height
                                    # ),
                                ],
                                #expand=True,  # Make the column expand to fill the row
                            ),
                            ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            
                                            add_category_button
                                        ],
                                        #alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    category_table
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
