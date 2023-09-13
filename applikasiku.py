import streamlit as st
import gspread
from google.oauth2 import service_account
import pandas as pd

# Define the path to your JSON key file
keyfile_path = "https://raw.githubusercontent.com/Frenky-sinaga/Frenky-sinaga/main/masterstore-398408-e5a0bae4d629.json"

# Define the desired OAuth2 scopes
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Authenticate using the JSON key file and scopes
credentials = service_account.Credentials.from_service_account_file(
    keyfile_path, scopes=scopes
)

# Authorize the client to access Google Sheets
gc = gspread.Client(auth=credentials)
gc.session.verify = False  # To suppress SSL certificate verification warnings

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
