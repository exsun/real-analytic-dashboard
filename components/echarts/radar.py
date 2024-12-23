import json

from streamlit_elements import mui, nivo
from .dashboard import Dashboard


class Radar(Dashboard.Item):

    DEFAULT_DATA = [
        { "taste": "چابکی", "pre-test": 93, "post-test": 61},
        { "taste": "سرعت", "pre-test": 91, "post-test": 37},
        { "taste": "قدرت", "pre-test": 56, "post-test": 95},
        { "taste": "استقامت عضلانی", "pre-test": 64, "post-test": 90},
        { "taste": "استقامت هوازی", "pre-test": 119, "post-test": 94},
        { "taste": "سرعت عکس العمل", "pre-test": 119, "post-test": 94},

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

    def __call__(self, input_json):
        if input_json:
            data = input_json
        else:
            data = self.DEFAULT_DATA

        with mui.Paper(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            with self.title_bar():
                mui.icon.Radar()
                mui.Typography("Radar chart", sx={"flex": 1})

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                nivo.Radar(
                    data=data,
                    theme=self._theme["dark" if self._dark_mode else "light"],
                    keys=[ "pre-test", "post-test"],
                    indexBy="taste",
                    valueFormat=">-.2f",
                    margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
                    borderColor={ "from": "color" },
                    gridLabelOffset=36,
                    dotSize=10,
                    dotColor={ "theme": "background" },
                    dotBorderWidth=2,
                    motionConfig="wobbly",
                    legends=[
                        {
                            "anchor": "top-left",
                            "direction": "column",
                            "translateX": -50,
                            "translateY": -40,
                            "itemWidth": 80,
                            "itemHeight": 20,
                            "itemTextColor": "#999",
                            "symbolSize": 12,
                            "symbolShape": "circle",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemTextColor": "#000"
                                    }
                                }
                            ]
                        }
                    ]
                )
