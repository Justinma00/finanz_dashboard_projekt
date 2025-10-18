import os
from typing import Optional, Tuple

import pandas as pd
import plotly.express as px
import plotly.io as pio
import sqlalchemy
from flask import Flask, render_template
from sqlalchemy.engine import Engine

app = Flask(__name__)

DB_URL: str = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://airflow:airflow@postgres:5432/airflow"
)


def get_database_engine() -> Engine:
    """Create database engine."""
    return sqlalchemy.create_engine(DB_URL)


def fetch_financial_data() -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """Fetch financial data from database."""
    engine = get_database_engine()

    try:
        conn = engine.raw_connection()
        try:
            df = pd.read_sql("SELECT * FROM finanz_kpis ORDER BY datum", conn)
        finally:
            conn.close()
        return df, None
    except Exception as e:
        return None, str(e)


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Process DataFrame for display."""
    df.columns = df.columns.str.lower()

    if "datum" in df.columns:
        df["datum"] = pd.to_datetime(df["datum"]).dt.strftime("%d.%m.%Y")

    return df


def generate_chart(df: pd.DataFrame) -> str:
    """Generate chart HTML."""
    if "datum" in df.columns and "betrag" in df.columns:
        fig = px.line(
            df,
            x="datum",
            y="betrag",
            title="Finanzentwicklung",
            labels={"datum": "Datum", "betrag": "Betrag (€)"},
        )
        fig.update_layout(
            xaxis_title="Datum", yaxis_title="Betrag (€)", hovermode="x unified"
        )
        return pio.to_html(fig, full_html=False)
    else:
        return "<p>Kein Diagramm verfügbar (Spalten fehlen)</p>"


@app.route("/")
def index() -> str:
    """Main dashboard route."""
    df, error = fetch_financial_data()

    if error:
        return f"<h1>Datenbankfehler</h1><p>{error}</p>"

    if df.empty:
        return (
            "<h1>Keine Daten</h1>"
            "<p>Die Tabelle 'finanz_kpis' existiert, aber hat keine Zeilen. "
            "Führen Sie zuerst Ihren ETL DAG aus.</p>"
        )

    df_processed = process_dataframe(df)
    table_html = df_processed.to_html(classes="data", index=False)
    chart_html = generate_chart(df_processed)

    return render_template("index.html", table=table_html, chart=chart_html)


@app.route("/testdb")
def testdb() -> str:
    """Database connectivity test."""
    try:
        engine = get_database_engine()
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text("SELECT 1")).scalar()
        return f"✅ Datenbank OK → {result}"
    except Exception as e:
        return f"❌ Datenbankfehler: {e}"


@app.route("/health")
def health() -> str:
    """Health check endpoint."""
    return "OK"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
