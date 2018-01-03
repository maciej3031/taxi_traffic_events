from collections import Counter
from datetime import datetime

from flask import render_template, request, flash, redirect, url_for

from taxi_traffic import app, forms
from taxi_traffic.couchdb_utils import CouchDBConnection

conn = CouchDBConnection()


@app.route('/', methods=['GET', 'POST'])
def results():
    form = forms.EventForm()
    if request.method == 'POST' and form.validate():
        artist_name = request.form.get('artist')
        genre_name = request.form.get('genre')

        if artist_name:
            events = conn.get_events_by_artist(artist_name)
        elif genre_name:
            events = conn.get_events_by_genre(genre_name)
        else:
            flash('Choose one filter!')
            return redirect(url_for('results'))

        result = Counter()
        for event in events:
            try:
                event_datetime = datetime.strptime(event.key, '%Y-%m-%dT%H:%M:%S%z')
            except ValueError:
                event_datetime = datetime.strptime("{}T20:00:00-0400".format(event.key), '%Y-%m-%dT%H:%M:%S%z')
            event_dt_string = datetime.strftime(event_datetime, '%Y-%m-%d %H:%M:%S')

            taxi_traffic = conn.get_taxi_traffic_n_hours_after_event(event_dt_string, event.value['neighborhood'], 6)
            neighborhoods = [e.value['dropoff_neighborhood'] for e in taxi_traffic]

            result += Counter(neighborhoods)

        return render_template('index.html', result=dict(result), form=form)

    return render_template('index.html', form=form)
