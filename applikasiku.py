import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


# Set up the scope and credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("https://github.com/Frenky-sinaga/Frenky-sinaga/blob/main/masterstore-398408-e5a0bae4d629.json", scope)

client = gspread.authorize(creds)

# Access your Google Sheets spreadsheet by title or URL
spreadsheet = client.open("MasterStores")

# Access a specific worksheet
worksheet = spreadsheet.worksheet("Sheet1")  # Replace with your sheet name

data = worksheet.get_all_records()

# Convert data to a Pandas DataFrame for grouping
df = pd.DataFrame(data)

# Group the data by a specific column (e.g., "Category")
grouped = df.groupby("Koneksi")

selected_category = st.selectbox("Select a Category", grouped.groups.keys())

rows_per_page=25


# Get the current page from the user's input or default to the first page
group_data = grouped.get_group(selected_category)
num_pages = (len(group_data) - 1) // rows_per_page + 1
page_number = st.number_input("Enter Page Number", min_value=1, max_value=num_pages, step=1, value=1)


# Calculate the start and end indices for the current page
start_index = (page_number - 1) * rows_per_page
end_index = min(page_number * rows_per_page, len(df))
# Display the data for the current page in a table
#st.table(data[start_index:end_index])
# Display the data for the selected category in a table
st.write(f"Displaying data for {selected_category} category (Page {page_number}/{num_pages}):")
st.table(group_data[start_index:end_index])