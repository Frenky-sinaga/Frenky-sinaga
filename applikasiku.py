import streamlit as st
import gspread
from google.oauth2 import service_account
import pandas as pd

def authenticate_google_sheets():
    credentials = service_account.Credentials.from_service_account_file(
        "masterstore-398408-5f63e59d0f2c.json", scopes="https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"]
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
st.title("Google Sheets Data Viewer")

# User selects a category
selected_category = st.selectbox("Select a Category", list(grouped.groups.keys()))

# Display the selected category's data
if selected_category in grouped.groups:
    selected_data = grouped.get_group(selected_category)
    st.write(f"Displaying data for {selected_category} category:")
    st.table(selected_data)
else:
    st.warning("Selected category not found.")

# Optional: Add pagination or other features as needed


