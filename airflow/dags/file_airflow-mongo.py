import datetime
from airflow.sensors.filesystem import FileSensor
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator

from docker.types import Mount

@dag(start_date=datetime.datetime(2021, 1, 1), schedule="@once", max_active_runs=1)
def copy_tranform_to_mongo():
       
    waiting_for_data = FileSensor(
        
        task_id='waiting_for_data',
        filepath = 'in/tiktok_google_play_reviews.csv',
        fs_conn_id='fs_default',
        timeout=60,
        poke_interval=10
    )

    transform_data_by_pandas = DockerOperator(
        
        task_id='transform_data_by_pandas',
        image='python/pandas:1.0.0',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        command='papermill /opt/pandasapp/in_notebooks/tiktok_google_reviews.ipynb /opt/pandasapp/out_notebooks/tiktok_google_reviews.ipynb ',
        xcom_all = False,
        mount_tmp_dir = False,
        network_mode='bridge',
        mounts = [Mount(source='/home/mikvar/Training/projects/airflow', target='/opt',type='bind')]

    )

    load_data_to_mongo = DockerOperator(
        
        task_id='load_data_to_mongo',
        image='python/pandas:1.0.0',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        command='python /opt/pandasapp/script/load_to_mongo.py ',
        xcom_all = False,
        mount_tmp_dir = False,
        network_mode='airflow_default',
        mounts = [Mount(source='/home/mikvar/Training/projects/airflow', target='/opt',type='bind')]

    )

    delete_output_file = BashOperator(
        task_id='delete_output_file',
        bash_command= " rm /opt/out/*.json"
    )

    

    waiting_for_data >> transform_data_by_pandas >> load_data_to_mongo >> delete_output_file




copy_tranform_to_mongo()

