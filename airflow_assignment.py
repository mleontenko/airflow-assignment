# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

default_args = {
    'owner': 'Marin',
    'start_date': days_ago(0),
    'email': ['marin@somemail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# define the DAG
dag = DAG(
    dag_id='ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

# define the tasks

# define the task to unzip data
extract = BashOperator(
    task_id='unzip_data',
    bash_command='tar zxvf /home/project/tolldata.tgz -C /home/project/airflow/dags/finalassignment',
    dag=dag,
)


# define the task to extract data from csv file
transform = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -d"," -f1-4 /home/project/airflow/dags/finalassignment/vehicle-data.csv > /home/project/airflow/dags/finalassignment/staging/csv_data.csv',
    dag=dag,
)

# define the task to extract data from tsv file
# cut -d$'\t' -f5-7 /home/project/airflow/dags/finalassignment/staging/tollplaza-data.tsv | tr "\\t" "," > /home/project/airflow/dags/finalassignment/staging/tsv_data.csv
transform = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut -d$\'\t\' -f5-7 /home/project/airflow/dags/finalassignment/tollplaza-data.tsv | tr "\\t" "," > /home/project/airflow/dags/finalassignment/staging/tsv_data.csv',
    dag=dag,
)

# define the task to extract data from fixed width file
transform = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='cut -b 59-62,63-67 /home/project/airflow/dags/finalassignment/payment-data.txt | tr " " "," > /home/project/airflow/dags/finalassignment/staging/fixed_width_data.csv',
    dag=dag,
)
