import openpyxl, io
import logging
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from dashboard.utils.file_processor import process_excel_file, process_csv_file
from dashboard.constants import REQUIRED_COLUMNS

logger = logging.getLogger(__name__)


class ProcessFileTests(TestCase):
    def create_excel_file_with_columns(self, columns, rows):
        """
        Creates an in-memory Excel file with the specified columns and rows.

        This function generates an Excel file using the provided column headers
        and row data, and returns it as a file-like object.

        Args:
            columns (list): A list of column headers for the Excel file.
            rows (list of lists): A list of rows, where each row is a list of values.

        Returns:
            io.BytesIO: A file-like object containing the generated Excel file.
        """
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(columns)
        for row in rows:
            ws.append(row)
        file_stream = io.BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)
        return file_stream

    def test_process_excel_file_valid(self):
        """
        Tests the `process_excel_file` function with a valid Excel file.

        This test creates an in-memory Excel file with the required columns and
        sample rows, uploads it, and verifies that the function processes the file
        correctly without errors.

        Steps:
            - Creates an Excel file with the required columns and sample data.
            - Uploads the file using `SimpleUploadedFile`.
            - Calls the `process_excel_file` function.
            - Asserts that no errors are returned.
            - Asserts that the returned data is a list with the correct number of rows.
            - Verifies that all required columns are present in the processed data.

        Raises:
            AssertionError: If any of the assertions fail.
        """
        logger.info("Running test_process_excel_file_valid")
        columns = list(REQUIRED_COLUMNS)
        rows = [
            ["John", "Doe", "123456", "Toyota"],
            ["Jane", "Smith", "654321", "Honda"],
        ]
        excel_file = self.create_excel_file_with_columns(columns, rows)
        uploaded_file = SimpleUploadedFile(
            "test.xlsx",
            excel_file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        data, error = process_excel_file(uploaded_file)
        assert error is None
        assert isinstance(data, list)
        assert len(data) == 2
        for d in data:
            for col in columns:
                assert col in d
        logger.info("test_process_excel_file_valid passed")

    def test_process_excel_file_missing_columns(self):
        """
        Tests the `process_excel_file` function with an Excel file missing required columns.

        This test creates an in-memory Excel file that lacks some of the required columns,
        uploads it, and verifies that the function returns an appropriate error message.

        Steps:
            - Creates an Excel file with missing required columns.
            - Uploads the file using `SimpleUploadedFile`.
            - Calls the `process_excel_file` function.
            - Asserts that the returned data is None.
            - Asserts that the error message contains the missing required columns.

        Raises:
            AssertionError: If any of the assertions fail.
        """
        logger.info("Running test_process_excel_file_missing_columns")
        columns = ["Nombre", "Apellido"]  # Missing some required columns
        rows = [
            ["John", "Doe"],
        ]
        excel_file = self.create_excel_file_with_columns(columns, rows)
        uploaded_file = SimpleUploadedFile(
            "test.xlsx",
            excel_file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        data, error = process_excel_file(uploaded_file)
        assert data is None
        for col in REQUIRED_COLUMNS:
            if col not in columns:
                assert col in error
        logger.info("test_process_excel_file_missing_columns passed")

    def test_process_csv_file_valid(self):
        """
        Tests the `process_csv_file` function with a valid CSV file.

        This test creates an in-memory CSV file with the required columns and
        sample rows, uploads it, and verifies that the function processes the file
        correctly without errors.

        Steps:
            - Creates a CSV file with the required columns and sample data.
            - Uploads the file using `SimpleUploadedFile`.
            - Calls the `process_csv_file` function.
            - Asserts that no errors are returned.
            - Asserts that the returned data is a list with the correct number of rows.
            - Verifies that all required columns are present in the processed data.

        Raises:
            AssertionError: If any of the assertions fail.
        """
        logger.info("Running test_process_csv_file_valid")
        columns = list(REQUIRED_COLUMNS)
        rows = [
            ["John", "Doe", "123456", "Toyota"],
            ["Jane", "Smith", "654321", "Honda"],
        ]
        csv_content = ",".join(columns) + "\n"
        for row in rows:
            csv_content += ",".join(row) + "\n"
        uploaded_file = SimpleUploadedFile(
            "test.csv", csv_content.encode("utf-8"), content_type="text/csv"
        )
        data, error = process_csv_file(uploaded_file)
        assert error is None
        assert isinstance(data, list)
        assert len(data) == 2
        for d in data:
            for col in columns:
                assert col in d
        logger.info("test_process_csv_file_valid passed")

    def test_process_csv_file_missing_columns(self):
        """
        Tests the `process_csv_file` function with a CSV file missing required columns.

        This test creates an in-memory CSV file that lacks some of the required columns,
        uploads it, and verifies that the function returns an appropriate error message.

        Steps:
            - Creates a CSV file with missing required columns.
            - Uploads the file using `SimpleUploadedFile`.
            - Calls the `process_csv_file` function.
            - Asserts that the returned data is None.
            - Asserts that the error message contains the missing required columns.

        Raises:
            AssertionError: If any of the assertions fail.
        """
        logger.info("Running test_process_csv_file_missing_columns")
        columns = ["Nombre", "Apellido"]  # Missing some required columns
        rows = [
            ["John", "Doe"],
        ]
        csv_content = ",".join(columns) + "\n"
        for row in rows:
            csv_content += ",".join(row) + "\n"
        uploaded_file = SimpleUploadedFile(
            "test.csv", csv_content.encode("utf-8"), content_type="text/csv"
        )
        data, error = process_csv_file(uploaded_file)
        assert data is None
        for col in REQUIRED_COLUMNS:
            if col not in columns:
                assert col in error
        logger.info("test_process_csv_file_missing_columns passed")
