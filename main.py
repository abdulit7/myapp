import flet as ft
from pages.dashboard.home import Home
from pages.dashboard.users import Users
from components.userform import UserForm
from pages.dashboard.asset2 import AssetPagee
from components.assetform import AssetFormPage
from pages.dashboard.components import Components
from pages.dashboard.saleforce import SaleForcePage
from pages.dashboard.category import Category
from components.assetdialog import AssetDialog
from pages.dashboard.department import Department

def main(page: ft.Page):
    page.title = "Asset Management System"
    page.expand = True
    page.scroll = "adaptive"

    # Function to handle route changes
    def change_route(route):
        """Handles navigation between different pages."""
        page.views.clear()  # Ensure only one active view at a time

        routes = {
            "/dashboard": Home,
            "/user": Users,
            "/userform": UserForm,
            "/asset": AssetPagee,
            "/assetform": AssetFormPage,
            "/component": Components,
            "/saleforce": SaleForcePage,
            "/category": Category,
            "/department": Department,
            "/assetformdialog": AssetDialog,
        }

        if page.route in routes:
            page.views.append(ft.View(page.route, controls=[routes[page.route](page)]))
        else:
            page.views.append(ft.View("/", controls=[ft.Text("Page not found")]))
        
        page.update()

    def view_pop(view):
        """Handles back navigation."""
        if len(page.views) > 1:
            page.views.pop()
            page.go(page.views[-1].route)  # Ensure it redirects to the last valid route
        else:
            print("No more views to pop!")

    # Assign event handlers
    page.on_route_change = change_route
    page.on_view_pop = view_pop

    # Start the app at the dashboard page
    page.go("/dashboard")

ft.app(target=main, assets_dir="assets", view=None, port=8000, host="0.0.0.0")

