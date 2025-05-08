from openpyxl import Workbook
from io import BytesIO, TextIOWrapper
import csv

def generate_excel(columns, data):
    """
    Generates an Excel file with the specified columns and data.

    Args:
        columns (list): A list of column headers for the Excel file.
        data (list of dict): A list of dictionaries representing the rows of data.

    Returns:
        tuple: A tuple containing:
            - BytesIO: The in-memory Excel file.
            - str: The content type of the file ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet').
            - str: The suggested filename ('reporte.xlsx').
    """
    wb = Workbook()
    ws = wb.active
    ws.append(columns)
    for row in data:
        ws.append([row.get(col, '') for col in columns])
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'reporte.xlsx'

def generate_csv(columns, data):
    """
    Generates a CSV file with the specified columns and data.

    Args:
        columns (list): A list of column headers for the CSV file.
        data (list of dict): A list of dictionaries representing the rows of data.

    Returns:
        tuple: A tuple containing:
            - BytesIO: The in-memory CSV file.
            - str: The content type of the file ('text/csv').
            - str: The suggested filename ('reporte.csv').
    """
    output = BytesIO()
    text_output = TextIOWrapper(output, encoding='utf-8', newline='', line_buffering=True)
    writer = csv.writer(text_output)
    writer.writerow(columns)
    for row in data:
        writer.writerow([row.get(col, '') for col in columns])
    text_output.flush()
    text_output.detach()
    output.seek(0)
    return output, 'text/csv', 'reporte.csv'