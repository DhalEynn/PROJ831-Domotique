# PROJ831 - Database and use project

## Dependencies :

* python 3.X (tested with python 3.7.4 with or without Anaconda 3)
* python packages :
  * pymongo (https://pymongo.readthedocs.io/en/stable/installation.html)
  * Flask (https://flask.palletsprojects.com/en/1.1.x/installation/#installation)
  * plotly (https://github.com/plotly/plotly.py)
* MongoDB (https://www.mongodb.com/community)


## Instructions :

0. Create the file "env.py" like this:
```python
import os

os.environ['DB_PASSWORD'] = password
os.environ['DB_USERNAME'] = username
os.environ['DB_SERVER'] = ip
```


**Input data program:**

1. Put your input data file in "Files" folder (some example are in the repo)

2. Edit main.py to use your file

3. Run main.py


**Web server :**
1. Install dependencies:

`pip install Flask`

`pip install pymongo`


2. Go in Dashboard folder:

`cd Dashboards`


3. Add the application as env var:
  * (Windows PowerShell): `$env:FLASK_APP = "application.py"`
  * (Windows CMD) : `set FLASK_APP=application.py`
  * (Linux): `export FLASK_APP=application.py`


4. Run the server:

`flask run`

5. The web server is running on localhost:5000
