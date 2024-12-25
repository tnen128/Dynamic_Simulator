
# Airflow-Django Integration Project

This project integrates **Apache Airflow** with **Django** to dynamically create DAGs based on simulator configurations stored in a Django database. It demonstrates how to build, manage, and schedule workflows for KPI calculations using a hybrid setup of Airflow and Django.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Django Models](#django-models)
- [Dynamic DAG Creation](#dynamic-dag-creation)
- [Docker Setup](#docker-setup)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- Dynamically generate Airflow DAGs for each simulator stored in the Django database.
- Calculate KPIs for each simulator based on customizable formulas.
- Schedule DAGs according to intervals defined in the database.
- Store and update results back into the Django database.

---

## Project Structure
```plaintext
airflow_django/
├── airflow_django/      # Django application settings and configurations
├── dags/                # Airflow DAGs folder for dynamically generated workflows
├── simulator/           # Django app managing simulator models and business logic
├── db.sqlite3           # SQLite database for storing simulator data
├── docker-compose.yaml  # Docker setup for Airflow and Django
└── manage.py            # Django management script
```

---


## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/<your-username>/Dynamic_Simulator.git
   cd airflow-django
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Django:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run the Django Server:**
   ```bash
   python manage.py runserver
   ```

6. **Run Airflow:**
   - Initialize the Airflow database:
     ```bash
     airflow db init
     ```
   - Start the Airflow webserver and scheduler:
     ```bash
     airflow webserver --port 8080
     airflow scheduler
     ```

---

## Usage

1. **Add Simulators in Django Admin:**
   - Access the Django admin panel at `http://127.0.0.1:8000/admin`.
   - Add simulators with the following fields:
     - **Name**: Name of the simulator.
     - **Formula**: KPI calculation formula (e.g., `value * 2`).
     - **Interval**: Schedule interval (e.g., every 60 seconds).
     - **Start Date**: Start date for the DAG.

2. **Dynamically Generate DAGs:**
   - The project script dynamically creates DAGs for all simulators in the database.
   - Access Airflow at `http://127.0.0.1:8080` to view and manage DAGs.

3. **Monitor Results:**
   - Results are calculated and stored in the `Simulator` model's `last_result` field.

---

## Django Models

The **Simulator** model contains:
- **Name**: The name of the simulator.
- **Formula**: The KPI calculation logic.
- **Interval**: The execution frequency for the simulator (in seconds).
- **Start Date**: The start time of the schedule.
- **Last Result**: Stores the most recent KPI calculation.

---

## Dynamic DAG Creation

Each simulator generates an Airflow DAG using:
- **DAG ID**: Unique to the simulator (e.g., `simulator_1_dag`).
- **Schedule Interval**: Set by the simulator's `interval` field.
- **Task**: Executes the KPI calculation logic using `PythonOperator`.

---

## Docker Setup

1. **Build and Start Containers:**
   ```bash
   docker-compose up --build
   ```

2. **Access Services:**
   - Django: `http://127.0.0.1:8000`
   - Airflow: `http://127.0.0.1:8080`

3. **Stop Containers:**
   ```bash
   docker-compose down
   ```

