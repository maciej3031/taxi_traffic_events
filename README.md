### Application to analyze music preferences in NYC in specific neighborhoods based on taxi traffic from september and october 2015.

#### Installation instructions:
1. Install couchdb.
2. Run `./couchdb_backup.sh -r -H 127.0.0.1 -d tass -f db.json -u "username" -p "password" -c` to create db and read data.
Username and password are your couchdb credentials.
3. Create Python (version 3.5+) virtual environment using: `virtualenv venv --python=python3.5`
4. Activate virtual env using `source venv/bin/activate`
5. Install python packages using `pip install -r requirements.txt`
6. Run `python run.py` to start application and go to: `http://127.0.0.1:5000/`.


![alt text](https://github.com/maciej3031/taxi_traffic_events/blob/master/app_screen.png)