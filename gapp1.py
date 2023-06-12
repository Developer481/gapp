import streamlit as st
import gspread
# Authenticate with Google Sheets using service account credentials
gc =  gspread.service_account(filename="developer-374205-27d86b37709f.json")

# Open the target spreadsheet and select the worksheet
spreadsheet = gc.open('sample_sales')
worksheet = spreadsheet.worksheet('Sheet1')


def main():
    # Add a text input for the data to update
    data = st.text_input('Enter data:')

    # Add a button to trigger the update
    if st.button('Update Sheet'):
        # Update the worksheet with the new data
        cell_range = 'A1'
        worksheet.update(cell_range, data)
        st.success('Sheet updated successfully!')

if __name__ == '__main__':
    main()
