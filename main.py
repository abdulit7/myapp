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
from nav.sidebar import TopBar  # Import the updated TopBar without sidebar toggle
from components.componentform import ComponentFormPage

def main(page: ft.Page):
    page.title = "Asset Management System"
    page.expand = True
    page.scroll = "adaptive"
    page.padding = 0
    page.bgcolor = ft.colors.BLUE_GREY_50
    appbar_text_ref = ft.Ref[ft.Text]()

    

    # Determine content area padding based on screen size
    def get_content_padding():
        window_width = page.window.width if page.window.width > 0 else 800
        if window_width <= 600:  # Mobile
            return ft.padding.symmetric(horizontal=10, vertical=5)
        elif window_width <= 1024:  # Tablet
            return ft.padding.symmetric(horizontal=15, vertical=10)
        else:  # Desktop
            return ft.padding.symmetric(horizontal=20, vertical=15)

    # Create a fixed TopBar and scrollable content area
    top_bar = TopBar(page)
    content_area = ft.Container(
        expand=True,
        padding=get_content_padding(),  # Initial padding
    )

    def change_route(route):
        print(f"Changing route to: {route}")

        routes = {
            "/dashboard": Home,
            "/user": Users,
            "/userform": UserForm,
            "/asset": AssetPagee,
            "/assetform": AssetFormPage,
            "/component": Components,
            "/saleforce": SaleForcePage,
            "/category": Category,
            "/componentform": ComponentFormPage,
            "/department": Department,
            "/assetformdialog": AssetDialog,
            "/login": lambda page: ft.Container(
                content=ft.Column([
                    ft.Text("Login", size=24, weight=ft.FontWeight.BOLD),
                    ft.TextField(label="Username", width=300),
                    ft.TextField(label="Password", width=300, password=True),
                    ft.ElevatedButton("Login", width=300, on_click=lambda e: page.go("/dashboard")),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                bgcolor=ft.colors.BLUE_GREY_50,
                expand=True,
            ),
            "/profile": lambda page: ft.Text("Profile Page", size=20),
            "/settings": lambda page: ft.Text("Settings Page", size=20),
            "/notifications": lambda page: ft.Text("Notifications Page", size=20),
            "/logout": lambda page: ft.Text("Logged Out - Redirecting...", size=20, on_create=lambda e: page.go("/login")),
        }

        if page.route in routes:
            content = routes[page.route](page)
            content_area.content = ft.Column(
                controls=[content],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                spacing=0,
            )
        else:
            content_area.content = ft.Column(
                controls=[
                    ft.Text("Page not found", size=20, color=ft.colors.RED_600),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=0,
            )
        page.update()

    def view_pop(view):
        if len(page.views) > 1:
            page.views.pop()
            page.go(page.views[-1].route)
        else:
            print("No more views to pop!")
            page.go("/login")

    # Update layout on window resize
    def on_resize(e):
        content_area.padding = get_content_padding()
        print(f"Resized: Content padding={content_area.padding}")
        page.update()

    # Set initial layout
    page.views.append(
        ft.View(
            "/",
            controls=[
                ft.Column(
                    controls=[
                        
                        top_bar,  # Fixed TopBar
                        content_area,  # Scrollable content area
                    ],
                    expand=True,
                    spacing=0,
                ),
            ],
            padding=0,
            bgcolor=ft.colors.WHITE,
        )
    )

    # Attach resize handler
    page.on_resize = on_resize
    page.on_route_change = change_route
    page.on_view_pop = view_pop
    page.go("/dashboard")

ft.app(target=main, assets_dir="assets", view=ft.AppView.FLET_APP, route_url_strategy="hash")

# import flet as ft
# from pages.dashboard.home import Home
# from pages.dashboard.users import Users
# from components.userform import UserForm
# from pages.dashboard.asset2 import AssetPagee
# from components.assetform import AssetFormPage
# from pages.dashboard.components import Components
# from pages.dashboard.saleforce import SaleForcePage
# from pages.dashboard.category import Category
# from components.assetdialog import AssetDialog
# from pages.dashboard.department import Department

# def main(page: ft.Page):
#     page.title = "Asset Management System"
#     page.expand = True
#     page.scroll = "adaptive"

#     # Function to handle route changes
#     def change_route(route):
#         """Handles navigation between different pages."""
#         page.views.clear()  # Ensure only one active view at a time

#         routes = {
#             "/dashboard": Home,
#             "/user": Users,
#             "/userform": UserForm,
#             "/asset": AssetPagee,
#             "/assetform": AssetFormPage,
#             "/component": Components,
#             "/saleforce": SaleForcePage,
#             "/category": Category,
#             "/department": Department,
#             "/assetformdialog": AssetDialog,
#         }

#         if page.route in routes:
#             page.views.append(ft.View(page.route, controls=[routes[page.route](page)]))
#         else:
#             page.views.append(ft.View("/", controls=[ft.Text("Page not found")]))
        
#         page.update()

#     def view_pop(view):
#         """Handles back navigation."""
#         if len(page.views) > 1:
#             page.views.pop()
#             page.go(page.views[-1].route)  # Ensure it redirects to the last valid route
#         else:
#             print("No more views to pop!")

#     # Assign event handlers
#     page.on_route_change = change_route
#     page.on_view_pop = view_pop

#     # Start the app at the dashboard page
#     page.go("/dashboard")

# #ft.app(target=main, assets_dir="assets", view=None, port=8080, host="0.0.0.0")      # for docker

# ft.app(target=main, assets_dir="assets",)   # for local
# #ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER)   # for local browser
# #ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER, port=8080)   # for local browser with port

# #ft.app(target=main, view=ft.WEB_BROWSER)   # for github

