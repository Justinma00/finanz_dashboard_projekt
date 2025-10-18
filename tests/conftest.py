import os
from typing import Generator
from unittest.mock import patch

import pandas as pd
import pytest
from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

os.environ["DATABASE_URL"] = "sqlite:///:memory:"


@pytest.fixture
def test_engine() -> Generator[Engine, None, None]:
    """Create test database engine."""
    engine = create_engine("sqlite:///:memory:")

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

    yield engine
    engine.dispose()


@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Create sample financial data."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "datum": ["2023-01-01", "2023-01-02", "2023-01-03"],
            "betrag": [110.0, 220.0, 330.0],
            "created_at": [
                "2023-01-01 10:00:00",
                "2023-01-02 10:00:00",
                "2023-01-03 10:00:00",
            ],
        }
    )


@pytest.fixture
def mock_flask_app() -> Flask:
    """Create Flask app for testing."""
    from dashboard.app.app import app

    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(mock_flask_app: Flask):
    """Create test client."""
    return mock_flask_app.test_client()


@pytest.fixture
def mock_database_connection(test_engine: Engine, sample_data: pd.DataFrame):
    """Mock database connection with sample data."""
    with patch("dashboard.app.app.get_database_engine", return_value=test_engine):
        with test_engine.begin() as conn:
            sample_data.to_sql("finanz_kpis", conn, if_exists="replace", index=False)
        yield test_engine
