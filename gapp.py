import gspread
sa = gspread.service_account(filename="developer-374205-27d86b37709f.json")
sheet = sa.open("sample_sales")
work_sheet = sheet.worksheet("Sheet1")
data = 'pythons'
cell_range = 'A1'

# Update the values in the worksheet
work_sheet.update(cell_range, data)
