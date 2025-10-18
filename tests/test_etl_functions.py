from unittest.mock import MagicMock, patch

import pytest

from dags.etl_pipeline import TEST_DATA, create_table, insert_testdata


class TestETLFunctions:

    def test_create_table_success(self) -> None:
        """Test successful table creation."""
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.begin.return_value.__enter__.return_value = mock_conn
        
        with patch("dags.etl_pipeline.sqlalchemy.create_engine", return_value=mock_engine):
            create_table()
            
        mock_engine.begin.assert_called_once()
        mock_conn.execute.assert_called_once()

    def test_create_table_database_error(self) -> None:
        """Test table creation with database error."""
        mock_engine = MagicMock()
        mock_engine.begin.side_effect = Exception("Database connection failed")
        
        with patch("dags.etl_pipeline.sqlalchemy.create_engine", return_value=mock_engine):
            with pytest.raises(Exception, match="Database connection failed"):
                create_table()

    def test_insert_testdata_success(self) -> None:
        """Test successful test data insertion."""
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.begin.return_value.__enter__.return_value = mock_conn
        
        with patch("dags.etl_pipeline.sqlalchemy.create_engine", return_value=mock_engine):
            insert_testdata()
            
        mock_engine.begin.assert_called_once()
        # Should call execute for TRUNCATE and each INSERT
        assert mock_conn.execute.call_count == len(TEST_DATA) + 1

    def test_insert_testdata_database_error(self) -> None:
        """Test test data insertion with database error."""
        mock_engine = MagicMock()
        mock_engine.begin.side_effect = Exception("Database connection failed")
        
        with patch("dags.etl_pipeline.sqlalchemy.create_engine", return_value=mock_engine):
            with pytest.raises(Exception, match="Database connection failed"):
                insert_testdata()

    def test_test_data_structure(self) -> None:
        """Test that TEST_DATA has the expected structure."""
        assert isinstance(TEST_DATA, list)
        assert len(TEST_DATA) == 3
        
        for item in TEST_DATA:
            assert isinstance(item, dict)
            assert "datum" in item
            assert "betrag" in item
            assert isinstance(item["betrag"], float)

    def test_test_data_values(self) -> None:
        """Test that TEST_DATA contains expected values."""
        expected_dates = ["2023-01-01", "2023-01-02", "2023-01-03"]
        expected_amounts = [110.0, 220.0, 330.0]
        
        for i, item in enumerate(TEST_DATA):
            assert item["datum"] == expected_dates[i]
            assert item["betrag"] == expected_amounts[i]
