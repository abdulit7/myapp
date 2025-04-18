import flet as ft

class ChartPage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        normal_radius = 150
        hover_radius = 170
        normal_title_style = ft.TextStyle(
            size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD
        )
        hover_title_style = ft.TextStyle(
            size=16,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK54),
        )
        normal_badge_size = 60

        def badge(icon, size):
            return ft.Container(
                ft.Icon(icon),
                width=size,
                height=size,
                border=ft.border.all(1, ft.Colors.BROWN),
                border_radius=size / 2,
                bgcolor=ft.Colors.WHITE,
            )

        def on_chart_event(e: ft.PieChartEvent):
            for idx, section in enumerate(chart.sections):
                if idx == e.section_index:
                    section.radius = hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = normal_radius
                    section.title_style = normal_title_style
            chart.update()

        chart = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    40,
                    title="40%",
                    title_style=normal_title_style,
                    color=ft.Colors.BLUE,
                    radius=normal_radius,
                    badge=badge(ft.Icons.AC_UNIT, normal_badge_size),
                    badge_position=0.98,
                ),
                ft.PieChartSection(
                    30,
                    title="30%",
                    title_style=normal_title_style,
                    color=ft.Colors.YELLOW,
                    radius=normal_radius,
                    badge=badge(ft.Icons.ACCESS_ALARM, normal_badge_size),
                    badge_position=0.98,
                ),
                ft.PieChartSection(
                    15,
                    title="15%",
                    title_style=normal_title_style,
                    color=ft.Colors.PURPLE,
                    radius=normal_radius,
                    badge=badge(ft.Icons.APPLE, normal_badge_size),
                    badge_position=0.98,
                ),
                ft.PieChartSection(
                    15,
                    title="15%",
                    title_style=normal_title_style,
                    color=ft.Colors.GREEN,
                    radius=normal_radius,
                    badge=badge(ft.Icons.PEDAL_BIKE, normal_badge_size),
                    badge_position=0.98,
                ),
            ],
            sections_space=0,
            center_space_radius=0,
            on_chart_event=on_chart_event,
            expand=True,

            
            
        )

        # ✅ Add the chart to the container's content
        self.content = chart


def chart_page(page):
    return ChartPage(page)
