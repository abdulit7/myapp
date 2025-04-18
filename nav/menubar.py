# import flet as ft

# class MenuBar(ft.Container):
#     def __init__(self, page: ft.Page):
#         super().__init__()

#         # Expand the top bar to full width
#         self.expand = False

#         # Top Bar Container
#         self.content = ft.Container(
#             bgcolor="#1E88E5",  # Blue background
#             padding=ft.padding.symmetric(vertical=15, horizontal=20),
#             content=ft.Row(
#                 controls=[
#                     # Logo and Title
#                     ft.Row(
#                         controls=[
#                             ft.Icon(ft.Icons.COMPUTER, size=30, color=ft.Colors.WHITE),
#                             ft.Text(
#                                 "Asset Management System",
#                                 color=ft.Colors.WHITE,
#                                 size=22,
#                                 weight=ft.FontWeight.BOLD,
#                             ),
#                         ],
#                         alignment=ft.MainAxisAlignment.START,
#                     ),

#                     # Spacer to push items to the right
#                     ft.Container(expand=True),

#                     # Action Buttons
#                     ft.Row(
#                         controls=[
#                             ft.IconButton(
#                                 icon=ft.Icons.NOTIFICATIONS,
#                                 icon_color=ft.Colors.WHITE,
#                                 tooltip="Notifications",
#                                 on_click=lambda e: print("Notifications clicked"),
#                             ),
#                             ft.IconButton(
#                                 icon=ft.Icons.MESSAGE,
#                                 icon_color=ft.Colors.WHITE,
#                                 tooltip="Messages",
#                                 on_click=lambda e: print("Messages clicked"),
#                             ),
#                         ],
#                     ),

#                     # Profile Section with Dropdown Menu
#                     ft.PopupMenuButton(
#                         content=ft.Row(
#                             controls=[
#                                 ft.Container(
#                                     content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color=ft.Colors.WHITE, size=35),
#                                     border_radius=25,
#                                 ),
#                                 ft.Text(
#                                     "Admin",
#                                     color=ft.Colors.WHITE,
#                                     size=16,
#                                     weight=ft.FontWeight.BOLD,
#                                 ),
#                             ],
#                             alignment=ft.MainAxisAlignment.CENTER,
#                             spacing=10,
#                         ),
#                         items=[
#                             ft.PopupMenuItem(text="Profile", on_click=lambda e: print("Profile clicked")),
#                             ft.PopupMenuItem(text="Settings", on_click=lambda e: print("Settings clicked")),
#                             ft.PopupMenuItem(text="Logout", on_click=lambda e: page.go("/logout")),
#                         ],
#                     ),
#                 ],
#                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#             ),
#         )

# def TopBarPage(page):
#     return MenuBar(page)
