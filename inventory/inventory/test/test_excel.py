from inventory.spreadsheet import dataload

def load_data():
    file_path = "C:\\workspace\\aiops\\aiops-datafeed\\inventory\\inventory\\test\\host_data.xlsx"
    sheet = "Master"
    dataload.load_excel(file_path, sheet)

load_data()