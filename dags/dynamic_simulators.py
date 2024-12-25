from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import random
import os
import django

# Setup Django integration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airflow_django.settings')
django.setup()

from simulator.models import Simulator

def calculate_kpi(simulator_id, **kwargs):
    """
    Fetches a Simulator instance, calculates the KPI value, and stores it.
    This version is independent of any other simulators.
    """
    # Fetch simulator instance
    simulator = Simulator.objects.get(id=simulator_id)

    # Generate random value or use some other logic specific to the simulator
    value = random.randint(1, 100)  # Replace with more advanced logic if needed

    # Evaluate formula (use value only, no dependencies on others)
    result = eval(simulator.formula, {"value": value})
    print(f"Simulator {simulator.name} Result: {result}")

    # Optionally save the result back to the database
    simulator.last_result = result
    simulator.save()

    return result

def create_dag(simulator):
    """
    Creates a DAG dynamically for each simulator.
    """
    default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
    }

    dag = DAG(
        dag_id=f"simulator_{simulator.id}_dag",
        default_args=default_args,
        description=f"DAG for {simulator.name}",
        schedule_interval=timedelta(seconds=simulator.interval.total_seconds()),
        start_date=simulator.start_date,
        catchup=False,
    )

    with dag:
        PythonOperator(
            task_id=f"run_simulator_{simulator.id}",
            python_callable=calculate_kpi,
            op_kwargs={'simulator_id': simulator.id},
        )

    return dag

# Fetch simulators from the database and generate DAGs dynamically
simulators = Simulator.objects.all()
for simulator in simulators:
    globals()[f"simulator_{simulator.id}_dag"] = create_dag(simulator)
