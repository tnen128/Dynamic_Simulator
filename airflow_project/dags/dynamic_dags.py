from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
from django_project.simulator.models import Simulator

def call_kpi_endpoint(simulator_id):
    simulator = Simulator.objects.get(id=simulator_id)
    value = random.randint(1, 100)
    response = requests.post(
        "http://localhost:8000/kpi/",
        json={"value": value, "kpi_id": simulator.kpi_id}
    )
    print(f"Simulator {simulator_id}: {response.json()}")

def create_dag(simulator):
    default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
    }
    dag = DAG(
        dag_id=f"simulator_{simulator.id}",
        default_args=default_args,
        description='Dynamic DAG',
        schedule_interval=simulator.interval,
        start_date=simulator.start_date,
        catchup=False,
    )
    with dag:
        PythonOperator(
            task_id=f"simulate_{simulator.id}",
            python_callable=call_kpi_endpoint,
            op_kwargs={'simulator_id': simulator.id}
        )
    return dag

simulators = Simulator.objects.all()
for simulator in simulators:
    globals()[f"simulator_{simulator.id}"] = create_dag(simulator)
