import streamlit as st
import gspread
from google.oauth2 import service_account
import pandas as pd
import gcsfs

# Authenticate with Google Sheets using credentials from JSON file
def authenticate_google_sheets():
    credentials = service_account.Credentials.from_service_account_file(
        "https://github.com/Frenky-sinaga/Frenky-sinaga/blob/main/masterstore-398408-e5a0bae4d629.json", scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    gc = gspread.service_account(credentials=credentials)
    return gc

# Rest of your code remains the same

# Connect to Google Sheets and fetch data
def get_data_from_google_sheets():
    client = authenticate_google_sheets()
    sheet = client.open("MasterStores").sheet1  # Replace with your Google Sheet name
    data = sheet.get_all_records()
    return data

# Read JSON data from a cloud storage bucket (e.g., Google Cloud Storage)
def get_json_data_from_cloud():
    gcs = gcsfs.GCSFileSystem(project="your-gcs-project")
    with gcs.open("gs://your-bucket-name/your-json-file.json") as f:
        json_data = pd.read_json(f)
    return json_data

st.title("Streamlit App with Google Sheets and Cloud JSON")

# Fetch data from Google Sheets
gs_data = get_data_from_google_sheets()
st.write("Data from Google Sheets:")
st.write(pd.DataFrame(gs_data))

# Fetch JSON data from cloud storage
cloud_json_data = get_json_data_from_cloud()
st.write("JSON Data from Cloud:")
st.write(cloud_json_data)
