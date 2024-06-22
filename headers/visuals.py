import flet as ft


class State:
    toggle = True

    def __init__(self) -> None:
        self.data1 = [
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(0, 3),
                    ft.LineChartDataPoint(2.6, 2),
                    ft.LineChartDataPoint(4.9, 5),
                    ft.LineChartDataPoint(6.8, 3.1),
                    ft.LineChartDataPoint(8, 4),
                    ft.LineChartDataPoint(9.5, 3),
                    ft.LineChartDataPoint(11, 4),
                ],
                stroke_width=5,
                color=ft.colors.CYAN,
                curved=True,
                stroke_cap_round=True,
            )
        ]

        self.data2 = [
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(0, 3.44),
                    ft.LineChartDataPoint(2.6, 3.44),
                    ft.LineChartDataPoint(4.9, 3.44),
                    ft.LineChartDataPoint(6.8, 3.44),
                    ft.LineChartDataPoint(8, 3.44),
                    ft.LineChartDataPoint(9.5, 3.44),
                    ft.LineChartDataPoint(11, 3.44),
                ],
                stroke_width=5,
                color=ft.colors.CYAN,
                curved=True,
                stroke_cap_round=True,
            )
        ]

        self.chart = ft.LineChart(
            data_series=self.data1,
            border=ft.border.all(3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=1,
                color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE),
                width=1,
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=1,
                color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE),
                width=1,
            ),
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=1,
                        label=ft.Text("10K", size=14, weight=ft.FontWeight.BOLD),
                    ),
                    ft.ChartAxisLabel(
                        value=3,
                        label=ft.Text("30K", size=14, weight=ft.FontWeight.BOLD),
                    ),
                    ft.ChartAxisLabel(
                        value=5,
                        label=ft.Text("50K", size=14, weight=ft.FontWeight.BOLD),
                    ),
                ],
                labels_size=40,
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=2,
                        label=ft.Container(
                            ft.Text(
                                "MAR",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                    ),
                    ft.ChartAxisLabel(
                        value=5,
                        label=ft.Container(
                            ft.Text(
                                "JUN",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                    ),
                    ft.ChartAxisLabel(
                        value=8,
                        label=ft.Container(
                            ft.Text(
                                "SEP",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                    ),
                ],
                labels_size=32,
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
            min_y=0,
            max_y=6,
            min_x=0,
            max_x=11,
            # animate=5000,
            expand=True,
        )

    def toggle_data(self, e):
        if self.toggle:
            self.chart.data_series = self.data2
            self.chart.interactive = True
        else:
            self.chart.data_series = self.data1
            self.chart.interactive = True
        self.toggle = not self.toggle
        self.chart.update()
