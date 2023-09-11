import streamlit as st
import gspread
from streamlit_gsheets import GSheetsConnection

url = "https://docs.google.com/spreadsheets/d/10xSu47HrGItuIkUL-o8lbnfgFpwrq5kDkrot4EtOIX0/edit?usp=sharing"

conn = st.experimental_connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url,  worksheet="1055513374")
st.dataframe(data)
