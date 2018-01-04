from collections import Counter

from flask import render_template, request, flash, redirect, url_for

from taxi_traffic import app, forms
from taxi_traffic.couchdb_utils import CouchDBConnection
from taxi_traffic.utils import get_event_datetime_string

conn = CouchDBConnection()


@app.route('/', methods=['GET', 'POST'])
def results():
    form = forms.EventForm()
    result = Counter()

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

        for event in events:
            event_dt_string = get_event_datetime_string(event)
            taxi_traffic = conn.get_taxi_traffic_n_hours_after_event(event_dt_string, event.value['neighborhood'], 5)
            neighborhoods = [e.value['dropoff_neighborhood'] for e in taxi_traffic]

            result += Counter(neighborhoods)

        number_of_courses = sum(result.values())

        return render_template('index.html', result=dict(result), number_of_courses=number_of_courses, form=form)

    return render_template('index.html', form=form)
