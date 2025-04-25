import flet as ft

def TopBar(page: ft.Page, height=55, bg_color="#4682B4"):
    """
    Creates a top bar matching the Snipe-IT design with logo, search bar, user profile, and a menu bar.
    
    Args:
        page (ft.Page): The Flet page instance.
        height (int): Height of the top bar (default: 80 to accommodate the menu bar).
        bg_color (str): Background color (default: #4682B4, matching the screenshot).
    """
    def handle_logout(e):
        print("Logging out")
        page.close_dialog()
        page.go("/logout")
        page.update()

    # Logo

    # Search bar
    search_bar = ft.Container(
        content=ft.TextField(
            hint_text="Lookup by Asset Tag",
            width=200,
            height=35,
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=5,
            prefix_icon=ft.Icons.SEARCH,
            text_size=14,
            content_padding=ft.padding.symmetric(vertical=0, horizontal=10),
            visible=True,
        ),
        width=200,
    )

    # Icons and user profile
    user_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(
                text="John Doe",
                on_click=lambda e: page.go("/profile"),
            ),
            ft.PopupMenuItem(
                text="Create New",
                on_click=lambda e: page.go("/assetform"),
            ),
            ft.PopupMenuItem(
                text="Messages (57)",
                on_click=lambda e: page.go("/messages"),
            ),
            ft.PopupMenuItem(
                text="Logout",
                on_click=handle_logout,
            ),
        ],
        content=ft.Row([
            ft.Icon(ft.Icons.PERSON, color=ft.colors.WHITE, size=24),
            ft.Text("John Doe", color=ft.colors.WHITE, size=14),
            ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=ft.colors.WHITE, size=18),
        ], spacing=5),
        tooltip="User Menu",
    )

    # Menu bar with submenu buttons
    menubar = ft.MenuBar(
        #expand=True,
        style=ft.MenuStyle(
            
            alignment=ft.alignment.top_left,
            bgcolor="#4682B4",  # Slightly darker blue to match the top bar
            mouse_cursor={
                ft.ControlState.HOVERED: ft.MouseCursor.ALIAS,  # Hand cursor on hover
                ft.ControlState.DEFAULT: ft.MouseCursor.BASIC,
            },
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Menu", color=ft.colors.WHITE),
                leading=ft.Icon(ft.Icons.MENU, color=ft.colors.WHITE),
         
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                ),
                # Optional: Add a tooltip to the menu button
                tooltip="Menu",
                # Optional: Add a badge to indicate new items
                
                

                
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Dashboard"),
                        leading=ft.Icon(ft.Icons.DASHBOARD),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/dashboard"),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Assets"),
                        leading=ft.Icon(ft.Icons.REPORT),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/asset"),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Components"),
                        leading=ft.Icon(ft.Icons.INVENTORY),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/component"),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Users"),
                        leading=ft.Icon(ft.Icons.PEOPLE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/user"),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Category"),
                        leading=ft.Icon(ft.Icons.LABEL),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/category"),
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("Consumable"),
                        leading=ft.Icon(ft.Icons.LABEL),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/consumable"),
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("Sale Force"),
                        leading=ft.Icon(ft.Icons.BUSINESS),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/saleforce"),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Departments"),
                        leading=ft.Icon(ft.Icons.HDR_OFF_SELECT_OUTLINED),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/department"),
                    ),
                ],
            ),
            
            
        ], 
    )


    settingbar = ft.MenuBar(
        #expand=True,
        style=ft.MenuStyle(
            
            alignment=ft.alignment.top_left,
            bgcolor=ft.Colors.GREEN,  # Slightly darker blue to match the top bar
            mouse_cursor={
                ft.ControlState.HOVERED: ft.MouseCursor.ALIAS,  # Hand cursor on hover
                ft.ControlState.DEFAULT: ft.MouseCursor.BASIC,
            },
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Setting"),
                
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Profile"),
                        leading=ft.Icon(ft.Icons.PERSON),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/profile"),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Settings"),
                        leading=ft.Icon(ft.Icons.SETTINGS),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/settings"),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Notifications"),
                        leading=ft.Icon(ft.Icons.NOTIFICATIONS),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_100}
                        ),
                        on_click=lambda e: page.go("/notifications"),
                    ),
                ],
            ),
            
            
        ], 
    )

    # Layout with the menu bar below the top bar elements
    top_bar = ft.Container(
        bgcolor=bg_color,
        padding=ft.padding.symmetric(vertical=10, horizontal=15),
        height=height,
        shadow=ft.BoxShadow(
            blur_radius=10,
            spread_radius=1,
            color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
        ),
        content=ft.Column([
            ft.Row([
                menubar,
                settingbar,
           
                ft.Container(expand=True),  # Spacer
                search_bar,
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ADD,
                        icon_color=ft.colors.WHITE,
                        icon_size=24,
                        tooltip="Create New",
                        on_click=lambda e: page.go("/assetform"),
                        style=ft.ButtonStyle(
                            bgcolor={"hovered": "#5A9BD5"},
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.MESSAGE,
                        icon_color=ft.colors.WHITE,
                        icon_size=24,
                        tooltip="Messages (57)",
                        on_click=lambda e: page.go("/messages"),
                        style=ft.ButtonStyle(
                            bgcolor={"hovered": "#5A9BD5"},
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    ),
                    user_menu,
                ], spacing=10),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
              # Add the menu bar below the top row
        ], spacing=5),
    )

    page.update()
    return top_bar