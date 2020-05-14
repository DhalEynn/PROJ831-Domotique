# PROJ831 - Database and use project

## Dependencies :

* python 3.X (tested with python 3.7.4 with or without Anaconda 3)
* python packages :
  * pymongo
  * Flask
  * pandas
  * plotly
* MongoDB (https://www.mongodb.com/community)


## Instructions :
**General:**

1. Start a mongoDB server

2. Install dependencies

3. Create the file "env.py" like this:
```python
import os

os.environ['DB_PASSWORD'] = 'password'
os.environ['DB_USERNAME'] = 'username'
os.environ['DB_SERVER'] = 'ip'
os.environ['COLLECTION_LOGS'] = 'logs'
os.environ['COLLECTION_ANALYSIS'] = 'analysis'

```

**Input data program:**

1. Put your input data file in "Files" folder (some example are in the repo)

2. Edit #parameters section of main.py (logs filename)

3. Run main.py


**Web server :**

1. Go in Dashboards folder: `cd Dashboards`

2. Add the application as env var:
  * (Windows PowerShell): `$env:FLASK_APP = "application.py"`
  * (Windows CMD) : `set FLASK_APP=application.py`
  * (Linux): `export FLASK_APP=application.py`

3. Run the server: `flask run`

4. The web server is running on localhost:5000
