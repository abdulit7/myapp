import flet as ft
import requests  # Ensure `requests` is installed: pip install requests

API_URL = "http://localhost:5000/api/categories"  # Your Flask API URL

def main(page: ft.Page):
    page.title = "Category Management"

    # Category Table with Image Column
    category_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Category Name")),
            ft.DataColumn(ft.Text("Description")),
            ft.DataColumn(ft.Text("Image")),  # New column for image
        ],
        rows=[]
    )

    def fetch_categories():
        """Fetch data from the Flask API and populate the table."""
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                categories = response.json()
                category_table.rows.clear()

                for category in categories:
                    category_table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(category["id"]))),
                                ft.DataCell(ft.Text(category["name"])),
                                ft.DataCell(ft.Text(category["description"])),
                                ft.DataCell(ft.Image(category.get("image", ""), width=50, height=50)),  # Image
                            ]
                        )
                    )
                page.update()
            else:
                print(f"Error fetching categories: {response.status_code}")
        except Exception as e:
            print(f"Exception: {e}")

    # Fetch button
    fetch_button = ft.ElevatedButton("Fetch Categories", on_click=lambda _: fetch_categories())

    # Layout
    page.add(fetch_button, category_table)

ft.app(target=main)
