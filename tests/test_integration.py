"""Integration tests for the financial dashboard project."""

from unittest.mock import patch

import pytest
from sqlalchemy import create_engine, text

from dags.etl_pipeline import create_table, insert_testdata
from dashboard.app.app import fetch_financial_data, process_dataframe


class TestIntegration:
    """Integration tests for the complete workflow."""

    def test_etl_to_dashboard_workflow(self) -> None:
        """Test complete ETL to dashboard workflow."""
        # Use in-memory SQLite for integration testing
        engine = create_engine("sqlite:///:memory:")

        # Create table using ETL function
        with patch("dags.etl_pipeline.sqlalchemy.create_engine", return_value=engine):
            create_table()

            # Verify table was created
            with engine.connect() as conn:
                result = conn.execute(
                    text(
                        "SELECT name FROM sqlite_master WHERE type='table' "
                        "AND name='finanz_kpis'"
                    )
                )
                assert result.fetchone() is not None

        # Insert test data using ETL function
        with patch("dags.etl_pipeline.sqlalchemy.create_engine", return_value=engine):
            insert_testdata()

            # Verify data was inserted
            with engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM finanz_kpis"))
                count = result.scalar()
                assert count == 3

        # Fetch data using dashboard function
        with patch("dashboard.app.app.get_database_engine", return_value=engine):
            df, error = fetch_financial_data()

            assert error is None
            assert not df.empty
            assert len(df) == 3

            # Process data using dashboard function
            processed_df = process_dataframe(df)

            # Verify processing worked
            assert "datum" in processed_df.columns
            assert "betrag" in processed_df.columns
            assert len(processed_df) == 3

    def test_data_consistency(self) -> None:
        """Test that data remains consistent through the pipeline."""
        engine = create_engine("sqlite:///:memory:")

        # Run complete ETL pipeline
        with patch("dags.etl_pipeline.sqlalchemy.create_engine", return_value=engine):
            create_table()
            insert_testdata()

        # Fetch and process data
        with patch("dashboard.app.app.get_database_engine", return_value=engine):
            df, error = fetch_financial_data()
            processed_df = process_dataframe(df)

        # Verify data integrity
        assert error is None
        assert len(processed_df) == 3

        # Check that all expected amounts are present
        amounts = processed_df["betrag"].tolist()
        expected_amounts = [110.0, 220.0, 330.0]

        for expected in expected_amounts:
            assert expected in amounts

    def test_error_handling_integration(self) -> None:
        """Test error handling across the integration."""
        # Test with invalid database URL
        invalid_engine = create_engine("sqlite:///nonexistent.db")

        with patch(
            "dashboard.app.app.get_database_engine", return_value=invalid_engine
        ):
            df, error = fetch_financial_data()

            # Should handle the error gracefully
            assert df is None
            assert error is not None

    @pytest.mark.slow
    def test_performance_with_large_dataset(self) -> None:
        """Test performance with a larger dataset."""
        engine = create_engine("sqlite:///:memory:")

        # Create table
        with engine.begin() as conn:
            conn.execute(
                text(
                    """
                CREATE TABLE finanz_kpis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datum DATE,
                    betrag REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
                )
            )

            # Insert larger dataset
            import datetime

            base_date = datetime.date(2023, 1, 1)
            for i in range(1000):
                date = base_date + datetime.timedelta(days=i)
                amount = 100.0 + i * 10.0
                conn.execute(
                    text(
                        "INSERT INTO finanz_kpis (datum, betrag) VALUES "
                        "(:date, :amount)"
                    ),
                    {"date": date, "amount": amount},
                )

        # Test fetching and processing
        with patch("dashboard.app.app.get_database_engine", return_value=engine):
            df, error = fetch_financial_data()
            processed_df = process_dataframe(df)

        assert error is None
        assert len(processed_df) == 1000
        assert "datum" in processed_df.columns
        assert "betrag" in processed_df.columns
