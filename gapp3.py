import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

import os
import urllib.request
from xhtml2pdf import pisa
from bs4 import BeautifulSoup
import streamlit as st


# ...

def convert_to_pdf(input_folder_url, output_folder_path):
    retry_count = 3  # Number of retries
    retry_delay = 1  # Delay in seconds between retries

    # Build the Google Drive API client
    drive_service = build('drive', 'v3')

    # Get the folder ID from the input folder URL
    folder_id = input_folder_url.split('/')[-1]

    # Retrieve the list of files in the folder
    response = drive_service.files().list(q=f"'{folder_id}' in parents").execute()
    files = response.get('files', [])

    if not files:
        print('No files found in the folder.')
        return

    for file in files:
        file_name = file['name']
        file_id = file['id']

        for _ in range(retry_count):
            try:
                # Download the file content
                request = drive_service.files().get_media(fileId=file_id)
                file_content = io.BytesIO()
                downloader = MediaIoBaseDownload(file_content, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                
                # Convert the file content to PDF
                output_file_path = os.path.join(output_folder_path, f"{file_name}.pdf")
                with open(output_file_path, "wb") as f:
                    f.write(file_content.getvalue())
                print(f"File converted: {output_file_path}")
                break  # Exit the retry loop if successful
            except Exception as e:
                print(f"Error converting file '{file_name}': {str(e)}")
                time.sleep(retry_delay)
        else:
            print(f"Failed to convert file '{file_name}' after {retry_count} retries.")


def main():
    # Add a text input for the folder URL and output folder path
    input_folder_url = st.text_input('Enter folder URL:')
    output_folder_path = st.text_input('Enter output folder path:')
    
    # Add a button to trigger the conversion
    if st.button('Convert to PDF'):
        # Call the convert_to_pdf function for the specified folder URL and output folder path
        convert_to_pdf(input_folder_url, output_folder_path)
        
        st.success('Files converted successfully!')


if __name__ == '__main__':
    main()
