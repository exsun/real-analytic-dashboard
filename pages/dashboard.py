import streamlit as st
from streamlit import session_state as state
from streamlit_elements import elements, mui, html, sync, event
import pandas as pd
from requests.exceptions import ConnectionError
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
from types import SimpleNamespace

from components import Dashboard, Editor, Card, DataGrid, Radar, Pie, Line

from components.metrics import CHABOKI_DATA, SORAT_DATA, GHODRAT_DATA


st.title("سامانه پایش کشتی گیران ایران")
# if not data.empty:
#     st.subheader('ورزشکاران')
#     # data['نام_و_نام_خانوادگی_ورزشکار'] = data['نام_و_نام_خانوادگی_ورزشکار'].apply(make_clickable)
#     # display_dataframe(data)
#     st.write(data)
    
if "w" not in state:
    board = Dashboard()
    w = SimpleNamespace(
        dashboard=board,
        line=Line(board, 0, 0, 6, 7, minW=3, minH=4),
        radar=Radar(board, 6, 0, 3, 7, minW=2, minH=4),
        radar1=Radar(board, 9, 0, 3, 7, minW=2, minH=4),
        radar2=Radar(board, 0, 2, 3, 7, minW=2, minH=4),
        
        pie=Pie(board, 0, 0, 6, 7, minW=3, minH=4),
        # data_grid=DataGrid(board, 6, 13, 6, 7, minH=4),
    )
    state.w = w

else:
    w = state.w

with elements("demo"):
    event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

    with w.dashboard(rowHeight=57):
        # w.pie()
        w.line()
        w.radar(CHABOKI_DATA, title="چابکی")
        w.radar1(GHODRAT_DATA, title="(Squat) قدرت")
        # w.radar2(GHODRAT_DATA, title="(Heap Trust) قدرت")
        


        # w.data_grid()



