import streamlit as st
import os
import oss2
from datetime import datetime
from dotenv import load_dotenv
from main import run_image_insertion # IMPORT THE LOGIC HERE

# Load .env only if it exists (local testing)
if os.path.exists(".env"):
    load_dotenv()

# This will fetch from GitHub Secrets (in Docker) OR .env (locally)
OSS_ACCESS_KEY = os.getenv('OSS_ACCESS_KEY')
OSS_SECRET_KEY = os.getenv('OSS_SECRET_KEY')
OSS_ENDPOINT = os.getenv('OSS_ENDPOINT')
OSS_BUCKET = os.getenv('OSS_BUCKET')

auth = oss2.Auth(OSS_ACCESS_KEY, OSS_SECRET_KEY)

st.title("📦 Excel Inventory Image Inserter")
st.write("Upload your Excel, and I'll fetch images from Alibaba Storage.")

# User uploads the file
uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])

if uploaded_file:
    if st.button("🚀 Process My File"):
        with st.spinner("Processing... this may take a minute."):
            try:
                # Call the function from processor.py
                final_excel_data = run_image_insertion(uploaded_file, OSS_BUCKET, auth, OSS_ENDPOINT)
                
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