import streamlit as st
import gspread
import time

import os
import urllib.request
from xhtml2pdf import pisa
from bs4 import BeautifulSoup
import streamlit as st

# Authenticate with Google Sheets using service account credentials
gc =  gspread.service_account(filename="developer-374205-27d86b37709f.json")

# Open the target spreadsheet and select the worksheet
spreadsheet = gc.open('sample_sales')
worksheet = spreadsheet.worksheet('Sheet1')


def convert_to_pdf(input_file_url, output_folder_path):
    retry_count = 3  # Number of retries
    retry_delay = 1  # Delay in seconds between retries

    for _ in range(retry_count):
        try:
            response = urllib.request.urlopen(input_file_url)
            break  # Exit the loop if the request is successful
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Too Many Requests error
                print("Too many requests. Retrying after delay...")
                time.sleep(retry_delay)
            else:
                raise e

    
    # Download the content of the file
    response = urllib.request.urlopen(input_file_url)

    # Create a BeautifulSoup object to parse the content
    soup = BeautifulSoup(response.read(), "html.parser")

    # Find the elements you want to scrape
    data = soup.find_all()

    # Convert the scraped data to a PDF
    output_file_name = "output.pdf"
    output_file_path = os.path.join(output_folder_path, output_file_name)
    with open(output_file_path, "wb") as f:
        html = "<html><head><meta charset='UTF-8'></head><body>"
        for d in data:
            html += str(d)
        html += "</body></html>"
        pisa.CreatePDF(html, dest=f)
    print(f"File converted: {output_file_path}")
    response.close()


def main():
    # Add a text input for the data to update
    input_file_url = worksheet.cell(2, 1).value
    output_folder_path = st.text_input('Enter outputfolderpath:')
    


    # Add a button to trigger the update
    if st.button('convert to pdf'):
        convert_to_pdf(input_file_url, output_folder_path)
        st.success('Sheet updated successfully!')


        

if __name__ == '__main__':
    main()
