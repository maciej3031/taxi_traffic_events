1. Install couchdb.
2. Run `./couchdb_backup.sh -r -H 127.0.0.1 -d tass -f db.json -c` to create db.
3. Create python (version 3.5) virtual environment using: `virtualenv venv --python=python3.5`
4. Activate virtual env using `source venv/bin/activate`
5. Install python packages using `pip install -r requirements.txt`
6. Run `python run.py` to start application and go to: `http://127.0.0.1:5000/`. 