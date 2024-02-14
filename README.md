# Migration tool for RDS  
This is a simple migration script initially developed for two AWS RDS, but you can connect it to pretty much any mysql database.  
Included is a docker-compose.yml file with two databases if you want to try it out or develop modifications for your usecase.  
## Setup  
In the `tables.json` file, write a json array with every tables you want to migrate.  
In the script there is a `source_db_config` and a `destination_db_config` dictionnaries in which you need to put the data relative to the databases.
```bash
python -m venv .venv
activate .venv/bin/activate
pip install -r requirements.txt
```
## Execute
```bash
python migrate.py
```
Logs go in a `data_migration.log` file in the project's root directory.