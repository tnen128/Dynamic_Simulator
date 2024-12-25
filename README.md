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
- Call Django REST API endpoints from Airflow tasks.
- Store results back into the Django database.

---

## Project Structure
```plaintext
django_airflow_project/
├── airflow_project/       # Airflow-specific files and DAGs
├── django_project/        # Django application containing project settings and apps
│   ├── mysite/            # Django project settings
│   ├── simulator/         # Django app managing simulator and KPI models
├── db.sqlite3             # SQLite database for Django
├── docker-compose.yaml    # Docker setup for Airflow and Django
└── manage.py              # Django management script
```

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/<your-username>/Dynamic_Simulator_project.git
   cd django_airflow_project
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install django djangorestframework apache-airflow requests
   ```

4. **Set Up Django:**
   ```bash
   python manage.py makemigrations
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

1. **Add KPIs and Simulators in Django Admin:**
   - Access the Django admin panel at `http://127.0.0.1:8000/admin`.
   - Add KPIs with the following fields:
     - **Name**: Name of the KPI (e.g., "Add 2", "Add 6").
     - **Formula**: KPI calculation formula (e.g., `value + 2`).
   - Add simulators with the following fields:
     - **Start Date**: Start date for the DAG.
     - **Interval**: Schedule interval (e.g., `*/2 * * * * *` for every 2 seconds).
     - **KPI ID**: Select the associated KPI.

2. **Dynamically Generate DAGs:**
   - The project script dynamically creates DAGs for all simulators in the database.
   - Access Airflow at `http://127.0.0.1:8080` to view and manage DAGs.

3. **Monitor Results:**
   - Logs and outputs are stored in the Airflow UI and Django database.

---

## Django Models

The **Simulator** model contains:
- **Start Date**: The start time of the schedule.
- **Interval**: The execution frequency for the simulator (in cron format).
- **KPI ID**: The associated KPI.

The **Kpi** model contains:
- **Name**: The name of the KPI.
- **Formula**: The KPI calculation logic (e.g., `value + 2`).

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
