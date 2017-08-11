for project instalation:
1. create virtual environment: _virtualenv -p python3 env_
2. activate created environment: _source env/bin/activate_
3. install requirements: _pip install -r requirements/environments/development.txt_

For using celery redis server(or another celery broker) should be installed.
default CELERY_BROKER_URL = 'redis://localhost:6379/0'
