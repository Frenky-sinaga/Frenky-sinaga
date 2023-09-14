import streamlit as st
import gspread
from google.oauth2 import service_account
import pandas as pd
import matplotlib.pyplot as plt
from gspread_dataframe import get_as_dataframe
from pandasql import sqldf


def authenticate_google_sheets():
    credentials = service_account.Credentials.from_service_account_file(
        "masterstore-398408-5f63e59d0f2c.json", scopes=["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
    )
    gc = gspread.Client(auth=credentials)
    gc.login()
    return gc

# Authenticate and get the Google Sheets client
gc = authenticate_google_sheets()

# Open the specific Google Sheets spreadsheet
spreadsheet = gc.open("MasterStores")

# Select a worksheet by name (e.g., "Sheet1")
worksheet = spreadsheet.worksheet("Sheet1")

# Get all records from the worksheet and convert to a Pandas DataFrame
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Group the data by the "Koneksi" column
grouped = df.groupby("Koneksi")


# Streamlit UI
st.title("Master Koneksi toko Cilacap")

# User selects a category


selected_category = st.sidebar.selectbox("Tampilkan toko dengan koneksi", list(grouped.groups.keys()))

# Display the selected category's data
if selected_category in grouped.groups:
    selected_data = grouped.get_group(selected_category)
    st.write(f"Tampilkan toko dengan koneksi {selected_category} category:")
    st.table(selected_data)
else:
    st.warning("Selected category not found.")


# Optional: Add pagination or other features as needed
#---------------------------------------------------------------------------

test = st.sidebar.radio("Navigation", ['Home', 'Columns', 'Tabs', 'expander & container', 'Status Elements'])


if test == "Columns":
 #   st.subheader("Hai, Sahabat Kelas Awan Pintar :wave:")
 #  st.write("Kita akan belajar di halaman ini menggunakan fungsi Column")

    col1, col2 = st.columns([3, 1])

    # Define your SQL-like query

    # Fetch data from Google Sheets and convert to a DataFrame
    df = get_as_dataframe(worksheet)
    
    pysql = lambda q: sqldf(q, globals())
    
    # Define your SQL-like query
    query = 'SELECT Koneksi, COUNT(KODE) as "JLH_TK" FROM df GROUP BY Koneksi ORDER BY JLH_TK'

    # Execute the query
    result_df = pysql(query)

    col1.subheader("Menampilkan data dengan grafik")

    bar_colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightseagreen']
    fig, ax = plt.subplots()
    bars = result_df.plot(kind='bar', x='Koneksi', y='JLH_TK', ax=ax, color=bar_colors)
    
    # Add labels on top of each bar
    for bar in bars.patches:
        ax.annotate(format(bar.get_height(), '.0f'),
                    (bar.get_x() + bar.get_width() / 2,
                     bar.get_height()), ha='center', va='center',
                    size=10, xytext=(0, 5),
                    textcoords='offset points', weight='bold')
        

    col1.pyplot(fig)


