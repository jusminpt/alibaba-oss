import streamlit as st
import os
import oss2
from datetime import datetime
from dotenv import load_dotenv
from main import run_image_insertion # IMPORT THE LOGIC HERE

# Load keys from .env
load_dotenv()

# Setup Alibaba Auth once
auth = oss2.Auth(os.getenv('OSS_ACCESS_KEY'), os.getenv('OSS_SECRET_KEY'))
endpoint = os.getenv('OSS_ENDPOINT')
bucket_name = os.getenv('OSS_BUCKET')

st.title("📦 Excel Inventory Image Inserter")
st.write("Upload your Excel, and I'll fetch images from Alibaba OSS.")

# User uploads the file
uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])

if uploaded_file:
    if st.button("🚀 Process My File"):
        with st.spinner("Processing... this may take a minute."):
            try:
                # Call the function from processor.py
                final_excel_data = run_image_insertion(uploaded_file, bucket_name, auth, endpoint)
                
                # Setup dynamic name
                date_str = datetime.now().strftime("%d-%m-%Y")
                file_name = f"Inventory_Finished({date_str}).xlsx"

                st.success("✅ Done!")
                st.download_button(
                    label="📥 Download Result",
                    data=final_excel_data,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Frontend Error: {e}")