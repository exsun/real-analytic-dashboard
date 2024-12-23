from streamlit_elements import media, mui, sync, lazy
from .dashboard import Dashboard

class Player(Dashboard.Item):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._url = "https://www.aparat.com/v/iox6n98"

    def _set_url(self, event):
        self._url = event.target.value

    def __call__(self):
        with mui.Paper(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            with self.title_bar(padding="10px 15px 10px 15px", dark_switcher=False):
                mui.icon.OndemandVideo()
                mui.Typography("Media player")

            with mui.Stack(direction="row", spacing=2, justifyContent="space-evenly", alignItems="center", sx={"padding": "10px"}):
                mui.IconButton(mui.icon.PlayCircleFilled, onClick=sync(), sx={"color": "primary.main"})

            media.Player(self._url, controls=True, width="100%", height="100%")
