# Finanz Dashboard Projekt

Ein modernes Finanz-Dashboard mit ETL-Pipeline und Weboberfläche. Das Projekt verwendet Docker, Apache Airflow für die Datenverarbeitung und Flask für die Visualisierung von Finanzdaten.

## 🚀 Features

- **ETL-Pipeline**: Automatisierte Datenverarbeitung mit Apache Airflow
- **Web-Dashboard**: Interaktive Visualisierung mit Flask und Plotly
- **Datenbank**: PostgreSQL für zuverlässige Datenspeicherung
- **Docker**: Vollständig containerisierte Anwendung
- **Tests**: Umfassende Testabdeckung mit pytest
- **Code-Qualität**: PEP8-konform mit Type Hints und Linting

## 📁 Projektstruktur

```
finanz_dashboard_projekt/
├── docker-compose.yml       # Docker Setup für alle Services
├── pyproject.toml          # Python Projektkonfiguration
├── .flake8                 # Linting-Konfiguration
├── .pre-commit-config.yaml # Pre-commit Hooks
├── dags/                   # ETL-Pipelines (Apache Airflow)
│   ├── etl_pipeline.py     # Haupt-ETL-Pipeline
│   └── data/               # Beispieldaten
├── dashboard/              # Web-Dashboard
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── app.py          # Flask-Anwendung
│       ├── static/
│       └── templates/
│           └── index.html  # Dashboard-Template
├── tests/                  # Test-Suite
│   ├── conftest.py         # Pytest-Konfiguration
│   ├── test_etl_pipeline.py
│   ├── test_dashboard_app.py
│   └── test_integration.py
└── data/                   # Weitere Beispieldaten
```

## 🛠️ Voraussetzungen

- Docker
- Docker Compose
- Python 3.10+ (für lokale Entwicklung)

## 🚀 Installation & Nutzung

### Mit Docker (Empfohlen)

1. **Repository klonen:**
   ```bash
   git clone https://github.com/Justinma00/finanz_dashboard_projekt
   cd finanz_dashboard_projekt
   ```

2. **Services starten:**
   ```bash
   docker-compose up --build
   ```

3. **Services zugreifen:**
   - **Airflow Web UI**: http://localhost:8080
   - **Dashboard**: http://localhost:5000
   - **Datenbank**: localhost:5432

### Lokale Entwicklung

1. **Abhängigkeiten installieren:**
   ```bash
   pip install -e .
   pip install -e ".[dev]"  # Für Entwicklungstools
   ```

2. **Tests ausführen:**
   ```bash
   pytest tests/ -v
   ```

3. **Code formatieren:**
   ```bash
   black .
   isort .
   flake8 .
   ```

## 📊 Verwendung

1. **ETL-Pipeline starten:**
   - Öffnen Sie http://localhost:8080
   - Loggen Sie sich mit `admin/admin` ein
   - Aktivieren Sie den `etl_pipeline` DAG
   - Führen Sie den DAG aus

2. **Dashboard anzeigen:**
   - Öffnen Sie http://localhost:5000
   - Sehen Sie die visualisierten Finanzdaten

## 🧪 Testing

Das Projekt verfügt über eine umfassende Test-Suite:

```bash
# Alle Tests ausführen
pytest tests/ -v

# Mit Coverage-Report
pytest tests/ --cov=dashboard --cov=dags --cov-report=html

# Nur schnelle Tests
pytest tests/ -m "not slow"
```

**Test-Abdeckung:** 100% Code Coverage

## 🔧 Entwicklung

### Code-Qualität

Das Projekt verwendet moderne Python-Entwicklungstools:

- **Black**: Code-Formatierung
- **isort**: Import-Organisation
- **flake8**: Linting
- **mypy**: Type Checking
- **pre-commit**: Automatische Hooks

### Pre-commit Hooks einrichten:

```bash
pip install pre-commit
pre-commit install
```

## 📈 Monitoring

- **Health Check**: http://localhost:5000/health
- **Datenbank-Test**: http://localhost:5000/testdb

---

# Financial Dashboard Project

A modern financial dashboard with ETL pipeline and web interface. The project uses Docker, Apache Airflow for data processing, and Flask for financial data visualization.

## 🚀 Features

- **ETL Pipeline**: Automated data processing with Apache Airflow
- **Web Dashboard**: Interactive visualization with Flask and Plotly
- **Database**: PostgreSQL for reliable data storage
- **Docker**: Fully containerized application
- **Testing**: Comprehensive test coverage with pytest
- **Code Quality**: PEP8 compliant with type hints and linting

## 📁 Project Structure

```
finanz_dashboard_projekt/
├── docker-compose.yml       # Docker setup for all services
├── pyproject.toml          # Python project configuration
├── .flake8                 # Linting configuration
├── .pre-commit-config.yaml # Pre-commit hooks
├── dags/                   # ETL Pipelines (Apache Airflow)
│   ├── etl_pipeline.py     # Main ETL pipeline
│   └── data/               # Sample data
├── dashboard/              # Web Dashboard
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── app.py          # Flask application
│       ├── static/
│       └── templates/
│           └── index.html  # Dashboard template
├── tests/                  # Test Suite
│   ├── conftest.py         # Pytest configuration
│   ├── test_etl_pipeline.py
│   ├── test_dashboard_app.py
│   └── test_integration.py
└── data/                   # Additional sample data
```

## 🛠️ Prerequisites

- Docker
- Docker Compose
- Python 3.10+ (for local development)

## 🚀 Installation & Usage

### With Docker (Recommended)

1. **Clone repository:**
   ```bash
   git clone https://github.com/Justinma00/finanz_dashboard_projekt
   cd finanz_dashboard_projekt
   ```

2. **Start services:**
   ```bash
   docker-compose up --build
   ```

3. **Access services:**
   - **Airflow Web UI**: http://localhost:8080
   - **Dashboard**: http://localhost:5000
   - **Database**: localhost:5432

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -e .
   pip install -e ".[dev]"  # For development tools
   ```

2. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

3. **Format code:**
   ```bash
   black .
   isort .
   flake8 .
   ```

## 📊 Usage

1. **Start ETL Pipeline:**
   - Open http://localhost:8080
   - Login with `admin/admin`
   - Enable the `etl_pipeline` DAG
   - Run the DAG

2. **View Dashboard:**
   - Open http://localhost:5000
   - See the visualized financial data

## 🧪 Testing

The project has a comprehensive test suite:

```bash
# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=dashboard --cov=dags --cov-report=html

# Only fast tests
pytest tests/ -m "not slow"
```

**Test Coverage:** 100% Code Coverage

## 🔧 Development

### Code Quality

The project uses modern Python development tools:

- **Black**: Code formatting
- **isort**: Import organization
- **flake8**: Linting
- **mypy**: Type checking
- **pre-commit**: Automatic hooks

### Setup pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

## 📈 Monitoring

- **Health Check**: http://localhost:5000/health
- **Database Test**: http://localhost:5000/testdb

## 🏗️ Architecture

The project follows a modern microservices architecture:

1. **ETL Layer**: Apache Airflow handles data extraction, transformation, and loading
2. **Data Layer**: PostgreSQL stores the processed financial data
3. **API Layer**: Flask provides REST endpoints for data access
4. **Presentation Layer**: HTML templates with Plotly for interactive charts

## 🔒 Security

- Database credentials are configurable via environment variables
- All database connections use parameterized queries to prevent SQL injection
- Input validation and error handling throughout the application

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📞 Support

For questions or issues, please open an issue in the repository.