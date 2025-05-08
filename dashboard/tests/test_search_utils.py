from django.test import TestCase

from dashboard.utils.search_utils import filter_data

class SearchUtilsTests(TestCase):

    def sample_data(self):
        """
        Provides sample data for testing.

        Returns:
            list: A list of dictionaries representing sample data with fields
            'Nombre', 'Apellido', 'Documento', and 'Carro'.
        """
        return [
            {"Nombres": "John", "Apellidos": "Doe", "Número de documento": "123456", "Placa del auto": "789-XYZ"},
            {"Nombres": "Jane", "Apellidos": "Smith", "Número de documento": "654321", "Placa del auto": "189-XYZ"},
            {"Nombres": "Alice", "Apellidos": "Johnson", "Número de documento": "111222", "Placa del auto": "289-XYZ"},
            {"Nombres": "Bob", "Apellidos": "Brown", "Número de documento": "333444", "Placa del auto": "389-XYZ"},
        ]

    def test_filter_data_by_nombre(self):
        """
        Tests the `filter_data` function by filtering data based on the 'Nombre' field.

        Args:
            sample_data (list): The sample data to filter.

        Asserts:
            - The result contains entries with 'Nombre' matching the query.
            - The result length matches the expected number of matches.
        """
        result = filter_data(self.sample_data(), "john")
        assert any(r["Nombres"] == "John" for r in result)
        assert any(r["Nombres"] == "Alice" for r in result)
        assert len(result) == 2
    
    def test_filter_data_by_apellido(self):
        """
        Tests the `filter_data` function by filtering data based on the 'Apellido' field.

        Args:
            sample_data (list): The sample data to filter.

        Asserts:
            - The result contains one entry with 'Apellido' matching the query.
            - The 'Apellido' field in the result matches the query.
        """
        result = filter_data(self.sample_data(), "smith")
        assert len(result) == 1
        assert result[0]["Apellidos"] == "Smith"
    
    def test_filter_data_by_documento(self):
        """
        Tests the `filter_data` function by filtering data based on the 'Documento' field.

        Args:
            sample_data (list): The sample data to filter.

        Asserts:
            - The result contains one entry with 'Documento' matching the query.
            - The 'Documento' field in the result matches the query.
        """
        result = filter_data(self.sample_data(), "333444")
        assert len(result) == 1
        assert result[0]["Número de documento"] == "333444"


    def test_filter_data_by_carro(self):
        """
        Tests the `filter_data` function by filtering data based on the 'Carro' field.

        Args:
            sample_data (list): The sample data to filter.

        Asserts:
            - The result contains one entry with 'Carro' matching the query.
            - The 'Carro' field in the result matches the query.
        """
        result = filter_data(self.sample_data(), "789-XYZ")
        assert len(result) == 1
        assert result[0]["Placa del auto"] == "789-XYZ"


    def test_filter_data_no_results(self):
        """
        Tests the `filter_data` function with a query that yields no results.

        Args:
            sample_data (list): The sample data to filter.

        Asserts:
            - The result is an empty list when no matches are found.
        """
        result = filter_data(self.sample_data(), "nonexistent")
        assert result == []
