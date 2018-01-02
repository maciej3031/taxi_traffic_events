from collections import Counter
from datetime import datetime

from flask import render_template, request

from taxi_traffic import app, forms
from taxi_traffic.couchdb_utils import CouchDBConnection

conn = CouchDBConnection()


@app.route('/', methods=['GET', 'POST'])
def results():
    form = forms.EventForm()
    if request.method == 'POST' and form.validate():
        event_id = request.form.get('event')
        event = conn.get_event_by_id(id=event_id)

        try:
            event_datetime = datetime.strptime(event.key, '%Y-%m-%dT%H:%M:%S%z')
        except ValueError:
            event_datetime = datetime.strptime("{}T20:00:00-0400".format(event.key), '%Y-%m-%dT%H:%M:%S%z')
        event_dt_string = datetime.strftime(event_datetime, '%Y-%m-%d %H:%M:%S')

        taxi_traffic = conn.get_taxi_traffic_n_hours_after_event_start(event_dt_string, event.value['neighborhood'], 8)
        neighborhoods = [e.value['dropoff_neighborhood'] for e in taxi_traffic]

        result = dict(Counter(neighborhoods))

        return render_template('index.html', result=result, form=form)

    return render_template('index.html', form=form)
