import streamlit as st
import gspread
# Authenticate with Google Sheets using service account credentials
gc =  gspread.service_account(filename="developer-374205-27d86b37709f.json")

# Open the target spreadsheet and select the worksheet
spreadsheet = gc.open('sample_sales')
worksheet = spreadsheet.worksheet('Sheet1')


def main():
    # Add a text input for the data to update
     st.title("Data Entry Form")

    # Add a button to trigger the update
    # Add input fields for name, age, address, phone, subject, and fees
    name = st.text_input("Name")
    age = st.number_input("Age")
    address = st.text_area("Address")
    phone = st.text_input("Phone")
    subject = st.text_input("Subject")
    fees = st.number_input("Fees")

    # Add a button to trigger the update
    if st.button("Update Sheet"):
        # Create a list with the values to update in the worksheet
        data = [name, age, address, phone, subject, fees]

        # Update the worksheet with the new data
        cell_range = "A2:F2"  # Assuming the data starts from the first row
        worksheet.update(cell_range, [data])
        st.success("Sheet updated successfully!")

if __name__ == '__main__':
    main()
