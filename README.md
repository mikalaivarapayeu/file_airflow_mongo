# This is training airflow pipeline project
## The pipeline works in the following way:
1. Csv should be place in the in folder;
2.  jupyter note book loads this file, makes transformations, writes results of transformation to json output.json into the out folder;
3. python script from pandasapp load this file and inserted into a mongdb database;
4. output.json file is temporary and is deleted at the end pipeline.

## Technical notes of the pipeline
The whole pipeline works as docker containers, so docker and docker compose should be installed.

To start application move to folder where docker-compose.yaml file is loacated and run in terminal the following command: _docker compose -f docker-compose.yaml up -d_.

There are no mappings of mongodb to local computer, so as soon as containers are stopped data in mongoDb is deleted.

## There several commands should be executed to make operational:
- ensure that airflow/airflow folder recursively has permission 777 for users, group and others;
- run the following command _sudo chmod /var/run/docker.sock_ to give permission airflow to docker deamon

After starting airfllow, one should go to localhost:8080/ , then to Admin/connections and create the following connection:
- connection id : _fs_default_,
- type connection: _File(path)_,
- extra : _{“path”:”/opt”}_

