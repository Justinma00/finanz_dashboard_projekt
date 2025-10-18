from datetime import datetime
from typing import Any, Dict, List

import sqlalchemy
from airflow import DAG
from airflow.operators.python import PythonOperator
from sqlalchemy import text
from sqlalchemy.engine import Engine

DB_URL: str = "postgresql+psycopg2://airflow:airflow@postgres:5432/airflow"

TEST_DATA: List[Dict[str, Any]] = [
    {"datum": "2023-01-01", "betrag": 110.0},
    {"datum": "2023-01-02", "betrag": 220.0},
    {"datum": "2023-01-03", "betrag": 330.0},
]


def create_table() -> None:
    """Create finanz_kpis table."""
    engine: Engine = sqlalchemy.create_engine(DB_URL)
    ddl: str = """
    CREATE TABLE IF NOT EXISTS finanz_kpis (
        id SERIAL PRIMARY KEY,
        datum DATE UNIQUE,
        betrag NUMERIC,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with engine.begin() as conn:
        conn.execute(text(ddl))


def insert_testdata() -> None:
    """Insert test data into finanz_kpis table."""
    engine: Engine = sqlalchemy.create_engine(DB_URL)

    with engine.begin() as conn:
        if "sqlite" in str(engine.url):
            conn.execute(text("DELETE FROM finanz_kpis;"))
            try:
                conn.execute(
                    text("DELETE FROM sqlite_sequence WHERE name='finanz_kpis';")
                )
            except Exception:
                pass
        else:
            conn.execute(text("TRUNCATE TABLE finanz_kpis RESTART IDENTITY;"))

        for row in TEST_DATA:
            conn.execute(
                text(
                    "INSERT INTO finanz_kpis (datum, betrag) VALUES (:datum, :betrag)"
                ),
                row,
            )


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

try:
    with DAG(
        dag_id="etl_pipeline",
        default_args=default_args,
        description="ETL Pipeline für Finanz-KPIs",
        schedule_interval="@once",
        start_date=datetime(2025, 1, 1),
        catchup=False,
        tags=["finanz"],
    ) as dag:
        t1 = PythonOperator(
            task_id="create_table",
            python_callable=create_table,
        )

        t2 = PythonOperator(
            task_id="insert_testdata",
            python_callable=insert_testdata,
        )

        t1 >> t2
except TypeError:
    try:
        with DAG(
            dag_id="etl_pipeline",
            default_args=default_args,
            description="ETL Pipeline für Finanz-KPIs",
            schedule="@once",
            start_date=datetime(2025, 1, 1),
            catchup=False,
            tags=["finanz"],
        ) as dag:
            t1 = PythonOperator(
                task_id="create_table",
                python_callable=create_table,
            )

            t2 = PythonOperator(
                task_id="insert_testdata",
                python_callable=insert_testdata,
            )

            t1 >> t2
    except Exception:
        dag = None
