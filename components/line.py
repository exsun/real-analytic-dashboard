import json

from streamlit_elements import nivo, mui
from .dashboard import Dashboard


class Line(Dashboard.Item):

    DEFAULT_DATA = [
        {
            "id": "Squat",
            "color": "hsl(60, 20%, 23%)",
            "data": [
            {
                "x": "یک تکرار بیشینه",
                "y": 190
            },
            {
                "x": "50 درصد",
                "y": 95
            },
            {
                "x": "60 درصد",
                "y": 114
            },
            {
                "x": "70 درصد",
                "y": 133
            },
            {
                "x": "75 درصد",
                "y": 143
            },
            {
                "x": "80 درصد",
                "y": 152
            },
            {
                "x": "درصد85 ",
                "y": 161.5
            },
            {
                "x": "90 درصد",
                "y": 171
            },

            ]
        },
        {
            "id": "پرس سینه",
            "color": "hsl(220, 70%, 50%)",
            "data": [
            {
                "x": "یک تکرار بیشینه",
                "y": 190
            },
            {
                "x": "50 درصد",
                "y": 95
            },
            {
                "x": "60 درصد",
                "y": 114
            },
            {
                "x": "70 درصد",
                "y": 133
            },
            {
                "x": "75 درصد",
                "y": 143
            },
            {
                "x": "80 درصد",
                "y": 152
            },
            {
                "x": "درصد85 ",
                "y": 161.5
            },
            {
                "x": "90 درصد",
                "y": 171
            },
            ]
        },
    #     {
    #         "id": "us",
    #         "color": "hsl(354, 70%, 50%)",
    #         "data": [
    #         {
    #             "x": "plane",
    #             "y": 74
    #         },
    #         {
    #             "x": "helicopter",
    #             "y": 1
    #         },
    #         {
    #             "x": "boat",
    #             "y": 279
    #         },
    #         {
    #             "x": "train",
    #             "y": 45
    #         },
    #         {
    #             "x": "subway",
    #             "y": 87
    #         },
    #         {
    #             "x": "bus",
    #             "y": 182
    #         },
    #         {
    #             "x": "car",
    #             "y": 185
    #         },
    #         {
    #             "x": "moto",
    #             "y": 203
    #         },
    #         {
    #             "x": "bicycle",
    #             "y": 154
    #         },
    #         {
    #             "x": "horse",
    #             "y": 77
    #         },
    #         {
    #             "x": "skateboard",
    #             "y": 104
    #         },
    #         {
    #             "x": "others",
    #             "y": 270
    #         }
    #         ]
    #     },
    #     {
    #         "id": "germany",
    #         "color": "hsl(168, 70%, 50%)",
    #         "data": [
    #         {
    #             "x": "plane",
    #             "y": 49
    #         },
    #         {
    #             "x": "helicopter",
    #             "y": 152
    #         },
    #         {
    #             "x": "boat",
    #             "y": 259
    #         },
    #         {
    #             "x": "train",
    #             "y": 133
    #         },
    #         {
    #             "x": "subway",
    #             "y": 26
    #         },
    #         {
    #             "x": "bus",
    #             "y": 196
    #         },
    #         {
    #             "x": "car",
    #             "y": 273
    #         },
    #         {
    #             "x": "moto",
    #             "y": 196
    #         },
    #         {
    #             "x": "bicycle",
    #             "y": 38
    #         },
    #         {
    #             "x": "horse",
    #             "y": 118
    #         },
    #         {
    #             "x": "skateboard",
    #             "y": 85
    #         },
    #         {
    #             "x": "others",
    #             "y": 46
    #         }
    #         ]
    #     },
    #     {
    #     "id": "norway",
    #     "color": "hsl(203, 70%, 50%)",
    #     "data": [
    #     {
    #         "x": "plane",
    #         "y": 157
    #     },
    #     {
    #         "x": "helicopter",
    #         "y": 150
    #     },
    #     {
    #         "x": "boat",
    #         "y": 136
    #     },
    #     {
    #         "x": "train",
    #         "y": 221
    #     },
    #     {
    #         "x": "subway",
    #         "y": 81
    #     },
    #     {
    #         "x": "bus",
    #         "y": 149
    #     },
    #     {
    #         "x": "car",
    #         "y": 24
    #     },
    #     {
    #         "x": "moto",
    #         "y": 207
    #     },
    #     {
    #         "x": "bicycle",
    #         "y": 168
    #     },
    #     {
    #         "x": "horse",
    #         "y": 17
    #     },
    #     {
    #         "x": "skateboard",
    #         "y": 141
    #     },
    #     {
    #         "x": "others",
    #         "y": 109
    #     }
    #     ]
    # }
    
    ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._theme = {
            "dark": {
                "background": "#252526",
                "textColor": "#FAFAFA",
                "tooltip": {
                    "container": {
                        "background": "#3F3F3F",
                        "color": "FAFAFA",
                    }
                }
            },
            "light": {
                "background": "#FFFFFF",
                "textColor": "#31333F",
                "tooltip": {
                    "container": {
                        "background": "#FFFFFF",
                        "color": "#31333F",
                    }
                }
            }
        }

    def __call__(self):
    
        data = self.DEFAULT_DATA

        with mui.Paper(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            with self.title_bar():
                mui.icon.PieChart()
                mui.Typography("رکورد", sx={"flex": 1})

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                nivo.Line(
                    data=data,
                    theme=self._theme["dark" if self._dark_mode else "light"],
                    margin={"top": 50, "right": 110, "bottom": 50, "left": 60 },
                    xScale={"type": 'point'},
                    yScale={
                        "type": 'linear',
                        "min": 'auto',
                        "max": 'auto',
                        "stacked": True,
                        "reverse": False
                    },
                    yFormat=" >-.2f",
                    axisBottom={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": 'transportation',
                        "legendOffset": 36,
                        "legendPosition": 'middle',
                        "truncateTickAt": 0
                    },
                    axisLeft={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": 'count',
                        "legendOffset": -40,
                        "legendPosition": 'middle',
                        "truncateTickAt": 0
                    },
                    pointSize=10,
                    pointColor={ "theme": 'background'},
                    pointBorderWidth=2,
                    pointBorderColor={ "from": 'serieColor' },
                    pointLabel="data.yFormatted",
                    pointLabelYOffset=-12,
                    enableTouchCrosshair=True,
                    useMesh=True,
                    legends=[
                        {
                            "anchor": 'bottom-right',
                            "direction": 'column',
                            "justify": False,
                            "translateX": 100,
                            "translateY": 0,
                            "itemsSpacing": 0,
                            "itemDirection": 'right-to-left',
                            "itemWidth": 80,
                            "itemHeight": 20,
                            "itemOpacity": 0.75,
                            "symbolSize": 12,
                            "symbolShape": 'circle',
                            "symbolBorderColor": 'rgba(0, 0, 0, .5)',
                            "effects": [
                                {
                                    "on": 'hover',
                                    "style": {
                                        "itemBackground": 'rgba(0, 0, 0, .03)',
                                        "itemOpacity": 1
                                    }
                                }
                            ]
                        }
                    ]
                )




