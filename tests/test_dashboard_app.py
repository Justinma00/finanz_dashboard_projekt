"""Tests for the Flask dashboard application."""

from unittest.mock import MagicMock, patch

import pandas as pd

from dashboard.app.app import (
    fetch_financial_data,
    generate_chart,
    get_database_engine,
    process_dataframe,
)


class TestDashboardApp:
    """Test cases for dashboard application functions."""

    def test_get_database_engine(self) -> None:
        """Test database engine creation."""
        with patch("dashboard.app.app.sqlalchemy.create_engine") as mock_create:
            mock_engine = MagicMock()
            mock_create.return_value = mock_engine

            result = get_database_engine()

            mock_create.assert_called_once()
            assert result == mock_engine

    def test_fetch_financial_data_success(self, test_engine, sample_data) -> None:
        """Test successful data fetching."""
        # Insert sample data
        with test_engine.begin() as conn:
            sample_data.to_sql("finanz_kpis", conn, if_exists="replace", index=False)

        with patch("dashboard.app.app.get_database_engine", return_value=test_engine):
            df, error = fetch_financial_data()

        assert error is None
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert len(df) == 3

    def test_fetch_financial_data_error(self) -> None:
        """Test data fetching with database error."""
        mock_engine = MagicMock()
        mock_engine.raw_connection.side_effect = Exception("Connection failed")

        with patch("dashboard.app.app.get_database_engine", return_value=mock_engine):
            df, error = fetch_financial_data()

        assert df is None
        assert error == "Connection failed"

    def test_process_dataframe(self, sample_data) -> None:
        """Test DataFrame processing."""
        # Convert to the format expected by the function
        df = sample_data.copy()
        df.columns = df.columns.str.upper()  # Simulate database column names

        result = process_dataframe(df)

        # Check column names are lowercase
        assert all(col.islower() for col in result.columns)

        # Check date formatting
        if "datum" in result.columns:
            assert (
                result["datum"].dtype == "object"
            )  # Should be string after formatting

    def test_generate_chart_with_data(self, sample_data) -> None:
        """Test chart generation with valid data."""
        df = sample_data.copy()
        df["datum"] = pd.to_datetime(df["datum"]).dt.strftime("%d.%m.%Y")

        chart_html = generate_chart(df)

        assert isinstance(chart_html, str)
        assert "plotly" in chart_html.lower()

    def test_generate_chart_missing_columns(self) -> None:
        """Test chart generation with missing columns."""
        df = pd.DataFrame({"other_col": [1, 2, 3]})

        chart_html = generate_chart(df)

        assert chart_html == "<p>Kein Diagramm verfügbar (Spalten fehlen)</p>"

    def test_generate_chart_empty_dataframe(self) -> None:
        """Test chart generation with empty DataFrame."""
        df = pd.DataFrame()

        chart_html = generate_chart(df)

        assert chart_html == "<p>Kein Diagramm verfügbar (Spalten fehlen)</p>"


class TestFlaskRoutes:
    """Test cases for Flask routes."""

    def test_index_route_success(
        self, client, mock_database_connection, sample_data
    ) -> None:
        """Test successful index route."""
        response = client.get("/")

        assert response.status_code == 200
        assert b"Finanz Dashboard" in response.data
        assert b"110" in response.data  # Sample data should be present

    def test_index_route_no_data(self, client) -> None:
        """Test index route with no data."""
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.raw_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None

        # Mock empty DataFrame
        with patch("dashboard.app.app.get_database_engine", return_value=mock_engine):
            with patch("pandas.read_sql", return_value=pd.DataFrame()):
                response = client.get("/")

        assert response.status_code == 200
        assert b"Keine Daten" in response.data

    def test_index_route_database_error(self, client) -> None:
        """Test index route with database error."""
        mock_engine = MagicMock()
        mock_engine.raw_connection.side_effect = Exception("Database error")

        with patch("dashboard.app.app.get_database_engine", return_value=mock_engine):
            response = client.get("/")

        assert response.status_code == 200
        assert b"Datenbankfehler" in response.data

    def test_testdb_route_success(self, client) -> None:
        """Test successful testdb route."""
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value.scalar.return_value = 1

        with patch("dashboard.app.app.get_database_engine", return_value=mock_engine):
            response = client.get("/testdb")

        assert response.status_code == 200
        assert b"Datenbank OK" in response.data

    def test_testdb_route_error(self, client) -> None:
        """Test testdb route with error."""
        mock_engine = MagicMock()
        mock_engine.connect.side_effect = Exception("Connection failed")

        with patch("dashboard.app.app.get_database_engine", return_value=mock_engine):
            response = client.get("/testdb")

        assert response.status_code == 200
        assert b"Datenbankfehler" in response.data

    def test_health_route(self, client) -> None:
        """Test health check route."""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.data == b"OK"
