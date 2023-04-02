import openpyxl

# Load the workbook
workbook = openpyxl.load_workbook('Davis_Spr_2023.xlsx')

worksheet = workbook['Sunday 02 Apr 2023']


# Print the value of cell A1
for row in worksheet.iter_rows():
    # Draw the match card
    print(row[7].value)